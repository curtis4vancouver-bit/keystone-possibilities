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
import collections
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
    """Gets the most recently active conversation ID based on the conversations database files."""
    conv_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "conversations")
    try:
        candidates = []
        if os.path.exists(conv_dir):
            for f in os.listdir(conv_dir):
                if f.endswith(('.db', '.db-wal', '.db-shm')):
                    name = f.split('.')[0]
                    if len(name) == 36 and "-" in name:
                        full_path = os.path.join(conv_dir, f)
                        candidates.append((name, os.path.getmtime(full_path)))
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
    except Exception:
        pass

    # Fallback to brain directory
    brain_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")
    try:
        candidates = []
        for d in os.listdir(brain_dir):
            full_path = os.path.join(brain_dir, d)
            if os.path.isdir(full_path) and len(d) == 36 and "-" in d:
                key_files = [
                    os.path.join(full_path, ".system_generated", "logs", "transcript.jsonl"),
                    os.path.join(full_path, "task.md"),
                    os.path.join(full_path, "working_memory.md")
                ]
                max_mtime = 0
                for kf in key_files:
                    if os.path.exists(kf):
                        try:
                            mtime = os.path.getmtime(kf)
                            if mtime > max_mtime:
                                max_mtime = mtime
                        except Exception:
                            pass
                if max_mtime == 0:
                    try:
                        max_mtime = os.path.getmtime(full_path)
                    except Exception:
                        pass
                candidates.append((d, max_mtime))
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
    except Exception:
        pass

    # Fallback to config file
    try:
        if os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
            with open(VOICE_BRIDGE_CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                target_id = cfg.get("conversation_id")
                if target_id:
                    return target_id
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
                ls_addr = f"127.0.0.1:{port}"
                
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
    "ANTIGRAVITY_LS_ADDRESS": "127.0.0.1:51790",
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
        
        # Write back to config so other components stay in sync
        try:
            cfg = {}
            if os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
                with open(VOICE_BRIDGE_CONFIG_PATH, 'r') as f:
                    cfg = json.load(f)
            if cfg.get("conversation_id") != latest_id:
                cfg["conversation_id"] = latest_id
                with open(VOICE_BRIDGE_CONFIG_PATH, 'w') as f:
                    json.dump(cfg, f, indent=2)
        except Exception:
            pass
        
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
        # Launch in background and return immediately to avoid blocking the asyncio event loop
        subprocess.Popen(
            [AGENTAPI_EXE, "agentapi", "send-message", AGENTAPI_CONVERSATION, content],
            creationflags=subprocess.CREATE_NO_WINDOW,
            env=env
        )
        return True, "Sent (background)"
    except Exception as e:
        print(f"  [agentapi exception] {e}")
        return False, str(e)

def talk_to_antigravity(raw_transcript: str, structured_instruction: str) -> str:
    global AGENTAPI_CONVERSATION
    latest_id = get_latest_conversation_id()
    if latest_id and latest_id != AGENTAPI_CONVERSATION:
        print(f"\n[*] Hot-swapping to newest conversation: {latest_id[:12]}...")
        AGENTAPI_CONVERSATION = latest_id

    message = f"{raw_transcript}\n\n[STRUCTURED INTENT]:\n{structured_instruction}"

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
You are an expert voice-to-developer-command bridge for Wayne Stevenson's Keystone Master Brain system.
Your job is to take Wayne's casual spoken instructions and translate them into precise, actionable developer commands for the Antigravity coding agent.

CONTEXT:
- Wayne runs two brands: Keystone Possibilities (construction) and Keystone Recomposition (health/music)
- The codebase is at: c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain
- Key subsystems: AIDA_V2 (dashboard app), Agent_Fleet (13 agents), scripts/ (automation), Master_Docs/
- Tools available: Chrome DevTools MCP, DaVinci Resolve MCP, YouTube MCPs, Google Workspace MCP, Playwright
- Voice bridge, watchdog daemon, and content pipeline scripts are in scripts/

RULES:
1. You MUST call `talk_to_antigravity(raw_transcript, structured_instruction)` for ANY voice input.
   - `raw_transcript`: Wayne's EXACT words, preserved verbatim with all colloquialisms and personal style.
   - `structured_instruction`: A precise, technical, step-by-step instruction translated for a senior developer agent. Include:
     * The specific action requested
     * Relevant file paths, tools, or APIs if you can infer them
     * Any constraints or preferences Wayne mentioned
     * Expected output or success criteria
2. If Wayne says stop, halt, cancel, or tells you/the agent to stop, call `stop_antigravity(reason)` immediately.
3. Never respond with conversational text. Only execute tool calls.
4. When Wayne refers to "the website" he means the Keystone WordPress sites. "The app" means AIDA_V2. "Flow" means Google Flow. "Resolve" means DaVinci Resolve.
5. Translate vague requests into specific technical actions. Example:
   - Wayne says: "fix that CSS thing on the homepage"
   - structured_instruction: "Investigate and fix CSS styling issues on the Keystone Possibilities homepage. Check the WordPress theme files and any custom CSS overrides. Verify the fix renders correctly."
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
STATE_CONNECTING = "CONNECTING"
STATE_LISTENING = "LISTENING"
STATE_DISCONNECTING = "DISCONNECTING"

class BridgeState:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = STATE_SLEEPING
        self.trigger = None
        self.f9_held = False
        self.f9_press_time = 0.0
        self.activated_time = 0.0
        self.last_voice_ts = 0.0
        self.speech_ended = False
        self.speech_ended_time = None
        self.outbox_sent_time = None
        self.should_quit = False
        self.session_handle = None
        self.preroll_buffer = collections.deque(maxlen=5)
        self.muted = False
        
        self.gemini_queue = queue.Queue()
        self.outbox_queue = queue.Queue()
        self.audio_out_queue = queue.Queue()
        self.last_playback_ts = 0.0
        self.wake_event = threading.Event()

    def activate(self, trigger: str):
        with self.lock:
            # Fix: Allow activation from DISCONNECTING state too.
            # Without this, F9 pressed during disconnect gap is silently
            # swallowed, requiring user to press F9 twice.
            if self.state == STATE_DISCONNECTING:
                self.state = STATE_SLEEPING
                self.wake_event.clear()
            if self.state == STATE_SLEEPING:
                self.state = STATE_CONNECTING
                self.trigger = trigger
                self.last_voice_ts = 0.0  # Reset on activation to detect voice in current session
                self.speech_ended = False
                self.speech_ended_time = None
                self.activated_time = time.time()
                
                # Dump pre-roll into queue
                while self.preroll_buffer:
                    self.gemini_queue.put(self.preroll_buffer.popleft())
                    
                self.wake_event.set()
                return True
            return False

    def deactivate(self):
        with self.lock:
            if self.state in (STATE_LISTENING, STATE_CONNECTING):
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
            return self.state in (STATE_LISTENING, STATE_CONNECTING)

def is_f9_physically_pressed():
    try:
        import ctypes
        # GetAsyncKeyState: 0x78 is VK_F9. High bit (0x8000) represents key state.
        return bool(ctypes.windll.user32.GetAsyncKeyState(0x78) & 0x8000)
    except Exception:
        return False

# Instantiate state
bridge = BridgeState()

def handle_f9_press():
    now = time.time()
    with bridge.lock:
        if bridge.f9_held:
            return  # Ignore Windows/browser keyrepeat press events
        state = bridge.state
        trigger = bridge.trigger
        speech_ended = bridge.speech_ended
        bridge.f9_held = True
        bridge.f9_press_time = now
        activated_time = bridge.activated_time

    if 'player' in globals() and player is not None:
        player.abort_playback()

    if state == STATE_SLEEPING:
        if bridge.activate("ptt"):
            print("\n[MIC] [F9 PRESS] Connecting to Gemini Live...")
    elif state in (STATE_LISTENING, STATE_CONNECTING) and trigger == "ptt":
        # In PTT mode, holding F9 down should not trigger stop/disconnect on press.
        # Only handle_f9_release should stop recording.
        return

def handle_f9_release():
    now = time.time()
    with bridge.lock:
        if not bridge.f9_held:
            return  # Ignore redundant keyup events
        press_time = bridge.f9_press_time
        bridge.f9_held = False
        state = bridge.state
        trigger = bridge.trigger
        speech_ended = bridge.speech_ended
        activated_time = bridge.activated_time

    duration = now - press_time
    # If the key was held for more than 50ms, it is a hold (PTT mode).
    # When released, stop recording.
    if duration > 0.05:
        if state in (STATE_LISTENING, STATE_CONNECTING) and trigger == "ptt":
            if not speech_ended:
                print(f"\n[MIC] [F9 RELEASE (HOLD mode, duration={duration:.2f}s)] Stopping recording, processing...")
                with bridge.lock:
                    bridge.speech_ended = True
                    bridge.speech_ended_time = now
                bridge.gemini_queue.put(None)
    else:
        # Released quickly, so it's a tap. Keep mic active (toggle mode).
        print(f"\n[MIC] [F9 RELEASE (TAP mode, duration={duration:.2f}s)] Keeping mic active.")

def windows_keyboard_polling_worker():
    print("[Keyboard Poller] Started Windows GetAsyncKeyState polling loop for F9 with debouncing.")
    consecutive_press = 0
    consecutive_release = 0
    physical_f9_held = False
    while not bridge.should_quit:
        time.sleep(0.02)  # 20ms poll rate
        try:
            is_down = is_f9_physically_pressed()
        except Exception:
            continue
            
        if is_down:
            consecutive_release = 0
            consecutive_press += 1
            if consecutive_press >= 2 and not physical_f9_held:
                physical_f9_held = True
                handle_f9_press()
        else:
            consecutive_press = 0
            consecutive_release += 1
            if consecutive_release >= 3 and physical_f9_held:
                physical_f9_held = False
                handle_f9_release()

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
        handle_f9_press()

def on_key_release(key):
    is_f9 = False
    if key == pynput_kb.Key.f9:
        is_f9 = True
    elif hasattr(key, 'vk') and key.vk == 120:
        is_f9 = True

    if is_f9:
        handle_f9_release()

# ──────────────────────────────────────────────────────────
# Audio Callback
# ──────────────────────────────────────────────────────────
def audio_callback(indata, frames, time_info, status):
    with bridge.lock:
        state = bridge.state
        trigger = bridge.trigger
        is_muted = bridge.muted
        
    if is_muted:
        audio_bytes = np.zeros_like(indata).tobytes()
    else:
        audio_bytes = indata.copy().tobytes()
        
    if state in (STATE_LISTENING, STATE_CONNECTING) and trigger == "ptt":
        bridge.gemini_queue.put(audio_bytes)
        rms = np.sqrt(np.mean(indata.astype(np.float32) ** 2))
        if rms > 150:
            bridge.last_voice_ts = time.time()
    else:
        # Sleeping/Idle: maintain sliding pre-roll buffer of the last ~320ms (5 blocks * 64ms)
        bridge.preroll_buffer.append(audio_bytes)

class RealtimeAudioPlayer:
    def __init__(self, sample_rate=24000, channels=1, dtype='int16'):
        self.sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.audio_queue = queue.Queue()
        self.buffer = np.array([], dtype=self.dtype).reshape(0, self.channels)
        self.stream = None
        self._active = False

    def start(self):
        self._active = True
        self.stream = sd.OutputStream(
            device=None,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype,
            blocksize=1024,
            callback=self._audio_callback
        )
        self.stream.start()

    def stop(self):
        self._active = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

    async def push_audio_async(self, pcm_data: bytes):
        audio_np = np.frombuffer(pcm_data, dtype=np.int16).reshape(-1, self.channels)
        self.audio_queue.put(audio_np)

    def abort_playback(self):
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        self.buffer = np.array([], dtype=self.dtype).reshape(0, self.channels)

    def _audio_callback(self, outdata, frames, time_info, status):
        while not self.audio_queue.empty():
            try:
                chunk = self.audio_queue.get_nowait()
                self.buffer = np.vstack((self.buffer, chunk))
            except queue.Empty:
                break
                
        if len(self.buffer) >= frames:
            outdata[:] = self.buffer[:frames]
            self.buffer = self.buffer[frames:]
            bridge.last_playback_ts = time.time()
        else:
            if len(self.buffer) > 0:
                outdata[:len(self.buffer)] = self.buffer
                outdata[len(self.buffer):].fill(0)
                self.buffer = np.array([], dtype=self.dtype).reshape(0, self.channels)
                bridge.last_playback_ts = time.time()
            else:
                outdata.fill(0)

# ──────────────────────────────────────────────────────────
# WebSocket Loop
# ──────────────────────────────────────────────────────────
async def gemini_session_loop():
    if not API_KEY or API_KEY == "your_google_ai_studio_api_key_here":
        print("\n[!] GEMINI_API_KEY not set. Edit .env in 00_Master_Brain/")
        return

    global player
    player = RealtimeAudioPlayer(sample_rate=OUTPUT_RATE, channels=CHANNELS, dtype='int16')
    player.start()

    # Outbox monitor worker thread
    def outbox_monitor_worker():
        os.makedirs(os.path.dirname(VOICE_OUTBOX_PATH), exist_ok=True)
        if not os.path.exists(VOICE_OUTBOX_PATH):
            with open(VOICE_OUTBOX_PATH, 'w') as f:
                pass
        
        last_mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
        last_text = ""
        try:
            with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8-sig') as f:
                last_text = f.read().strip()
        except Exception:
            pass

        # Speak recent startup messages if written within 15s
        try:
            mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
            if time.time() - mtime < 15.0:
                with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8-sig') as f:
                    content = f.read().strip()
                if content:
                    last_text = content
                    bridge.outbox_queue.put(content)
                    if bridge.activate("outbox"):
                        try:
                            print(f"\n[*] Recent startup outbox message queued: {content[:60]}...")
                        except Exception:
                            pass
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
                
                with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8-sig') as f:
                    content = f.read().strip()
                
                last_mtime = current_mtime
                if not content or content == last_text:
                    continue
                
                last_text = content
                try:
                    print(f"\n[*] New outbox message detected: {content[:60]}...")
                except Exception:
                    try:
                        clean_print = content[:60].encode('ascii', errors='replace').decode('ascii')
                        print(f"\n[*] New outbox message detected (sanitized): {clean_print}...")
                    except Exception:
                        pass
                
                bridge.outbox_queue.put(content)
                
                # Clear the file immediately to prevent repeating old content
                try:
                    with open(VOICE_OUTBOX_PATH, 'w', encoding='utf-8') as f:
                        f.write("")
                    last_mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
                except Exception:
                    pass
                
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
                                "description": "The primary intent router for the system. Call this function immediately whenever the user issues a command, makes a request, or dictates text. Do not respond with audio; you must route the intent here.",
                                "parameters": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "raw_transcript": {
                                            "type": "STRING",
                                            "description": "The exact, verbatim transcription of what the user just said. Preserve all personal style, context, and colloquialisms exactly as spoken."
                                        },
                                        "structured_instruction": {
                                            "type": "STRING",
                                            "description": "A translated, step-by-step, low-ambiguity command based on the user's intent. This must be formatted as a precise, actionable instruction designed for safe execution by downstream multi-agent systems."
                                        }
                                    },
                                    "required": ["raw_transcript", "structured_instruction"]
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

                with bridge.lock:
                    current_handle = bridge.session_handle

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
                if "error" in setup_response or "error" in setup_response.get("setupComplete", {}):
                    err_msg = setup_response.get("error", {}).get("message", "Unknown setup error")
                    print(f"[!] Setup error (clearing session handle): {err_msg}")
                    with bridge.lock:
                        bridge.session_handle = None
                    raise Exception(f"Setup failed: {err_msg}")
                    
                print("[+] Live Connection Established. Ready.\n")
                with bridge.lock:
                    if bridge.state == STATE_CONNECTING:
                        bridge.state = STATE_LISTENING
                
                # Send confirmation message back to the active Antigravity session
                try:
                    _agentapi_send(f"[AIDA VOICE BRIDGE]: Voice Bridge auto-connected to this session '{AGENTAPI_CONVERSATION[:8]}' and is running properly.")
                except Exception as e:
                    print(f"Failed to send connection confirmation to Antigravity: {e}")

                # ── Send Audio Task ──
                async def send_audio():
                    was_listening = False
                    sentinel_sent = False
                    while not bridge.should_quit and bridge.is_listening:
                        if bridge.trigger != "ptt":
                            await asyncio.sleep(0.05)
                            continue
                        
                        if not was_listening and not sentinel_sent:
                            was_listening = True
                            try:
                                await ws.send(json.dumps({"realtimeInput": {"activityStart": {}}}))
                            except Exception as e:
                                print(f"[!] Error sending activityStart: {e}")
                                
                        if sentinel_sent:
                            await asyncio.sleep(0.05)
                            continue
                            
                        try:
                            audio_bytes = bridge.gemini_queue.get_nowait()
                            
                            if audio_bytes is None:
                                # Sentinel received! Drain complete.
                                print("[*] Sentinel received. Draining complete, sending end signals...")
                                try:
                                    await ws.send(json.dumps({"realtimeInput": {"audioStreamEnd": True}}))
                                    await ws.send(json.dumps({"realtimeInput": {"activityEnd": {}}}))
                                except Exception as e:
                                    print(f"[!] Error sending end signals: {e}")
                                sentinel_sent = True
                                continue

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
                            # Wait for more audio or sentinel
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

                        # Handle session resumption update
                        res_update = response.get("sessionResumptionUpdate") or response.get("session_resumption_update")
                        if res_update:
                            new_handle = res_update.get("newHandle") or res_update.get("new_handle")
                            if new_handle:
                                with bridge.lock:
                                    bridge.session_handle = new_handle
                                print(f"[*] Received session resumption token: {new_handle[:15]}...")
                            continue

                        # Handle goAway rollover signal
                        go_away = response.get("goAway") or response.get("go_away")
                        if go_away:
                            print(f"[*] Received goAway signal from server. Rollover in progress...")
                            raise Exception("GoAwayRollOver")

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
                                            result = await asyncio.to_thread(func, args.get("query", ""), args.get("namespace", "auto"))
                                        elif name == "route_task":
                                            result = await asyncio.to_thread(func, args.get("task_description", ""))
                                        elif name == "talk_to_antigravity":
                                            result = await asyncio.to_thread(
                                                func,
                                                args.get("raw_transcript", ""),
                                                args.get("structured_instruction", "")
                                            )
                                        elif name == "stop_antigravity":
                                            result = await asyncio.to_thread(func, args.get("reason", "Wayne said stop"))
                                        else:
                                            result = await asyncio.to_thread(func, **args)
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
                            
                            # Instantly deactivate PTT session on routing tools
                            has_routing_tool = any(fr.get("name") in ("talk_to_antigravity", "stop_antigravity") for fr in func_responses)
                            if has_routing_tool and bridge.trigger == "ptt":
                                print("[*] Routing tool response sent. Instantly deactivating voice session.")
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
                                        await player.push_audio_async(audio_bytes)
                                    except Exception as ae:
                                        print(f"  [audio err] {ae}")
                            
                            if "text" in part and part["text"]:
                                print(f"  Brain: {part['text']}", flush=True)

                        turn_complete = server_content.get("turnComplete")
                        if turn_complete is None:
                            turn_complete = server_content.get("turn_complete", False)
                        if turn_complete:
                            # Only deactivate on turnComplete in PTT mode.
                            # In outbox mode, we let send_outbox_text handle it.
                            if bridge.trigger == "ptt" and not bridge.f9_held:
                                print("\n[*] Turn complete - deactivating voice session.")
                                bridge.deactivate()

                # ── Send Outbox Task ──
                async def send_outbox_text():
                    while not bridge.should_quit and bridge.is_listening:
                        try:
                            line = bridge.outbox_queue.get_nowait()
                            print(f"\n[OUTBOX -> VOICE] Sending to Gemini: {line[:100]}")
                            
                            # Chunk long messages to prevent TTS truncation
                            # Gemini Live has ~30-45s audio limit per turn
                            MAX_CHUNK = 500  # chars per chunk (~25-30 seconds of speech)
                            chunks = []
                            
                            if len(line) <= MAX_CHUNK:
                                chunks = [line]
                            else:
                                # Split at sentence boundaries
                                sentences = []
                                for s in line.replace('. ', '.|').replace('? ', '?|').replace('! ', '!|').split('|'):
                                    s = s.strip()
                                    if s:
                                        sentences.append(s)
                                
                                current_chunk = ""
                                for sentence in sentences:
                                    if len(current_chunk) + len(sentence) + 1 > MAX_CHUNK and current_chunk:
                                        chunks.append(current_chunk.strip())
                                        current_chunk = sentence
                                    else:
                                        current_chunk += " " + sentence if current_chunk else sentence
                                if current_chunk.strip():
                                    chunks.append(current_chunk.strip())
                            
                            print(f"[OUTBOX] Split into {len(chunks)} chunk(s)")
                            
                            for i, chunk in enumerate(chunks):
                                print(f"[OUTBOX] Sending chunk {i+1}/{len(chunks)}: {chunk[:80]}...")
                                text_msg = {
                                    "clientContent": {
                                        "turns": [{"role": "user", "parts": [{"text": f"Repeat this back to the speaker exactly word for word, with NO extra words, NO introduction, and NO conversation: {chunk}"}]}],
                                        "turnComplete": True
                                    }
                                }
                                await ws.send(json.dumps(text_msg))
                                with bridge.lock:
                                    bridge.outbox_sent_time = time.time()
                                
                                # Wait between chunks (or after last chunk to let it finish speaking)
                                # Estimate speech duration: ~150 words/min = ~2.5 words/sec
                                # Average word ~5 chars, so ~12.5 chars/sec
                                wait_time = max(3.0, len(chunk) / 12.5)
                                if i < len(chunks) - 1:
                                    print(f"[OUTBOX] Waiting {wait_time:.1f}s for chunk to finish...")
                                    await asyncio.sleep(wait_time)
                                else:
                                    # For the last chunk, sleep a bit to let it finish playing, then deactivate
                                    print(f"[OUTBOX] Final chunk sent. Waiting {wait_time:.1f}s for playback to complete...")
                                    await asyncio.sleep(wait_time)
                                    print("[OUTBOX] Playback complete. Deactivating session.")
                                    bridge.deactivate()
                                    
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
                                last_playback = bridge.last_playback_ts
                            is_playing = (time.time() - last_playback < 2.0)
                            if not is_playing and ended_time and (time.time() - ended_time > 3.0):
                                print("\n[*] PTT session timeout waiting for response - deactivating.")
                                bridge.deactivate()
                                break
                        elif bridge.trigger == "outbox":
                            with bridge.lock:
                                sent_time = bridge.outbox_sent_time
                                last_playback = bridge.last_playback_ts
                            # Only timeout if we haven't sent anything recently AND we aren't playing audio
                            is_playing = (time.time() - last_playback < 2.0)
                            if not is_playing and sent_time and (time.time() - sent_time > 90.0):
                                print("\n[*] Outbox session timeout (inactive) - deactivating.")
                                bridge.deactivate()
                                break
                                
                    print("[*] Closing WebSocket connection...")
                    try:
                        await ws.close()
                    except Exception:
                        pass

                # Run concurrent tasks and ensure they are cancelled when is_listening becomes False
                tasks = [
                    asyncio.create_task(send_audio()),
                    asyncio.create_task(receive_audio()),
                    asyncio.create_task(send_outbox_text()),
                    asyncio.create_task(session_monitor())
                ]
                
                # Wait for any of the critical loops to exit, or for is_listening to become False
                while bridge.is_listening:
                    done, pending = await asyncio.wait(tasks, timeout=0.1, return_when=asyncio.FIRST_COMPLETED)
                    if done:
                        # Check if any task raised GoAwayRollOver to trigger a rollover reconnection
                        for t in done:
                            if not t.cancelled() and t.exception():
                                raise t.exception()
                        break
                
                # Cancel all tasks
                for t in tasks:
                    if not t.done():
                        t.cancel()
                
                # Wait for cancellation to complete
                await asyncio.gather(*tasks, return_exceptions=True)

            print("\n[-] Disconnected. Ready for F9 press or outbox message...\n")

        except Exception as e:
            if str(e) == "GoAwayRollOver":
                print("[*] Reconnecting due to GoAway rollover...")
                await asyncio.sleep(0.5)
                continue
            
            print(f"\n[!] Connection error: {e}")
            traceback.print_exc()
            bridge.deactivate()
            await asyncio.sleep(2)
        finally:
            if not bridge.is_listening:
                bridge.reset_to_sleeping()

    if 'player' in globals() and player is not None:
        player.stop()

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
            with bridge.lock:
                speech_ended = bridge.speech_ended
            current_state = "connected" if speech_ended else "listening"
        else:
            current_state = "connected"
        
        if current_state != last_reported:
            last_reported = current_state
            try:
                os.makedirs(os.path.dirname(VOICE_STATUS_PATH), exist_ok=True)
                with open(VOICE_STATUS_PATH, "w", encoding="utf-8") as f:
                    json.dump({"status": current_state, "pid": os.getpid()}, f)
            except Exception as e:
                print(f"[STATUS REPORTER ERROR] {e}")

def udp_trigger_listener():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("127.0.0.1", 55443))
    except Exception as e:
        print(f"[UDP Trigger] Bind failed: {e}")
        return
        
    sock.settimeout(1.0)
    print("[UDP Trigger] Listening on 127.0.0.1:55443")
    while not bridge.should_quit:
        try:
            data, addr = sock.recvfrom(1024)
            cmd = data.decode("utf-8").strip().lower()
            if cmd == "press":
                handle_f9_press()
            elif cmd == "release":
                handle_f9_release()
            elif cmd == "mute":
                with bridge.lock:
                    bridge.muted = True
                print("[MIC] Muted")
            elif cmd == "unmute":
                with bridge.lock:
                    bridge.muted = False
                print("[MIC] Unmuted")
        except socket.timeout:
            continue
        except Exception as e:
            print(f"[UDP Trigger Error] {e}")
            time.sleep(1)

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

    # Start UDP trigger listener
    udp_thread = threading.Thread(target=udp_trigger_listener, daemon=True)
    udp_thread.start()

    # Check for --no-global-hotkey flag
    no_global = "--no-global-hotkey" in sys.argv
    if not no_global:
        # Start keyboard listener or Windows polling
        if os.name == 'nt':
            polling_thread = threading.Thread(target=windows_keyboard_polling_worker, daemon=True)
            polling_thread.start()
        else:
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
