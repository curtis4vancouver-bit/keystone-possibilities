"""
Keystone Voice Bridge — Raw WebSocket Gemini Live API
=====================================================
Built from the official Google Gemini Cookbook pattern:
  wss://generativelanguage.googleapis.com/ws/...BidiGenerateContent

Modes:
  1. Push-to-Talk: Hold F9 to stream. Release to stop.
  2. Outbox: Reads text from voice_outbox.txt and plays voice response.

Features:
  - System Persona: Orus, voice of the Master Brain
  - Tool Calling: search_master_brain, route_task, talk_to_antigravity, stop_antigravity
  - Persistent WebSocket — stays connected between PTT presses
  - Raw PCM audio over WebSocket (no SDK bugs)
  - Global F9 hotkey support using pynput (works in background CREATE_NO_WINDOW)
  - Auto-discovery of local language server address and CSRF token
  - Dynamic chat hot-swapping
"""

import asyncio
import os
import sys
import json
import time
import queue
import base64
import threading
import traceback
import re
import numpy as np
import sounddevice as sd
import psutil
from pynput import keyboard as pynput_kb
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosed

# Import Master Brain Tools
sys.path.append(r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\Qdrant_Brain')
sys.path.append(r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts')

# ──────────────────────────────────────────────────────────
# Tool Functions
# ──────────────────────────────────────────────────────────
def search_master_brain(query: str, namespace: str = "auto") -> str:
    try:
        from qdrant_hybrid_search import hybrid_search
        results = hybrid_search(query, namespace=namespace, top_k=5)
        if not results:
            return "No results found in the brain."
        summaries = []
        for r in results[:3]:
            text = r.get("text", r.get("content", ""))[:500]
            score = r.get("score", 0)
            summaries.append(f"[score={score:.2f}] {text}")
        return "\n---\n".join(summaries)
    except Exception as e:
        return f"Brain search error: {e}"

def route_task(task_description: str) -> str:
    try:
        inbox_path = os.path.join(
            r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain',
            'Agent_Fleet', 'chronos_master', 'INBOX.json'
        )
        os.makedirs(os.path.dirname(inbox_path), exist_ok=True)
        import datetime
        entry = {
            "task": task_description,
            "source": "voice_bridge",
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "pending"
        }
        existing = []
        if os.path.exists(inbox_path):
            try:
                with open(inbox_path, 'r') as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.append(entry)
        with open(inbox_path, 'w') as f:
            json.dump(existing, f, indent=2)
        return f"Task routed to Chronos Master: {task_description[:100]}"
    except Exception as e:
        return f"Route task error: {e}"

# ──────────────────────────────────────────────────────────
# Voice Bridge Config & Auto-Discovery
# ──────────────────────────────────────────────────────────
VOICE_BRIDGE_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
)
VOICE_OUTBOX_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_outbox.txt"
)
VOICE_STATUS_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_status.json"
)

def get_latest_conversation_id():
    """Gets the targeted conversation ID from config, falling back to newest brain folder."""
    try:
        if os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
            with open(VOICE_BRIDGE_CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                target_id = cfg.get("conversation_id")
                if target_id:
                    return target_id
    except Exception:
        pass

    # Fallback to scanning brain directory
    brain_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")
    try:
        dirs = [os.path.join(brain_dir, d) for d in os.listdir(brain_dir) if os.path.isdir(os.path.join(brain_dir, d))]
        dirs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        for d in dirs:
            basename = os.path.basename(d)
            if len(basename) == 36 and "-" in basename:
                return basename
    except Exception:
        pass
    return None

def auto_discover_agent_config():
    """Dynamically discover LS_ADDRESS and CSRF_TOKEN from the running language_server.exe process."""
    try:
        ls_proc = None
        for p in psutil.process_iter(['name', 'pid', 'cmdline']):
            try:
                if p.info['name'] and p.info['name'].lower() == 'language_server.exe':
                    ls_proc = p
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if ls_proc:
            pid = ls_proc.info['pid']
            cmdline = ls_proc.info['cmdline'] or []
            
            # Extract --csrf_token from cmdline args
            csrf = None
            for i, arg in enumerate(cmdline):
                if arg == '--csrf_token' and i + 1 < len(cmdline):
                    csrf = cmdline[i + 1]
                    break
            
            # Extract HTTP port from language_server.log
            log_path = os.path.join(
                os.environ.get("APPDATA", ""),
                "Antigravity", "logs", "language_server.log"
            )
            port = None
            if csrf and os.path.exists(log_path):
                port_pattern = re.compile(r"Language server listening on random port at (\d+) for HTTP")
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    # Search backwards, prefer lines matching our PID
                    for line in reversed(lines):
                        if str(pid) in line:
                            match = port_pattern.search(line)
                            if match:
                                port = match.group(1)
                                break
                    # Fallback: latest port line regardless of PID
                    if not port:
                        for line in reversed(lines):
                            match = port_pattern.search(line)
                            if match:
                                port = match.group(1)
                                break
                except Exception:
                    pass
            
            if csrf and port:
                ls_addr = f"localhost:{port}"
                
                # Write back to config so other components stay in sync
                try:
                    cfg = {}
                    if os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
                        with open(VOICE_BRIDGE_CONFIG_PATH, 'r') as f:
                            cfg = json.load(f)
                    cfg["ls_address"] = ls_addr
                    cfg["csrf_token"] = csrf
                    with open(VOICE_BRIDGE_CONFIG_PATH, 'w') as f:
                        json.dump(cfg, f, indent=2)
                except Exception:
                    pass
                    
                return ls_addr, csrf
    except Exception as e:
        print(f"  [Discovery] Process scan failed: {e}")
    
    # Fallback to reading config file
    try:
        if os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
            with open(VOICE_BRIDGE_CONFIG_PATH, 'r') as f:
                cfg = json.load(f)
            ls_addr = cfg.get("ls_address")
            csrf = cfg.get("csrf_token")
            if ls_addr and csrf:
                return ls_addr, csrf
    except Exception:
        pass
    return None, None

AGENTAPI_ENV = {
    "ANTIGRAVITY_AGENT": "1",
    "ANTIGRAVITY_LS_ADDRESS": "localhost:51790",
    "ANTIGRAVITY_CSRF_TOKEN": "",
    "ANTIGRAVITY_PROJECT_ID": "",
}
AGENTAPI_EXE = os.path.join(
    os.path.expanduser("~"), "AppData", "Local", "Programs",
    "Antigravity", "resources", "bin", "language_server.exe"
)
AGENTAPI_CONVERSATION = ""
_last_auto_check = 0.0

def check_and_reload_config():
    global AGENTAPI_ENV, AGENTAPI_CONVERSATION, _last_auto_check
    changed = False
    
    # 1. Always check conversation target
    latest_id = get_latest_conversation_id()
    if latest_id and latest_id != AGENTAPI_CONVERSATION:
        AGENTAPI_CONVERSATION = latest_id
        changed = True
        
    # 2. Periodically check language server connection details
    now = time.time()
    if now - _last_auto_check > 3.0:
        _last_auto_check = now
        ls_addr, csrf = auto_discover_agent_config()
        if ls_addr and csrf:
            if AGENTAPI_ENV.get("ANTIGRAVITY_LS_ADDRESS") != ls_addr or AGENTAPI_ENV.get("ANTIGRAVITY_CSRF_TOKEN") != csrf:
                AGENTAPI_ENV["ANTIGRAVITY_LS_ADDRESS"] = ls_addr
                AGENTAPI_ENV["ANTIGRAVITY_CSRF_TOKEN"] = csrf
                changed = True

    if changed:
        print(f"\n[Config] Active Target: {AGENTAPI_CONVERSATION[:12]}... on {AGENTAPI_ENV.get('ANTIGRAVITY_LS_ADDRESS')}")
        return True
    return False

def _agentapi_send(content: str) -> tuple:
    import subprocess
    env = {**os.environ, **AGENTAPI_ENV}
    try:
        result = subprocess.run(
            [AGENTAPI_EXE, "agentapi", "send-message", AGENTAPI_CONVERSATION, content],
            capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW,
            env=env
        )
        if result.returncode == 0:
            return True, result.stdout
        else:
            print(f"  [agentapi error] exit={result.returncode} stderr={result.stderr[:200]}")
            return False, result.stderr
    except Exception as e:
        print(f"  [agentapi exception] {e}")
        return False, str(e)

def talk_to_antigravity(message: str) -> str:
    global AGENTAPI_CONVERSATION
    latest_id = get_latest_conversation_id()
    if latest_id and latest_id != AGENTAPI_CONVERSATION:
        print(f"\n[*] Hot-swapping to newest conversation: {latest_id[:12]}...")
        AGENTAPI_CONVERSATION = latest_id

    success, output = _agentapi_send(f"[VOICE COMMAND from Wayne]: {message}")
    if success:
        return "Sent."
    else:
        # Fallback to file relay
        inbox_path = os.path.join(
            os.path.expanduser("~"),
            ".gemini", "antigravity", "brain",
            AGENTAPI_CONVERSATION,
            "scratch", "voice_inbox.txt"
        )
        os.makedirs(os.path.dirname(inbox_path), exist_ok=True)
        with open(inbox_path, "a", encoding="utf-8") as f:
            f.write(f"[VOICE COMMAND]: {message}\n")
        return "Failed to send directly, used fallback file relay."

def stop_antigravity(reason: str = "Wayne said stop") -> str:
    success, output = _agentapi_send(f"[PRIORITY STOP from Wayne]: {reason} - STOP immediately.")
    return "Stopped." if success else "Failed."

TOOL_FUNCTIONS = {
    "search_master_brain": search_master_brain,
    "route_task": route_task,
    "talk_to_antigravity": talk_to_antigravity,
    "stop_antigravity": stop_antigravity,
}

SYSTEM_INSTRUCTION_PTT = """
You are a voice-to-text routing bridge for the Antigravity coding agent.
Your ONLY job is to transcribe the user's voice input and send it to the agent on the screen using the `talk_to_antigravity(message)` tool.

RULES:
1. You MUST call the `talk_to_antigravity(message)` tool for ANY voice input, request, or comment from the user. Use the user's exact words as the message.
2. If the user says stop, halt, cancel, or tells you/the agent to stop, call the `stop_antigravity(reason)` tool immediately.
3. Never respond with conversational text. Do not explain, do not say hello, do not say "I don't know". You must only execute a tool call.
"""

SYSTEM_INSTRUCTION_OUTBOX = """
You are a pure Text-to-Speech engine. You MUST repeat the EXACT text provided to you, word for word, with natural articulation. Do NOT converse, do NOT answer questions, and do NOT add any of your own thoughts. Simply read the text verbatim out loud.
"""

# ──────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────
SAMPLE_RATE = 16000
OUTPUT_RATE = 24000
CHANNELS = 1
BLOCK_SIZE = 1024

def get_device_index(keywords, is_input=True):
    try:
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            channels = dev['max_input_channels'] if is_input else dev['max_output_channels']
            if channels > 0 and any(kw.lower() in dev['name'].lower() for kw in keywords):
                return idx
    except Exception:
        pass
    return None

INPUT_DEVICE = get_device_index(["Logitech", "PRO X"], is_input=True)
OUTPUT_DEVICE = get_device_index(["EP-HDMI-RX"], is_input=False)

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
except ImportError:
    pass

API_KEY = os.environ.get("GEMINI_API_KEY", "")
WS_HOST = "generativelanguage.googleapis.com"
WS_MODEL = "gemini-3.1-flash-live-preview"
WS_URI = f"wss://{WS_HOST}/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={API_KEY}"

# ──────────────────────────────────────────────────────────
# State Machine
# ──────────────────────────────────────────────────────────
STATE_SLEEPING = "SLEEPING"
STATE_LISTENING = "LISTENING"
STATE_DISCONNECTING = "DISCONNECTING"

class BridgeState:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = STATE_SLEEPING
        self.trigger = None
        self.f9_held = False
        self.last_voice_ts = 0.0
        self.speech_ended = False
        self.speech_ended_time = None
        self.outbox_sent_time = None
        self.should_quit = False
        
        self.gemini_queue = queue.Queue()
        self.outbox_queue = queue.Queue()
        self.audio_out_queue = queue.Queue()
        self.last_playback_ts = 0.0
        self.wake_event = threading.Event()

    def activate(self, trigger: str):
        with self.lock:
            if self.state == STATE_SLEEPING:
                self.state = STATE_LISTENING
                self.trigger = trigger
                self.last_voice_ts = time.time()
                self.speech_ended = False
                self.speech_ended_time = None
                self.wake_event.set()
                return True
            return False

    def deactivate(self):
        with self.lock:
            if self.state == STATE_LISTENING:
                self.state = STATE_DISCONNECTING
                self.trigger = None
                self.speech_ended = False
                self.speech_ended_time = None
                self.outbox_sent_time = None
                self.wake_event.set()
                # Flush queues
                while not self.gemini_queue.empty():
                    try:
                        self.gemini_queue.get_nowait()
                    except queue.Empty:
                        break

    def reset_to_sleeping(self):
        with self.lock:
            self.state = STATE_SLEEPING
            self.wake_event.clear()

    @property
    def is_listening(self):
        with self.lock:
            return self.state == STATE_LISTENING

bridge = BridgeState()

# ──────────────────────────────────────────────────────────
# Global Keyboard Listener (pynput)
# ──────────────────────────────────────────────────────────
def on_key_press(key):
    is_f9 = False
    if key == pynput_kb.Key.f9:
        is_f9 = True
    elif hasattr(key, 'vk') and key.vk == 120:
        is_f9 = True

    if is_f9:
        if not bridge.f9_held:
            bridge.f9_held = True
            # Clear output audio queue to interrupt playback immediately
            while not bridge.audio_out_queue.empty():
                try:
                    bridge.audio_out_queue.get_nowait()
                except queue.Empty:
                    break
            if bridge.activate("ptt"):
                print("\n[MIC] [F9 HELD] Listening... (release to stop)")

def on_key_release(key):
    is_f9 = False
    if key == pynput_kb.Key.f9:
        is_f9 = True
    elif hasattr(key, 'vk') and key.vk == 120:
        is_f9 = True

    if is_f9:
        bridge.f9_held = False
        if bridge.is_listening and bridge.trigger == "ptt":
            print("\n[MIC] [F9 RELEASE] Processing...")
            with bridge.lock:
                bridge.speech_ended = True
                bridge.speech_ended_time = time.time()

# ──────────────────────────────────────────────────────────
# Audio Callback
# ──────────────────────────────────────────────────────────
def audio_callback(indata, frames, time_info, status):
    if bridge.is_listening and bridge.trigger == "ptt":
        audio_bytes = indata.copy().tobytes()
        bridge.gemini_queue.put(audio_bytes)
        rms = np.sqrt(np.mean(indata.astype(np.float32) ** 2))
        if rms > 200:
            bridge.last_voice_ts = time.time()

# ──────────────────────────────────────────────────────────
# WebSocket Loop
# ──────────────────────────────────────────────────────────
async def gemini_session_loop():
    if not API_KEY or API_KEY == "your_google_ai_studio_api_key_here":
        print("\n[!] GEMINI_API_KEY not set. Edit .env in 00_Master_Brain/")
        return

    # Start playback device
    out_stream = sd.OutputStream(
        device=OUTPUT_DEVICE,
        samplerate=OUTPUT_RATE,
        channels=CHANNELS,
        dtype='int16',
        blocksize=1024
    )
    out_stream.start()

    # Audio playback worker thread
    def audio_playback_worker():
        while not bridge.should_quit:
            try:
                audio_chunk = bridge.audio_out_queue.get(timeout=0.1)
                if audio_chunk is not None:
                    out_stream.write(audio_chunk)
                    bridge.last_playback_ts = time.time()
            except queue.Empty:
                pass
            except Exception as e:
                print(f"[Audio Playback Error] {e}")

    playback_thread = threading.Thread(target=audio_playback_worker, daemon=True)
    playback_thread.start()

    # Outbox monitor worker thread
    def outbox_monitor_worker():
        os.makedirs(os.path.dirname(VOICE_OUTBOX_PATH), exist_ok=True)
        if not os.path.exists(VOICE_OUTBOX_PATH):
            with open(VOICE_OUTBOX_PATH, 'w') as f:
                pass
        
        last_mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
        last_text = ""
        try:
            with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8') as f:
                last_text = f.read().strip()
        except Exception:
            pass

        # Speak recent startup messages if written within 15s
        try:
            mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
            if time.time() - mtime < 15.0:
                with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    last_text = content
                    bridge.outbox_queue.put(content)
                    if bridge.activate("outbox"):
                        print(f"\n[*] Recent startup outbox message queued: {content[:60]}...")
        except Exception:
            pass

        while not bridge.should_quit:
            time.sleep(0.5)
            if not os.path.exists(VOICE_OUTBOX_PATH):
                continue
            try:
                current_mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
                if current_mtime <= last_mtime:
                    continue
                
                with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                last_mtime = current_mtime
                if not content or content == last_text:
                    continue
                
                last_text = content
                print(f"\n[*] New outbox message detected: {content[:60]}...")
                
                bridge.outbox_queue.put(content)
                
                while True:
                    with bridge.lock:
                        current_state = bridge.state
                    if current_state == STATE_DISCONNECTING:
                        time.sleep(0.1)
                        continue
                    break
                
                if bridge.activate("outbox"):
                    print(f"[*] Outbox message triggered wake up!")
                
            except Exception as e:
                print(f"[OUTBOX MONITOR ERROR] {e}")

    outbox_thread = threading.Thread(target=outbox_monitor_worker, daemon=True)
    outbox_thread.start()

    print("\n" + "=" * 55)
    print("  KEYSTONE VOICE BRIDGE — ACTIVE")
    print("=" * 55)
    print("  Hold F9 to talk (Push-to-Talk) — saves API cost!")
    print("  Press Ctrl+C to exit")
    print("=" * 55 + "\n")

    while not bridge.should_quit:
        bridge.wake_event.wait(timeout=1.0)
        if not bridge.is_listening:
            check_and_reload_config()
            continue

        print("[*] Connecting to Google Gemini Live API...")
        try:
            async with connect(WS_URI, additional_headers={}) as ws:
                # ── Setup Message ──
                if bridge.trigger == "ptt":
                    response_modalities = ["AUDIO"]
                    sys_instruction = SYSTEM_INSTRUCTION_PTT
                    tools = [{
                        "functionDeclarations": [
                            {
                                "name": "talk_to_antigravity",
                                "description": "Send a direct message or instruction to the active coding AI agent (Antigravity) on the computer screen.",
                                "parameters": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "message": {"type": "STRING", "description": "The instruction to send to the Antigravity AI agent."}
                                    },
                                    "required": ["message"]
                                }
                            },
                            {
                                "name": "stop_antigravity",
                                "description": "Urgently stop the Antigravity coding agent from whatever it is currently doing. Use when Wayne says stop, halt, cancel.",
                                "parameters": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "reason": {"type": "STRING", "description": "Why Wayne wants to stop. E.g. 'Wayne does not like the current approach'"}
                                    },
                                    "required": ["reason"]
                                }
                            }
                        ]
                    }]
                else:
                    response_modalities = ["AUDIO"]
                    sys_instruction = SYSTEM_INSTRUCTION_OUTBOX
                    tools = []

                setup_msg = {
                    "setup": {
                        "model": f"models/{WS_MODEL}",
                        "generationConfig": {
                            "responseModalities": response_modalities,
                            "speechConfig": {
                                "voiceConfig": {
                                    "prebuiltVoiceConfig": {
                                        "voiceName": "Orus"
                                    }
                                }
                            }
                        },
                        "realtimeInputConfig": {
                            "automaticActivityDetection": {
                                "disabled": True
                            }
                        },
                        "systemInstruction": {
                            "parts": [{"text": sys_instruction}]
                        }
                    }
                }
                if tools:
                    setup_msg["setup"]["tools"] = tools
                
                await ws.send(json.dumps(setup_msg))
                
                # Wait for setup complete
                raw_setup = await ws.recv(decode=False)
                setup_response = json.loads(raw_setup.decode("utf-8"))
                print("[+] Live Connection Established. Ready.\n")

                # ── Send Audio Task ──
                async def send_audio():
                    was_listening = False
                    while not bridge.should_quit and bridge.is_listening:
                        if bridge.trigger != "ptt":
                            await asyncio.sleep(0.05)
                            continue
                        
                        if not was_listening and not bridge.speech_ended:
                            was_listening = True
                            try:
                                await ws.send(json.dumps({"realtimeInput": {"activityStart": {}}}))
                            except Exception as e:
                                print(f"[!] Error sending activityStart: {e}")
                        
                        if bridge.speech_ended:
                            if was_listening:
                                was_listening = False
                                try:
                                    await ws.send(json.dumps({"realtimeInput": {"audioStreamEnd": True}}))
                                    await ws.send(json.dumps({"realtimeInput": {"activityEnd": {}}}))
                                except Exception as e:
                                    print(f"[!] Error sending end signals: {e}")
                            await asyncio.sleep(0.05)
                        else:
                            try:
                                audio_bytes = bridge.gemini_queue.get_nowait()
                                msg = {
                                    "realtimeInput": {
                                        "audio": {
                                            "data": base64.b64encode(audio_bytes).decode("utf-8"),
                                            "mimeType": f"audio/pcm;rate={SAMPLE_RATE}"
                                        }
                                    }
                                }
                                await ws.send(json.dumps(msg))
                            except queue.Empty:
                                await asyncio.sleep(0.01)
                            except Exception as e:
                                print(f"[!] Send error: {e}")
                                break

                # ── Receive Audio Task ──
                async def receive_audio():
                    while not bridge.should_quit and bridge.is_listening:
                        try:
                            raw = await asyncio.wait_for(ws.recv(decode=False), timeout=0.5)
                            response = json.loads(raw.decode("utf-8"))
                        except asyncio.TimeoutError:
                            continue
                        except Exception as e:
                            if isinstance(e, ConnectionClosed):
                                print("[-] Connection closed.")
                            else:
                                print(f"[!] Receive error: {e}")
                            break

                        # Handle tools
                        tool_call = response.get("toolCall") or response.get("tool_call")
                        if tool_call:
                            func_calls = tool_call.get("functionCalls") or tool_call.get("function_calls") or []
                            func_responses = []
                            for fc in func_calls:
                                name = fc.get("name", "")
                                args = fc.get("args", {})
                                call_id = fc.get("id", "")
                                print(f"\n[AI Tool Call] {name}({args})")
                                
                                func = TOOL_FUNCTIONS.get(name)
                                if func:
                                    try:
                                        if name == "search_master_brain":
                                            result = func(args.get("query", ""), args.get("namespace", "auto"))
                                        elif name == "route_task":
                                            result = func(args.get("task_description", ""))
                                        elif name == "talk_to_antigravity":
                                            result = func(args.get("message", ""))
                                        elif name == "stop_antigravity":
                                            result = func(args.get("reason", "Wayne said stop"))
                                        else:
                                            result = func(**args)
                                    except Exception as e:
                                        result = f"Tool error: {e}"
                                else:
                                    result = f"Unknown tool: {name}"
                                
                                print(f"  -> Result: {result[:200]}")
                                fr = {"name": name, "response": {"result": result}}
                                if call_id:
                                    fr["id"] = call_id
                                func_responses.append(fr)
                            
                            tool_resp_msg = {
                                "toolResponse": {
                                    "functionResponses": func_responses
                                }
                            }
                            await ws.send(json.dumps(tool_resp_msg))
                            
                            if bridge.trigger == "ptt":
                                print("\n[*] Tool response sent in PTT mode - deactivating voice session.")
                                bridge.deactivate()
                            continue

                        # Handle server content
                        server_content = response.get("serverContent") or response.get("server_content")
                        if not server_content:
                            continue

                        model_turn = server_content.get("modelTurn") or server_content.get("model_turn") or {}
                        parts = model_turn.get("parts", [])

                        for part in parts:
                            if part.get("thought", False):
                                continue

                            inline_data = part.get("inlineData") or part.get("inline_data")
                            if inline_data:
                                audio_b64 = inline_data.get("data", "")
                                if audio_b64:
                                    try:
                                        audio_bytes = base64.b64decode(audio_b64)
                                        audio_np = np.frombuffer(audio_bytes, dtype=np.int16).reshape(-1, 1)
                                        bridge.audio_out_queue.put(audio_np)
                                    except Exception as ae:
                                        print(f"  [audio err] {ae}")
                            
                            if "text" in part and part["text"]:
                                print(f"  Brain: {part['text']}", flush=True)

                        turn_complete = server_content.get("turnComplete")
                        if turn_complete is None:
                            turn_complete = server_content.get("turn_complete", False)
                        if turn_complete:
                            if not bridge.f9_held:
                                print("\n[*] Turn complete - deactivating voice session.")
                                bridge.deactivate()

                # ── Send Outbox Task ──
                async def send_outbox_text():
                    while not bridge.should_quit and bridge.is_listening:
                        try:
                            line = bridge.outbox_queue.get_nowait()
                            print(f"\n[OUTBOX -> VOICE] Sending to Gemini: {line[:100]}")
                            text_msg = {
                                "clientContent": {
                                    "turns": [{"role": "user", "parts": [{"text": f"Repeat this back to the speaker exactly word for word, with NO extra words, NO introduction, and NO conversation: {line}"}]}],
                                    "turnComplete": True
                                }
                            }
                            await ws.send(json.dumps(text_msg))
                            with bridge.lock:
                                bridge.outbox_sent_time = time.time()
                        except queue.Empty:
                            await asyncio.sleep(0.1)
                        except Exception as e:
                            print(f"[!] Outbox send error: {e}")
                            break

                # ── Session Monitor Task ──
                async def session_monitor():
                    while not bridge.should_quit and bridge.is_listening:
                        await asyncio.sleep(0.5)
                        check_and_reload_config()
                        
                        if bridge.trigger == "ptt" and bridge.speech_ended:
                            with bridge.lock:
                                ended_time = bridge.speech_ended_time
                            if ended_time and (time.time() - ended_time > 5.0):
                                print("\n[*] PTT session timeout waiting for response - deactivating.")
                                bridge.deactivate()
                                break
                        elif bridge.trigger == "outbox":
                            with bridge.lock:
                                sent_time = bridge.outbox_sent_time
                            if sent_time and (time.time() - sent_time > 15.0):
                                print("\n[*] Outbox session timeout waiting for response - deactivating.")
                                bridge.deactivate()
                                break
                                
                    print("[*] Closing WebSocket connection...")
                    try:
                        await ws.close()
                    except Exception:
                        pass

                # Run concurrent tasks
                try:
                    await asyncio.gather(
                        send_audio(),
                        receive_audio(),
                        send_outbox_text(),
                        session_monitor()
                    )
                except Exception as eg:
                    print(f"[!] Tasks encountered error: {eg}")

            print("\n[-] Disconnected. Ready for F9 press or outbox message...\n")

        except Exception as e:
            print(f"\n[!] Connection error: {e}")
            traceback.print_exc()
            bridge.deactivate()
            await asyncio.sleep(2)
        finally:
            bridge.reset_to_sleeping()

    out_stream.stop()
    out_stream.close()

# ──────────────────────────────────────────────────────────
# Main & State Reporter
# ──────────────────────────────────────────────────────────
def state_reporter_worker():
    last_reported = None
    while not bridge.should_quit:
        time.sleep(0.1)
        if time.time() - bridge.last_playback_ts < 0.5:
            current_state = "speaking"
        elif bridge.is_listening:
            current_state = "listening"
        else:
            current_state = "connected"
        
        if current_state != last_reported:
            last_reported = current_state
            try:
                os.makedirs(os.path.dirname(VOICE_STATUS_PATH), exist_ok=True)
                with open(VOICE_STATUS_PATH, "w", encoding="utf-8") as f:
                    json.dump({"status": current_state}, f)
            except Exception as e:
                print(f"[STATUS REPORTER ERROR] {e}")

def main():
    # Load initial config details
    ls_init, cs_init = auto_discover_agent_config()
    if ls_init and cs_init:
        AGENTAPI_ENV["ANTIGRAVITY_LS_ADDRESS"] = ls_init
        AGENTAPI_ENV["ANTIGRAVITY_CSRF_TOKEN"] = cs_init
    conv_init = get_latest_conversation_id()
    if conv_init:
        global AGENTAPI_CONVERSATION
        AGENTAPI_CONVERSATION = conv_init

    print(f"Starting Keystone Voice Bridge...")
    print(f"Conversation ID: {AGENTAPI_CONVERSATION[:12]}...")
    print(f"LS Address:      {AGENTAPI_ENV['ANTIGRAVITY_LS_ADDRESS']}")

    # Start status reporter
    reporter_thread = threading.Thread(target=state_reporter_worker, daemon=True)
    reporter_thread.start()

    # Start pynput keyboard listener
    listener = pynput_kb.Listener(on_press=on_key_press, on_release=on_key_release)
    listener.start()

    # Start input audio device stream
    in_stream = sd.InputStream(
        device=INPUT_DEVICE,
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='int16',
        blocksize=BLOCK_SIZE,
        callback=audio_callback
    )
    in_stream.start()

    try:
        asyncio.run(gemini_session_loop())
    except KeyboardInterrupt:
        print("\nShutting down Keystone Voice Bridge...")
    finally:
        bridge.should_quit = True
        in_stream.stop()
        in_stream.close()
        print("Shutdown complete.")

if __name__ == "__main__":
    main()
