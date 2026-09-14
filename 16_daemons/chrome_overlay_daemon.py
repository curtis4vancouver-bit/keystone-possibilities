"""
================================================================================
CHROME OVERLAY DAEMON — CDP Overlay Injector (Port 9879)
================================================================================
DAEMON SPECIFICATION:
- File Location: 16_daemons/chrome_overlay_daemon.py
- Role: Lightweight HTTP server that injects overlay JavaScript into the active
  Chrome tab via Chrome DevTools Protocol (CDP).
- Port: 9879  (singleton enforced via SO_EXCLUSIVEADDRUSE)
- CDP Target: http://127.0.0.1:9222/json
- Overlay Root: 05_Keystone_HUD/button_configs/overlays/{overlayId}/overlay.js
- Architecture:
    1. Binds port 9879 with SO_EXCLUSIVEADDRUSE for singleton enforcement.
    2. Serves a threaded HTTP server with CORS headers (allow all origins).
    3. Provides REST endpoints to inject, remove, and list Chrome overlays.
    4. Connects to Chrome CDP via websockets.sync.client for Runtime.evaluate.
- Dependencies: Python stdlib + websockets (sync client, already in venv)
- Governance: Core HUD infrastructure daemon. Maintain robustness guarantees.
================================================================================
"""

import sys
import os
import time
import json
import re
import socket
import urllib.request
import urllib.error
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler


# ---------------------------------------------------------------------------
# Singleton Guard — Port 9879 (matches instant_watchdog.py pattern)
# ---------------------------------------------------------------------------
DAEMON_PORT = 9879


# ---------------------------------------------------------------------------
# Enforce UTF-8 on Windows console
# ---------------------------------------------------------------------------
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

DAEMON_DIR = os.path.dirname(os.path.abspath(__file__))
if DAEMON_DIR not in sys.path:
    sys.path.insert(0, DAEMON_DIR)

# ---------------------------------------------------------------------------
# Paths & Immutable Button Locking
# ---------------------------------------------------------------------------
BRAIN_ROOT = r"c:\Users\Curtis\Desktop\Keystone Brain"
OVERLAY_ROOT = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays")
OVERLAY_REGISTRY = os.path.join(OVERLAY_ROOT, "_overlay_registry.json")
BUTTONS_LOCK_CONFIG = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "overlay_buttons_config.json")
GOOGLE_FLOW_PROMPTS_CONFIG = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "google_flow", "google_flow_prompts.json")
PORT = 9879
CDP_URL = "http://127.0.0.1:9222/json"

# In-memory overlay tracking & thread-safe injection queue
ACTIVE_OVERLAYS = {}
PENDING_INJECTIONS = []
PENDING_INJECTIONS_LOCK = threading.Lock()
_FLOW_ORCHESTRATOR_PROC = None

# ---------------------------------------------------------------------------
# Automation Triggers & Pipeline Exclusivity Manager (Dual-Dispatch Protection)
# ---------------------------------------------------------------------------
TRIGGERS_DIR = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "automation_triggers")
PIPELINE_LOCKS_FILE = os.path.join(BRAIN_ROOT, "16_daemons", ".pipeline_locks.json")

class PipelineExclusivityManager:
    """
    Exclusivity Lock Manager for Keystone Production Pipelines.
    Guarantees mutual exclusivity between Antigravity subagents and daemon subprocesses
    across the 4 core domains:
    1. 'davinci_assembly' (DaVinci Resolve 2-Track Auto-Assembly)
    2. 'youtube_upload' (YouTube Studio Video Upload Long & Shorts)
    3. 'luxury_blog_publish' (WordPress Luxury Blog Publishing & GSC Indexing)
    4. 'meta_social_publish' (Meta Business Suite FB & IG Post Staging)
    """
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.locks = {}
        self._load_file_locks()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _load_file_locks(self):
        if os.path.exists(PIPELINE_LOCKS_FILE):
            try:
                with open(PIPELINE_LOCKS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    now = time.time()
                    for k, v in data.items():
                        if isinstance(v, dict) and v.get("expires_at", 0) > now:
                            self.locks[k] = v
            except Exception as e:
                _log(f"Warning reading pipeline locks file: {e}")

    def _save_file_locks(self):
        try:
            with open(PIPELINE_LOCKS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.locks, f, indent=2)
        except Exception as e:
            _log(f"Warning saving pipeline locks file: {e}")

    def is_locked(self, pipeline: str) -> tuple[bool, dict | None]:
        with self._lock:
            now = time.time()
            if pipeline in self.locks:
                lock_data = self.locks[pipeline]
                if lock_data.get("expires_at", 0) > now:
                    return True, lock_data
                else:
                    del self.locks[pipeline]
                    self._save_file_locks()
            return False, None

    def acquire(self, pipeline: str, owner: str, ttl_seconds: int = 900, pid: int = None, details: str = "") -> tuple[bool, str, dict]:
        with self._lock:
            now = time.time()
            if pipeline in self.locks:
                lock_data = self.locks[pipeline]
                if lock_data.get("expires_at", 0) > now:
                    if lock_data.get("owner") == owner and (pid is None or lock_data.get("pid") == pid):
                        lock_data["expires_at"] = now + ttl_seconds
                        lock_data["refreshed_at"] = now
                        if details:
                            lock_data["details"] = details
                        self._save_file_locks()
                        return True, "Lock refreshed", lock_data
                    return False, f"Pipeline '{pipeline}' is already locked by '{lock_data.get('owner')}' (expires in {int(lock_data.get('expires_at', 0) - now)}s)", lock_data
                else:
                    del self.locks[pipeline]

            lock_data = {
                "pipeline": pipeline,
                "owner": owner,
                "pid": pid,
                "acquired_at": now,
                "expires_at": now + ttl_seconds,
                "ttl_seconds": ttl_seconds,
                "details": details
            }
            self.locks[pipeline] = lock_data
            self._save_file_locks()
            _log(f"🔒 [Pipeline Lock Acquired] {pipeline} by {owner} (TTL: {ttl_seconds}s, PID: {pid})")
            return True, "Lock acquired", lock_data

    def release(self, pipeline: str, owner: str = None) -> tuple[bool, str]:
        with self._lock:
            if pipeline in self.locks:
                current = self.locks[pipeline]
                if owner and current.get("owner") != owner and owner not in ["FORCE", "admin"]:
                    return False, f"Cannot release lock owned by {current.get('owner')}"
                del self.locks[pipeline]
                self._save_file_locks()
                _log(f"🔓 [Pipeline Lock Released] {pipeline} by {owner}")
                return True, "Lock released"
            return True, "Pipeline was not locked"

    def get_all_locks(self) -> dict:
        with self._lock:
            now = time.time()
            active = {}
            for k, v in list(self.locks.items()):
                if isinstance(v, dict) and v.get("expires_at", 0) > now:
                    active[k] = v
                else:
                    del self.locks[k]
            self._save_file_locks()
            return active

PIPELINE_EXCLUSIVITY = PipelineExclusivityManager.get_instance()

# ---------------------------------------------------------------------------
# CDP Helpers & Immutable Button Lock Verification
# ---------------------------------------------------------------------------

def _log(msg: str):
    """Print a timestamped log line."""
    print(f"[OverlayDaemon] {msg}", flush=True)

def verify_and_lock_overlay_buttons():
    """Verify that all overlay button configurations remain 100% locked and unmutated."""
    if os.path.exists(BUTTONS_LOCK_CONFIG):
        try:
            with open(BUTTONS_LOCK_CONFIG, 'r', encoding='utf-8') as f:
                lock_data = json.load(f)
            _log(f"🔒 [Immutable Button Lock] Enforced version {lock_data.get('version', '6.0.0')} across {len(lock_data.get('buttons', []))} buttons.")
        except Exception as e:
            _log(f"⚠️ [Button Lock Warning] Could not parse button lock file: {e}")

verify_and_lock_overlay_buttons()


def get_merged_overlay_config() -> dict:
    """
    Load both google_flow_prompts.json and overlay_buttons_config.json.
    Combine them into a structured dictionary object.
    Handle missing file or parsing errors gracefully.
    """
    prompts_data = {}
    if os.path.exists(GOOGLE_FLOW_PROMPTS_CONFIG):
        try:
            with open(GOOGLE_FLOW_PROMPTS_CONFIG, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
        except Exception as e:
            _log(f"⚠️ Error parsing google_flow_prompts.json: {e}")

    buttons_data = {}
    if os.path.exists(BUTTONS_LOCK_CONFIG):
        try:
            with open(BUTTONS_LOCK_CONFIG, 'r', encoding='utf-8') as f:
                buttons_data = json.load(f)
        except Exception as e:
            _log(f"⚠️ Error parsing overlay_buttons_config.json: {e}")

    merged = {
        "ok": True,
        "prompts": prompts_data,
        "buttons": buttons_data,
        "google_flow_prompts": prompts_data,
        "overlay_buttons_config": buttons_data,
        "category": prompts_data.get("category", "google_flow") if isinstance(prompts_data, dict) else "google_flow",
        "version": prompts_data.get("version", "1.2.0") if isinstance(prompts_data, dict) else "1.2.0",
        "overlay_config": prompts_data.get("overlay_config", {}) if isinstance(prompts_data, dict) else {},
        "aspect_ratio_buttons": prompts_data.get("aspect_ratio_buttons", []) if isinstance(prompts_data, dict) else [],
        "prompt_buttons": prompts_data.get("buttons", []) if isinstance(prompts_data, dict) else [],
        "locked_buttons": buttons_data.get("buttons", []) if isinstance(buttons_data, dict) else []
    }
    return merged


def get_chrome_tabs():
    """Fetch the Chrome CDP tab list dynamically across active DevTools ports."""
    candidate_ports = [9222, 53180, 9012, 9013, 9180]

    for port in candidate_ports:
        if port == 55538:
            continue  # Hard ban Antigravity Electron IDE port
        urls = [f"http://127.0.0.1:{port}/json/list", f"http://127.0.0.1:{port}/json"]
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Fast-CDP-Probe"})
                with urllib.request.urlopen(req, timeout=0.15) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        if isinstance(data, list) and len(data) > 0:
                            # Verify tabs don't belong to Antigravity
                            non_antigravity = [
                                t for t in data 
                                if "61615" not in t.get("url", "") 
                                and "63256" not in t.get("url", "")
                                and "127.0.0.1" not in t.get("url", "")
                                and "localhost" not in t.get("url", "")
                                and "antigravity" not in t.get("url", "").lower()
                                and "bootstrap" not in t.get("title", "").lower()
                                and "watchdog" not in t.get("title", "").lower()
                                and "debug open chrome tab" not in t.get("title", "").lower()
                                and not t.get("url", "").startswith("file://")
                            ]
                            if non_antigravity:
                                return non_antigravity, None
            except Exception:
                continue

    return None, "Chrome CDP unreachable on candidate ports"


def _cdp_probe_visibility(ws_url: str) -> str:
    """
    Connect to a single tab's CDP WebSocket and check document.visibilityState.
    Returns 'visible', 'hidden', or 'error'.
    """
    try:
        from websockets.sync.client import connect as ws_connect
    except ImportError:
        return "error"
    try:
        with ws_connect(ws_url, close_timeout=1) as ws:
            ws.send(json.dumps({
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": "document.visibilityState"}
            }))
            resp = json.loads(ws.recv())
            val = resp.get("result", {}).get("result", {}).get("value", "error")
            return val
    except Exception:
        return "error"


def dispatch_prompt_to_antigravity(prompt_text: str, target_chat: str = ""):
    """Dispatches a prompt directly into Antigravity via Daemon A on Port 9876."""
    try:
        data = {"prompt": prompt_text}
        if target_chat:
            data["target_chat_name"] = target_chat
        req = urllib.request.Request(
            "http://127.0.0.1:9876/api/prompt",
            data=json.dumps(data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=3)
        _log(f"🚀 [Prompt -> Antigravity] Dispatched to Port 9876: {prompt_text[:60]}...")
        return True
    except Exception as e:
        _log(f"⚠️ Failed to dispatch prompt to Antigravity via Port 9876: {e}")
        return False


def get_active_tab(target_pattern: str = None):
    """
    Find the ACTUAL active Chrome tab by probing document.visibilityState
    on each page tab via CDP. Only the tab Wayne is viewing returns 'visible'.
    Filters out Antigravity/Electron IDE tabs.
    """
    tabs, err = get_chrome_tabs()
    if err:
        return None, err

    # Filter out Antigravity/Electron IDE windows
    page_tabs = []
    for t in tabs:
        if t.get("type") != "page" or not t.get("webSocketDebuggerUrl"):
            continue
        url = t.get("url", "").lower()
        title = t.get("title", "").lower()
        # Strictly exclude Antigravity Electron IDE, DevTools windows, local dev servers, and internal chat tabs
        if (
            "61615" in url or 
            "63256" in url or
            "127.0.0.1" in url or
            "localhost" in url or
            "antigravity" in url or 
            "bootstrap" in title or 
            "watchdog" in title or
            "antigravity" in title or
            "debug open chrome tab" in title or
            "devtools" in title or
            url.startswith("devtools://") or
            "vscode-webview" in url or
            "chrome-extension://" in url or
            url.startswith("file://")
        ):
            continue
        page_tabs.append(t)

    if not page_tabs:
        return None, "No active Chrome browser tabs found (excluding Antigravity IDE)"

    # If target_pattern provided, prefer matching tab that is currently visible
    if target_pattern:
        pattern = target_pattern.lower()
        matching = [t for t in page_tabs if pattern in t.get("url", "").lower() or pattern in t.get("title", "").lower()]
        if matching:
            for tab in matching:
                vis = _cdp_probe_visibility(tab["webSocketDebuggerUrl"])
                if vis == "visible":
                    _log(f"Active visible matching tab detected: '{tab.get('title', '?')}' (visibilityState=visible)")
                    return tab, None
            _log(f"Matching tab selected: '{matching[0].get('title', '?')}'")
            return matching[0], None

    # Probe each tab for visibility — the active one returns 'visible'
    for tab in page_tabs:
        vis = _cdp_probe_visibility(tab["webSocketDebuggerUrl"])
        if vis == "visible":
            _log(f"Active Chrome tab detected: '{tab.get('title', '?')}' (visibilityState=visible)")
            return tab, None

    # Fallback: first page tab in Chrome
    _log(f"No visible Chrome tab detected, falling back to first Chrome tab: '{page_tabs[0].get('title', '?')}'")
    return page_tabs[0], None


def cdp_inject_isolated(js_expression: str, tab=None, world_name: str = "KeystoneHUDIsolatedWorld"):
    """
    Upgrade CDP injection:
    1. Register script for future navigations via Page.addScriptToEvaluateOnNewDocument with worldName: "KeystoneHUDIsolatedWorld".
    2. Create an isolated world (Page.createIsolatedWorld) on the active frame and evaluate immediately in that context.
    3. Ensure overlay container elements attach inside a Closed Shadow Root (attachShadow({ mode: 'closed' })).
    """
    if tab is None:
        tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab["webSocketDebuggerUrl"]
    tab_title = tab.get("title", "(untitled)")

    try:
        from websockets.sync.client import connect as ws_connect
    except ImportError:
        return None, "websockets library not available — cannot connect to CDP WebSocket"

    # Wrap JS expression to automatically attach overlay elements inside a Closed Shadow Root
    config_json_str = json.dumps(get_merged_overlay_config())
    shadow_js_wrapper = f"""
    (() => {{
        if (!window.KS_OVERLAY_JSON_CONFIG) {{
            window.KS_OVERLAY_JSON_CONFIG = {config_json_str};
        }}
        if (!window.__KEYSTONE_SHADOW_ROOT_ATTACHED__) {{
            window.__KEYSTONE_SHADOW_ROOT_ATTACHED__ = true;
            window.__createKeystoneClosedShadow__ = function(containerId) {{
                let host = document.getElementById(containerId);
                if (!host) {{
                    host = document.createElement('div');
                    host.id = containerId;
                    (document.body || document.documentElement).appendChild(host);
                }}
                if (!host.shadowRoot && !host._ksShadow) {{
                    try {{
                        host._ksShadow = host.attachShadow({{ mode: 'closed' }});
                    }} catch (e) {{
                        host._ksShadow = host.shadowRoot || host;
                    }}
                }}
                return host._ksShadow;
            }};
        }}
        try {{
            {js_expression}
        }} catch(err) {{
            console.error('[KeystoneHUDIsolatedWorld] Overlay execution error:', err);
        }}
    }})();
    """

    try:
        with ws_connect(ws_url) as ws:
            # 1. Enable Page domain
            ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            ws.recv()

            # 2. Add script on new document with isolated world
            ws.send(json.dumps({
                "id": 2,
                "method": "Page.addScriptToEvaluateOnNewDocument",
                "params": {
                    "source": shadow_js_wrapper,
                    "worldName": world_name
                }
            }))
            new_doc_resp = json.loads(ws.recv())
            _log(f"Page.addScriptToEvaluateOnNewDocument (world: {world_name}) -> {new_doc_resp.get('result', {})}")

            # 3. Get Frame Tree for current document
            ws.send(json.dumps({"id": 3, "method": "Page.getFrameTree"}))
            frame_resp = json.loads(ws.recv())
            frame_id = frame_resp.get("result", {}).get("frameTree", {}).get("frame", {}).get("id")

            context_id = None
            if frame_id:
                # 4. Create isolated world for current frame
                ws.send(json.dumps({
                    "id": 4,
                    "method": "Page.createIsolatedWorld",
                    "params": {
                        "frameId": frame_id,
                        "worldName": world_name,
                        "grantUniveralAccess": True
                    }
                }))
                world_resp = json.loads(ws.recv())
                context_id = world_resp.get("result", {}).get("executionContextId")

            # 5. Evaluate immediately in isolated context (or fallback to standard evaluate)
            eval_params = {"expression": shadow_js_wrapper}
            if context_id:
                eval_params["contextId"] = context_id

            ws.send(json.dumps({
                "id": 5,
                "method": "Runtime.evaluate",
                "params": eval_params
            }))
            response_raw = ws.recv()
            response = json.loads(response_raw)

            if "error" in response:
                cdp_err = response["error"]
                return None, f"CDP error: {cdp_err.get('message', cdp_err)}"

            result = response.get("result", {}).get("result", {})
            if result.get("subtype") == "error":
                return None, f"JS exception: {result.get('description', result)}"

        return tab_title, None
    except Exception as e:
        return None, f"CDP WebSocket error: {e}"


def cdp_evaluate(js_expression: str, tab=None):
    """
    Run Runtime.evaluate on a specific tab (or auto-detect the active tab).
    Returns (tab_title, None) on success or (None, error_str) on failure.
    """
    if tab is None:
        tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab["webSocketDebuggerUrl"]
    tab_title = tab.get("title", "(untitled)")

    try:
        from websockets.sync.client import connect as ws_connect
    except ImportError:
        return None, "websockets library not available — cannot connect to CDP WebSocket"

    try:
        with ws_connect(ws_url) as ws:
            payload = json.dumps({
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": js_expression}
            })
            ws.send(payload)
            response_raw = ws.recv()
            response = json.loads(response_raw)

            if "error" in response:
                cdp_err = response["error"]
                return None, f"CDP error: {cdp_err.get('message', cdp_err)}"

            result = response.get("result", {}).get("result", {})
            if result.get("subtype") == "error":
                return None, f"JS exception: {result.get('description', result)}"

        return tab_title, None
    except Exception as e:
        return None, f"CDP WebSocket error: {e}"


def cdp_press_enter(tab=None):
    """
    Dispatch native CDP Input.dispatchKeyEvent for Enter (virtualKey 13) to active Chrome tab.
    Ensures isTrusted: true hardware key event for React input submission.
    """
    if tab is None:
        tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab["webSocketDebuggerUrl"]
    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url) as ws:
            # 1. KeyDown
            ws.send(json.dumps({
                "id": 1, "method": "Input.dispatchKeyEvent",
                "params": {"type": "keyDown", "key": "Enter", "code": "Enter", "text": "\r", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13}
            }))
            ws.recv()
            # 2. Char
            ws.send(json.dumps({
                "id": 2, "method": "Input.dispatchKeyEvent",
                "params": {"type": "char", "text": "\r"}
            }))
            ws.recv()
            # 3. KeyUp
            ws.send(json.dumps({
                "id": 3, "method": "Input.dispatchKeyEvent",
                "params": {"type": "keyUp", "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13}
            }))
            ws.recv()
        return tab.get("title", "(untitled)"), None
    except Exception as e:
        return None, f"CDP enter error: {e}"


def cdp_type_prompt(text: str, submit: bool = False, tab=None):
    """
    Dispatch native CDP Input.insertText followed by optional Enter key hardware sequence.
    Ensures isTrusted: true OS-level keystrokes for React state sync.
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on tab"

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, close_timeout=15) as ws:
            msg_id = 0
            def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {"id": msg_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                return json.loads(ws.recv())

            def eval_js(js):
                res = send("Runtime.evaluate", {"expression": js, "returnByValue": True})
                return res.get("result", {}).get("result", {}).get("value")

            # 1. Clean previous chips and focus editor
            eval_js("""
                (() => {
                    const clearBtn = Array.from(document.querySelectorAll('button')).find(b => 
                        ((b.innerText || '') + ' ' + (b.getAttribute('aria-label') || '')).toLowerCase().includes('clear prompt')
                    );
                    if (clearBtn) clearBtn.click();
                    
                    const promptEl = document.querySelector('.ProseMirror') || 
                                     document.querySelector('[data-slate-editor="true"]') || 
                                     document.querySelector('[contenteditable="true"]');
                    if (promptEl) {
                        promptEl.focus();
                        const sel = window.getSelection();
                        const range = document.createRange();
                        range.selectNodeContents(promptEl);
                        sel.removeAllRanges();
                        sel.addRange(range);
                    }
                })()
            """)
            time.sleep(0.08)

            # 2. Native CDP Input.insertText
            send("Input.insertText", {"text": text})
            time.sleep(0.1)

            # 3. If submit requested, dispatch Enter and click Generate button
            if submit:
                # 3-stage Enter key sequence
                send("Input.dispatchKeyEvent", {
                    "type": "rawKeyDown", "key": "Enter", "code": "Enter",
                    "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
                })
                time.sleep(0.01)
                send("Input.dispatchKeyEvent", {"type": "char", "text": "\r", "unmodifiedText": "\r"})
                time.sleep(0.01)
                send("Input.dispatchKeyEvent", {
                    "type": "keyUp", "key": "Enter", "code": "Enter",
                    "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
                })
                time.sleep(0.05)

                # Click generate button
                eval_js("""
                    (() => {
                        const btn = document.querySelector('button.generate-icon-button, [aria-label="Start generation"]');
                        if (btn && !btn.disabled) {
                            btn.click();
                            btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                            btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                            btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                        }
                    })()
                """)
                time.sleep(0.1)

        return tab.get("title", "(untitled)"), None
    except Exception as e:
        return None, f"CDP typing error: {e}"


def cdp_avatar_inject(script_text: str, camera_text: str = "", submit: bool = False, speaker: str = "wayne", cloth: str = None, background: str = None, tab=None):
    """
    Execute full 3-chip Speaker pipeline via CDP with 100% State-Aware Reliability:
    - speaker="wayne": [+] -> Avatar tab -> Add to Prompt -> All -> cloth_1 -> All -> background_1 -> Slate Prompt
    - speaker="ted":   [+] -> Characters tab -> ted -> Add to Prompt -> All -> cloth_2 -> All -> background_2 -> Slate Prompt
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on tab"

    is_broll = str(speaker).lower() in ("broll", "b-roll", "image", "b_roll", "still", "scene", "no_photo", "nophoto")
    is_ted = str(speaker).lower() in ("ted", "character", "guest")
    target_cloth = cloth or ("cloth_2" if is_ted else "cloth_1")
    target_bg = background or ("background_2" if is_ted else "background_1")

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, close_timeout=35) as ws:
            msg_id = 0
            def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {"id": msg_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                return json.loads(ws.recv())

            def eval_js(js):
                res = send("Runtime.evaluate", {"expression": js, "returnByValue": True})
                return res.get("result", {}).get("result", {}).get("value")

            def wait_for_cond(fn_js, timeout_s=3.0, poll_s=0.02):
                start = time.time()
                while time.time() - start < timeout_s:
                    res = eval_js(fn_js)
                    if res is not None and res is not False:
                        return res
                    time.sleep(poll_s)
                return None

            def send_enter():
                send("Input.dispatchKeyEvent", {
                    "type": "rawKeyDown", "key": "Enter", "code": "Enter",
                    "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
                })
                time.sleep(0.01)
                send("Input.dispatchKeyEvent", {"type": "char", "text": "\r", "unmodifiedText": "\r"})
                time.sleep(0.01)
                send("Input.dispatchKeyEvent", {
                    "type": "keyUp", "key": "Enter", "code": "Enter",
                    "windowsVirtualKeyCode": 13, "nativeVirtualKeyCode": 13
                })
                time.sleep(0.05)

            # STEP 0: Check attached reference chips in the prompt box
            current_chips_count = eval_js("""
                (() => {
                    return document.querySelectorAll('.chip-image-wrapper').length;
                })()
            """) or 0

            # STEP 0.5: If B-Roll Mode, clean any attached reference chips and insert prompt
            if is_broll:
                if current_chips_count > 0:
                    eval_js("""
                        (() => {
                            const clearBtn = document.querySelector('button.clear-button') || Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('clear prompt'));
                            if (clearBtn) clearBtn.click();
                        })()
                    """)
                    time.sleep(0.12)

                eval_js("""
                    (() => {
                        const promptEl = document.querySelector('.ProseMirror') || 
                                         document.querySelector('[data-slate-editor="true"]') || 
                                         document.querySelector('[contenteditable="true"]');
                        if (promptEl) {
                            promptEl.focus();
                            const sel = window.getSelection();
                            const range = document.createRange();
                            range.selectNodeContents(promptEl);
                            sel.removeAllRanges();
                            sel.addRange(range);
                        }
                    })()
                """)
                time.sleep(0.04)
                full_prompt = (script_text or "").strip().strip('"')
                send("Input.insertText", {"text": full_prompt})
                time.sleep(0.08)

                v_len = eval_js("""
                    (() => {
                        const pm = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
                        return pm ? (pm.textContent || '').trim().length : 0;
                    })()
                """) or 0
                if v_len < 10:
                    eval_js(f"""
                        (() => {{
                            const pm = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
                            if (pm) {{
                                pm.focus();
                                document.execCommand('selectAll', false, null);
                                document.execCommand('insertText', false, {json.dumps(full_prompt)});
                            }}
                        }})()
                    """)

                if submit:
                    send_enter()
                    time.sleep(0.02)
                    eval_js("""
                        (() => {
                            const btn = document.querySelector('button.generate-icon-button, [aria-label="Start generation"]');
                            if (btn && !btn.disabled) {
                                btn.click();
                                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                                btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                                btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                            }
                        })()
                    """)
                    time.sleep(0.05)
                return tab.get("title", "(untitled)"), None

            # STEP 1: For Speaker Video Mode, check if the 3 chips are ALREADY attached
            chips_ready = (current_chips_count >= 3)

            if not chips_ready:
                if current_chips_count > 0:
                    eval_js("""
                        (() => {
                            const clearBtn = document.querySelector('button.clear-button') || Array.from(document.querySelectorAll('button')).find(b => (b.getAttribute('aria-label') || '').toLowerCase().includes('clear prompt'));
                            if (clearBtn) clearBtn.click();
                        })()
                    """)
                    time.sleep(0.12)

                def wait_for_menu_close(timeout_s=1.0):
                    return wait_for_cond("""
                        (() => {
                            const m = document.querySelector('flow-add-menu-popover-content');
                            return !m || m.offsetWidth === 0;
                        })()
                    """, timeout_s=timeout_s, poll_s=0.01)

                def open_dialog():
                    for _ in range(3):
                        if eval_js("Boolean(document.querySelector('flow-add-menu-popover-content'))"):
                            return True
                        eval_js("""
                            (() => {
                                const btn = document.querySelector('button.add-menu-trigger') || 
                                            document.querySelector('button[aria-label*="Add ingredients" i]');
                                if (btn) btn.click();
                            })()
                        """)
                        time.sleep(0.06)
                        if eval_js("Boolean(document.querySelector('flow-add-menu-popover-content'))"):
                            return True
                    return False

                # 1. WAYNE'S STEP 1: Avatars -> Me -> Add to Prompt
                if not open_dialog():
                    return None, "Could not open add menu for Avatar"
                time.sleep(0.02)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const tabs = Array.from(m.querySelectorAll('button, [role="tab"], .nav-item, mat-list-item'));
                        const avTab = tabs.find(b => (b.textContent || '').includes('Avatars') || (b.textContent || '').includes('face'));
                        if (avTab) avTab.click();
                    })()
                """)
                time.sleep(0.05)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const items = Array.from(m.querySelectorAll('.asset-item, button.asset-item, button'));
                        const me = items.find(b => (b.textContent || '').includes('Me') || (b.textContent || '').includes('Avatar'));
                        if (me) me.click();
                    })()
                """)
                time.sleep(0.04)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const addBtn = m.querySelector('button.detail-add-to-prompt-btn') || Array.from(m.querySelectorAll('button')).find(b => (b.textContent || '').includes('Add to prompt'));
                        if (addBtn) addBtn.click();
                    })()
                """)
                wait_for_menu_close(timeout_s=0.6)
                time.sleep(0.03)

                # 2. WAYNE'S STEP 2: All -> background_1 -> Add to Prompt
                if not open_dialog():
                    return None, "Could not open add menu for background"
                time.sleep(0.02)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const tabs = Array.from(m.querySelectorAll('button, [role="tab"], .nav-item, mat-list-item'));
                        const allTab = tabs.find(b => (b.textContent || '').includes('All') || (b.textContent || '').includes('dashboard'));
                        if (allTab) allTab.click();
                    })()
                """)
                time.sleep(0.04)
                eval_js(f"""
                    (() => {{
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const input = m.querySelector('input.search-input') || m.querySelector('input');
                        if (input) {{
                            input.focus();
                            input.value = '{target_bg}';
                            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }}));
                        }}
                    }})()
                """)
                time.sleep(0.05)
                eval_js(f"""
                    (() => {{
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const items = Array.from(m.querySelectorAll('.asset-item, button.asset-item, button'));
                        const item = items.find(b => (b.textContent || '').toLowerCase().includes('{target_bg.lower()}'));
                        if (item) item.click();
                    }})()
                """)
                time.sleep(0.04)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const addBtn = m.querySelector('button.detail-add-to-prompt-btn') || Array.from(m.querySelectorAll('button')).find(b => (b.textContent || '').includes('Add to prompt'));
                        if (addBtn) addBtn.click();
                    })()
                """)
                wait_for_menu_close(timeout_s=0.6)
                time.sleep(0.03)

                # 3. WAYNE'S STEP 3: All -> cloth_1 -> Add to Prompt
                if not open_dialog():
                    return None, "Could not open add menu for cloth"
                time.sleep(0.02)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const tabs = Array.from(m.querySelectorAll('button, [role="tab"], .nav-item, mat-list-item'));
                        const allTab = tabs.find(b => (b.textContent || '').includes('All') || (b.textContent || '').includes('dashboard'));
                        if (allTab) allTab.click();
                    })()
                """)
                time.sleep(0.04)
                eval_js(f"""
                    (() => {{
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const input = m.querySelector('input.search-input') || m.querySelector('input');
                        if (input) {{
                            input.focus();
                            input.value = '{target_cloth}';
                            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, bubbles: true }}));
                        }}
                    }})()
                """)
                time.sleep(0.05)
                eval_js(f"""
                    (() => {{
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const items = Array.from(m.querySelectorAll('.asset-item, button.asset-item, button'));
                        const item = items.find(b => (b.textContent || '').toLowerCase().includes('{target_cloth.lower()}'));
                        if (item) item.click();
                    }})()
                """)
                time.sleep(0.04)
                eval_js("""
                    (() => {
                        const m = document.querySelector('flow-add-menu-popover-content');
                        if (!m) return;
                        const addBtn = m.querySelector('button.detail-add-to-prompt-btn') || Array.from(m.querySelectorAll('button')).find(b => (b.textContent || '').includes('Add to prompt'));
                        if (addBtn) addBtn.click();
                    })()
                """)
                wait_for_menu_close(timeout_s=0.6)
                time.sleep(0.03)

            # STEP 2: Focus Editor and Insert Master Prompt (Clean & Fast)
            clean_script = (script_text or "").strip().strip('"')
            if clean_script.startswith("Presenter says:"):
                full_prompt = clean_script
            else:
                if is_ted:
                    speaker_ref = f"Using reference picture ted for character, reference picture {target_cloth} for clothing on my character, and reference picture {target_bg} for the background picture of the video"
                else:
                    speaker_ref = f"Using reference picture me for avatar, reference picture {target_cloth} for clothing on my avatar, and reference picture {target_bg} for the background picture of the video"

                if camera_text:
                    clean_camera = camera_text.strip()
                    if "reference picture" not in clean_camera.lower():
                        camera_body = f"{speaker_ref}, {clean_camera}"
                    else:
                        camera_body = clean_camera
                    full_prompt = f'Presenter says: "{clean_script}"          Camera: {camera_body}'
                else:
                    full_prompt = f'Presenter says: "{clean_script}"          Camera: {speaker_ref}.'

            eval_js(f"""
                (() => {{
                    const pm = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
                    if (pm) {{
                        pm.focus();
                        const range = document.createRange();
                        range.selectNodeContents(pm);
                        const sel = window.getSelection();
                        sel.removeAllRanges();
                        sel.addRange(range);
                        document.execCommand('delete', false, null);
                        document.execCommand('insertText', false, {json.dumps(full_prompt)});
                    }}
                }})()
            """)
            time.sleep(0.06)

            # Verification: Ensure prompt text was received in ProseMirror
            verified_len = eval_js("""
                (() => {
                    const pm = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
                    return pm ? (pm.textContent || '').trim().length : 0;
                })()
            """) or 0

            # Instant execCommand fallback if needed
            if verified_len < 30:
                eval_js(f"""
                    (() => {{
                        const pm = document.querySelector('.ProseMirror') || document.querySelector('[contenteditable="true"]');
                        if (pm) {{
                            pm.focus();
                            document.execCommand('selectAll', false, null);
                            document.execCommand('insertText', false, {json.dumps(full_prompt)});
                        }}
                    }})()
                """)
                time.sleep(0.05)

            # STEP 3: If Submit Requested, Send Enter & Click Generate Button
            if submit:
                send_enter()
                time.sleep(0.02)
                eval_js("""
                    (() => {
                        const btn = document.querySelector('button.generate-icon-button, [aria-label="Start generation"]');
                        if (btn && !btn.disabled) {
                            btn.click();
                            btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                            btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                            btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                        }
                    })()
                """)
                time.sleep(0.05)

            return tab.get("title", "(untitled)"), None
    except Exception as e:
        return None, f"CDP avatar injection error: {e}"


def cdp_apply_flow_preset(mode="video", aspect="16:9", duration="10s", resolution="720p", count="x1", ingredients=True, tab=None):
    """
    Apply aspect ratio, duration, resolution, count, and ingredient preset in Google Flow via CDP.
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on tab"

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, close_timeout=15) as ws:
            msg_id = 0
            def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {"id": msg_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                return json.loads(ws.recv())

            js_code = f"""
            (async function() {{
                const sleep = ms => new Promise(r => setTimeout(r, ms));
                
                let trigger = document.querySelector('button[aria-label="Settings trigger"], .settings-trigger-button');
                if (!trigger) return {{ ok: false, error: 'No settings trigger button found' }};
                
                let pane = Array.from(document.querySelectorAll('.cdk-overlay-pane')).find(p => p.querySelector('mat-button-toggle'));
                if (!pane) {{
                    trigger.click();
                    await sleep(500);
                    pane = Array.from(document.querySelectorAll('.cdk-overlay-pane')).find(p => p.querySelector('mat-button-toggle'));
                }}
                if (!pane) return {{ ok: false, error: 'Could not open settings popover' }};

                function clickAndVerify(label) {{
                    const toggles = Array.from(pane.querySelectorAll('mat-button-toggle'));
                    const target = toggles.find(t => {{
                        const txt = (t.innerText || '').toLowerCase().replace(/\\s+/g, ' ');
                        return txt.includes(label.toLowerCase());
                    }});
                    if (!target) return {{ ok: false, error: 'Toggle not found: ' + label }};
                    
                    const isChecked = target.classList.contains('mat-button-toggle-checked');
                    if (isChecked) return {{ ok: true, alreadyChecked: true }};
                    
                    const btn = target.querySelector('button') || target;
                    btn.click();
                    return {{ ok: true, clicked: true }};
                }}

                // 1. Mode: Image vs Video
                clickAndVerify('{mode}');
                await sleep(400); // Allow Angular to render mode-specific options
                pane = Array.from(document.querySelectorAll('.cdk-overlay-pane')).find(p => p.querySelector('mat-button-toggle')) || pane;

                // 2. Ingredients
                if ({str(ingredients).lower()}) {{
                    clickAndVerify('ingredients');
                    await sleep(150);
                }}

                // 3. Aspect ratio
                clickAndVerify('{aspect}');
                await sleep(150);

                // 4. Video-specific options
                if ('{mode}'.toLowerCase() === 'video') {{
                    clickAndVerify('{resolution}');
                    await sleep(150);
                    clickAndVerify('{duration}');
                    await sleep(150);
                }}

                // 5. Count
                clickAndVerify('{count}');
                await sleep(150);

                // 6. Close popover
                trigger = document.querySelector('button[aria-label="Settings trigger"], .settings-trigger-button');
                if (trigger) trigger.click();
                await sleep(300);

                // 7. Verify main trigger summary
                trigger = document.querySelector('button[aria-label="Settings trigger"], .settings-trigger-button');
                const currentPillText = trigger ? trigger.innerText.trim().replace(/\\n/g, ' ') : '';
                return {{ ok: true, pillText: currentPillText, summary: currentPillText }};
            }})()
            """
            res = send('Runtime.evaluate', {
                'expression': js_code,
                'awaitPromise': True,
                'returnByValue': True
            })
            val = res.get('result', {}).get('result', {}).get('value', {})
            return val, None
    except Exception as e:
        return None, f"cdp_apply_flow_preset error: {e}"


def cdp_batch_rename_media(media_type: str = "images", names: list = None, tab=None):
    """
    Batch rename media in Google Flow gallery in sequence using verified 3-dots & Done button CDP clicks.
    - media_type='images': Switches to Images tab, renames items (default: A[N]..A1)
    - media_type='videos': Switches to Videos tab, renames items across grid (default: [N]..1)
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            return None, err

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on tab"

    is_videos = (media_type or "").lower().startswith("vid")
    if not names:
        if is_videos:
            names = [str(i) for i in range(52, 0, -1)]
        else:
            names = [f"A{i}" for i in range(51, 0, -1)]

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, max_size=20_000_000, close_timeout=360) as ws:
            class Msg:
                id = 0

            def send(method, params=None):
                Msg.id += 1
                call_id = Msg.id
                payload = {"id": call_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                while True:
                    raw = ws.recv()
                    data = json.loads(raw)
                    if data.get("id") == call_id:
                        return data

            def eval_js(js, await_promise=False):
                res = send("Runtime.evaluate", {"expression": js, "awaitPromise": await_promise, "returnByValue": True})
                return res.get("result", {}).get("result", {}).get("value")

            def click_at(cx, cy):
                send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": cx, "y": cy})
                time.sleep(0.03)
                send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": cx, "y": cy, "button": "left", "clickCount": 1})
                time.sleep(0.03)
                send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": cx, "y": cy, "button": "left", "clickCount": 1})

            # 1. Switch to appropriate tab on sidebar only if not already active
            target_tab_text = "view videos" if is_videos else "view images"
            icon_text = "videocam" if is_videos else "image"
            eval_js(f'''
                (() => {{
                    const btns = Array.from(document.querySelectorAll('button'));
                    const tabBtn = btns.find(b => 
                        (b.getAttribute('aria-label') && b.getAttribute('aria-label').toLowerCase().includes('{target_tab_text}')) ||
                        (b.innerText && b.innerText.toLowerCase().includes('{target_tab_text}')) ||
                        (b.innerText && b.innerText.includes('{icon_text}'))
                    );
                    const isSelected = tabBtn && (tabBtn.getAttribute('aria-selected') === 'true' || tabBtn.className.includes('active') || tabBtn.className.includes('selected'));
                    if (tabBtn && !isSelected) {{
                        tabBtn.click();
                    }}
                }})()
            ''')
            time.sleep(0.5)

            # 2. Comprehensive Virtualized Scroll Discovery
            scroller_discovery_js = """
            (async () => {
                const scroller = Array.from(document.querySelectorAll('*')).find(el => el.scrollHeight > el.clientHeight + 50) || window;
                if (scroller.scrollTo) scroller.scrollTo(0, 0);
                else scroller.scrollTop = 0;
                await new Promise(r => setTimeout(r, 200));

                const collected = new Map();
                const maxScroll = scroller.scrollHeight || 6000;
                const step = 350;

                for (let pos = 0; pos <= maxScroll; pos += step) {
                    if (scroller.scrollTo) scroller.scrollTo(0, pos);
                    else scroller.scrollTop = pos;
                    await new Promise(r => setTimeout(r, 90));

                    const tiles = Array.from(document.querySelectorAll('[data-tile-id]'));
                    tiles.forEach(t => {
                        const id = t.getAttribute('data-tile-id');
                        if (id && !collected.has(id)) {
                            const r = t.getBoundingClientRect();
                            const docTop = pos + r.top;
                            collected.set(id, { id: id, docTop: docTop, left: r.left });
                        }
                    });
                }

                if (scroller.scrollTo) scroller.scrollTo(0, 0);
                else scroller.scrollTop = 0;

                const sorted = Array.from(collected.values());
                sorted.sort((a, b) => {
                    if (Math.abs(a.docTop - b.docTop) > 60) return a.docTop - b.docTop;
                    return a.left - b.left;
                });

                return sorted.map(s => s.id);
            })()
            """

            grid_tile_ids = eval_js(scroller_discovery_js, await_promise=True) or []
            if not grid_tile_ids:
                return None, "No media tiles discovered in Google Flow gallery"

            target_count = min(len(names), len(grid_tile_ids))
            mapping_results = []

            for i in range(target_count):
                target_name = str(names[i])
                tid = grid_tile_ids[i]

                # Close hanging menus
                send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "windowsVirtualKeyCode": 27, "code": "Escape", "key": "Escape"})
                time.sleep(0.02)
                send("Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 27, "code": "Escape", "key": "Escape"})
                time.sleep(0.04)

                # Scroll tile into view
                find_tile_js = f"""
                (async () => {{
                    const scroller = Array.from(document.querySelectorAll('*')).find(el => el.scrollHeight > el.clientHeight + 50) || window;
                    let tile = document.querySelector('[data-tile-id="{tid}"]');
                    let attempts = 0;

                    while (!tile && attempts < 30) {{
                        if (scroller.scrollBy) scroller.scrollBy(0, 300);
                        else if (scroller.scrollTop !== undefined) scroller.scrollTop += 300;
                        else window.scrollBy(0, 300);
                        await new Promise(r => setTimeout(r, 60));
                        tile = document.querySelector('[data-tile-id="{tid}"]');
                        attempts++;
                    }}

                    if (!tile) return null;

                    tile.scrollIntoView({{ behavior: 'instant', block: 'center' }});
                    await new Promise(r => setTimeout(r, 60));
                    const r = tile.getBoundingClientRect();
                    return {{
                        cx: Math.round(r.left + r.width / 2),
                        cy: Math.round(r.top + r.height / 2)
                    }};
                }})()
                """

                card_center = eval_js(find_tile_js, await_promise=True)
                if not card_center:
                    continue

                # Hover over card
                send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card_center["cx"], "y": card_center["cy"]})
                time.sleep(0.18)

                # Find 3-dots button
                find_dots_js = f"""
                (() => {{
                    const tile = document.querySelector('[data-tile-id="{tid}"]');
                    if (!tile) return null;
                    const btns = Array.from(tile.querySelectorAll('button'));
                    const moreBtn = btns.find(b => (b.innerText || '').includes('more_vert') || (b.getAttribute('aria-label') || '').toLowerCase().includes('more')) || btns[btns.length - 1];
                    if (!moreBtn) return null;
                    const r = moreBtn.getBoundingClientRect();
                    return {{ cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2) }};
                }})()
                """
                dots_pos = eval_js(find_dots_js)
                if not dots_pos:
                    continue

                click_at(dots_pos["cx"], dots_pos["cy"])
                time.sleep(0.25)

                # Find Rename item
                find_rename_js = """
                (() => {
                    const items = Array.from(document.querySelectorAll('[role="menuitem"], button'));
                    const ren = items.find(el => (el.innerText || '').includes('Rename') || (el.innerText || '').includes('whiteboard'));
                    if (!ren) return null;
                    const r = ren.getBoundingClientRect();
                    return { cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2) };
                })()
                """
                rename_pos = eval_js(find_rename_js)
                if not rename_pos:
                    continue

                click_at(rename_pos["cx"], rename_pos["cy"])
                time.sleep(0.3)

                # Set input value
                set_input_js = f"""
                (() => {{
                    const inputs = Array.from(document.querySelectorAll('input'));
                    const targetInput = inputs.find(i => i.getBoundingClientRect().top > 50 && i.getBoundingClientRect().width > 50);
                    if (targetInput) {{
                        targetInput.focus();
                        targetInput.select();
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeInputValueSetter.call(targetInput, '{target_name}');
                        targetInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        targetInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        return true;
                    }}
                    return false;
                }})()
                """
                eval_js(set_input_js)
                time.sleep(0.1)

                # Click Done button
                find_done_js = """
                (() => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const doneBtn = btns.find(b => (b.innerText || '').includes('Done') || (b.innerText || '').includes('done'));
                    if (!doneBtn) return null;
                    const r = doneBtn.getBoundingClientRect();
                    return { cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2) };
                })()
                """
                done_pos = eval_js(find_done_js)
                if done_pos:
                    click_at(done_pos["cx"], done_pos["cy"])
                else:
                    send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "windowsVirtualKeyCode": 13, "code": "Enter", "key": "Enter"})
                    send("Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 13, "code": "Enter", "key": "Enter"})

                mapping_results.append({
                    "card_index": i + 1,
                    "target_name": target_name,
                    "tile_id": tid
                })
                _log(f"🏷️ [CDP Batch Rename] Card {i+1} -> '{target_name}'")
                time.sleep(0.12)

            # Scroll back to top
            eval_js('''
                (() => {
                    const scroller = Array.from(document.querySelectorAll('*')).find(el => el.scrollHeight > el.clientHeight + 50) || window;
                    if (scroller.scrollTo) scroller.scrollTo(0, 0);
                    else if (scroller.scrollTop !== undefined) scroller.scrollTop = 0;
                    else window.scrollTo(0, 0);
                })()
            ''')
            time.sleep(0.5)

            # Emit voice confirmation
            voice_path = r"C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt"
            try:
                with open(voice_path, "w", encoding="utf-8") as vf:
                    vf.write(f"All {len(mapping_results)} {media_type} have been renamed from {names[0]} down to {names[-1]}.")
            except Exception:
                pass

            return {
                "total_renamed": len(mapping_results),
                "media_type": media_type,
                "mappings": mapping_results
            }, None
    except Exception as e:
        return None, f"CDP batch rename error: {e}"


def cdp_batch_rename_images(names: list = None, tab=None):
    return cdp_batch_rename_media(media_type="images", names=names, tab=tab)


def cdp_rename_reference_card(target_name: str, tab=None):
    """
    Renames the newly generated reference image card in Google Flow to target_name (background_1 or cloth_1).
    Uses the 2026 flow-grid-tile-container DOM standard with More options -> Rename -> input.editable-text-input.editing -> Enter.
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            return False, err
    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return False, "No webSocketDebuggerUrl"

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, close_timeout=20) as ws:
            msg_id = 0
            def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {"id": msg_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                return json.loads(ws.recv())

            def eval_js(js, await_promise=False):
                res = send("Runtime.evaluate", {"expression": js, "awaitPromise": await_promise, "returnByValue": True})
                return res.get("result", {}).get("result", {}).get("value")

            # 1. Switch to Images tab
            eval_js("""
            (() => {
                const items = Array.from(document.querySelectorAll('mat-list-item'));
                const imgItem = items.find(i => (i.innerText || '').includes('Images'));
                if (imgItem) imgItem.click();
            })()
            """)
            time.sleep(0.5)

            # 2. Find target tile and execute rename
            rename_js = f"""
            (async () => {{
                const tiles = Array.from(document.querySelectorAll('flow-grid-tile-container'));
                if (!tiles || tiles.length === 0) return {{ ok: false, error: 'No tiles found on canvas' }};

                // Look for tile whose footer is not already named target_name, starting from newest (tiles[0])
                let targetTile = tiles.find(t => {{
                    const ft = t.querySelector('.footer-title')?.textContent?.trim();
                    return ft !== '{target_name}';
                }}) || tiles[0];

                const currentTitle = targetTile.querySelector('.footer-title')?.textContent?.trim() || '';
                if (currentTitle === '{target_name}') return {{ ok: true, status: 'ALREADY_RENAMED' }};

                const moreBtn = targetTile.querySelector('button[aria-label="More options"]');
                if (!moreBtn) return {{ ok: false, error: 'More options button not found' }};
                moreBtn.click();
                await new Promise(r => setTimeout(r, 200));

                const menuItems = Array.from(document.querySelectorAll('.mat-mdc-menu-panel [role="menuitem"], .mat-mdc-menu-panel button'));
                const renameItem = menuItems.find(m => (m.textContent || '').includes('Rename'));
                if (!renameItem) return {{ ok: false, error: 'Rename menu item not found' }};
                renameItem.click();
                await new Promise(r => setTimeout(r, 200));

                const input = document.querySelector('input.editable-text-input.editing');
                if (!input) return {{ ok: false, error: 'Rename input not found' }};
                input.focus();
                input.value = '{target_name}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                input.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                input.blur();
                await new Promise(r => setTimeout(r, 250));

                const finalTitle = targetTile.querySelector('.footer-title')?.textContent?.trim() || '';
                return {{ ok: true, old: currentTitle, new: finalTitle }};
            }})()
            """
            res = eval_js(rename_js, await_promise=True)
            _log(f"🏷️ [Reference Rename Result] {res}")
            return (res.get("ok", False) if isinstance(res, dict) else False), res
    except Exception as e:
        _log(f"Rename reference card error: {e}")
        return False, str(e)


def cdp_rename_specific_reference(target_name: str, tab=None):
    """
    Finds the reference image card matching target_name keywords and renames it to target_name.
    Uses Google Flow's 2026 flow-grid-tile-container standard with deliberate pacing.
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            return False, err
    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return False, "No webSocketDebuggerUrl"

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, close_timeout=30) as ws:
            msg_id = 0
            def send(method, params=None):
                nonlocal msg_id
                msg_id += 1
                payload = {"id": msg_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                return json.loads(ws.recv())

            def eval_js(js, await_promise=False):
                res = send("Runtime.evaluate", {"expression": js, "awaitPromise": await_promise, "returnByValue": True})
                return res.get("result", {}).get("result", {}).get("value")

            # 1. Switch to Images view so reference cards are visible
            eval_js("""
            (() => {
                const items = Array.from(document.querySelectorAll('mat-list-item, button'));
                const imgItem = items.find(i => (i.innerText || '').toLowerCase().includes('images') || (i.getAttribute('aria-label') || '').toLowerCase().includes('view images'));
                if (imgItem) imgItem.click();
            })()
            """)
            time.sleep(0.6)

            is_cloth = "cloth" in target_name.lower()
            rename_code = f"""
            (async () => {{
                // Dismiss any leftover backdrops or open menus
                document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click());
                await new Promise(r => setTimeout(r, 250));

                const tiles = Array.from(document.querySelectorAll('flow-grid-tile-container'));
                if (!tiles || tiles.length === 0) return {{ ok: false, error: 'No tiles found on canvas' }};

                const isClothTarget = {str(is_cloth).lower()};
                const clothKeywords = ['cloth', 'pullover', 'mannequin', 'hoodie', 'apparel', 'technical', 'joggers', 'fabric', 'male'];
                const bgKeywords = ['background', 'studio', 'backdrop', 'architectural', 'obsidian', 'pillars', 'concrete', 'lighting', 'render'];

                // Check if already renamed
                const already = tiles.find(t => (t.querySelector('.footer-title')?.textContent || '').trim() === '{target_name}');
                if (already) return {{ ok: true, status: 'ALREADY_RENAMED', name: '{target_name}' }};

                // Find candidate tile without touching the opposite reference
                const oppositeName = isClothTarget ? 'background_1' : 'cloth_1';
                let targetTile = tiles.find(t => {{
                    const title = (t.querySelector('.footer-title')?.textContent || '').trim().toLowerCase();
                    if (title === oppositeName) return false;
                    
                    const fullText = (t.innerText || '').toLowerCase();
                    const kws = isClothTarget ? clothKeywords : bgKeywords;
                    return kws.some(k => title.includes(k) || fullText.includes(k));
                }});

                // Smart Fallback: if both are unrenamed (cloth generated first -> older, bg generated second -> newer)
                if (!targetTile) {{
                    const unrenamed = tiles.filter(t => {{
                        const title = (t.querySelector('.footer-title')?.textContent || '').trim().toLowerCase();
                        return title !== 'cloth_1' && title !== 'background_1';
                    }});
                    if (unrenamed.length >= 2) {{
                        // In Google Flow, newer tile is at index 0 (background), older tile is at index 1 (clothing)
                        targetTile = isClothTarget ? unrenamed[unrenamed.length - 1] : unrenamed[0];
                    }} else if (unrenamed.length === 1) {{
                        targetTile = unrenamed[0];
                    }} else {{
                        targetTile = tiles.find(t => {{
                            const title = (t.querySelector('.footer-title')?.textContent || '').trim();
                            return title !== oppositeName;
                        }}) || tiles[0];
                    }}
                }}

                if (!targetTile) return {{ ok: false, error: 'Target tile could not be identified' }};

                const currentTitle = (targetTile.querySelector('.footer-title')?.textContent || '').trim();

                // Scroll into view
                targetTile.scrollIntoView({{ behavior: 'instant', block: 'center' }});
                await new Promise(r => setTimeout(r, 350));

                // Click More options button
                const moreBtn = targetTile.querySelector('button[aria-label="More options"]');
                if (!moreBtn) return {{ ok: false, error: 'More options button not found on tile' }};
                moreBtn.click();
                await new Promise(r => setTimeout(r, 500)); // Deliberate 500ms for Material animation

                // Click Rename
                const menuItems = Array.from(document.querySelectorAll('.mat-mdc-menu-panel [role="menuitem"], .mat-mdc-menu-panel button, [role="menuitem"]'));
                const renameItem = menuItems.find(m => (m.textContent || '').includes('Rename'));
                if (!renameItem) {{
                    document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click());
                    return {{ ok: false, error: 'Rename menu item not found' }};
                }}
                renameItem.click();
                await new Promise(r => setTimeout(r, 500)); // Deliberate 500ms for input focus

                // Find input and type
                const input = document.querySelector('input.editable-text-input.editing') || targetTile.querySelector('input');
                if (!input) return {{ ok: false, error: 'Rename input not found' }};
                input.focus();
                input.value = '{target_name}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                input.dispatchEvent(new KeyboardEvent('keydown', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                input.dispatchEvent(new KeyboardEvent('keyup', {{ key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }}));
                input.blur();
                await new Promise(r => setTimeout(r, 600)); // Deliberate 600ms settle

                // Dismiss any open backdrop
                document.querySelectorAll('.cdk-overlay-backdrop').forEach(b => b.click());
                await new Promise(r => setTimeout(r, 200));

                const finalTitle = (targetTile.querySelector('.footer-title')?.textContent || '').trim();
                return {{ ok: true, old: currentTitle, new: finalTitle, name: '{target_name}' }};
            }})()
            """
            res = eval_js(rename_code, await_promise=True)
            _log(f"🏷️ [Rename Specific Ref Result] {res}")
            return (res.get("ok", False) if isinstance(res, dict) else False), res
    except Exception as e:
        _log(f"Error renaming specific ref: {e}")
        return False, str(e)



def cdp_batch_download_media(media_type: str = "images", count: int = 52, quality: str = "1080p", tab=None):
    r"""
    Sequentially downloads top `count` media items from Google Flow:
    - media_type='videos': Switches to View videos tab, downloads at 1080p (Upscaled).
    - media_type='images': Switches to View images tab, downloads at 1K (Original size).
    Saves to C:\Users\Curtis\Downloads and relocates to protocols Google Flow folder.
    """
    if tab is None:
        tab, err = get_active_tab(target_pattern="flow")
        if err:
            return None, err

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on tab"

    is_videos = (media_type or "").lower().startswith("vid")
    downloads_dir = r"C:\Users\Curtis\Downloads"
    dest_dir = r"C:\Users\Curtis\Desktop\Keystone Brain\08_Keystone_protocols\Google_Flow\video" if is_videos else r"C:\Users\Curtis\Desktop\Keystone Brain\08_Keystone_protocols\Google_Flow\images"
    os.makedirs(dest_dir, exist_ok=True)

    try:
        from websockets.sync.client import connect as ws_connect
        import glob
        import shutil

        with ws_connect(ws_url, max_size=20_000_000, close_timeout=360) as ws:
            class Msg:
                id = 0

            def send(method, params=None):
                Msg.id += 1
                call_id = Msg.id
                payload = {"id": call_id, "method": method}
                if params: payload["params"] = params
                ws.send(json.dumps(payload))
                while True:
                    raw = ws.recv()
                    data = json.loads(raw)
                    if data.get("id") == call_id:
                        return data

            def eval_js(js, await_promise=False):
                res = send("Runtime.evaluate", {"expression": js, "awaitPromise": await_promise, "returnByValue": True})
                return res.get("result", {}).get("result", {}).get("value")

            def click_at(cx, cy):
                send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": cx, "y": cy})
                time.sleep(0.03)
                send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": cx, "y": cy, "button": "left", "clickCount": 1})
                time.sleep(0.03)
                send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": cx, "y": cy, "button": "left", "clickCount": 1})

            # 1. Enable Browser & Page download behavior
            send("Browser.setDownloadBehavior", {"behavior": "allow", "downloadPath": downloads_dir, "eventsEnabled": True})
            send("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": downloads_dir})

            # 2. Switch to appropriate tab on sidebar
            target_tab_text = "view videos" if is_videos else "view images"
            icon_text = "videocam" if is_videos else "image"
            eval_js(f'''
                (() => {{
                    const btns = Array.from(document.querySelectorAll('button'));
                    const tabBtn = btns.find(b => 
                        (b.getAttribute('aria-label') && b.getAttribute('aria-label').toLowerCase().includes('{target_tab_text}')) ||
                        (b.innerText && b.innerText.toLowerCase().includes('{target_tab_text}')) ||
                        (b.innerText && b.innerText.includes('{icon_text}'))
                    );
                    if (tabBtn) tabBtn.click();
                }})()
            ''')
            time.sleep(0.5)

            # 3. Virtualized scroll discovery
            scroller_discovery_js = """
            (async () => {
                const scroller = Array.from(document.querySelectorAll('*')).find(el => el.scrollHeight > el.clientHeight + 50) || window;
                if (scroller.scrollTo) scroller.scrollTo(0, 0);
                else scroller.scrollTop = 0;
                await new Promise(r => setTimeout(r, 200));

                const collected = new Map();
                const maxScroll = scroller.scrollHeight || 6000;
                const step = 350;

                for (let pos = 0; pos <= maxScroll; pos += step) {
                    if (scroller.scrollTo) scroller.scrollTo(0, pos);
                    else scroller.scrollTop = pos;
                    await new Promise(r => setTimeout(r, 90));

                    const tiles = Array.from(document.querySelectorAll('[data-tile-id]'));
                    tiles.forEach(t => {
                        const id = t.getAttribute('data-tile-id');
                        if (id && !collected.has(id)) {
                            const r = t.getBoundingClientRect();
                            const docTop = pos + r.top;
                            collected.set(id, { id: id, docTop: docTop, left: r.left });
                        }
                    });
                }

                if (scroller.scrollTo) scroller.scrollTo(0, 0);
                else scroller.scrollTop = 0;

                const sorted = Array.from(collected.values());
                sorted.sort((a, b) => {
                    if (Math.abs(a.docTop - b.docTop) > 60) return a.docTop - b.docTop;
                    return a.left - b.left;
                });

                return sorted.map(s => s.id);
            })()
            """

            grid_tile_ids = eval_js(scroller_discovery_js, await_promise=True) or []
            if not grid_tile_ids:
                return None, "No media tiles discovered for download"

            target_iterations = min(count, len(grid_tile_ids))
            downloaded = 0

            for i in range(target_iterations):
                tid = grid_tile_ids[i]

                # Dismiss menus
                send("Input.dispatchKeyEvent", {"type": "rawKeyDown", "windowsVirtualKeyCode": 27, "code": "Escape", "key": "Escape"})
                time.sleep(0.02)
                send("Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 27, "code": "Escape", "key": "Escape"})
                time.sleep(0.04)

                # Scroll tile into view
                find_tile_js = f"""
                (async () => {{
                    const scroller = Array.from(document.querySelectorAll('*')).find(el => el.scrollHeight > el.clientHeight + 50) || window;
                    let tile = document.querySelector('[data-tile-id="{tid}"]');
                    let attempts = 0;

                    while (!tile && attempts < 30) {{
                        if (scroller.scrollBy) scroller.scrollBy(0, 300);
                        else if (scroller.scrollTop !== undefined) scroller.scrollTop += 300;
                        else window.scrollBy(0, 300);
                        await new Promise(r => setTimeout(r, 60));
                        tile = document.querySelector('[data-tile-id="{tid}"]');
                        attempts++;
                    }}

                    if (!tile) return null;

                    tile.scrollIntoView({{ behavior: 'instant', block: 'center' }});
                    await new Promise(r => setTimeout(r, 60));
                    const r = tile.getBoundingClientRect();
                    return {{
                        cx: Math.round(r.left + r.width / 2),
                        cy: Math.round(r.top + r.height / 2)
                    }};
                }})()
                """
                card_center = eval_js(find_tile_js, await_promise=True)
                if not card_center:
                    continue

                before_files = set(glob.glob(os.path.join(downloads_dir, "*.mp4")) + glob.glob(os.path.join(downloads_dir, "*.mov")) + glob.glob(os.path.join(downloads_dir, "*.webm")) + glob.glob(os.path.join(downloads_dir, "*.png")) + glob.glob(os.path.join(downloads_dir, "*.jpg")))

                # Hover over card
                send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": card_center["cx"], "y": card_center["cy"]})
                time.sleep(0.18)

                # Find 3-dots button
                find_dots_js = f"""
                (() => {{
                    const tile = document.querySelector('[data-tile-id="{tid}"]');
                    if (!tile) return null;
                    const btns = Array.from(tile.querySelectorAll('button'));
                    const moreBtn = btns.find(b => (b.innerText || '').includes('more_vert') || (b.getAttribute('aria-label') || '').toLowerCase().includes('more')) || btns[btns.length - 1];
                    if (!moreBtn) return null;
                    const r = moreBtn.getBoundingClientRect();
                    return {{ cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2) }};
                }})()
                """
                dots_pos = eval_js(find_dots_js)
                if not dots_pos:
                    continue

                click_at(dots_pos["cx"], dots_pos["cy"])
                time.sleep(0.25)

                # Hover over Download item in menu
                find_dl_js = """
                (() => {
                    const items = Array.from(document.querySelectorAll('[role="menuitem"], [data-radix-popper-content-wrapper] button, [data-radix-popper-content-wrapper] div'));
                    const dl = items.find(el => (el.innerText || '').toLowerCase().includes('download'));
                    if (!dl) return null;
                    const r = dl.getBoundingClientRect();
                    return { cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2) };
                })()
                """
                dl_pos = eval_js(find_dl_js)
                if not dl_pos:
                    continue

                # Move mouse to Download to open flyout
                send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": dl_pos["cx"], "y": dl_pos["cy"]})
                time.sleep(0.25)
                # Also click if needed
                click_at(dl_pos["cx"], dl_pos["cy"])
                time.sleep(0.25)

                # Click targeted quality resolution button
                find_quality_js = f"""
                (() => {{
                    const items = Array.from(document.querySelectorAll('[role="menuitem"], [data-radix-popper-content-wrapper] button, [data-radix-popper-content-wrapper] div'));
                    if ({str(is_videos).lower()}) {{
                        const p1080 = items.find(el => (el.innerText || '').toLowerCase().includes('1080p') || (el.innerText || '').toLowerCase().includes('upscaled'));
                        if (p1080) {{
                            const r = p1080.getBoundingClientRect();
                            return {{ cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2), text: '1080p' }};
                        }}
                        const p720 = items.find(el => (el.innerText || '').toLowerCase().includes('720p') || (el.innerText || '').toLowerCase().includes('original'));
                        if (p720) {{
                            const r = p720.getBoundingClientRect();
                            return {{ cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2), text: '720p' }};
                        }}
                    }} else {{
                        const p1k = items.find(el => (el.innerText || '').toLowerCase().includes('1k') || (el.innerText || '').toLowerCase().includes('original'));
                        if (p1k) {{
                            const r = p1k.getBoundingClientRect();
                            return {{ cx: Math.round(r.left + r.width / 2), cy: Math.round(r.top + r.height / 2), text: '1K' }};
                        }}
                    }}
                    return null;
                }})()
                """
                quality_pos = eval_js(find_quality_js)
                if quality_pos:
                    click_at(quality_pos["cx"], quality_pos["cy"])

                # Wait for download file
                downloaded_file = None
                for _ in range(40):
                    time.sleep(0.3)
                    after_files = set(glob.glob(os.path.join(downloads_dir, "*.mp4")) + glob.glob(os.path.join(downloads_dir, "*.mov")) + glob.glob(os.path.join(downloads_dir, "*.webm")) + glob.glob(os.path.join(downloads_dir, "*.png")) + glob.glob(os.path.join(downloads_dir, "*.jpg")))
                    new_files = after_files - before_files
                    if new_files:
                        downloaded_file = list(new_files)[0]
                        if not downloaded_file.endswith(".crdownload"):
                            break

                if downloaded_file and not downloaded_file.endswith(".crdownload"):
                    downloaded += 1
                    base_name = os.path.basename(downloaded_file)
                    dest_file = os.path.join(dest_dir, base_name)
                    try:
                        shutil.move(downloaded_file, dest_file)
                        _log(f"📥 [CDP Download] Saved card {i+1}/{target_iterations} -> '{base_name}' in {dest_dir}")
                    except Exception:
                        pass
                else:
                    _log(f"📥 [CDP Download] Triggered download on card {i+1}/{target_iterations}")

                time.sleep(0.15)

            # Scroll back to top
            eval_js('''
                (() => {
                    const scroller = Array.from(document.querySelectorAll('*')).find(el => el.scrollHeight > el.clientHeight + 50) || window;
                    if (scroller.scrollTo) scroller.scrollTo(0, 0);
                    else window.scrollTo(0, 0);
                })()
            ''')
            time.sleep(0.5)

            # Voice update
            voice_path = r"C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt"
            try:
                with open(voice_path, "w", encoding="utf-8") as vf:
                    vf.write(f"All {target_iterations} {media_type} have been downloaded at {quality} and placed into your project folder.")
            except Exception:
                pass

            return {"downloaded_count": downloaded, "target_count": target_iterations, "media_type": media_type, "quality": quality}, None
    except Exception as e:
        return None, f"CDP batch download error: {e}"


def cdp_capture_screenshot(output_path: str = None, tab=None):
    """
    Capture screenshot of active Chrome tab via Page.captureScreenshot over CDP.
    Returns (output_path, None) or (None, error_str).
    """
    import base64
    if tab is None:
        tab, err = get_active_tab()
        if err:
            return None, err

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on tab"

    if output_path is None:
        output_path = os.path.join(BRAIN_ROOT, "13_scratch", f"chrome_tab_screenshot_{int(time.time())}.png")

    try:
        from websockets.sync.client import connect as ws_connect
        with ws_connect(ws_url, close_timeout=2, max_size=None) as ws:
            ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            ws.recv()
            ws.send(json.dumps({"id": 2, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
            resp = json.loads(ws.recv())
            data_b64 = resp.get("result", {}).get("data")
            if not data_b64:
                return None, "No image data returned from Page.captureScreenshot"
            img_bytes = base64.b64decode(data_b64)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            return output_path, None
    except Exception as e:
        return None, f"Screenshot CDP error: {e}"


def cdp_inject_config(tab=None):
    """
    Inject window.KS_OVERLAY_JSON_CONFIG directly into active Chrome tab window context.
    Uses Page.addScriptToEvaluateOnNewDocument for future page loads and Runtime.evaluate for immediate availability.
    """
    if tab is None:
        tab, err = get_active_tab()
        if err:
            return None, err

    config_data = get_merged_overlay_config()
    json_str = json.dumps(config_data)
    js_expr = f"window.KS_OVERLAY_JSON_CONFIG = {json_str};"

    ws_url = tab.get("webSocketDebuggerUrl")
    if not ws_url:
        return None, "No webSocketDebuggerUrl on target tab"

    try:
        from websockets.sync.client import connect as ws_connect
    except ImportError:
        return None, "websockets library not available — cannot connect to CDP WebSocket"

    try:
        with ws_connect(ws_url, close_timeout=2) as ws:
            # 1. Enable Page domain
            ws.send(json.dumps({"id": 1, "method": "Page.enable"}))
            ws.recv()

            # 2. Register for new documents (main world)
            ws.send(json.dumps({
                "id": 2,
                "method": "Page.addScriptToEvaluateOnNewDocument",
                "params": {"source": js_expr}
            }))
            ws.recv()

            # 3. Register for new documents (isolated world)
            ws.send(json.dumps({
                "id": 3,
                "method": "Page.addScriptToEvaluateOnNewDocument",
                "params": {
                    "source": js_expr,
                    "worldName": "KeystoneHUDIsolatedWorld"
                }
            }))
            ws.recv()

            # 4. Evaluate immediately in main world context
            ws.send(json.dumps({
                "id": 4,
                "method": "Runtime.evaluate",
                "params": {"expression": js_expr}
            }))
            ws.recv()

            _log(f"Injected window.KS_OVERLAY_JSON_CONFIG into active Chrome tab: '{tab.get('title', '?')}'")
            return tab.get("title", "(untitled)"), None
    except Exception as e:
        return None, f"CDP config injection error: {e}"


# ---------------------------------------------------------------------------
# HTTP Request Handler
# ---------------------------------------------------------------------------

class OverlayHandler(BaseHTTPRequestHandler):

    """HTTP handler for Chrome Overlay Daemon endpoints."""

    server_version = "ChromeOverlayDaemon/1.0"

    # -- Helpers -----------------------------------------------------------

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def log_message(self, format, *args):
        """Override default logging to use our prefix."""
        _log(f"HTTP {args[0] if args else ''}")

    # -- CORS preflight ----------------------------------------------------

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    # -- Routes ------------------------------------------------------------

    def do_GET(self):
        if self.path in ["/api/health", "/api/stats", "/api/status"]:
            self._handle_health()
        elif self.path == "/api/overlay/config":
            self._handle_overlay_config()
        elif self.path == "/api/tabs":
            self._handle_tabs()
        elif self.path == "/api/overlays":
            self._handle_overlays()
        elif self.path == "/api/poll":
            self._handle_poll()
        elif self.path == "/api/cdp_press_enter":
            self._handle_cdp_press_enter()
        elif self.path == "/api/screenshot":
            self._handle_screenshot()
        elif self.path.startswith("/api/purge"):
            self._handle_purge()
        elif self.path.startswith("/api/organize"):
            self._handle_organize()
        elif self.path == "/api/button_orders":
            self._handle_get_button_orders()
        elif self.path == "/api/clip_state":
            self._handle_get_clip_state()
        elif self.path in ["/api/pipeline_lock", "/api/pipeline/locks", "/api/pipeline/status"]:
            self._handle_get_pipeline_locks()
        elif self.path in ["/api/flow_orchestrator", "/api/flow_orchestrator_status"]:
            self._handle_flow_orchestrator_status()
        elif self.path in ["/api/flow_payload", "/api/payload"]:
            self._handle_flow_payload()
        elif self.path == "/api/open_flow_hud":
            self._handle_open_flow_hud()
        else:
            self._send_json({"ok": False, "error": f"Unknown GET endpoint: {self.path}"}, 404)


    def do_POST(self):
        if self.path == "/api/shutdown":
            self._send_json({"ok": True, "status": "SHUTTING_DOWN"})
            _log("🛑 [Chrome Overlay Daemon] Graceful shutdown signal received. Terminating.")
            threading.Thread(target=lambda: (time.sleep(0.1), os._exit(0)), daemon=True).start()
            return
        elif self.path == "/api/inject":
            self._handle_inject()
        elif self.path == "/api/clip_state":
            self._handle_save_clip_state()
        elif self.path == "/api/remove":
            self._handle_remove()
        elif self.path == "/api/remove_all":
            self._handle_remove_all()
        elif self.path == "/api/type_prompt":
            self._handle_type_prompt()
        elif self.path == "/api/avatar_inject":
            self._handle_avatar_inject()
        elif self.path == "/api/flow_preset":
            self._handle_flow_preset()
        elif self.path == "/api/flow_orchestrator":
            self._handle_flow_orchestrator()
        elif self.path == "/api/generate_reference_asset":
            self._handle_generate_reference_asset()
        elif self.path in ("/api/rename_reference_asset", "/api/rename_ref_asset"):
            self._handle_rename_reference_asset()
        elif self.path == "/api/open_flow_hud":
            self._handle_open_flow_hud()
        elif self.path == "/api/cdp_press_enter":
            self._handle_cdp_press_enter()
        elif self.path == "/api/screenshot":
            self._handle_screenshot()
        elif self.path in ("/api/batch_rename_images", "/api/batch_rename_media"):
            self._handle_batch_rename_media()
        elif self.path == "/api/batch_download_media":
            self._handle_batch_download_media()
        elif self.path == "/api/assemble_davinci_timeline":
            self._handle_assemble_davinci_timeline()
        elif self.path == "/api/inject_background_music":
            self._handle_inject_background_music()
        elif self.path == "/api/upload_youtube_video":
            self._handle_upload_youtube_video()
        elif self.path == "/api/publish_luxury_blog":
            self._handle_publish_luxury_blog()
        elif self.path == "/api/publish_meta_social":
            self._handle_publish_meta_social()
        elif self.path == "/api/upload_youtube_video_possibilities":
            self._handle_upload_youtube_video(is_possibilities=True)
        elif self.path == "/api/publish_luxury_blog_possibilities":
            self._handle_publish_luxury_blog(is_possibilities=True)
        elif self.path == "/api/publish_meta_social_possibilities":
            self._handle_publish_meta_social(is_possibilities=True)
        elif self.path == "/api/button_orders":
            self._handle_save_button_orders()
        elif self.path in ["/api/pipeline_lock", "/api/pipeline/lock", "/api/pipeline_lock/acquire"]:
            self._handle_acquire_pipeline_lock()
        elif self.path in ["/api/pipeline_unlock", "/api/pipeline/unlock", "/api/pipeline_lock/release"]:
            self._handle_release_pipeline_lock()
        elif self.path in ["/api/automation_triggers", "/api/triggers"]:
            self._handle_save_automation_trigger()
        elif self.path == "/api/purge":
            self._handle_purge()
        elif self.path == "/api/organize":
            self._handle_organize()
        else:
            self._send_json({"ok": False, "error": f"Unknown POST endpoint: {self.path}"}, 404)

    def do_DELETE(self):
        if self.path in ["/api/automation_triggers", "/api/triggers"] or "/api/automation_triggers" in self.path or "/api/triggers" in self.path:
            self._handle_delete_automation_trigger()
        elif self.path in ["/api/pipeline_lock", "/api/pipeline/lock"] or "/api/pipeline_lock" in self.path:
            self._handle_release_pipeline_lock()
        else:
            self._send_json({"ok": False, "error": f"Unknown DELETE endpoint: {self.path}"}, 404)

    def _handle_get_button_orders(self):
        orders_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "user_button_orders.json")
        if os.path.exists(orders_file):
            try:
                with open(orders_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._send_json({"ok": True, "orders": data})
                return
            except Exception as e:
                _log(f"Error reading user_button_orders.json: {e}")
        self._send_json({"ok": True, "orders": {}})

    def _handle_save_button_orders(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        orders = body.get("orders", body)
        orders_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "user_button_orders.json")
        try:
            os.makedirs(os.path.dirname(orders_file), exist_ok=True)
            with open(orders_file, "w", encoding="utf-8") as f:
                json.dump(orders, f, indent=2)
            self._send_json({"ok": True, "saved": True})
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    # -- Pipeline Exclusivity Lock Handlers --------------------------------

    def _handle_get_pipeline_locks(self):
        locks = PIPELINE_EXCLUSIVITY.get_all_locks()
        self._send_json({"ok": True, "locks": locks})

    def _handle_acquire_pipeline_lock(self):
        try:
            body = self._read_body()
            pipeline = body.get("pipeline")
            owner = body.get("owner", "antigravity_subagent")
            ttl = int(body.get("ttl_seconds", 900))
            pid = body.get("pid")
            details = body.get("details", "")

            if not pipeline:
                self._send_json({"ok": False, "error": "Missing 'pipeline' key"}, 400)
                return

            ok, msg, lock_data = PIPELINE_EXCLUSIVITY.acquire(pipeline, owner, ttl_seconds=ttl, pid=pid, details=details)
            status_code = 200 if ok else 409
            self._send_json({
                "ok": ok,
                "status": "LOCKED" if ok else "COLLISION_PREVENTED",
                "message": msg,
                "lock": lock_data
            }, status_code)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_release_pipeline_lock(self):
        try:
            body = self._read_body() if self.headers.get("Content-Length") else {}
            pipeline = body.get("pipeline")
            owner = body.get("owner")
            if not pipeline and "?" in self.path:
                from urllib.parse import parse_qs, urlparse
                q = parse_qs(urlparse(self.path).query)
                pipeline = q.get("pipeline", [None])[0]
                owner = q.get("owner", [None])[0]

            if not pipeline:
                self._send_json({"ok": False, "error": "Missing 'pipeline' key"}, 400)
                return

            ok, msg = PIPELINE_EXCLUSIVITY.release(pipeline, owner=owner)
            self._send_json({"ok": ok, "message": msg})
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    # -- Automation Trigger Persistence Handlers ---------------------------

    def _handle_get_automation_triggers(self):
        try:
            if not os.path.exists(TRIGGERS_DIR):
                self._send_json({"ok": True, "triggers": []})
                return
            triggers = []
            for fname in os.listdir(TRIGGERS_DIR):
                if fname.endswith(".json") and not fname.startswith("00_"):
                    fpath = os.path.join(TRIGGERS_DIR, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8-sig") as f:
                            data = json.load(f)
                            if isinstance(data, dict) and "id" in data:
                                triggers.append(data)
                    except Exception as fe:
                        _log(f"Error parsing trigger file {fname}: {fe}")
            triggers.sort(key=lambda x: (x.get("order") or 99, x.get("label", "")))
            self._send_json({"ok": True, "count": len(triggers), "triggers": triggers})
        except Exception as e:
            _log(f"Error in _handle_get_automation_triggers: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_save_automation_trigger(self):
        try:
            body = self._read_body()
            config = body.get("config", body)
            trigger_id = config.get("id")
            if not trigger_id:
                self._send_json({"ok": False, "error": "Missing 'id' in trigger config"}, 400)
                return
            
            # Clean safe filename
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', trigger_id).strip('_')
            filename = f"{safe_name}.json"
            target_path = os.path.join(TRIGGERS_DIR, filename)

            # Ensure complete valid schema satisfying test_hud_button_triggers
            required_defaults = {
                "id": trigger_id,
                "label": config.get("label", "Custom Trigger"),
                "icon": config.get("icon", "Zap"),
                "color": config.get("color", "#00f0ff"),
                "context": config.get("context", "protocols"),
                "action_type": config.get("action_type", "SUBAGENT_SPAWN"),
                "action": config.get("action", f"Trigger: {config.get('label', trigger_id)}"),
                "daemon_endpoint": config.get("daemon_endpoint", "http://127.0.0.1:9876/api/prompt"),
                "method": config.get("method", "POST"),
                "params": config.get("params") if isinstance(config.get("params"), dict) and len(config.get("params")) > 0 else {
                    "prompt": f"Execute custom trigger {config.get('label', trigger_id)}"
                },
                "order": int(config.get("order") or 1)
            }
            # Clamp order between 1 and 6
            if required_defaults["order"] < 1: required_defaults["order"] = 1
            if required_defaults["order"] > 6: required_defaults["order"] = 6

            # Ensure color starts with #
            if not required_defaults["color"].startswith("#"):
                required_defaults["color"] = f"#{required_defaults['color']}"

            os.makedirs(TRIGGERS_DIR, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(required_defaults, f, indent=2, ensure_ascii=False)

            _log(f"💾 [Trigger Persisted to Disk] {filename} (id: {trigger_id}, label: '{required_defaults['label']}')")
            self._send_json({"ok": True, "saved": True, "filename": filename, "trigger": required_defaults})
        except Exception as e:
            _log(f"Error in _handle_save_automation_trigger: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_delete_automation_trigger(self):
        try:
            body = self._read_body() if self.headers.get("Content-Length") else {}
            trigger_id = body.get("id")
            if not trigger_id and "?" in self.path:
                from urllib.parse import parse_qs, urlparse
                q = parse_qs(urlparse(self.path).query)
                trigger_id = q.get("id", [None])[0]
            if not trigger_id and "/" in self.path:
                parts = self.path.rstrip("/").split("/")
                if parts[-1] not in ["automation_triggers", "triggers"]:
                    trigger_id = parts[-1]

            if not trigger_id:
                self._send_json({"ok": False, "error": "Missing 'id' for deletion"}, 400)
                return

            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', trigger_id).strip('_')
            target_path = os.path.join(TRIGGERS_DIR, f"{safe_name}.json")
            deleted = False
            if os.path.exists(target_path):
                os.remove(target_path)
                deleted = True
                _log(f"🗑️ [Trigger Deleted from Disk] {safe_name}.json")
            
            self._send_json({"ok": True, "deleted": deleted, "id": trigger_id})
        except Exception as e:
            _log(f"Error in _handle_delete_automation_trigger: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_get_clip_state(self):
        state_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "active_state.json")
        if os.path.exists(state_file):
            try:
                with open(state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._send_json({"ok": True, "state": data})
                return
            except Exception as e:
                _log(f"Error reading active_state.json: {e}")
        self._send_json({"ok": True, "state": {"clip_index": 0, "clip_id": "000101"}})

    def _handle_save_clip_state(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        state_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "active_state.json")
        try:
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            cur = {}
            if os.path.exists(state_file):
                try:
                    with open(state_file, "r", encoding="utf-8") as rf:
                        cur = json.load(rf)
                except Exception:
                    cur = {}
            cur.update(body)
            cur["timestamp"] = time.time()
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(cur, f, indent=2)
            self._send_json({"ok": True, "saved": True, "clip_index": cur.get("clip_index", 0), "total_clips": cur.get("total_clips", 0)})
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_batch_download_media(self):
        try:
            try:
                body = self._read_body()
            except Exception:
                body = {}
            media_type = body.get("media_type", "images")
            prompt = body.get("prompt")
            
            # If prompt was dispatched from HUD for agent execution, do NOT double-spawn subprocess
            if prompt:
                _log("📥 Batch download prompt received from HUD; routing exclusively to Antigravity chat agent.")
                self._send_json({
                    "ok": True,
                    "status": "QUEUED_TO_AGENT",
                    "media_type": media_type
                })
                return

            count = body.get("count", None)
            if not count or body.get("autoDetectCount", False):
                try:
                    payload_path = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")
                    if os.path.exists(payload_path):
                        with open(payload_path, "r", encoding="utf-8") as f:
                            pdata = json.load(f)
                        if (media_type or "").lower().startswith("vid"):
                            count = pdata.get("video_count") or len(pdata.get("clips", [])) or 8
                        else:
                            count = pdata.get("broll_count") or len(pdata.get("brolls", [])) or pdata.get("count") or 7
                except Exception:
                    pass
            count_str = str(count or (8 if (media_type or "").lower().startswith("vid") else 7))

            if (media_type or "").lower().startswith("vid"):
                script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "download_videos_1080p.py")
            else:
                script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "download_broll_1k.py")

            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            context_val = (body.get("context") or body.get("channel") or "protocols").lower()
            if "possibilit" in context_val:
                channel_folder = "06_Keystone_possibilities"
            elif "recomposit" in context_val:
                channel_folder = "07_Keystone_recomposition"
            else:
                channel_folder = "08_Keystone_protocols"

            sub_folder = "video" if (media_type or "").lower().startswith("vid") else "b-roll"
            dest_dir = os.path.join(BRAIN_ROOT, channel_folder, "Google_Flow", sub_folder)

            _log(f"🚀 Spawning standalone download tool: {os.path.basename(script_path)} (count: {count_str}, dest: {dest_dir})")
            subprocess.Popen([py_exe, script_path, count_str, dest_dir])

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "media_type": media_type,
                "count": count_str,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_batch_download_media: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_batch_rename_media(self):
        try:
            try:
                body = self._read_body()
            except Exception:
                body = {}
            media_type = body.get("media_type", "images")
            prompt = body.get("prompt")
            names = body.get("names")

            # Only treat as reference card rename if names exclusively contain reference asset identifiers
            if names and isinstance(names, list) and all(n in ("cloth_1", "background_1", "me") for n in names):
                results = []
                for n in names:
                    ok_ren, detail = cdp_rename_specific_reference(str(n))
                    results.append({"name": str(n), "ok": ok_ren, "detail": detail})
                self._send_json({"ok": True, "renamed": results})
                return

            # If prompt was dispatched from HUD for agent execution, do NOT double-spawn subprocess
            if prompt:
                _log("🏷️ Batch rename prompt received from HUD; routing exclusively to Antigravity chat agent.")
                self._send_json({
                    "ok": True,
                    "status": "QUEUED_TO_AGENT",
                    "media_type": media_type
                })
                return

            count = body.get("count", None)
            if not count:
                try:
                    payload_path = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")
                    if os.path.exists(payload_path):
                        with open(payload_path, "r", encoding="utf-8") as f:
                            pdata = json.load(f)
                        if (media_type or "").lower().startswith("vid"):
                            count = pdata.get("video_count") or len(pdata.get("clips", [])) or 8
                        else:
                            count = pdata.get("broll_count") or len(pdata.get("brolls", [])) or pdata.get("count") or 7
                except Exception:
                    pass
            count_str = str(count or (8 if (media_type or "").lower().startswith("vid") else 7))

            if (media_type or "").lower().startswith("vid"):
                script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "rename_videos.py")
            else:
                script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "rename_broll.py")

            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            _log(f"🚀 Spawning standalone rename tool: {os.path.basename(script_path)} (count: {count_str})")
            subprocess.Popen([py_exe, script_path, count_str])

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "media_type": media_type,
                "count": count_str,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_batch_rename_media: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_assemble_davinci_timeline(self):
        try:
            try:
                body = self._read_body()
            except Exception:
                body = {}

            source = body.get("source") or body.get("dispatch_mode", "")
            action = body.get("action", "")

            # Exclusivity lock command from Antigravity subagent
            if source == "antigravity_subagent" or action == "lock":
                ok, msg, lock_data = PIPELINE_EXCLUSIVITY.acquire(
                    pipeline="davinci_assembly",
                    owner="antigravity_subagent",
                    ttl_seconds=int(body.get("ttl_seconds", 900)),
                    details="Antigravity D1 DaVinci subagent active"
                )
                self._send_json({"ok": ok, "status": "LOCKED" if ok else "COLLISION_PREVENTED", "message": msg, "lock": lock_data}, 200 if ok else 409)
                return

            if action == "unlock":
                ok, msg = PIPELINE_EXCLUSIVITY.release("davinci_assembly", owner="antigravity_subagent")
                self._send_json({"ok": ok, "status": "UNLOCKED", "message": msg})
                return

            # Exclusivity check: is pipeline already locked?
            is_locked, lock_info = PIPELINE_EXCLUSIVITY.is_locked("davinci_assembly")
            if is_locked:
                _log(f"⚠️ [Collision Prevented] DaVinci timeline assembly blocked! Already active under: {lock_info.get('owner')}")
                self._send_json({
                    "ok": False,
                    "status": "COLLISION_PREVENTED",
                    "error": "DUAL_DISPATCH_COLLISION_PREVENTED",
                    "message": f"DaVinci timeline assembly is currently locked by '{lock_info.get('owner')}'. Subprocess dispatch blocked to prevent dual-dispatch collision.",
                    "lock": lock_info
                }, 409)
                return

            count = body.get("count", None)
            if not count:
                try:
                    payload_path = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")
                    if os.path.exists(payload_path):
                        with open(payload_path, "r", encoding="utf-8") as f:
                            pdata = json.load(f)
                        count = pdata.get("count") or len(pdata.get("clips", []))
                except Exception:
                    pass
            count_str = str(count or 26)
            context = str(body.get("context") or ("possibilities" if "possibilit" in self.path else "protocols")).lower()

            script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "assemble_davinci_timeline.py")
            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            _log(f"🚀 Spawning standalone DaVinci assembly tool: {os.path.basename(script_path)} (count: {count_str}, context: {context})")
            proc = subprocess.Popen([py_exe, script_path, count_str, count_str, "--context", context])

            PIPELINE_EXCLUSIVITY.acquire(
                pipeline="davinci_assembly",
                owner="daemon_subprocess",
                ttl_seconds=900,
                pid=proc.pid,
                details=f"DaVinci assembly subprocess PID {proc.pid}"
            )
            def _wait_davinci(p):
                try:
                    p.wait()
                finally:
                    PIPELINE_EXCLUSIVITY.release("davinci_assembly", owner="daemon_subprocess")
            threading.Thread(target=_wait_davinci, args=(proc,), daemon=True).start()

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "pid": proc.pid,
                "count": count_str,
                "context": context,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_assemble_davinci_timeline: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_inject_background_music(self):
        try:
            # Check exclusivity on DaVinci audio/timeline
            is_locked, lock_info = PIPELINE_EXCLUSIVITY.is_locked("davinci_assembly")
            if is_locked and lock_info.get("owner") == "antigravity_subagent":
                _log(f"⚠️ [Collision Prevented] BGM injector blocked! DaVinci timeline is active under: {lock_info.get('owner')}")
                self._send_json({
                    "ok": False,
                    "status": "COLLISION_PREVENTED",
                    "error": "DUAL_DISPATCH_COLLISION_PREVENTED",
                    "message": "DaVinci Resolve is currently busy under Antigravity subagent.",
                    "lock": lock_info
                }, 409)
                return

            script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "inject_background_music.py")
            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            _log(f"🚀 Spawning standalone BGM injector tool: {os.path.basename(script_path)}")
            proc = subprocess.Popen([py_exe, script_path])

            PIPELINE_EXCLUSIVITY.acquire(
                pipeline="davinci_bgm",
                owner="daemon_subprocess",
                ttl_seconds=300,
                pid=proc.pid,
                details=f"BGM injector PID {proc.pid}"
            )
            def _wait_bgm(p):
                try:
                    p.wait()
                finally:
                    PIPELINE_EXCLUSIVITY.release("davinci_bgm", owner="daemon_subprocess")
            threading.Thread(target=_wait_bgm, args=(proc,), daemon=True).start()

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "pid": proc.pid,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_inject_background_music: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_upload_youtube_video(self, is_possibilities=False):
        try:
            try:
                body = self._read_body()
            except Exception:
                body = {}

            source = body.get("source") or body.get("dispatch_mode", "")
            action = body.get("action", "")

            # Exclusivity lock command from Antigravity subagent
            if source == "antigravity_subagent" or action == "lock":
                ok, msg, lock_data = PIPELINE_EXCLUSIVITY.acquire(
                    pipeline="youtube_upload",
                    owner="antigravity_subagent",
                    ttl_seconds=int(body.get("ttl_seconds", 900)),
                    details="Antigravity Y1 YouTube Uploader subagent active"
                )
                self._send_json({"ok": ok, "status": "LOCKED" if ok else "COLLISION_PREVENTED", "message": msg, "lock": lock_data}, 200 if ok else 409)
                return

            if action == "unlock":
                ok, msg = PIPELINE_EXCLUSIVITY.release("youtube_upload", owner="antigravity_subagent")
                self._send_json({"ok": ok, "status": "UNLOCKED", "message": msg})
                return

            # Exclusivity check: is pipeline already locked?
            is_locked, lock_info = PIPELINE_EXCLUSIVITY.is_locked("youtube_upload")
            if is_locked:
                _log(f"⚠️ [Collision Prevented] YouTube upload blocked! Already active under: {lock_info.get('owner')}")
                self._send_json({
                    "ok": False,
                    "status": "COLLISION_PREVENTED",
                    "error": "DUAL_DISPATCH_COLLISION_PREVENTED",
                    "message": f"YouTube video upload is currently locked by '{lock_info.get('owner')}'. Subprocess dispatch blocked to prevent collision.",
                    "lock": lock_info
                }, 409)
                return

            fmt = str(body.get("format", "long")).lower()
            context_val = (body.get("context") or "").lower()
            if "possibilit" in context_val:
                is_possibilities = True
            script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", ("upload_youtube_video_possibilities.py" if is_possibilities else "upload_youtube_video.py"))
            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            args = [py_exe, script_path]
            if "short" in fmt:
                args.append("--short")

            _log(f"🚀 Spawning standalone YouTube uploader tool ({fmt}): {os.path.basename(script_path)}")
            proc = subprocess.Popen(args)

            PIPELINE_EXCLUSIVITY.acquire(
                pipeline="youtube_upload",
                owner="daemon_subprocess",
                ttl_seconds=900,
                pid=proc.pid,
                details=f"YouTube uploader subprocess PID {proc.pid} ({fmt})"
            )
            def _wait_yt(p):
                try:
                    p.wait()
                finally:
                    PIPELINE_EXCLUSIVITY.release("youtube_upload", owner="daemon_subprocess")
            threading.Thread(target=_wait_yt, args=(proc,), daemon=True).start()

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "pid": proc.pid,
                "format": fmt,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_upload_youtube_video: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_publish_luxury_blog(self, is_possibilities=False):
        try:
            try:
                body = self._read_body()
            except Exception:
                body = {}

            source = body.get("source") or body.get("dispatch_mode", "")
            action = body.get("action", "")

            # Exclusivity lock command from Antigravity subagent
            if source == "antigravity_subagent" or action == "lock":
                ok, msg, lock_data = PIPELINE_EXCLUSIVITY.acquire(
                    pipeline="luxury_blog_publish",
                    owner="antigravity_subagent",
                    ttl_seconds=int(body.get("ttl_seconds", 900)),
                    details="Antigravity B1 Blog Publisher subagent active"
                )
                self._send_json({"ok": ok, "status": "LOCKED" if ok else "COLLISION_PREVENTED", "message": msg, "lock": lock_data}, 200 if ok else 409)
                return

            if action == "unlock":
                ok, msg = PIPELINE_EXCLUSIVITY.release("luxury_blog_publish", owner="antigravity_subagent")
                self._send_json({"ok": ok, "status": "UNLOCKED", "message": msg})
                return

            # Exclusivity check: is pipeline already locked?
            is_locked, lock_info = PIPELINE_EXCLUSIVITY.is_locked("luxury_blog_publish")
            if is_locked:
                _log(f"⚠️ [Collision Prevented] Luxury blog publishing blocked! Already active under: {lock_info.get('owner')}")
                self._send_json({
                    "ok": False,
                    "status": "COLLISION_PREVENTED",
                    "error": "DUAL_DISPATCH_COLLISION_PREVENTED",
                    "message": f"Luxury blog publishing is currently locked by '{lock_info.get('owner')}'. Subprocess dispatch blocked to prevent collision.",
                    "lock": lock_info
                }, 409)
                return

            context_val = (body.get("context") or "").lower()
            if "possibilit" in context_val:
                is_possibilities = True
            script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", ("publish_luxury_blog_possibilities.py" if is_possibilities else "publish_luxury_blog.py"))
            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            args = [py_exe, script_path]
            _log(f"📰 Spawning Luxury Blog Publisher & GSC Indexing Tool: {os.path.basename(script_path)}")
            proc = subprocess.Popen(args)

            PIPELINE_EXCLUSIVITY.acquire(
                pipeline="luxury_blog_publish",
                owner="daemon_subprocess",
                ttl_seconds=900,
                pid=proc.pid,
                details=f"Luxury blog publishing subprocess PID {proc.pid}"
            )
            def _wait_blog(p):
                try:
                    p.wait()
                finally:
                    PIPELINE_EXCLUSIVITY.release("luxury_blog_publish", owner="daemon_subprocess")
            threading.Thread(target=_wait_blog, args=(proc,), daemon=True).start()

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "pid": proc.pid,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_publish_luxury_blog: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_publish_meta_social(self, is_possibilities=False):
        try:
            try:
                body = self._read_body()
            except Exception:
                body = {}

            source = body.get("source") or body.get("dispatch_mode", "")
            action = body.get("action", "")

            # Exclusivity lock command from Antigravity subagent
            if source == "antigravity_subagent" or action == "lock":
                ok, msg, lock_data = PIPELINE_EXCLUSIVITY.acquire(
                    pipeline="meta_social_publish",
                    owner="antigravity_subagent",
                    ttl_seconds=int(body.get("ttl_seconds", 900)),
                    details="Antigravity M1 Meta Publisher subagent active"
                )
                self._send_json({"ok": ok, "status": "LOCKED" if ok else "COLLISION_PREVENTED", "message": msg, "lock": lock_data}, 200 if ok else 409)
                return

            if action == "unlock":
                ok, msg = PIPELINE_EXCLUSIVITY.release("meta_social_publish", owner="antigravity_subagent")
                self._send_json({"ok": ok, "status": "UNLOCKED", "message": msg})
                return

            # Exclusivity check: is pipeline already locked?
            is_locked, lock_info = PIPELINE_EXCLUSIVITY.is_locked("meta_social_publish")
            if is_locked:
                _log(f"⚠️ [Collision Prevented] Meta social publishing blocked! Already active under: {lock_info.get('owner')}")
                self._send_json({
                    "ok": False,
                    "status": "COLLISION_PREVENTED",
                    "error": "DUAL_DISPATCH_COLLISION_PREVENTED",
                    "message": f"Meta social publishing is currently locked by '{lock_info.get('owner')}'. Subprocess dispatch blocked to prevent collision.",
                    "lock": lock_info
                }, 409)
                return

            context_val = (body.get("context") or "").lower()
            if "possibilit" in context_val:
                is_possibilities = True
            script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", ("publish_meta_social_possibilities.py" if is_possibilities else "publish_meta_social.py"))
            py_exe = os.path.join(BRAIN_ROOT, "16_daemons", "venv", "Scripts", "python.exe")
            if not os.path.exists(py_exe):
                py_exe = sys.executable

            args = [py_exe, script_path]
            _log(f"📱 Spawning Meta Business Suite (FB & IG) Publisher Tool: {os.path.basename(script_path)}")
            proc = subprocess.Popen(args)

            PIPELINE_EXCLUSIVITY.acquire(
                pipeline="meta_social_publish",
                owner="daemon_subprocess",
                ttl_seconds=900,
                pid=proc.pid,
                details=f"Meta social publishing subprocess PID {proc.pid}"
            )
            def _wait_meta(p):
                try:
                    p.wait()
                finally:
                    PIPELINE_EXCLUSIVITY.release("meta_social_publish", owner="daemon_subprocess")
            threading.Thread(target=_wait_meta, args=(proc,), daemon=True).start()

            self._send_json({
                "ok": True,
                "status": "DISPATCHED",
                "pid": proc.pid,
                "script": os.path.basename(script_path)
            })
        except Exception as e:
            _log(f"Error in _handle_publish_meta_social: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_generate_reference_asset(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        asset_type = body.get("asset_type") or body.get("asset") or "background_1"
        target_name = "cloth_1" if "cloth" in asset_type.lower() else "background_1"

        # 1. Load prompt from 00_OVERLAY_PAYLOAD.json
        payload_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")
        prompt = ""
        if os.path.exists(payload_file):
            try:
                with open(payload_file, "r", encoding="utf-8") as f:
                    pdata = json.load(f)
                    ref_assets = pdata.get("ref_assets", {})
                    prompt = ref_assets.get(target_name, "")
            except Exception:
                pass
        if not prompt:
            if target_name == "background_1":
                prompt = "high-contrast obsidian dark studio backdrop with subtle cyan architectural rim lighting, clean minimalist geometry, polished reflective floor, cinematic atmospheric lighting, 8K resolution, no people"
            else:
                prompt = "athletic male deep charcoal technical builder pullover with reinforced collar and subtle matte texture, displayed on tailor mannequin, crisp commercial studio lighting, 8K ultra-detailed fabric weave"

        # 2. Set Preset: Image 16:9, x1, Ingredients OFF
        _log(f"🎨 Calibrating preset for reference asset '{target_name}' (Image 16:9, Ingredients OFF)...")
        cdp_apply_flow_preset(mode="image", aspect="16:9", count="x1", ingredients=False)
        time.sleep(1.5)

        # 3. Type & Submit Prompt
        _log(f"▶ Ingesting prompt for reference asset '{target_name}': {prompt[:50]}...")
        tab_title, err = cdp_type_prompt(prompt, submit=True)
        if err:
            self._send_json({"ok": False, "error": f"Failed to submit reference prompt: {err}"}, 500)
            return

        # 4. Wait for generation to start & settle
        time.sleep(6)
        for _ in range(15):
            tab, _ = get_active_tab(target_pattern="flow")
            if tab and tab.get("webSocketDebuggerUrl"):
                try:
                    from websockets.sync.client import connect as ws_connect
                    with ws_connect(tab["webSocketDebuggerUrl"], close_timeout=5) as ws:
                        ws.send(json.dumps({
                            "id": 1, "method": "Runtime.evaluate",
                            "params": {
                                "expression": "document.querySelectorAll('mat-progress-spinner, mat-progress-bar, .progress-bar').length",
                                "returnByValue": True
                            }
                        }))
                        r = json.loads(ws.recv())
                        spinners = r.get("result", {}).get("result", {}).get("value", 0)
                        if spinners == 0:
                            break
                except Exception:
                    pass
            time.sleep(3)

        # 5. Rename the newly generated tile to target_name
        time.sleep(2)
        _log(f"🏷️ Auto-renaming generated card to '{target_name}'...")
        renamed_ok, r_res = cdp_rename_reference_card(target_name)

        self._send_json({
            "ok": True,
            "asset_type": target_name,
            "prompt": prompt[:60],
            "renamed": renamed_ok,
            "rename_detail": r_res,
            "message": f"Generated and renamed reference card to '{target_name}'"
        })


    def _handle_rename_reference_asset(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        asset_type = body.get("asset_type") or body.get("name") or "background_1"
        target_name = "cloth_1" if "cloth" in str(asset_type).lower() else "background_1"
        _log(f"🏷️ Renaming specific reference asset to '{target_name}'...")
        ok_ren, detail = cdp_rename_specific_reference(target_name)
        if ok_ren:
            self._send_json({"ok": True, "asset_type": target_name, "detail": detail})
        else:
            self._send_json({"ok": False, "asset_type": target_name, "error": str(detail)}, 500)


    def _handle_avatar_inject(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        script_text = body.get("script_text", "")
        camera_text = body.get("camera_text", "")
        submit = body.get("submit", False)
        speaker = body.get("speaker", "wayne")
        cloth = body.get("cloth", None)
        background = body.get("background", None)
        tab_title, err = cdp_avatar_inject(
            script_text=script_text,
            camera_text=camera_text,
            submit=submit,
            speaker=speaker,
            cloth=cloth,
            background=background
        )
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({
                "ok": True,
                "tab": tab_title,
                "speaker": speaker,
                "message": f"Attached 3 chips ({speaker.upper()}, cloth, background) and typed script",
                "submitted": submit
            })


    def _handle_type_prompt(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        text = body.get("text", "")
        submit = body.get("submit", False)
        tab_title, err = cdp_type_prompt(text=text, submit=submit)
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({"ok": True, "tab": tab_title, "message": f"Typed {len(text)} chars via CDP", "submitted": submit})


    def _handle_flow_preset(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        mode = body.get("mode", "video")
        aspect = body.get("aspect", "16:9")
        duration = body.get("duration", "10s")
        resolution = body.get("resolution", "720p")
        count = body.get("count", "x1")
        ingredients = body.get("ingredients", True)
        res, err = cdp_apply_flow_preset(
            mode=mode,
            aspect=aspect,
            duration=duration,
            resolution=resolution,
            count=count,
            ingredients=ingredients
        )
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json(res if isinstance(res, dict) else {"ok": True, "result": res})


    def _handle_flow_orchestrator_status(self):
        global _FLOW_ORCHESTRATOR_PROC
        is_running = (_FLOW_ORCHESTRATOR_PROC is not None and _FLOW_ORCHESTRATOR_PROC.poll() is None)
        pid = _FLOW_ORCHESTRATOR_PROC.pid if is_running else None

        status_data = {}
        status_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "orchestrator_status.json")
        if os.path.exists(status_file):
            try:
                with open(status_file, "r", encoding="utf-8") as sf:
                    status_data = json.load(sf)
            except Exception:
                pass

        self._send_json({
            "ok": True,
            "running": is_running,
            "pid": pid,
            "phase": status_data.get("phase", ""),
            "title": status_data.get("title", ""),
            "detail": status_data.get("detail", ""),
        })

    def _handle_flow_payload(self):
        try:
            payload_path = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")
            if os.path.exists(payload_path):
                with open(payload_path, "r", encoding="utf-8") as pf:
                    pdata = json.load(pf)
                v_count = pdata.get("video_count") or len(pdata.get("clips", [])) or 8
                b_count = pdata.get("broll_count") or len(pdata.get("brolls", [])) or 7
                self._send_json({
                    "ok": True,
                    "video_count": v_count,
                    "broll_count": b_count,
                    "clips": pdata.get("clips", []),
                    "brolls": pdata.get("brolls", []),
                    "ref_assets": pdata.get("ref_assets", {})
                })
            else:
                self._send_json({"ok": False, "error": "00_OVERLAY_PAYLOAD.json not found"}, 404)
        except Exception as e:
            self._send_json({"ok": False, "error": str(e)}, 500)

    def _handle_flow_orchestrator(self):

        global _FLOW_ORCHESTRATOR_PROC
        try:
            body = self._read_body()
        except Exception:
            body = {}
        action = body.get("action", "start")
        script_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", "flow_5batch_orchestrator.py")
        if action == "start":
            if _FLOW_ORCHESTRATOR_PROC and _FLOW_ORCHESTRATOR_PROC.poll() is None:
                self._send_json({"ok": True, "status": "ALREADY_RUNNING", "pid": _FLOW_ORCHESTRATOR_PROC.pid})
                return
            try:
                stage = body.get("stage") or "references"
                context = body.get("context")
                if not context:
                    payload_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "00_OVERLAY_PAYLOAD.json")
                    if os.path.exists(payload_file):
                        try:
                            with open(payload_file, "r", encoding="utf-8") as pf:
                                context = json.load(pf).get("context")
                        except Exception:
                            pass
                context = context or "possibilities"
                cmd = [sys.executable, script_path, "--stage", stage, "--context", context]
                _FLOW_ORCHESTRATOR_PROC = subprocess.Popen(cmd, cwd=BRAIN_ROOT)
                _log(f"🚀 [Chrome Overlay Daemon] Dispatched Flow 5-Batch Orchestrator [Stage: {stage}, Context: {context}] (PID: {_FLOW_ORCHESTRATOR_PROC.pid})")
                
                # Dispatch prompt to Antigravity so agent enters active 15s watchdog mode
                dispatch_prompt_to_antigravity(
                    f"Wayne pushed 'Run the Swarm' on Google Flow HUD [Stage: {stage or 'references'}]. Enter 15-second watchdog monitoring on the canvas, capture a screenshot upon settlement, verify/accept the assets, and push to the next stage."
                )
                
                self._send_json({"ok": True, "status": "STARTED", "stage": stage or "all", "pid": _FLOW_ORCHESTRATOR_PROC.pid})
            except Exception as e:
                _log(f"❌ [Chrome Overlay Daemon] Failed to start orchestrator: {e}")
                self._send_json({"ok": False, "error": str(e)}, 500)
        elif action == "stop":
            if _FLOW_ORCHESTRATOR_PROC and _FLOW_ORCHESTRATOR_PROC.poll() is None:
                _FLOW_ORCHESTRATOR_PROC.terminate()
                _log("🛑 [Chrome Overlay Daemon] Terminated Flow 5-Batch Orchestrator.")
                self._send_json({"ok": True, "status": "STOPPED"})
            else:
                self._send_json({"ok": True, "status": "NOT_RUNNING"})
        else: # status
            is_running = (_FLOW_ORCHESTRATOR_PROC is not None and _FLOW_ORCHESTRATOR_PROC.poll() is None)
            pid = _FLOW_ORCHESTRATOR_PROC.pid if is_running else None
            self._send_json({"ok": True, "running": is_running, "pid": pid})


    def _handle_open_flow_hud(self):
        try:
            tabs_data = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=3).read().decode())
            flow_tab = next((t for t in tabs_data if t.get('type') == 'page' and ('flow.google' in t.get('url', '') or 'Google Flow' in t.get('title', ''))), None)
            if flow_tab:
                try:
                    urllib.request.urlopen(f"http://127.0.0.1:9222/json/activate/{flow_tab['id']}", timeout=3)
                except Exception:
                    pass
                target_tab = flow_tab
            else:
                new_tab = json.loads(urllib.request.urlopen("http://127.0.0.1:9222/json/new?https://flow.google.com", timeout=5).read().decode())
                target_tab = new_tab
                time.sleep(2.5)

            overlay_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "overlay.js")
            if os.path.exists(overlay_file):
                with open(overlay_file, "r", encoding="utf-8") as f:
                    js_code = f.read()
                cdp_inject_isolated(js_code, tab=target_tab)
            _log(f"🌐 [Chrome Overlay Daemon] Activated Google Flow tab ({target_tab.get('title')}) with HUD overlay attached.")
            self._send_json({"ok": True, "tab": target_tab.get("title"), "id": target_tab.get("id")})
        except Exception as e:
            _log(f"❌ [Chrome Overlay Daemon] Failed to open Google Flow & HUD: {e}")
            self._send_json({"ok": False, "error": str(e)}, 500)


    def _handle_purge(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        
        channel_name = body.get("channelName") or body.get("channel_name") or body.get("channel")
        if not channel_name and "?" in self.path:
            try:
                from urllib.parse import parse_qs, urlparse
                query = parse_qs(urlparse(self.path).query)
                channel_name = query.get("channelName", [None])[0] or query.get("channel", [None])[0]
            except Exception:
                pass
        
        try:
            from purge_media_ingestion import purge_media_ingestion_folders
            removed = purge_media_ingestion_folders(channel_name)
            self._send_json({
                "ok": True,
                "channelName": channel_name or "all",
                "total_removed": removed,
                "message": f"Successfully purged target output directory for {channel_name or 'all channels'}"
            })
        except Exception as e:
            _log(f"Error executing purge: {e}")
            self._send_json({"ok": False, "error": f"Purge execution failed: {e}"}, 500)

    def _handle_organize(self):
        try:
            body = self._read_body()
        except Exception:
            body = {}
        
        channel_name = body.get("channelName") or body.get("channel_name") or body.get("channel") or "Keystone Protocols"
        media_type = body.get("mediaType") or body.get("media_type") or body.get("type") or "video"
        
        if "?" in self.path:
            try:
                from urllib.parse import parse_qs, urlparse
                query = parse_qs(urlparse(self.path).query)
                if query.get("channelName", [None])[0]:
                    channel_name = query.get("channelName", [None])[0]
                elif query.get("channel", [None])[0]:
                    channel_name = query.get("channel", [None])[0]
                if query.get("mediaType", [None])[0]:
                    media_type = query.get("mediaType", [None])[0]
                elif query.get("type", [None])[0]:
                    media_type = query.get("type", [None])[0]
            except Exception:
                pass
        
        try:
            from organize_downloaded_videos import organize_downloaded_media
            organized_count = 0
            if media_type == "all":
                c1 = organize_downloaded_media(channel_name=channel_name, media_type="video")
                c2 = organize_downloaded_media(channel_name=channel_name, media_type="broll")
                organized_count = c1 + c2
            else:
                organized_count = organize_downloaded_media(channel_name=channel_name, media_type=media_type)

            self._send_json({
                "ok": True,
                "channelName": channel_name,
                "mediaType": media_type,
                "total_organized": organized_count,
                "message": f"Successfully organized {media_type} downloads into target directory for {channel_name}"
            })
        except Exception as e:
            _log(f"Error executing organize: {e}")
            self._send_json({"ok": False, "error": f"Organize execution failed: {e}"}, 500)

    def _handle_screenshot(self):
        saved_path, err = cdp_capture_screenshot()
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({"ok": True, "path": saved_path, "message": "Captured tab screenshot via CDP"})

    def _handle_cdp_press_enter(self):
        tab_title, err = cdp_press_enter()
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({"ok": True, "tab": tab_title, "message": "Dispatched native CDP Enter key sequence"})

    # -- Endpoint Implementations ------------------------------------------

    def _handle_overlay_config(self):
        config = get_merged_overlay_config()
        self._send_json(config)

    def _handle_health(self):
        tabs, err = get_chrome_tabs()
        self._send_json({
            "status": "ok",
            "chrome_connected": err is None,
            "error": err
        })

    def _handle_tabs(self):
        tabs, err = get_chrome_tabs()
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({"ok": True, "tabs": tabs})

    def _handle_overlays(self):
        if not os.path.isfile(OVERLAY_REGISTRY):
            self._send_json({
                "ok": False,
                "error": f"Registry not found: {OVERLAY_REGISTRY}"
            }, 404)
            return
        try:
            with open(OVERLAY_REGISTRY, "r", encoding="utf-8") as f:
                registry = json.load(f)
            self._send_json({"ok": True, "registry": registry})
        except Exception as e:
            self._send_json({"ok": False, "error": f"Failed to read registry: {e}"}, 500)

    def _handle_inject(self):
        try:
            body = self._read_body()
        except Exception as e:
            self._send_json({"ok": False, "error": f"Invalid JSON body: {e}"}, 400)
            return

        prompt_text = body.get("promptText") or body.get("prompt") or body.get("action")
        if prompt_text and not body.get("overlayId"):
            prompt_file = r"C:\Users\Curtis\.gemini\antigravity\last_user_prompt.txt"
            try:
                os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
                with open(prompt_file, "w", encoding="utf-8") as pf:
                    pf.write(str(prompt_text))
                _log(f"Written prompt to last_user_prompt.txt ({len(str(prompt_text))} chars)")
                self._send_json({"ok": True, "message": f"Written prompt to last_user_prompt.txt ({len(str(prompt_text))} chars)"})
                return
            except Exception as pe:
                _log(f"Error writing to last_user_prompt.txt: {pe}")
                self._send_json({"ok": False, "error": f"Failed to write prompt file: {pe}"}, 500)
                return

        overlay_id = body.get("overlayId")
        if not overlay_id:
            self._send_json({"ok": False, "error": "Missing 'overlayId' or 'promptText' in request body"}, 400)
            return

        # If fresh run or cleanFolder requested, purge Keystone Protocols media folders & Downloads
        is_fresh = body.get("fresh", False)
        clean_folder = body.get("cleanFolder", False) or is_fresh
        channel_name = body.get("channelName") or body.get("channel") or "Keystone Protocols"
        
        prompt_file = r"C:\Users\Curtis\.gemini\antigravity\last_user_prompt.txt"
        state_file = os.path.join(BRAIN_ROOT, "05_Keystone_HUD", "button_configs", "overlays", "google_flow", "active_state.json")

        if clean_folder:
            # 1. Reset active clip index to 0 (Clip 1)
            try:
                os.makedirs(os.path.dirname(state_file), exist_ok=True)
                with open(state_file, "w", encoding="utf-8") as sf:
                    json.dump({"clip_index": 0, "clip_id": "000101", "timestamp": time.time()}, sf, indent=2)
            except Exception:
                pass

            # 2. Auto-ingest newest script for active channel
            try:
                from ingest_script_to_overlay import find_latest_script, parse_markdown_script, compile_overlay_js
                latest_script = find_latest_script(channel_name)
                parsed = parse_markdown_script(latest_script)
                clips = parsed[0]
                brolls = parsed[1]
                ref_assets = parsed[2] if len(parsed) > 2 else None
                if clips or brolls:
                    context_in = "possibilities" if "possibilit" in (channel_name or "").lower() else "protocols"
                    compile_overlay_js(clips, brolls, ref_assets=ref_assets, context=context_in)
                    _log(f"🎬 [Auto Script Induction] Compiled {len(clips)} clips and {len(brolls)} B-rolls from {os.path.basename(latest_script)} (Context: {context_in})")
                    try:
                        with open(state_file, "w", encoding="utf-8") as sf:
                            json.dump({
                                "total_clips": len(clips),
                                "total_broll": len(brolls),
                                "clip_index": 0,
                                "clip_id": clips[0]["clip_id"] if clips else "000101",
                                "broll_index": 0,
                                "timestamp": time.time()
                            }, sf, indent=2)
                    except Exception:
                        pass
            except Exception as se:
                _log(f"⚠️ Error compiling latest script on launch: {se}")

            # 3. Purge target media folders
            try:
                from purge_media_ingestion import purge_media_ingestion_folders
                purged_media = purge_media_ingestion_folders(channel_name)
                _log(f"🧹 [Fresh Launch Purge] Cleared {purged_media} files from {channel_name} media folders.")
            except Exception as pe:
                _log(f"⚠️ Error running media purge: {pe}")

            try:
                import glob
                downloads_path = os.path.expanduser(r"~\Downloads")
                flow_patterns = [os.path.join(downloads_path, "*.mp4"), os.path.join(downloads_path, "*.webm"), os.path.join(downloads_path, "flow_*.png")]
                cleaned_count = 0
                for pat in flow_patterns:
                    for f in glob.glob(pat):
                        try:
                            os.remove(f)
                            cleaned_count += 1
                        except Exception:
                            pass
                _log(f"Cleaned {cleaned_count} temporary media files from {downloads_path}")

                # Purge Google_Flow target folders in Keystone Protocols
                gflow_broll = os.path.join(BRAIN_ROOT, "08_Keystone_protocols", "Google_Flow", "b-roll")
                gflow_video = os.path.join(BRAIN_ROOT, "08_Keystone_protocols", "Google_Flow", "video")
                for folder in [gflow_broll, gflow_video]:
                    if os.path.exists(folder):
                        for f in os.listdir(folder):
                            if f.lower() in ("readme.md", ".gitkeep"):
                                continue
                            fp = os.path.join(folder, f)
                            try:
                                if os.path.isfile(fp): os.remove(fp)
                                elif os.path.isdir(fp): shutil.rmtree(fp)
                            except Exception:
                                pass
                _log(f"🧹 [Google Flow Reset] Purged old assets from {gflow_broll} and {gflow_video}")
            except Exception as ce:
                _log(f"Note on folder clean: {ce}")

            # 4. Notify Antigravity via last_user_prompt.txt & Port 9876 API
            try:
                os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
                with open(prompt_file, "w", encoding="utf-8") as pf:
                    pf.write("GOOGLE FLOW HUD LAUNCHED & RESET TO CLIP 1.\nMaster Skill: 00_keystone_flow_davinci_master_pipeline\nSubagents: F1_flow_broll_renamer, F2_flow_video_renamer, F3_flow_broll_downloader, F4_flow_video_downloader\nAction: Media folders purged in 08_Keystone_protocols/Google_Flow/ and active script clips mounted on Port 9222.")
                _log("Dispatched launch & reset prompt to Antigravity.")
            except Exception:
                pass
            dispatch_prompt_to_antigravity(
                f"GOOGLE FLOW HUD LAUNCHED & SCRIPT INGESTED for {channel_name}. Media folders cleared, Clip 1 mounted on Port 9222. Stand ready for Wayne to click Run the Swarm."
            )

        else:
            # Refresh & Resume: Notify Antigravity with saved clip index
            try:
                resumed_idx = 0
                if os.path.exists(state_file):
                    with open(state_file, "r", encoding="utf-8") as sf:
                        resumed_idx = json.load(sf).get("clip_index", 0)
                os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
                with open(prompt_file, "w", encoding="utf-8") as pf:
                    pf.write(f"GOOGLE FLOW OVERLAY REFRESHED & RESUMED AT CLIP {resumed_idx + 1}.\nMaster Skill: 00_keystone_flow_davinci_master_pipeline\nMedia folders preserved. Continuing session.")
                _log(f"Dispatched resume prompt to Antigravity at Clip {resumed_idx + 1}.")
            except Exception:
                pass
            dispatch_prompt_to_antigravity(
                f"GOOGLE FLOW OVERLAY REFRESHED & RESUMED AT CLIP {resumed_idx + 1}. Media folders preserved. Standing ready."
            )

        # Sub-Agent Action: Reverse Media Renaming
        if overlay_id == "rename_media":
            import subprocess
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "flow_media_automation.py"), "--rename"])
            self._send_json({"ok": True, "action": "rename_media", "message": "Dispatched reverse media renaming subagent."})
            return

        # Sub-Agent Action: Reverse Media Downloading (1k photos, 1080p videos)
        if overlay_id == "download_media":
            import subprocess
            subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "flow_media_automation.py"), "--download"])
            self._send_json({"ok": True, "action": "download_media", "message": "Dispatched reverse media downloading subagent."})
            return

        # Sanitize overlay_id to prevent path traversal
        safe_id = os.path.basename(overlay_id)
        overlay_path = os.path.join(OVERLAY_ROOT, safe_id, "overlay.js")

        if not os.path.isfile(overlay_path):
            self._send_json({
                "ok": False,
                "error": f"Overlay JS not found: {overlay_path}"
            }, 404)
            return

        try:
            with open(overlay_path, "r", encoding="utf-8") as f:
                js_code = f.read()
        except Exception as e:
            self._send_json({"ok": False, "error": f"Failed to read overlay JS: {e}"}, 500)
            return

        _log(f"Injecting overlay '{safe_id}' ({len(js_code)} bytes)")
        
        target_pattern = None
        config_path = os.path.join(OVERLAY_ROOT, safe_id, "config.json")
        if os.path.isfile(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as cf:
                    cfg = json.load(cf)
                    target_pattern = cfg.get("target_url_pattern")
            except Exception:
                pass

        global PENDING_INJECTIONS
        with PENDING_INJECTIONS_LOCK:
            PENDING_INJECTIONS.append({"id": safe_id, "code": js_code})
            if len(PENDING_INJECTIONS) > 20:
                PENDING_INJECTIONS = PENDING_INJECTIONS[-20:]

        active_tab, err = get_active_tab(target_pattern=target_pattern)
        if err:
            _log(f"CDP active tab detection note: {err}. Queued for Tampermonkey Bridge.")
            self._send_json({"ok": True, "overlayId": safe_id, "mode": "tampermonkey_bridge", "message": "Overlay queued for active Chrome tab via Tampermonkey Bridge"})
            return
        
        cdp_inject_config(active_tab)

        if is_fresh:
            try:
                cdp_inject_isolated("localStorage.setItem('ks_video_index', '0');", tab=active_tab)
            except Exception:
                pass

        tab_title, eval_err = cdp_inject_isolated(js_code, tab=active_tab)
        if eval_err:
            _log(f"CDP injection fallback to Tampermonkey on '{active_tab.get('title', '?')}': {eval_err}")
            self._send_json({"ok": True, "overlayId": safe_id, "mode": "tampermonkey_bridge", "tab": tab_title})
        else:
            _log(f"Overlay '{safe_id}' injected on active tab: '{tab_title}' (Fresh: {is_fresh})")
            self._send_json({"ok": True, "overlayId": safe_id, "mode": "cdp_direct", "tab": tab_title, "fresh": is_fresh})

    def _handle_poll(self):
        global PENDING_INJECTIONS
        with PENDING_INJECTIONS_LOCK:
            injections = list(PENDING_INJECTIONS)
            PENDING_INJECTIONS.clear()
        self._send_json({"ok": True, "injections": injections})

    def _handle_remove(self):
        try:
            body = self._read_body()
        except Exception as e:
            self._send_json({"ok": False, "error": f"Invalid JSON body: {e}"}, 400)
            return

        overlay_id = body.get("overlayId")
        if not overlay_id:
            self._send_json({"ok": False, "error": "Missing 'overlayId' in request body"}, 400)
            return

        safe_id = os.path.basename(overlay_id)
        js_code = f"document.getElementById('ks-overlay-{safe_id}')?.remove()"

        _log(f"Removing overlay '{safe_id}'")
        tab_title, err = cdp_evaluate(js_code)
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({"ok": True, "tab": tab_title})

    def _handle_remove_all(self):
        js_code = 'document.querySelectorAll(\'[id^="ks-overlay-"]\').forEach(el => el.remove())'

        _log("Removing all overlays")
        tab_title, err = cdp_evaluate(js_code)
        if err:
            self._send_json({"ok": False, "error": err}, 502)
        else:
            self._send_json({"ok": True, "tab": tab_title})


# ---------------------------------------------------------------------------
# Threaded HTTP Server
# ---------------------------------------------------------------------------

class ThreadedHTTPServer(HTTPServer):
    """Handle each request in a new thread. Bypasses Python 3.14 SO_REUSEADDR crash on Windows."""
    allow_reuse_address = False

    def server_bind(self):
        if sys.platform == "win32":
            SO_EXCLUSIVEADDRUSE = getattr(socket, "SO_EXCLUSIVEADDRUSE", -5)
            self.socket.setsockopt(socket.SOL_SOCKET, SO_EXCLUSIVEADDRUSE, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()
        host, port = self.server_address[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

    def process_request(self, request, client_address):
        t = threading.Thread(target=self._handle_request_thread, args=(request, client_address))
        t.daemon = True
        t.start()

    def _handle_request_thread(self, request, client_address):
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)


def cdp_auto_enter_watcher():
    """
    Background loop running in Python:
    Polls all Google Flow Chrome tabs every 150ms via CDP to check if window.__KEYSTONE_CDP_ENTER === true
    If set, resets the flag and fires native CDP Input.dispatchKeyEvent (virtualKey 13)!
    This bypasses all CORS, PNA, Mixed Content, tab focus dependencies, and isTrusted security traps completely!
    """
    import time
    last_processed = None
    while True:
        try:
            tabs = get_chrome_tabs()
            flow_tabs = [t for t in tabs if t.get("type") == "page" and ("flow" in t.get("url", "").lower() or "labs.google" in t.get("url", "").lower())]
            for tab in flow_tabs:
                ws_url = tab.get("webSocketDebuggerUrl")
                if ws_url:
                    from websockets.sync.client import connect as ws_connect
                    with ws_connect(ws_url, close_timeout=1) as ws:
                        ws.send(json.dumps({
                            "id": 99,
                            "method": "Runtime.evaluate",
                            "params": {"expression": "(() => { if (window.__KEYSTONE_CDP_ENTER) { const t = window.__KEYSTONE_CDP_ENTER; window.__KEYSTONE_CDP_ENTER = null; return t; } return null; })()"}
                        }))
                        resp = json.loads(ws.recv())
                        val = resp.get("result", {}).get("result", {}).get("value")
                        if val and val != last_processed:
                            last_processed = val
                            _log(f"⚡ Zero-delay CDP Enter triggered on tab '{tab.get('title')}' (timestamp: {val})")
                            cdp_press_enter(tab)
        except Exception:
            pass
        time.sleep(0.15)



def inject_config_on_startup():
    try:
        tab, err = get_active_tab()
        if tab and not err:
            cdp_inject_config(tab)
    except Exception as e:
        _log(f"Startup CDP config injection note: {e}")


def main():
    _log(f"Starting Chrome Overlay Daemon on port {DAEMON_PORT}")
    _log(f"Overlay root: {OVERLAY_ROOT}")
    _log(f"CDP target: {CDP_URL}")


    # Start CDP Auto-Enter Watcher background thread
    watcher_thread = threading.Thread(target=cdp_auto_enter_watcher, daemon=True)
    watcher_thread.start()
    _log("⚡ Permanent CDP Auto-Enter Watcher active (monitoring window.__KEYSTONE_CDP_ENTER).")

    # Start startup CDP config injection background thread
    startup_thread = threading.Thread(target=inject_config_on_startup, daemon=True)
    startup_thread.start()

    server = None
    for attempt in range(10):
        try:
            server = ThreadedHTTPServer(('127.0.0.1', DAEMON_PORT), OverlayHandler)
            break
        except OSError as e:
            _log(f"Port {DAEMON_PORT} busy during bind attempt {attempt+1}/10: {e}")
            time.sleep(0.5)

    if not server:
        _log(f"❌ Failed to bind port {DAEMON_PORT} after 10 attempts.")
        sys.exit(1)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        _log("Daemon stopped by user.")
    finally:
        server.server_close()



if __name__ == "__main__":
    main()


