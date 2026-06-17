"""
Keystone Voice Bridge — Raw WebSocket Gemini Live API
=====================================================
Built from the official Google Gemini Cookbook pattern:
  wss://generativelanguage.googleapis.com/ws/...BidiGenerateContent

Modes:
  1. Wake Word: Say "Keystone" to activate. Auto-deactivates after silence.
  2. Push-to-Talk: Hold F8 to stream. Release to stop.

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
from pynput import keyboard as kb

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
# Voice Bridge Config — auto-loaded from fixed config file
# ──────────────────────────────────────────────────────────
VOICE_BRIDGE_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
)
VOICE_OUTBOX_PATH = os.path.join(
    os.path.expanduser("~"), ".gemini", "antigravity", "voice_outbox.txt"
)

def _load_bridge_config():
    """Load Voice Bridge config from the central config file."""
    if not os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
        print(f"[!] Config not found: {VOICE_BRIDGE_CONFIG_PATH}")
        print("    Run this from Antigravity to generate it.")
        sys.exit(1)
    with open(VOICE_BRIDGE_CONFIG_PATH, 'r') as f:
        cfg = json.load(f)
    return cfg

_cfg = _load_bridge_config()
_last_config_mtime = os.path.getmtime(VOICE_BRIDGE_CONFIG_PATH)

AGENTAPI_ENV = {
    "ANTIGRAVITY_AGENT": "1",
    "ANTIGRAVITY_LS_ADDRESS": _cfg.get("ls_address", "localhost:51790"),
    "ANTIGRAVITY_CSRF_TOKEN": _cfg.get("csrf_token", ""),
    "ANTIGRAVITY_PROJECT_ID": _cfg.get("project_id", ""),
}
AGENTAPI_EXE = os.path.join(
    os.path.expanduser("~"), "AppData", "Local", "Programs",
    "Antigravity", "resources", "bin", "language_server.exe"
)
AGENTAPI_CONVERSATION = _cfg.get("conversation_id", "")

def check_and_reload_config():
    global _cfg, AGENTAPI_ENV, AGENTAPI_CONVERSATION, _last_config_mtime
    try:
        if not os.path.exists(VOICE_BRIDGE_CONFIG_PATH):
            return False
        mtime = os.path.getmtime(VOICE_BRIDGE_CONFIG_PATH)
        if mtime > _last_config_mtime:
            _last_config_mtime = mtime
            with open(VOICE_BRIDGE_CONFIG_PATH, 'r') as f:
                new_cfg = json.load(f)
            
            changed = (
                _cfg.get("conversation_id") != new_cfg.get("conversation_id") or
                _cfg.get("ls_address") != new_cfg.get("ls_address") or
                _cfg.get("csrf_token") != new_cfg.get("csrf_token")
            )
            if changed:
                _cfg = new_cfg
                AGENTAPI_ENV["ANTIGRAVITY_LS_ADDRESS"] = _cfg.get("ls_address", "localhost:51790")
                AGENTAPI_ENV["ANTIGRAVITY_CSRF_TOKEN"] = _cfg.get("csrf_token", "")
                AGENTAPI_ENV["ANTIGRAVITY_PROJECT_ID"] = _cfg.get("project_id", "")
                AGENTAPI_CONVERSATION = _cfg.get("conversation_id", "")
                print(f"\n[Config] Config changed! Reloaded. Conversation: {AGENTAPI_CONVERSATION[:12]}...")
                return True
    except Exception as e:
        print(f"Error checking config: {e}")
    return False

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
            capture_output=True, text=True, timeout=10, env=env
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
    """Send a message directly into the Antigravity agent's conversation via agentapi."""
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
You are a Text-to-Speech reader.
When you receive a message starting with "AGENT_OUTBOX:", speak the text following that prefix exactly, word-for-word.
Do NOT say "AGENT_OUTBOX:". Do NOT say "I don't know". Do NOT add any introduction, explanations, or remarks.
Speak the provided message verbatim.
"""


# ──────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────
PTT_KEY = kb.Key.f8
SAMPLE_RATE = 16000
OUTPUT_RATE = 24000
CHANNELS = 1
BLOCK_SIZE = 4000

INPUT_DEVICE = 1  # Logitech PRO X Gaming Headset Mic
OUTPUT_DEVICE = 4  # EP-HDMI-RX (NVIDIA High Definition Audio)

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
        self.f8_held = False
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
# F8 Push-to-Talk Listener
# ──────────────────────────────────────────────────────────
def on_key_press(key):
    if key == PTT_KEY:
        bridge.f8_held = True
        # Clear playback queue on interruption to stop speech immediately
        while not bridge.audio_out_queue.empty():
            try:
                bridge.audio_out_queue.get_nowait()
            except queue.Empty:
                break
        if bridge.activate("ptt"):
            print("\n[MIC] [F8 HELD] Listening... (release to stop)")

def on_key_release(key):
    if key == PTT_KEY:
        bridge.f8_held = False
        if bridge.is_listening and bridge.trigger == "ptt":
            print("\n[MIC] [F8 RELEASE] Processing...")
            with bridge.lock:
                bridge.speech_ended = True
                bridge.speech_ended_time = time.time()

hotkey_listener = kb.Listener(on_press=on_key_press, on_release=on_key_release)
hotkey_listener.daemon = True
hotkey_listener.start()
print("Push-to-talk ready on F8.")

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
        last_size = os.path.getsize(VOICE_OUTBOX_PATH)
        
        # Speak recent messages on startup
        try:
            mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
            if time.time() - mtime < 15.0:
                with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8') as f:
                    lines = [l.strip() for l in f.readlines() if l.strip()]
                    if lines:
                        recent_line = lines[-1]
                        bridge.outbox_queue.put(recent_line)
                        if bridge.activate("outbox"):
                            print(f"\n[*] Recent startup outbox message queued: {recent_line[:60]}...")
        except Exception as e:
            pass

        while not bridge.should_quit:
            time.sleep(2)
            if not os.path.exists(VOICE_OUTBOX_PATH):
                continue
            current_size = os.path.getsize(VOICE_OUTBOX_PATH)
            if current_size <= last_size:
                continue
            try:
                with open(VOICE_OUTBOX_PATH, 'r', encoding='utf-8') as f:
                    f.seek(last_size)
                    new_content = f.read()
                last_size = current_size
            except Exception as e:
                print(f"[OUTBOX READ ERROR] {e}")
                continue
            
            for line in new_content.strip().split('\n'):
                line = line.strip()
                if line:
                    bridge.outbox_queue.put(line)
                    # Loop/wait if it's currently disconnecting, to ensure we wake up clean
                    while True:
                        with bridge.lock:
                            current_state = bridge.state
                        if current_state == STATE_DISCONNECTING:
                            time.sleep(0.1)
                            continue
                        break
                    
                    if bridge.activate("outbox"):
                        print(f"\n[*] Outbox message triggered wake up!")

    outbox_thread = threading.Thread(target=outbox_monitor_worker, daemon=True)
    outbox_thread.start()

    print("\n" + "=" * 55)
    print("  KEYSTONE VOICE BRIDGE — ONLINE")
    print("=" * 55)
    print(f"  Hold F8 to talk (Push-to-Talk)")
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

                            # Audio response - ONLY play audio when in outbox mode (strict TTS read)
                            inline_data = part.get("inlineData") or part.get("inline_data")
                            if inline_data and bridge.trigger == "outbox":
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
                            if not bridge.f8_held:
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
                                    "turns": [{"role": "user", "parts": [{"text": f"Please read the following text verbatim out loud now. Do not add any comment, do not reply to it, just read it word-for-word: \"{line}\""}]}],
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
                            print("[*] Config change detected during active session. Reconnecting...")
                            bridge.deactivate()
                            break
                        
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

            print("\n[-] Disconnected. Waiting for wake word, F8, or incoming message...\n")

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
def main():
    print("\nStarting Keystone Voice Bridge...\n")
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
