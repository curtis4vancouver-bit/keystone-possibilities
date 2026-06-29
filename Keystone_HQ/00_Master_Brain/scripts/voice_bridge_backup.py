"""
Keystone Voice Bridge — Raw WebSocket Gemini Live API
=====================================================
Built from the official Google Gemini Cookbook pattern:
  wss://generativelanguage.googleapis.com/ws/...BidiGenerateContent

Modes:
  1. Wake Word: Say "Keystone" to activate. Auto-deactivates after silence.
  2. Push-to-Talk: Hold F9 to stream. Release to stop.

Features:
  - System Prompt (Persona: Master Brain)
  - Tool Calling (search_master_brain, route_task, talk_to_antigravity)
  - Persistent WebSocket — stays connected between PTT presses
  - Raw PCM audio over WebSocket (no SDK bugs)

Requirements: vosk, pynput, sounddevice, numpy, websockets, python-dotenv
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
import numpy as np
import sounddevice as sd
import keyboard

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
        entry = {"task": task_description, "source": "voice_bridge", "timestamp": datetime.datetime.now().isoformat(), "status": "pending"}
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
# Voice Bridge Config — Auto-Discovered
# ──────────────────────────────────────────────────────────
VOICE_BRIDGE_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
)
VOICE_OUTBOX_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_outbox.txt"
)

def get_latest_conversation_id():
    """Gets the targeted conversation ID from config, falling back to newest brain folder."""
    try:
        if os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
            with open(VOICE_BRIDGE_CONFIG_PATH, "r", encoding="utf-8") as f:
                import json
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
    """Dynamically discover LS_ADDRESS and CSRF_TOKEN from the running language_server.exe process.
    
    Strategy:
      1. Use psutil to find language_server.exe and extract --csrf_token from its cmdline.
      2. Parse the language server log file to find the HTTP port for the matching PID.
      3. Write discovered values back to voice_bridge_config.json for other components.
      4. Fall back to reading the existing config file if process discovery fails.
    """
    import json
    import re
    
    # --- Phase 1: Dynamic Process Discovery ---
    try:
        import psutil
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
                print(f"  [Discovery] Live process PID={pid} -> {ls_addr}, token={csrf[:12]}...")
                
                # Write back to config so AIDA dashboard and other components stay in sync
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
    except ImportError:
        pass  # psutil not available, fall through to config file
    except Exception as e:
        print(f"  [Discovery] Process scan failed: {e}")
    
    # --- Phase 2: Fallback to config file ---
    try:
        if not os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
            return None, None
            
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
    
    # 1. Always ensure we are targeting the newest conversation
    latest_id = get_latest_conversation_id()
    if latest_id and latest_id != AGENTAPI_CONVERSATION:
        AGENTAPI_CONVERSATION = latest_id
        changed = True
        
    # 2. Periodically auto-discover LS_ADDRESS and CSRF_TOKEN directly from the process
    import time
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

# Initial fast-load discovery
ls_init, cs_init = auto_discover_agent_config()
if ls_init and cs_init:
    AGENTAPI_ENV["ANTIGRAVITY_LS_ADDRESS"] = ls_init
    AGENTAPI_ENV["ANTIGRAVITY_CSRF_TOKEN"] = cs_init
conv_init = get_latest_conversation_id()
if conv_init:
    AGENTAPI_CONVERSATION = conv_init
    
print(f"[Config] Conversation: {AGENTAPI_CONVERSATION[:12]}...")
print(f"[Config] LS Address:   {AGENTAPI_ENV['ANTIGRAVITY_LS_ADDRESS']}")
print(f"[Config] Outbox:       {VOICE_OUTBOX_PATH}")


def _agentapi_send(content: str) -> tuple:
    """Send a message to Antigravity via agentapi. Returns (success: bool, output: str)."""
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
            with open("C:\\Users\\Curtis\\.gemini\\antigravity\\agentapi_debug.log", "w") as f:
                f.write(f"ENV: {env}\nCOMMAND: {result.args}\nSTDERR: {result.stderr}")
            return False, result.stderr
    except Exception as e:
        print(f"  [agentapi exception] {e}")
        return False, str(e)

def talk_to_antigravity(message: str) -> str:
    """Send a message directly into the Antigravity agent's conversation via agentapi."""
    global AGENTAPI_CONVERSATION
    
    # [HOT SWAP] Instantly sync to newest conversation to prevent 'double glitch' on new chats
    latest_id = get_latest_conversation_id()
    if latest_id and latest_id != AGENTAPI_CONVERSATION:
        print(f"\n[*] Hot-swapping to newest conversation: {latest_id[:12]}...")
        AGENTAPI_CONVERSATION = latest_id

    success, output = _agentapi_send(f"[VOICE COMMAND from Wayne]: {message}")
    if success:
        return "Sent."
    else:
        # Fallback to file-based relay
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
    """Send an urgent STOP command directly to the Antigravity agent via agentapi."""
    success, output = _agentapi_send(f"[PRIORITY STOP from Wayne]: {reason} - STOP immediately and check in with Wayne.")
    if success:
        return "Stopped."
    else:
        return "Failed."

def get_antigravity_status() -> str:
    """Read Antigravity's recent activity from the conversation transcript."""
    try:
        transcript_path = os.path.join(
            os.path.expanduser("~"),
            ".gemini", "antigravity", "brain",
            "236c85bb-e3ba-414e-bb2b-64e7699bb334",
            ".system_generated", "logs", "transcript.jsonl"
        )
        if not os.path.exists(transcript_path):
            return "Cannot read Antigravity status — transcript not found."
        
        # Read last 10 lines of the transcript for recent activity
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        recent = lines[-10:] if len(lines) >= 10 else lines
        summaries = []
        for line in recent:
            try:
                entry = json.loads(line.strip())
                step_type = entry.get("type", "")
                content = entry.get("content", "")
                if step_type == "PLANNER_RESPONSE" and content:
                    text = content[:500]
                    summaries.append(f"Agent said: {text}")
                elif step_type == "USER_INPUT" and content:
                    summaries.append(f"Wayne asked: {content[:200]}")
            except Exception:
                continue
        
        if not summaries:
            return "No recent activity found in Antigravity's transcript."
        
        return "\n".join(summaries[-3:])
    except Exception as e:
        return f"Status read error: {e}"

# Tool registry for dispatch
TOOL_FUNCTIONS = {
    "search_master_brain": search_master_brain,
    "route_task": route_task,
    "talk_to_antigravity": talk_to_antigravity,
    "stop_antigravity": stop_antigravity,
    "get_antigravity_status": get_antigravity_status,
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
You are Orus, the voice of the Master Brain. Please read the provided messages to Wayne naturally and directly.
"""


# ──────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────
PTT_KEY = 'f9'
SAMPLE_RATE = 16000
OUTPUT_RATE = 24000
CHANNELS = 1
BLOCK_SIZE = 4000

def get_device_index(keywords, is_input=True):
    try:
        devices = sd.query_devices()
        for idx, dev in enumerate(devices):
            channels = dev['max_input_channels'] if is_input else dev['max_output_channels']
            if channels > 0 and any(kw.lower() in dev['name'].lower() for kw in keywords):
                return idx
    except Exception as e:
        print(f"Error searching audio device: {e}")
    return None

INPUT_DEVICE = get_device_index(["Logitech", "PRO X"], is_input=True)
OUTPUT_DEVICE = get_device_index(["EP-HDMI-RX"], is_input=False)



print(f"[Audio] Selected Input Device: {INPUT_DEVICE} ({sd.query_devices(INPUT_DEVICE)['name'] if INPUT_DEVICE is not None else 'Default'})")
print(f"[Audio] Selected Output Device: {OUTPUT_DEVICE} ({sd.query_devices(OUTPUT_DEVICE)['name'] if OUTPUT_DEVICE is not None else 'Default'})")



VOSK_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "models", "vosk-model-small-en-us-0.15"
)

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
except ImportError:
    pass

API_KEY = os.environ.get("GEMINI_API_KEY", "")

# WebSocket endpoint — the CORRECT way per official Google docs
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
        self.has_spoken = False
        self.speech_ended = False
        self.speech_ended_time = None
        self.should_quit = False
        self.gemini_queue = queue.Queue()
        self.outbox_queue = queue.Queue()  # For messages waiting to be spoken
        self.audio_out_queue = queue.Queue()  # Decoupled audio playback queue
        self.last_playback_ts = 0.0
        self.wake_event = threading.Event()

    def activate(self, trigger: str):
        with self.lock:
            if self.state == STATE_SLEEPING:
                self.state = STATE_LISTENING
                self.trigger = trigger
                self.last_voice_ts = time.time()
                self.has_spoken = False
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
                self.has_spoken = False
                self.speech_ended = False
                self.speech_ended_time = None
                # Set wake_event so the main loop can wake up and handle the exit/disconnection
                self.wake_event.set()
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
# Wake Word Detection
# ──────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────
# F9 Push-to-Talk Listener
# ──────────────────────────────────────────────────────────
def on_key_press(event):
    if event.name == PTT_KEY:
        if not bridge.f9_held:
            bridge.f9_held = True
            # Clear playback queue on interruption to stop speech immediately
            while not bridge.audio_out_queue.empty():
                try:
                    bridge.audio_out_queue.get_nowait()
                except queue.Empty:
                    break
            if bridge.activate("ptt"):
                print("\n[MIC] [F9 HELD] Listening... (release to stop)")

def on_key_release(event):
    if event.name == PTT_KEY:
        bridge.f9_held = False
        if bridge.is_listening and bridge.trigger == "ptt":
            print("\n[MIC] [F9 RELEASE] Processing...")
            with bridge.lock:
                bridge.speech_ended = True
                bridge.speech_ended_time = time.time()

keyboard.on_press_key(PTT_KEY, on_key_press)
keyboard.on_release_key(PTT_KEY, on_key_release)
print("Push-to-talk ready on F9.")

# ──────────────────────────────────────────────────────────
# Audio Callback
# ──────────────────────────────────────────────────────────
def audio_callback(indata, frames, time_info, status):
    if bridge.is_listening and bridge.trigger == "ptt":
        audio_bytes = indata.copy().tobytes()
        bridge.gemini_queue.put(audio_bytes)
        rms = np.sqrt(np.mean(indata.astype(np.float32) ** 2))
        print(f"  [Volume RMS: {rms:.1f}]  ", end="\r", flush=True)
        if rms > 200:
            bridge.last_voice_ts = time.time()

# ──────────────────────────────────────────────────────────
# Raw WebSocket Gemini Live API (Official Pattern)
# ──────────────────────────────────────────────────────────
async def gemini_session_loop():
    from websockets.asyncio.client import connect

    if not API_KEY or API_KEY == "your_google_ai_studio_api_key_here":
        print("\n[!] GEMINI_API_KEY not set. Edit .env in 00_Master_Brain/")
        return

    # Set up speaker output
    out_stream = sd.OutputStream(
        device=OUTPUT_DEVICE,
        samplerate=OUTPUT_RATE,
        channels=CHANNELS,
        dtype='int16',
        blocksize=1024
    )
    out_stream.start()

    # Dedicated playback thread using the bridge's global audio queue
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
                print(f"Playback error: {e}")

    playback_thread = threading.Thread(target=audio_playback_worker, daemon=True)
    playback_thread.start()

    # ── Global Outbox Monitor Thread ──
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

        # Speak recent messages on startup if written in the last 15s
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
    print("  KEYSTONE VOICE BRIDGE — ONLINE")
    print("=" * 55)
    print(f"  Hold F9 to talk (Push-to-Talk)")
    print(f"  Press Ctrl+C to quit")
    print("=" * 55 + "\n")

    while not bridge.should_quit:
        # Wait for activation
        bridge.wake_event.wait(timeout=1.0)
        if not bridge.is_listening:
            check_and_reload_config()
            continue

        print("[*] Connecting to Master Brain Voice API...")
        try:
            async with connect(WS_URI, additional_headers={}) as ws:
                # ── Step 1: Send setup message ──
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
                                "description": "Urgently stop the Antigravity coding agent from whatever it is currently doing. Use when Wayne says stop, halt, cancel, or expresses displeasure with what the agent is doing.",
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
                
                # Wait for setup response
                raw_setup = await ws.recv(decode=False)
                setup_response = json.loads(raw_setup.decode("utf-8"))
                print("[+] Master Brain Connected! Speak now.\n")

                # ── Step 2: Concurrent send/receive loops ──
                async def send_audio():
                    """Stream mic audio to Gemini with manual PTT activity signals."""
                    was_listening = False
                    while not bridge.should_quit and bridge.is_listening:
                        if bridge.trigger != "ptt":
                            await asyncio.sleep(0.05)
                            continue
                        # User is speaking or session is active
                        if not was_listening and not bridge.speech_ended:
                            was_listening = True
                            try:
                                await ws.send(json.dumps({"realtimeInput": {"activityStart": {}}}))
                                print("  [-> activity_start sent]")
                            except Exception as e:
                                print(f"[!] Error sending activity_start: {e}")
                        
                        if bridge.speech_ended:
                            # Speech finished — send end signals once
                            if was_listening:
                                was_listening = False
                                try:
                                    await ws.send(json.dumps({"realtimeInput": {"audioStreamEnd": True}}))
                                    await ws.send(json.dumps({"realtimeInput": {"activityEnd": {}}}))
                                    print("\n  [-> audio_stream_end & activity_end sent - waiting for response]")
                                except Exception as e:
                                    print(f"[!] Error sending end signals: {e}")
                            await asyncio.sleep(0.05)
                        else:
                            # Stream audio
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

                async def receive_audio():
                    """Receive and play audio from Gemini."""
                    while not bridge.should_quit and bridge.is_listening:
                        try:
                            # Use timeout to allow checking loop conditions periodically
                            raw = await asyncio.wait_for(ws.recv(decode=False), timeout=0.5)
                            raw_str = raw.decode("utf-8")
                            response = json.loads(raw_str)
                            
                            # Log keys and short content for debugging
                            log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_bridge_debug.log")
                            with open(log_path, "a", encoding="utf-8") as df:
                                # Truncate audio data so log isn't massive
                                log_str = raw_str
                                if "inlineData" in log_str:
                                    log_str = log_str[:500] + "... [AUDIO DATA DETECTED] ..."
                                df.write(f"{time.time()}: {log_str[:1000]}\n")
                            
                            # Print keys to terminal for instant visibility
                            keys = list(response.keys())
                            if "serverContent" in keys or "sessionResumptionUpdate" in keys:
                                # Silently skip — these are high-frequency noise
                                pass
                            else:
                                print(f"  [recv] message type(s): {keys}")
                        except asyncio.TimeoutError:
                            continue
                        except Exception as e:
                            from websockets.exceptions import ConnectionClosed
                            if isinstance(e, ConnectionClosed):
                                if getattr(e, 'code', None) == 1000:
                                    print("[-] Connection closed gracefully.")
                                else:
                                    print(f"[-] Connection closed: {e}")
                            else:
                                print(f"[!] Receive error: {e}")
                            break

                        # Handle tool calls (support both toolCall and tool_call)
                        tool_call = response.get("toolCall") or response.get("tool_call")
                        if tool_call:
                            func_calls = tool_call.get("functionCalls") or tool_call.get("function_calls") or []
                            func_responses = []
                            for fc in func_calls:
                                name = fc.get("name", "")
                                args = fc.get("args", {})
                                call_id = fc.get("id", "")
                                print(f"\n[EXECUTING TOOL] {name}({args})")
                                
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
                                        elif name == "get_antigravity_status":
                                            result = func()
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
                            
                            # Send tool responses back (camelCase is verified correct for WebSocket)
                            tool_resp_msg = {
                                "toolResponse": {
                                    "functionResponses": func_responses
                                }
                            }
                            await ws.send(json.dumps(tool_resp_msg))
                            
                            # If this was a PTT session, deactivate immediately after sending response
                            if bridge.trigger == "ptt":
                                print("\n[*] Tool response sent in PTT mode - deactivating immediately.")
                                bridge.deactivate()
                            continue

                        # Handle server content (audio / text / turn signals - support both casings)
                        server_content = response.get("serverContent") or response.get("server_content")
                        if not server_content:
                            continue

                        model_turn = server_content.get("modelTurn") or server_content.get("model_turn") or {}
                        parts = model_turn.get("parts", [])

                        for part in parts:
                            # Skip thinking/reasoning parts
                            if part.get("thought", False):
                                continue

                            # Audio response - play audio when received
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
                            
                            # Text response (if any)
                            if "text" in part and part["text"]:
                                print(f"  Brain: {part['text']}", flush=True)

                        # Check turn_complete (support both casings)
                        turn_complete = server_content.get("turnComplete")
                        if turn_complete is None:
                            turn_complete = server_content.get("turn_complete", False)
                        if turn_complete:
                            if not bridge.f9_held:
                                print("\n[*] Turn complete - deactivating voice session.")
                                bridge.deactivate()

                async def send_outbox_text():
                    """Pulls text from outbox_queue and sends to Gemini."""
                    while not bridge.should_quit and bridge.is_listening:
                        try:
                            line = bridge.outbox_queue.get_nowait()
                            print(f"\n[OUTBOX -> VOICE] Sending to Gemini: {line[:100]}")
                            text_msg = {
                                "clientContent": {
                                    "turns": [{"role": "user", "parts": [{"text": line}]}],
                                    "turnComplete": True
                                }
                            }
                            await ws.send(json.dumps(text_msg))
                        except queue.Empty:
                            await asyncio.sleep(0.1)
                        except Exception as e:
                            print(f"[!] Outbox send error: {e}")
                            break

                async def session_monitor():
                    while not bridge.should_quit and bridge.is_listening:
                        await asyncio.sleep(0.5)
                        if check_and_reload_config():
                            print("[*] Config change detected during active session. Seamlessly synced!")
                            # REMOVED bridge.deactivate() here to prevent the "double glitching" disconnect.
                            # We stay connected to Gemini, and the next tool call automatically uses the new config.
                        
                        # Safety timeout for stuck PTT connections (5 seconds after speech ended)
                        if bridge.trigger == "ptt" and bridge.speech_ended:
                            with bridge.lock:
                                ended_time = bridge.speech_ended_time
                            if ended_time and (time.time() - ended_time > 5.0):
                                print("\n[*] PTT session timeout waiting for response - deactivating.")
                                bridge.deactivate()
                                break
                                
                    print("[*] Deactivation detected. Closing WebSocket connection...")
                    try:
                        await ws.close()
                    except Exception:
                        pass

                # Run loops concurrently
                try:
                    async with asyncio.TaskGroup() as tg:
                        tg.create_task(send_audio())
                        tg.create_task(receive_audio())
                        tg.create_task(send_outbox_text())
                        tg.create_task(session_monitor())
                except* Exception as eg:
                    for e in eg.exceptions:
                        from websockets.exceptions import ConnectionClosed
                        if not isinstance(e, ConnectionClosed):
                            print(f"[!] Task error: {e}")

            print("\n[-] Disconnected. Waiting for wake word, F9, or incoming message...\n")

        except Exception as e:
            print(f"\n[!] Voice connection error: {e}")
            traceback.print_exc()
            bridge.deactivate()
            await asyncio.sleep(2)
        finally:
            bridge.reset_to_sleeping()

    out_stream.stop()
    out_stream.close()

# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────
def state_reporter_worker():
    status_path = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_status.json"
    )
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
                os.makedirs(os.path.dirname(status_path), exist_ok=True)
                with open(status_path, "w", encoding="utf-8") as f:
                    json.dump({"status": current_state}, f)
            except Exception as e:
                print(f"[STATUS REPORTER ERROR] {e}")


def main():
    print("\nStarting Keystone Voice Bridge...\n")
    
    # Start status reporter thread
    reporter_thread = threading.Thread(target=state_reporter_worker, daemon=True)
    reporter_thread.start()

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
        print("\n\nShutting down Keystone Voice Bridge...")
    finally:
        bridge.should_quit = True
        in_stream.stop()
        in_stream.close()
        print("Goodbye.")

if __name__ == "__main__":
    main()

