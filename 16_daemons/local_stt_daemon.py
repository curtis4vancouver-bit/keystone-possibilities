"""
Daemon A: Local CUDA STT Daemon (Faster-Whisper on NVIDIA RTX 5060 Ti)
=========================================================================
Captures microphone audio via sounddevice, detects speech with Silero VAD,
transcribes with Faster-Whisper large-v3-turbo on CUDA FP16, and writes
the result to last_user_prompt.txt for Antigravity agent ingestion.

F9 = Global Push-to-Talk (system-wide, works from any app)
F8 = Emergency Stop

Architecture:
  [Logitech Mic] -> [Silero VAD] -> [Faster-Whisper CUDA FP16] -> [last_user_prompt.txt] -> [Antigravity]
"""

import sys
import os
import time
import json
import socket
import threading
import queue
import struct
import tempfile
import urllib.request
import urllib.error
import subprocess
import re

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import numpy as np
import sounddevice as sd
import keyboard  # Global hotkey listener (works system-wide)

from http.server import HTTPServer, BaseHTTPRequestHandler

# ── Paths ────────────────────────────────────────────────────────────────
LAST_USER_PROMPT_PATH = r"C:\Users\Curtis\.gemini\antigravity\last_user_prompt.txt"
VOICE_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_voice.txt"
SPEAKER_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_speaker.txt"
MIC_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_mic.txt"
DAEMON_LOG_DIR = r"C:\Users\Curtis\.gemini\antigravity\daemon_logs"
VOICE_LOG_PATH = os.path.join(DAEMON_LOG_DIR, "incoming_user_voice.json")
LAST_DISPATCH_META_PATH = r"C:\Users\Curtis\.gemini\antigravity\last_dispatch_meta.json"
PORT_9876 = 9876

CURRENT_BOUND_CHAT_ID = ""
CURRENT_BOUND_CHAT_NAME = ""

def get_current_bound_chat_id():
    global CURRENT_BOUND_CHAT_ID
    for af in [r"C:\Users\Curtis\.gemini\antigravity\active_conversation_id.txt", r"C:\Users\Curtis\Desktop\Keystone Brain\active_conversation_id.txt"]:
        if os.path.exists(af):
            try:
                with open(af, "r", encoding="utf-8") as _cf:
                    cid = _cf.read().strip()
                    if cid and len(cid) == 36:
                        CURRENT_BOUND_CHAT_ID = cid
                        return cid
            except Exception:
                pass
    return CURRENT_BOUND_CHAT_ID

get_current_bound_chat_id()

_last_cpu_pct = 15.0
_cached_gpu_stats = {
    "gpu_name": "NVIDIA GPU",
    "vram_used_gb": 0.0,
    "vram_total_gb": 16.0,
    "vram_percent": 0.0,
    "gpu_util_percent": 0.0
}

def _cpu_monitor_loop():
    global _last_cpu_pct
    try:
        import psutil
        # Primer call for psutil.cpu_percent
        psutil.cpu_percent(interval=None)
        while True:
            val = psutil.cpu_percent(interval=0.5)
            # Exponential Moving Average (EMA) smoothing for stable 100% accurate CPU telemetry
            _last_cpu_pct = round(_last_cpu_pct * 0.65 + val * 0.35, 1)
            time.sleep(0.2)
    except Exception:
        pass

threading.Thread(target=_cpu_monitor_loop, daemon=True).start()

def _gpu_monitor_loop():
    global _cached_gpu_stats
    import ctypes

    # Fast path: In-process NVML via ctypes (zero subprocess overhead, zero context-switch churn)
    nvml = None
    nvml_handle = None
    try:
        if sys.platform == "win32":
            nvml = ctypes.CDLL("nvml.dll")
        else:
            nvml = ctypes.CDLL("libnvidia-ml.so.1")
        if nvml:
            nvml.nvmlInit_v2()
            handle = ctypes.c_void_p()
            ret = nvml.nvmlDeviceGetHandleByIndex_v2(0, ctypes.byref(handle))
            if ret == 0:
                nvml_handle = handle
    except Exception:
        nvml = None
        nvml_handle = None

    class nvmlMemory_t(ctypes.Structure):
        _fields_ = [("total", ctypes.c_ulonglong), ("free", ctypes.c_ulonglong), ("used", ctypes.c_ulonglong)]

    class nvmlUtilization_t(ctypes.Structure):
        _fields_ = [("gpu", ctypes.c_uint), ("memory", ctypes.c_uint)]

    cached_gpu_name = None
    if nvml and nvml_handle:
        try:
            name_buf = ctypes.create_string_buffer(64)
            if nvml.nvmlDeviceGetName(nvml_handle, name_buf, 64) == 0:
                cached_gpu_name = name_buf.value.decode("utf-8", errors="replace")
        except Exception:
            cached_gpu_name = "NVIDIA GeForce RTX 5060 Ti"

    while True:
        updated = False
        if nvml and nvml_handle:
            try:
                mem = nvmlMemory_t()
                util = nvmlUtilization_t()
                r1 = nvml.nvmlDeviceGetMemoryInfo(nvml_handle, ctypes.byref(mem))
                r2 = nvml.nvmlDeviceGetUtilizationRates(nvml_handle, ctypes.byref(util))
                if r1 == 0 and r2 == 0:
                    vram_total_gb = round(mem.total / (1024.0 ** 3), 1)
                    vram_used_gb = round(mem.used / (1024.0 ** 3), 1)
                    vram_pct = round((mem.used / max(1, mem.total)) * 100.0, 1)
                    _cached_gpu_stats = {
                        "gpu_name": cached_gpu_name or "NVIDIA GPU",
                        "vram_used_gb": vram_used_gb,
                        "vram_total_gb": vram_total_gb,
                        "vram_percent": vram_pct,
                        "gpu_util_percent": float(util.gpu)
                    }
                    updated = True
            except Exception:
                pass

        # Throttled subprocess fallback (15s) only if NVML in-process is unavailable
        if not updated:
            try:
                import subprocess
                flags = 0x08000000 if sys.platform == "win32" else 0
                out = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,utilization.gpu", "--format=csv,noheader,nounits"],
                    stderr=subprocess.STDOUT,
                    timeout=2,
                    creationflags=flags
                ).decode("utf-8").strip()
                if out:
                    parts = [p.strip() for p in out.split(",")]
                    if len(parts) >= 4:
                        gpu_name = parts[0]
                        total_mb = float(parts[1])
                        used_mb = float(parts[2])
                        gpu_util_pct = float(parts[3])
                        vram_total_gb = round(total_mb / 1024.0, 1)
                        vram_used_gb = round(used_mb / 1024.0, 1)
                        vram_pct = round((used_mb / total_mb) * 100.0, 1)
                        _cached_gpu_stats = {
                            "gpu_name": gpu_name,
                            "vram_used_gb": vram_used_gb,
                            "vram_total_gb": vram_total_gb,
                            "vram_percent": vram_pct,
                            "gpu_util_percent": gpu_util_pct
                        }
            except Exception:
                pass
            time.sleep(15.0)
        else:
            time.sleep(2.0)

threading.Thread(target=_gpu_monitor_loop, daemon=True).start()

def get_realtime_hardware_stats():
    global _last_cpu_pct, _cached_gpu_stats
    cpu_pct = _last_cpu_pct
    ram_used_gb = 0.0
    ram_total_gb = 32.0
    ram_pct = 0.0

    try:
        import psutil
        mem = psutil.virtual_memory()
        ram_used_gb = round(mem.used / (1024**3), 1)
        ram_total_gb = round(mem.total / (1024**3), 1)
        ram_pct = round(mem.percent, 1)
    except Exception:
        pass

    # Native Win32 Kernel Fallback for 100% reliable Windows System RAM measurement
    if ram_used_gb == 0.0 and sys.platform == "win32":
        try:
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem)):
                ram_total_gb = round(mem.ullTotalPhys / (1024**3), 1)
                ram_used_gb = round((mem.ullTotalPhys - mem.ullAvailPhys) / (1024**3), 1)
                ram_pct = round((ram_used_gb / ram_total_gb) * 100.0, 1)
        except Exception:
            pass

    return {
        "cpu_percent": cpu_pct,
        "ram_used_gb": ram_used_gb,
        "ram_total_gb": ram_total_gb,
        "ram_percent": ram_pct,
        **_cached_gpu_stats,
        "timestamp": time.time()
    }

STATE_FILE_PATH = r"C:\Users\Curtis\.gemini\antigravity\voice_bridge_state.json"

def set_bridge_state(state_name: str, badge_label: str = None):
    if badge_label is None:
        badge_label = state_name.upper()
    data = {
        "state": state_name.lower(),
        "badge": badge_label,
        "timestamp": time.time()
    }
    try:
        os.makedirs(os.path.dirname(STATE_FILE_PATH), exist_ok=True)
        with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass
    print(f"⚡ [Bridge State Updated] -> {state_name} ({badge_label})")
    broadcast_ws({"type": "state", "state": state_name.lower(), "badge": badge_label, "timestamp": data["timestamp"]})

def get_bridge_state():
    try:
        if os.path.exists(STATE_FILE_PATH):
            with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {"state": "connected", "badge": "CONNECTED", "timestamp": time.time()}

# ── Audio Device Management & Dynamic WASAPI Enumeration ─────────────────
def get_current_speaker_setting():
    try:
        if os.path.exists(SPEAKER_CONFIG_PATH):
            with open(SPEAKER_CONFIG_PATH, "r", encoding="utf-8") as f:
                val = f.read().strip()
                if val:
                    return val
    except Exception:
        pass
    return "default"

def get_current_mic_setting():
    try:
        if os.path.exists(MIC_CONFIG_PATH):
            with open(MIC_CONFIG_PATH, "r", encoding="utf-8") as f:
                val = f.read().strip()
                if val:
                    return val
    except Exception:
        pass
    return "Microphone (Logitech PRO X Gaming Headset)"

def _is_device_active(name, selected):
    if not selected:
        return False
    if selected.lower() in ["default", "system default", "system default (auto-switch)"]:
        return name.lower() in ["default", "system default (auto-switch)"]
    n_lower = name.lower()
    s_lower = selected.lower()
    if n_lower == s_lower or s_lower in n_lower or n_lower in s_lower:
        return True
    words = [w for w in s_lower.split() if len(w) > 3]
    if words and all(w in n_lower for w in words):
        return True
    return False

def get_os_audio_devices():
    """Query sounddevice for active input and output devices filtered by Windows WASAPI host API."""
    try:
        devices = sd.query_devices()
        hostapis = sd.query_hostapis()
    except Exception as e:
        print(f"⚠️ [Audio Devices Error]: {e}")
        return {
            "input_devices": [],
            "output_devices": [],
            "active_input": get_current_mic_setting(),
            "active_output": get_current_speaker_setting(),
            "selected_speaker": get_current_speaker_setting(),
            "selected_mic": get_current_mic_setting(),
            "timestamp": time.time()
        }
    
    wasapi_index = None
    for idx, api in enumerate(hostapis):
        if "wasapi" in api.get("name", "").lower():
            wasapi_index = idx
            break

    selected_mic = get_current_mic_setting()
    selected_speaker = get_current_speaker_setting()
    is_default_spk = selected_speaker.lower() in ["default", "system default", "system default (auto-switch)"]

    input_devices = []
    output_devices = [
        {
            "id": "default",
            "name": "System Default (Auto-Switch)",
            "index": None,
            "channels": 2,
            "sample_rate": 48000,
            "is_active": is_default_spk
        }
    ]

    for idx, d in enumerate(devices):
        if wasapi_index is not None and d.get("hostapi") != wasapi_index:
            continue

        name = d.get("name", "").strip()
        if not name:
            continue

        if d.get("max_input_channels", 0) > 0:
            input_devices.append({
                "id": name,
                "name": name,
                "index": idx,
                "channels": d.get("max_input_channels"),
                "sample_rate": int(d.get("default_samplerate", 48000)),
                "is_active": _is_device_active(name, selected_mic)
            })

        if d.get("max_output_channels", 0) > 0:
            output_devices.append({
                "id": name,
                "name": name,
                "index": idx,
                "channels": d.get("max_output_channels"),
                "sample_rate": int(d.get("default_samplerate", 44100)),
                "is_active": _is_device_active(name, selected_speaker)
            })

    return {
        "input_devices": input_devices,
        "output_devices": output_devices,
        "active_input": selected_mic,
        "active_output": selected_speaker,
        "selected_mic": selected_mic,
        "selected_speaker": selected_speaker,
        "timestamp": time.time()
    }

def resolve_output_device_index(target_name):
    """Exact WASAPI output device index resolver."""
    if not target_name or target_name.strip().lower() in ["default", "system default", "system default (auto-switch)"]:
        return None
    try:
        devices = sd.query_devices()
        hostapis = sd.query_hostapis()
        target_clean = target_name.strip().lower()
        wasapi_idx = next((i for i, h in enumerate(hostapis) if "wasapi" in h.get("name", "").lower()), None)

        if wasapi_idx is not None:
            # Pass 1: Exact WASAPI match
            for idx, d in enumerate(devices):
                if d.get("hostapi") == wasapi_idx and d.get("max_output_channels", 0) > 0:
                    if d.get("name", "").strip().lower() == target_clean:
                        return idx

            # Pass 2: Substring WASAPI match
            for idx, d in enumerate(devices):
                if d.get("hostapi") == wasapi_idx and d.get("max_output_channels", 0) > 0:
                    if target_clean in d.get("name", "").strip().lower() or d.get("name", "").strip().lower() in target_clean:
                        return idx

        # Pass 3: Fallback match across all APIs
        for idx, d in enumerate(devices):
            if d.get("max_output_channels", 0) > 0:
                if target_clean in d.get("name", "").strip().lower():
                    return idx
    except Exception as e:
        print(f"⚠️ [Output Device Resolver Error]: {e}")
    return None

def play_confirmation_chime(device_name):
    """Play 1-second 440Hz -> 880Hz sine confirmation chime on target output device."""
    try:
        device_idx = resolve_output_device_index(device_name)
        sr = 44100
        t1 = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
        t2 = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
        vol_path = r"C:\Users\Curtis\.gemini\antigravity\selected_volume.txt"
        vol = 80
        if os.path.exists(vol_path):
            try:
                with open(vol_path, "r", encoding="utf-8") as vf:
                    vol = int(vf.read().strip())
            except Exception:
                vol = 80
        gain = (max(0, min(100, vol)) / 100.0) * 0.25
        tone1 = gain * np.sin(2 * np.pi * 440 * t1)
        tone2 = gain * np.sin(2 * np.pi * 880 * t2)
        chime = np.concatenate([tone1, tone2]).astype(np.float32)

        with sd.OutputStream(device=device_idx, samplerate=sr, channels=1, dtype='float32') as stream:
            stream.write(chime)
        print(f"🔔 [Audio Chime] 1s confirmation chime played on '{device_name}' (device {device_idx})")
        return True
    except Exception as e:
        print(f"⚠️ [Audio Chime Error]: {e}")
        return False

# ── WebSocket Push Broadcast Engine ──────────────────────────────────────
_ws_clients = set()
_ws_clients_lock = threading.Lock()

def broadcast_ws(payload: dict):
    """Push real-time JSON payload to all connected WebSocket clients on ws://127.0.0.1:9876/ws."""
    with _ws_clients_lock:
        if not _ws_clients:
            return
        msg_str = json.dumps(payload)
        dead = []
        for client in list(_ws_clients):
            try:
                client.send(msg_str)
            except Exception:
                dead.append(client)
        for d in dead:
            _ws_clients.discard(d)

def handle_ws_client(client_sock):
    """Handle threaded Push WebSocket connection (ws://127.0.0.1:9876/ws)."""
    ws = None
    try:
        client_sock.settimeout(None)
        from websockets.sync.server import ServerConnection
        from websockets.server import ServerProtocol
        proto = ServerProtocol()
        ws = ServerConnection(client_sock, proto)
        ws.handshake()
        
        with _ws_clients_lock:
            _ws_clients.add(ws)
        
        print("🌐 [WS Client Handshake] New WS client connected")
        # Immediate Push of state, hardware telemetry & OS audio devices upon client connect
        st = get_bridge_state()
        stats = get_realtime_hardware_stats()
        devices = get_os_audio_devices()
        try:
            ws.send(json.dumps({"type": "state", "state": st.get("state", "connected"), "badge": st.get("badge", "CONNECTED")}))
            ws.send(json.dumps({"type": "stats", "data": stats}))
            ws.send(json.dumps({"type": "devices", "data": devices, **devices}))
            vol, is_muted = get_windows_master_volume()
            ws.send(json.dumps({"type": "volume", "volume": vol, "muted": is_muted}))
        except Exception:
            pass

        # Keep connection alive & listen for client frames
        for _ in ws:
            pass
    except Exception as ws_err:
        import traceback
        traceback.print_exc()
    finally:
        with _ws_clients_lock:
            if ws in _ws_clients:
                _ws_clients.discard(ws)
        try: client_sock.close()
        except Exception: pass

def _ws_stats_broadcast_loop():
    while True:
        try:
            time.sleep(1.0)
            if _ws_clients:
                stats = get_realtime_hardware_stats()
                broadcast_ws({"type": "stats", "data": stats})
        except Exception:
            pass

threading.Thread(target=_ws_stats_broadcast_loop, daemon=True).start()

# ── Real-Time Windows System Master Volume Engine (pycaw CoreAudio) ─────────
_last_broadcast_volume = None
_last_broadcast_mute = None

def get_default_audio_device():
    """Retrieve the active Windows default audio render device (checking both eConsole and eMultimedia)."""
    try:
        import comtypes
        comtypes.CoInitialize()
        from pycaw.pycaw import AudioUtilities
        from pycaw.constants import EDataFlow, ERole
        enum = AudioUtilities.GetDeviceEnumerator()
        if enum:
            # Check eConsole first (system master/keyboard volume), then eMultimedia
            for role in (ERole.eConsole.value, ERole.eMultimedia.value):
                try:
                    dev_ptr = enum.GetDefaultAudioEndpoint(EDataFlow.eRender.value, role)
                    if dev_ptr:
                        dev = AudioUtilities.CreateDevice(dev_ptr)
                        if dev and dev.EndpointVolume:
                            return dev
                except Exception:
                    continue
        return AudioUtilities.GetSpeakers()
    except Exception:
        return None

def get_windows_master_volume():
    """Read actual Windows default endpoint master volume (0-100) and mute state via pycaw."""
    try:
        dev = get_default_audio_device()
        if dev and dev.EndpointVolume:
            scalar = dev.EndpointVolume.GetMasterVolumeLevelScalar()
            muted = bool(dev.EndpointVolume.GetMute())
            vol = round(scalar * 100)
            return max(0, min(100, vol)), muted
    except Exception:
        pass
    vol_path = r"C:\Users\Curtis\.gemini\antigravity\selected_volume.txt"
    vol = 80
    if os.path.exists(vol_path):
        try:
            with open(vol_path, "r", encoding="utf-8") as vf:
                vol = int(vf.read().strip())
        except Exception:
            pass
    return max(0, min(100, vol)), False

def set_windows_master_volume(vol, muted=None):
    """Set actual Windows default endpoint master volume scalar (0-100) and mute state."""
    vol = max(0, min(100, int(vol)))
    try:
        dev = get_default_audio_device()
        if dev and dev.EndpointVolume:
            ep = dev.EndpointVolume
            ep.SetMasterVolumeLevelScalar(vol / 100.0, None)
            if muted is not None:
                ep.SetMute(1 if muted else 0, None)
            elif vol > 0 and ep.GetMute():
                ep.SetMute(0, None)
    except Exception:
        pass
    vol_path = r"C:\Users\Curtis\.gemini\antigravity\selected_volume.txt"
    try:
        os.makedirs(os.path.dirname(vol_path), exist_ok=True)
        with open(vol_path + ".tmp", "w", encoding="utf-8") as vf:
            vf.write(str(vol))
        os.replace(vol_path + ".tmp", vol_path)
    except Exception:
        pass
    return vol

def _ws_volume_monitor_loop():
    """Lightweight background poller that detects keyboard/OS volume changes and device switching."""
    global _last_broadcast_volume, _last_broadcast_mute
    try:
        import comtypes
        comtypes.CoInitialize()
    except Exception:
        pass
    current_dev_id = None
    ep = None
    ticks = 0
    while True:
        try:
            time.sleep(0.08)  # Fast 80ms poll for instant keyboard response
            ticks += 1
            # Re-verify default device every 5 ticks (~400ms) or if ep is None to catch device swaps
            if ep is None or ticks >= 5:
                ticks = 0
                dev = get_default_audio_device()
                if dev:
                    new_id = getattr(dev, "id", None)
                    if new_id != current_dev_id or ep is None:
                        current_dev_id = new_id
                        ep = dev.EndpointVolume
                        # Device changed: broadcast new device info and volume
                        speaker_name = getattr(dev, "FriendlyName", "System Default")
                        try:
                            s = ep.GetMasterVolumeLevelScalar()
                            m = bool(ep.GetMute())
                            v = round(s * 100)
                            _last_broadcast_volume = v
                            _last_broadcast_mute = m
                            broadcast_ws({
                                "type": "speaker_changed",
                                "active_speaker": speaker_name,
                                "volume": v,
                                "muted": m
                            })
                        except Exception:
                            pass
            if ep:
                try:
                    scalar = ep.GetMasterVolumeLevelScalar()
                    mute = bool(ep.GetMute())
                    vol = round(scalar * 100)
                except Exception:
                    ep = None
                    current_dev_id = None
                    continue

                if vol != _last_broadcast_volume or mute != _last_broadcast_mute:
                    _last_broadcast_volume = vol
                    _last_broadcast_mute = mute
                    vol_path = r"C:\Users\Curtis\.gemini\antigravity\selected_volume.txt"
                    try:
                        os.makedirs(os.path.dirname(vol_path), exist_ok=True)
                        with open(vol_path + ".tmp", "w", encoding="utf-8") as vf:
                            vf.write(str(vol))
                        os.replace(vol_path + ".tmp", vol_path)
                    except Exception:
                        pass
                    broadcast_ws({
                        "type": "volume",
                        "volume": vol,
                        "muted": mute
                    })
        except Exception:
            time.sleep(0.2)

threading.Thread(target=_ws_volume_monitor_loop, daemon=True).start()

_last_chats_sync_time = 0
_cached_active_chats = []

def get_synced_active_chats(force_refresh=False):
    global _last_chats_sync_time, _cached_active_chats
    now = time.time()
    if force_refresh or (now - _last_chats_sync_time > 3.0) or not _cached_active_chats:
        try:
            import importlib
            import sync_active_chats
            importlib.reload(sync_active_chats)
            chats = sync_active_chats.sync_active_chats()
            if chats:
                _cached_active_chats = chats
                _last_chats_sync_time = now
                return _cached_active_chats
        except Exception as e:
            print(f"⚠️ [Sync Active Chats Error]: {e}")
    chats_file = r"C:\Users\Curtis\.gemini\antigravity\active_chats.json"
    if os.path.exists(chats_file):
        try:
            with open(chats_file, "r", encoding="utf-8") as f:
                _cached_active_chats = json.load(f)
        except Exception:
            pass
    return _cached_active_chats

class ChromePromptHTTPHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path in ["/api/status", "/health"]:
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"daemon": "Daemon A (Local STT)", "port": PORT_9876, "status": "ONLINE", "active_chat": CURRENT_BOUND_CHAT_ID}).encode("utf-8"))
        elif self.path in ["/api/stats", "/api/hardware"]:
            stats = get_realtime_hardware_stats()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(stats).encode("utf-8"))
        elif self.path in ["/api/state", "/api/voice/state"]:
            st = get_bridge_state()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(st).encode("utf-8"))
        elif self.path in ["/api/audio/devices", "/api/devices"]:
            devices_data = get_os_audio_devices()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(devices_data).encode("utf-8"))
        elif self.path.startswith("/api/chats") or self.path in ["/api/chat_targets", "/api/active-chats"]:
            targets_file = r"C:\Users\Curtis\.gemini\antigravity\chat_targets.json"
            active_file = r"C:\Users\Curtis\.gemini\antigravity\active_conversation_id.txt"
            targets = {}
            active_id = CURRENT_BOUND_CHAT_ID or ""
            if os.path.exists(active_file):
                try:
                    with open(active_file, "r", encoding="utf-8") as f:
                        active_id = f.read().strip()
                except Exception: pass
            if not active_id and CURRENT_BOUND_CHAT_ID:
                active_id = CURRENT_BOUND_CHAT_ID

            force = "refresh=1" in self.path
            active_chats = get_synced_active_chats(force_refresh=force)
            if active_id and active_chats:
                for ac in active_chats:
                    ac["is_active"] = (ac.get("id") == active_id)

            if os.path.exists(targets_file):
                try:
                    with open(targets_file, "r", encoding="utf-8") as f:
                        targets = json.load(f)
                except Exception: pass

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "targets": targets, "active_conversation_id": active_id, "active_chats": active_chats}).encode("utf-8"))
        elif self.path in ["/api/volume", "/api/audio/volume"]:
            vol, is_muted = get_windows_master_volume()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "volume": vol, "muted": is_muted}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global CURRENT_BOUND_CHAT_ID, CURRENT_BOUND_CHAT_NAME, is_f9_down, _cached_active_chats
        if self.path == "/api/shutdown":
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "SHUTTING_DOWN"}')
            print("🛑 [Local STT Daemon] Graceful shutdown signal received. Terminating.")
            threading.Thread(target=lambda: (time.sleep(0.1), os._exit(0)), daemon=True).start()
            return
        elif self.path in ["/api/set-target", "/api/set_target", "/api/chats/bind", "/api/chat_targets/bind", "/api/active-chat", "/api/select-chat"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            chat_name = (data.get("chat_name") or data.get("name") or data.get("title") or data.get("domain") or "").strip()
            conv_id = (data.get("conversation_id") or data.get("conversationId") or data.get("id") or data.get("target_id") or "").strip()
            active_file = r"C:\Users\Curtis\.gemini\antigravity\active_conversation_id.txt"
            targets_file = r"C:\Users\Curtis\.gemini\antigravity\chat_targets.json"
            chats_file = r"C:\Users\Curtis\.gemini\antigravity\active_chats.json"

            if (not conv_id or len(conv_id) != 36) and chat_name and os.path.exists(targets_file):
                try:
                    with open(targets_file, "r", encoding="utf-8") as f:
                        tar_lookup = json.load(f)
                    matched = tar_lookup.get(chat_name) or tar_lookup.get(chat_name.lower()) or tar_lookup.get(chat_name.lstrip("#")) or tar_lookup.get(re.sub(r"^\[#\d+\]\s*", "", chat_name).strip().lower())
                    if matched and len(matched) == 36:
                        conv_id = matched
                except Exception: pass

            if not conv_id and os.path.exists(active_file):
                try:
                    with open(active_file, "r", encoding="utf-8") as f:
                        conv_id = f.read().strip()
                except Exception: pass

            if conv_id and len(conv_id) == 36:
                CURRENT_BOUND_CHAT_ID = conv_id
                for af in [active_file, r"C:\Users\Curtis\Desktop\Keystone Brain\active_conversation_id.txt"]:
                    try:
                        os.makedirs(os.path.dirname(af), exist_ok=True)
                        tmp_act = af + ".tmp"
                        with open(tmp_act, "w", encoding="utf-8") as f:
                            f.write(conv_id)
                            f.flush()
                            os.fsync(f.fileno())
                        os.replace(tmp_act, af)
                    except Exception as e:
                        print(f"⚠️ [Local STT] Error updating {af}: {e}")

            if chat_name:
                CURRENT_BOUND_CHAT_NAME = chat_name

            targets = {}
            if os.path.exists(targets_file):
                try:
                    with open(targets_file, "r", encoding="utf-8") as f:
                        targets = json.load(f)
                except Exception: pass

            if conv_id:
                targets["default"] = conv_id
                if chat_name:
                    targets[chat_name] = conv_id
                    targets[chat_name.lower()] = conv_id
                    clean_name = re.sub(r"^\[#\d+\]\s*", "", chat_name).strip().lower()
                    if clean_name:
                        targets[clean_name] = conv_id
                try:
                    tmp_tar = targets_file + ".tmp"
                    with open(tmp_tar, "w", encoding="utf-8") as f:
                        json.dump(targets, f, indent=2)
                        f.flush()
                        os.fsync(f.fileno())
                    os.replace(tmp_tar, targets_file)
                    print(f"🎯 [Local STT] Target Chat Bound: '{chat_name or conv_id}' -> '{conv_id}'")
                except Exception as e:
                    print(f"❌ [Local STT Targets Error]: {e}")

            if os.path.exists(chats_file) and conv_id:
                try:
                    with open(chats_file, "r", encoding="utf-8") as f:
                        achats = json.load(f)
                    for ac in achats:
                        ac["is_active"] = (ac.get("id") == conv_id)
                    tmp_ch = chats_file + ".tmp"
                    with open(tmp_ch, "w", encoding="utf-8") as f:
                        json.dump(achats, f, indent=2)
                        f.flush()
                        os.fsync(f.fileno())
                    os.replace(tmp_ch, chats_file)
                    _cached_active_chats = achats
                except Exception as e:
                    print(f"⚠️ [Local STT Active Chats Update Error]: {e}")

            broadcast_ws({
                "type": "active_chat_updated",
                "active_conversation_id": conv_id,
                "conversation_id": conv_id,
                "title": chat_name,
                "name": chat_name
            })

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "SUCCESS",
                "chat_name": chat_name,
                "conversation_id": conv_id,
                "active_conversation_id": conv_id,
                "targets": targets
            }).encode("utf-8"))
        elif self.path in ["/api/audio/select", "/api/audio/speaker", "/api/select_device"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            device_name = (data.get("speaker") or data.get("device_name") or "").strip()
            device_type = data.get("type", "speaker").lower()

            target_path = SPEAKER_CONFIG_PATH if device_type == "speaker" else MIC_CONFIG_PATH

            # Atomic write to config file
            try:
                os.path.exists(target_path)
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                tmp_path = target_path + ".tmp"
                with open(tmp_path, "w", encoding="utf-8") as f:
                    f.write(device_name)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, target_path)
                print(f"🔊 [Audio Config] Updated {os.path.basename(target_path)} -> '{device_name}'")
            except Exception as e:
                print(f"❌ [Audio Config Write Error]: {e}")

            # Trigger stream re-initialization (mic) or chime (speaker)
            if device_type == "mic":
                if "stream_manager" in globals() and stream_manager:
                    stream_manager.start_or_switch(device_name)
            elif device_type == "speaker":
                threading.Thread(target=play_confirmation_chime, args=(device_name,), daemon=True).start()

            # Broadcast WebSocket updates to all connected clients
            updated_devices = get_os_audio_devices()
            broadcast_ws({"type": "devices_updated", "data": updated_devices, **updated_devices})
            broadcast_ws({"type": "devices", "data": updated_devices, **updated_devices})

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "type": device_type, "selected": device_name}).encode("utf-8"))
        elif self.path in ["/api/state", "/api/voice/state"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            new_state = data.get("state", "connected")
            new_badge = data.get("badge", new_state.upper())
            set_bridge_state(new_state, new_badge)
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "UPDATED", "state": new_state}).encode("utf-8"))
        elif self.path in ["/api/record/start", "/api/start"]:
            print("🌐 [Chrome HTTP -> Daemon A] F9 KeyDown trigger -> Starting recording")
            stop_active_tts_speech()
            set_bridge_state("listening", "LISTENING")
            start_recording()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "RECORDING"}).encode("utf-8"))
        elif self.path in ["/api/record/stop", "/api/stop_rec"]:
            global is_f9_down
            is_f9_down = False
            print("🌐 [Chrome HTTP -> Daemon A] F9 KeyUp trigger -> Stopping recording & transcribing")
            set_bridge_state("transmitting", "TRANSMITTING")
            threading.Thread(target=stop_recording_and_transcribe, daemon=True).start()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "TRANSCRIBING"}).encode("utf-8"))
        elif self.path in ["/api/volume", "/api/audio/volume"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            vol_val = data.get("volume", data.get("level"))
            is_muted = data.get("muted")
            if vol_val is not None:
                vol = max(0, min(100, int(vol_val)))
                set_windows_master_volume(vol, muted=is_muted)
            else:
                vol, current_mute = get_windows_master_volume()
                if is_muted is not None:
                    set_windows_master_volume(vol, muted=is_muted)
            global _last_broadcast_volume, _last_broadcast_mute
            _last_broadcast_volume = vol
            _last_broadcast_mute = bool(is_muted) if is_muted is not None else False
            broadcast_ws({"type": "volume", "volume": vol, "muted": bool(is_muted)})
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "volume": vol, "muted": bool(is_muted)}).encode("utf-8"))
        elif self.path in ["/api/prompt", "/api/config"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            is_mock = data.get("mock", False) or data.get("dry_run", False) or data.get("test", False)
            prompt_text = data.get("prompt", "")
            target_chat_name = data.get("target_chat_name") or data.get("chat_name") or data.get("domain") or ""
            target_conv_id = data.get("conversation_id") or data.get("conversationId") or ""
            
            if is_mock:
                print(f"🧪 [Chrome HTTP -> Daemon A] Mock prompt acknowledged (skipping Antigravity live dispatch): '{prompt_text[:80]}...'")
                set_bridge_state("working", "WORKING")
                self.send_response(200)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "MOCK_SUCCESS", "prompt": prompt_text}).encode("utf-8"))
                return

            if prompt_text:
                if not target_conv_id:
                    target_conv_id = get_current_bound_chat_id()
                print(f"🌐 [Chrome HTTP -> Daemon A] Received prompt (Target: {target_conv_id or target_chat_name or 'default'}): '{prompt_text[:80]}...'")
                
                # Auto-update selected_voice.txt / selected_speaker.txt if SYSTEM message
                if "Change voice output to " in prompt_text:
                    try:
                        v = prompt_text.split("Change voice output to ")[1].split()[0]
                        with open(VOICE_CONFIG_PATH, "w", encoding="utf-8") as f:
                            f.write(v)
                        print(f"🌐 [Chrome HTTP] Updated selected_voice.txt -> {v}")
                    except Exception as e: pass
                
                if "Switch audio output to " in prompt_text:
                    try:
                        s = prompt_text.split("Switch audio output to ")[1].strip().rstrip(".")
                        with open(SPEAKER_CONFIG_PATH, "w", encoding="utf-8") as f:
                            f.write(s)
                        print(f"🌐 [Chrome HTTP] Updated selected_speaker.txt -> {s}")
                    except Exception as e: pass

                dispatch_to_antigravity(prompt_text, target_conv_id=target_conv_id, target_chat_name=target_chat_name)

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "DISPATCHED", "prompt": prompt_text, "target": target_conv_id}).encode("utf-8"))
        elif self.path == "/api/open-folder":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            folder_path = data.get("path") or data.get("folderPath") or ""
            
            if folder_path:
                try:
                    target_abs = os.path.abspath(folder_path)
                    os.makedirs(target_abs, exist_ok=True)
                    if not os.path.isdir(target_abs):
                        self.send_response(400)
                        self._set_cors_headers()
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "ERROR", "error": "Path must be a directory"}).encode("utf-8"))
                        return

                    if sys.platform == "win32":
                        subprocess.Popen(["explorer.exe", target_abs])
                    else:
                        subprocess.Popen(["xdg-open", target_abs])
                    print(f"📂 [Local Daemon] Opened Windows Explorer folder: '{target_abs}'")
                    self.send_response(200)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "SUCCESS", "opened": target_abs}).encode("utf-8"))
                except Exception as e:
                    self.send_response(500)
                    self._set_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "ERROR", "error": str(e)}).encode("utf-8"))
            else:
                self.send_response(400)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
        elif self.path == "/api/focus-google-flow":
            try:
                # 1. Activate Google Flow Chrome Tab via CDP
                try:
                    with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=2) as resp:
                        tabs = json.loads(resp.read().decode())
                        for tab in tabs:
                            url = tab.get("url", "")
                            title = tab.get("title", "")
                            if "labs.google" in url or "flow" in url.lower() or "flow" in title.lower():
                                tid = tab.get("id")
                                if tid:
                                    urllib.request.urlopen(f"http://127.0.0.1:9222/json/activate/{tid}", timeout=2)
                                    print(f"🎯 [CDP] Activated Google Flow Tab ID: {tid}")
                                    break
                except Exception as ce:
                    print(f"⚠️ [CDP Focus Warning] {ce}")

                # 2. Bring Chrome window to foreground
                if sys.platform == "win32":
                    ps_cmd = 'Add-Type -TypeDefinition @"\nusing System;\nusing System.Runtime.InteropServices;\npublic class Win32 { [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd); [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow); }\n"@; $proc = Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1; if ($proc) { [Win32]::ShowWindow($proc.MainWindowHandle, 9); [Win32]::SetForegroundWindow($proc.MainWindowHandle); }'
                    subprocess.Popen(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd])

                # 3. Open production folder in Explorer
                gf_folder = r"c:\Users\Curtis\Desktop\Keystone Brain\08_Keystone_protocols\Google_Flow"
                os.makedirs(gf_folder, exist_ok=True)
                if sys.platform == "win32":
                    os.startfile(gf_folder)

                self.send_response(200)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "action": "focused_and_opened"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self._set_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ERROR", "error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

import ctypes
from ctypes import wintypes

PIPE_NAME = r"\\.\pipe\antigravity_ingest"
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3
INVALID_HANDLE_VALUE = -1

def send_to_named_pipe(prompt_text: str) -> bool:
    """Transmit prompt to Rust backend via Win32 Named Pipe in sub-millisecond (<1ms) speed."""
    if sys.platform != "win32":
        return False
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.CreateFileW(
            PIPE_NAME,
            GENERIC_WRITE,
            0,
            None,
            OPEN_EXISTING,
            0,
            None
        )
        if handle == INVALID_HANDLE_VALUE:
            return False
        
        data = f"VOICE_PROMPT: {prompt_text}".encode('utf-8')
        bytes_written = wintypes.DWORD()
        success = kernel32.WriteFile(
            handle,
            data,
            len(data),
            ctypes.byref(bytes_written),
            None
        )
        kernel32.CloseHandle(handle)
        return bool(success)
    except Exception:
        return False

class ExclusiveHTTPServer(HTTPServer):
    """HTTPServer enforcing SO_EXCLUSIVEADDRUSE on Windows. Bypasses Python 3.14 SO_REUSEADDR crash."""
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

def start_ipc_and_ws_server():
    http_server = ExclusiveHTTPServer(("127.0.0.1", PORT_9876), ChromePromptHTTPHandler, bind_and_activate=False)
    for attempt in range(10):
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if sys.platform == "win32":
                SO_EXCLUSIVEADDRUSE = getattr(socket, "SO_EXCLUSIVEADDRUSE", -5)
                server_sock.setsockopt(socket.SOL_SOCKET, SO_EXCLUSIVEADDRUSE, 1)
            server_sock.bind(("127.0.0.1", PORT_9876))
            server_sock.listen(128)
            print(f"🌐 [Local STT Daemon] HTTP Bridge & Push WebSocket listening on ws://127.0.0.1:{PORT_9876}/ws")
            
            while True:
                try:
                    client_sock, client_addr = server_sock.accept()
                    peek_data = client_sock.recv(4096, socket.MSG_PEEK)
                    peek_lower = peek_data.lower()
                    if b"upgrade: websocket" in peek_lower or b"/ws" in peek_lower:
                        threading.Thread(target=handle_ws_client, args=(client_sock,), daemon=True).start()
                    else:
                        threading.Thread(target=http_server.process_request, args=(client_sock, client_addr), daemon=True).start()
                except Exception:
                    time.sleep(0.01)
            return
        except OSError as e:
            print(f"⚠️ [IPC Server] Port {PORT_9876} busy (attempt {attempt+1}/10): {e}")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ [IPC Server Error]: {e}")
            return
    print(f"❌ [IPC Server] Failed to bind port {PORT_9876} after 10 attempts")


# ── Audio Config ─────────────────────────────────────────────────────────
SAMPLE_RATE = 16000       # Whisper expects 16kHz mono
CHANNELS = 1
DTYPE = "int16"
BLOCK_SIZE = 512          # ~32ms chunks for low-latency VAD
SILENCE_THRESHOLD = 1.5   # Seconds of silence before finalizing turn

# ── State ────────────────────────────────────────────────────────────────
is_recording = False
audio_buffer = []
audio_lock = threading.Lock()
silence_start = None
whisper_model = None
model_loaded = threading.Event()

def load_whisper_model():
    """Load Faster-Whisper model on CUDA GPU (or CPU fallback)."""
    global whisper_model
    try:
        from faster_whisper import WhisperModel
        
        # Detect CUDA availability
        try:
            import torch
            has_cuda = torch.cuda.is_available()
        except ImportError:
            # Check via ctranslate2 directly
            try:
                import ctranslate2
                has_cuda = "cuda" in ctranslate2.get_supported_compute_types("default")
            except Exception:
                has_cuda = False
        
        if has_cuda:
            print("🚀 [Local STT] Loading Faster-Whisper large-v3-turbo on CUDA FP16 (RTX 5060 Ti)...")
            try:
                whisper_model = WhisperModel(
                    "large-v3-turbo",
                    device="cuda",
                    compute_type="float16"
                )
                print("✅ [Local STT] Model loaded on CUDA FP16! Sub-50ms inference active.")
            except Exception as cuda_err:
                print(f"⚠️ [Local STT] CUDA initialization failed ({cuda_err}). Falling back to CPU (int8)...")
                whisper_model = WhisperModel(
                    "base",
                    device="cpu",
                    compute_type="int8",
                    cpu_threads=2
                )
                print("✅ [Local STT] Model loaded on CPU fallback.")
        else:
            print("⚠️ [Local STT] CUDA not available. Loading Faster-Whisper on CPU (int8 quantized)...")
            print("    To enable CUDA: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124")
            whisper_model = WhisperModel(
                "base",  # Use smaller model on CPU for acceptable speed
                device="cpu",
                compute_type="int8",
                cpu_threads=2
            )
            print("✅ [Local STT] Model loaded on CPU. Transcription will be slower (~500ms).")
    except ImportError as e:
        print(f"❌ [Local STT] faster-whisper not installed: {e}")
        print("    Run: pip install faster-whisper")
        sys.exit(1)
    
    model_loaded.set()


def transcribe_audio(audio_data: np.ndarray) -> str:
    """Transcribe audio numpy array using Faster-Whisper."""
    if whisper_model is None:
        return ""
    
    # Convert int16 to float32 normalized [-1.0, 1.0]
    audio_float = audio_data.astype(np.float32) / 32768.0
    
    start_time = time.perf_counter()
    
    segments, info = whisper_model.transcribe(
        audio_float,
        beam_size=5,           # High-precision beam search decoding
        best_of=5,
        temperature=0.0,
        vad_filter=True,       # Silero VAD pre-filtering
        vad_parameters=dict(
            min_silence_duration_ms=200,
            speech_pad_ms=300
        ),
        language="en",
        without_timestamps=True
    )
    
    transcript = " ".join([seg.text.strip() for seg in segments]).strip()
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    
    if transcript:
        print(f"⚡ [Local STT] Transcribed in {elapsed_ms:.0f}ms: \"{transcript}\"")
    
    return transcript


def get_antigravity_credentials() -> dict:
    """Dynamically discover live Language Server address and CSRF token."""
    # 1. Environment variables
    ls_addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS", "")
    csrf = os.environ.get("ANTIGRAVITY_CSRF_TOKEN", "")
    if ls_addr and csrf:
        return {"ls_address": ls_addr.replace("localhost", "127.0.0.1"), "csrf_token": csrf}

    # 2. Config files
    cfg_paths = [
        r"C:\Users\Curtis\.gemini\antigravity\voice_bridge_config.json",
        os.path.join(os.path.dirname(__file__), "voice_bridge_config.json"),
        os.path.expanduser("~/.gemini/antigravity/voice_bridge_config.json")
    ]
    for cfg_file in cfg_paths:
        if os.path.exists(cfg_file):
            try:
                with open(cfg_file, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    ls_addr = cfg.get("ls_address", "")
                    csrf = cfg.get("csrf_token", "")
                    if ls_addr and csrf:
                        return {"ls_address": ls_addr.replace("localhost", "127.0.0.1"), "csrf_token": csrf}
            except Exception:
                pass

    # 3. Dynamic zero-dependency CIM discovery fallback
    try:
        from sync_active_chats import discover_language_server_cim
        addr, token = discover_language_server_cim()
        if addr and token:
            return {"ls_address": addr.replace("localhost", "127.0.0.1"), "csrf_token": token}
    except Exception:
        pass

    return {"ls_address": "127.0.0.1:58868", "csrf_token": csrf}


def dispatch_to_antigravity(prompt_text: str, priority: str = "NORMAL", target_conv_id: str = "", target_chat_name: str = ""):
    """Write transcribed text to last_user_prompt.txt for Antigravity ingestion."""
    if not prompt_text.strip():
        return
    
    if not target_conv_id and CURRENT_BOUND_CHAT_ID:
        target_conv_id = CURRENT_BOUND_CHAT_ID
    if not target_chat_name and CURRENT_BOUND_CHAT_NAME:
        target_chat_name = CURRENT_BOUND_CHAT_NAME

    is_emergency = "EMERGENCY" in prompt_text.upper()
    
    if is_emergency:
        print(f"🚨 [Local STT → Antigravity] EMERGENCY: '{prompt_text}'")
    else:
        print(f"📤 [Local STT → Antigravity] Dispatching (Target: {target_chat_name or target_conv_id or 'default'}): '{prompt_text[:80]}...'")
    
    # 0. Push real-time transcript to all connected Push WebSocket clients
    broadcast_ws({"type": "transcript", "text": prompt_text, "priority": priority, "timestamp": time.time(), "target": target_chat_name or target_conv_id})

    # Set bridge state to working so avatar stays in holographic multitasking animation while Antigravity works
    if not is_emergency:
        set_bridge_state("working", "WORKING")

    # Record dispatch metadata to prevent duplicate dispatch in instant_watchdog
    try:
        with open(LAST_DISPATCH_META_PATH, "w", encoding="utf-8") as mf:
            json.dump({
                "timestamp": time.time(),
                "text": prompt_text.strip(),
                "target_conv_id": target_conv_id,
                "source": "local_stt_daemon"
            }, mf)
    except Exception:
        pass

    # 1. Atomic write to last_user_prompt.txt
    os.makedirs(os.path.dirname(LAST_USER_PROMPT_PATH), exist_ok=True)
    temp_path = LAST_USER_PROMPT_PATH + ".tmp"
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(prompt_text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, LAST_USER_PROMPT_PATH)
        print(f"✅ [Local STT → Antigravity] Written to last_user_prompt.txt ({len(prompt_text)} chars)")
    except Exception as e:
        print(f"❌ [File Write Error]: {e}")
        try:
            with open(LAST_USER_PROMPT_PATH, "w", encoding="utf-8") as f:
                f.write(prompt_text)
        except Exception as e2:
            print(f"❌ [Fallback Write Error]: {e2}")

    # 2. Win32 Named Pipe Transmission (<1ms latency)
    send_to_named_pipe(prompt_text)

    # 3. Direct Antigravity agentapi CLI dispatch to specific target conversation
    agentapi_bat = r"C:\Users\Curtis\.gemini\antigravity\bin\agentapi.bat"
    conv_file = r"C:\Users\Curtis\.gemini\antigravity\active_conversation_id.txt"
    targets_file = r"C:\Users\Curtis\.gemini\antigravity\chat_targets.json"
    brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"
    active_conv_id = ""

    # Priority 1: Explicit target_conv_id
    if target_conv_id and len(target_conv_id) == 36:
        active_conv_id = target_conv_id

    # Priority 2: Lookup target_chat_name in chat_targets.json
    if not active_conv_id and target_chat_name and os.path.exists(targets_file):
        try:
            with open(targets_file, "r", encoding="utf-8") as f:
                targets = json.load(f)
                matched_id = targets.get(target_chat_name) or targets.get(target_chat_name.lower())
                if matched_id and len(matched_id) == 36:
                    target_brain = os.path.join(brain_dir, matched_id)
                    if os.path.exists(target_brain):
                        active_conv_id = matched_id
                        print(f"🎯 [Named Router] Resolved chat name '{target_chat_name}' -> '{active_conv_id}'")
                    else:
                        print(f"⚠️ [Named Router] Target chat '{target_chat_name}' ({matched_id}) not found in brain dir. Falling back to active session.")
        except Exception as e:
            print(f"❌ [Named Router Lookup Error]: {e}")

    # Priority 3: Fallback to active_conversation_id.txt
    if not active_conv_id:
        for cf in [conv_file, r"C:\Users\Curtis\Desktop\Keystone Brain\active_conversation_id.txt"]:
            if os.path.exists(cf):
                try:
                    with open(cf, "r", encoding="utf-8") as f:
                        cid = f.read().strip()
                        if cid and len(cid) == 36:
                            active_conv_id = cid
                            break
                except Exception:
                    pass

    # Priority 4: Reject blind fallback to prevent cross-chat leakage!
    if not active_conv_id:
        print(f"⚠️ [Local STT] Dispatch aborted: No active conversation ID bound in active_conversation_id.txt. Blind dispatches to arbitrary conversations are forbidden.")
        return

    if os.path.exists(agentapi_bat):
        try:
            import subprocess
            flags = 0x08000000 if sys.platform == "win32" else 0
            dispatch_env = os.environ.copy()
            creds = get_antigravity_credentials()
            if creds.get("ls_address"):
                dispatch_env["ANTIGRAVITY_LS_ADDRESS"] = creds["ls_address"]
            if creds.get("csrf_token"):
                dispatch_env["ANTIGRAVITY_CSRF_TOKEN"] = creds["csrf_token"]
            dispatch_env["ANTIGRAVITY_AGENT"] = "1"

            if active_conv_id:
                subprocess.Popen(
                    [agentapi_bat, "send-message", active_conv_id, prompt_text],
                    env=dispatch_env,
                    creationflags=flags
                )
                print(f"🚀 [Local STT → Antigravity Direct IPC] Direct prompt sent to target chat {active_conv_id} (LS: {creds.get('ls_address', 'default')})")
            else:
                subprocess.Popen(
                    [agentapi_bat, "new-conversation", "--title=Keystone Swarm Trigger", prompt_text],
                    env=dispatch_env,
                    creationflags=flags
                )
                print(f"🚀 [Local STT → Antigravity Direct IPC] Spawned new conversation (LS: {creds.get('ls_address', 'default')})")
        except Exception as e:
            print(f"❌ [AgentAPI Dispatch Error]: {e}")

    
    # 2. Append to conversation scratch log
    os.makedirs(DAEMON_LOG_DIR, exist_ok=True)
    entry = {
        "timestamp": time.time(),
        "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "user_spoken_prompt": prompt_text,
        "priority": "EMERGENCY" if is_emergency else "NORMAL",
        "source": "LOCAL_FASTER_WHISPER_CUDA",
        "is_emergency": is_emergency
    }
    try:
        existing = []
        if os.path.exists(VOICE_LOG_PATH):
            try:
                with open(VOICE_LOG_PATH, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.append(entry)
        # Keep last 100 entries
        if len(existing) > 100:
            existing = existing[-100:]
        with open(VOICE_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)
    except Exception as e:
        print(f"[Scratch Log Error]: {e}")


def audio_callback(indata, frames, time_info, status):
    """Called by sounddevice for each audio block while recording."""
    global silence_start
    
    if status:
        print(f"[Audio Warning]: {status}")
    
    if not is_recording:
        return
    
    audio_chunk = indata[:, 0].copy()  # Mono channel
    
    # Simple energy-based voice activity detection
    energy = np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))
    
    with audio_lock:
        audio_buffer.append(audio_chunk)
    
    # Track silence for auto-finalization
    if energy > 200:  # Speech detected (int16 scale)
        silence_start = None
    elif silence_start is None:
        silence_start = time.time()


class AudioStreamManager:
    """Thread-safe manager for sounddevice.InputStream allowing dynamic mic hot-swapping."""
    def __init__(self, sample_rate=SAMPLE_RATE, channels=CHANNELS, dtype=DTYPE, block_size=BLOCK_SIZE, callback=audio_callback):
        self.target_sample_rate = sample_rate
        self.actual_sample_rate = sample_rate
        self.channels = channels
        self.dtype = dtype
        self.block_size = block_size
        self.user_callback = callback
        self.stream = None
        self.lock = threading.Lock()
        self.current_device_name = None

    def _internal_callback(self, indata, frames, time_info, status):
        if self.actual_sample_rate != self.target_sample_rate and indata.shape[0] > 0:
            chunk = indata[:, 0].copy()
            if self.actual_sample_rate % self.target_sample_rate == 0:
                step = int(self.actual_sample_rate // self.target_sample_rate)
                chunk_resampled = chunk[::step]
            else:
                orig_len = len(chunk)
                target_len = int(round(orig_len * (self.target_sample_rate / self.actual_sample_rate)))
                x_orig = np.linspace(0, 1, orig_len, endpoint=False)
                x_target = np.linspace(0, 1, target_len, endpoint=False)
                chunk_resampled = np.interp(x_target, x_orig, chunk).astype(np.int16)
            
            resample_indata = chunk_resampled[:, np.newaxis]
            self.user_callback(resample_indata, len(chunk_resampled), time_info, status)
        else:
            self.user_callback(indata, frames, time_info, status)

    def resolve_input_device_index(self, device_name):
        if not device_name or device_name.strip().lower() in ["default", "system default"]:
            return None
        
        try:
            devices = sd.query_devices()
            hostapis = sd.query_hostapis()
            wasapi_idx = next((i for i, h in enumerate(hostapis) if "wasapi" in h.get("name", "").lower()), None)
            target_clean = device_name.strip().lower()

            if wasapi_idx is not None:
                # 1. Exact match on WASAPI input devices
                for idx, d in enumerate(devices):
                    if d.get("hostapi") == wasapi_idx and d.get("max_input_channels", 0) > 0:
                        if d.get("name", "").strip().lower() == target_clean:
                            return idx
                # 2. Substring match on WASAPI input devices
                for idx, d in enumerate(devices):
                    if d.get("hostapi") == wasapi_idx and d.get("max_input_channels", 0) > 0:
                        if target_clean in d.get("name", "").strip().lower() or d.get("name", "").strip().lower() in target_clean:
                            return idx

            # 3. Fallback across all host APIs
            for idx, d in enumerate(devices):
                if d.get("max_input_channels", 0) > 0:
                    if target_clean in d.get("name", "").strip().lower():
                        return idx
        except Exception as e:
            print(f"⚠️ [Input Device Resolver Error]: {e}")
        return None

    def start_or_switch(self, device_name=None):
        with self.lock:
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except Exception as e:
                    print(f"⚠️ [Stream Stop Warning]: {e}")
                self.stream = None

            device_idx = self.resolve_input_device_index(device_name)
            self.current_device_name = device_name
            
            try_rates = [self.target_sample_rate]
            if device_idx is not None:
                try:
                    dev_info = sd.query_devices(device_idx)
                    native_sr = int(dev_info.get("default_samplerate", 48000))
                    if native_sr != self.target_sample_rate:
                        try_rates.append(native_sr)
                except Exception:
                    pass

            opened = False
            for sr in try_rates:
                try:
                    calc_block = self.block_size if sr == self.target_sample_rate else int(self.block_size * (sr / self.target_sample_rate))
                    self.stream = sd.InputStream(
                        device=device_idx,
                        samplerate=sr,
                        channels=self.channels,
                        dtype=self.dtype,
                        blocksize=calc_block,
                        callback=self._internal_callback
                    )
                    self.stream.start()
                    self.actual_sample_rate = sr
                    opened = True
                    idx_str = f"Device {device_idx}" if device_idx is not None else "Default Device"
                    print(f"🎙️ [Audio Stream Manager] Active on {idx_str}: '{device_name or 'Default'}' @ {sr}Hz (target: {self.target_sample_rate}Hz)")
                    break
                except Exception as open_err:
                    print(f"⚠️ [Stream Try SR {sr}Hz failed]: {open_err}")

            if not opened:
                print(f"❌ [Audio Stream Start Error]: Could not open input stream on device {device_idx}")
                return False
            return True

    def stop(self):
        with self.lock:
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except Exception:
                    pass
                self.stream = None

stream_manager = AudioStreamManager()

def start_recording():
    """Begin capturing microphone audio."""
    global is_recording, audio_buffer, silence_start
    
    if is_recording:
        return
    
    with audio_lock:
        audio_buffer = []
    silence_start = None
    is_recording = True
    print("🎙️ [Local STT] Recording started... (speak now)")


def stop_recording_and_transcribe():
    """Stop recording, transcribe accumulated audio, dispatch to Antigravity."""
    global is_recording, silence_start, is_f9_down
    
    is_f9_down = False
    if not is_recording:
        return
    
    is_recording = False
    silence_start = None
    
    try:
        with audio_lock:
            if not audio_buffer:
                print("[Local STT] No audio captured.")
                set_bridge_state("connected", "CONNECTED")
                broadcast_ws({"type": "recording_discarded", "reason": "empty"})
                return
            full_audio = np.concatenate(audio_buffer)
        
        # Check minimum audio length (~0.5 seconds)
        min_samples = SAMPLE_RATE // 2
        if len(full_audio) < min_samples:
            print("[Local STT] Audio too short, discarding.")
            set_bridge_state("connected", "CONNECTED")
            broadcast_ws({"type": "recording_discarded", "reason": "too_short"})
            return
        
        print(f"🔄 [Local STT] Processing {len(full_audio) / SAMPLE_RATE:.1f}s of audio...")
        
        # Transcribe on GPU
        transcript = transcribe_audio(full_audio)
        
        if transcript:
            # Apply phonetic corrections
            transcript = sanitize_phonetic_terms(transcript)
            active_chat = get_current_bound_chat_id()
            dispatch_to_antigravity(transcript, target_conv_id=active_chat, target_chat_name=CURRENT_BOUND_CHAT_NAME)
            set_bridge_state("working", "WORKING")
        else:
            print("[Local STT] No speech detected in audio.")
            set_bridge_state("connected", "CONNECTED")
            broadcast_ws({"type": "recording_discarded", "reason": "no_speech"})
    finally:
        is_f9_down = False


def sanitize_phonetic_terms(text: str) -> str:
    """Auto-correct common phonetic misrecognitions."""
    import re
    corrections = {
        r'\bTory\b': 'Tauri',
        r'\bTori\b': 'Tauri',
        r'\bTorrie\b': 'Tauri',
        r'\btory\b': 'Tauri',
        r'\bKeyston\b': 'Keystone',
        r'\bAntigrav\b': 'Antigravity',
        r'\bantigrav\b': 'Antigravity',
    }
    for pattern, replacement in corrections.items():
        text = re.sub(pattern, replacement, text)
    return text


is_ptt_down = False
is_f9_down = False
release_timer = None

def stop_active_tts_speech():
    try:
        import urllib.request
        req = urllib.request.Request("http://127.0.0.1:9877/api/stop", data=b"{}", headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=0.5)
    except Exception:
        pass

def setup_global_hotkeys():
    """Register F8 & F9 (push-to-talk) and Shift+F8 / Escape (emergency stop) as SYSTEM-WIDE global hotkeys."""
    global is_ptt_down, release_timer
    
    def on_ptt_press(event):
        global is_ptt_down
        if is_ptt_down:
            return  # Ignore Windows key-repeat events!
        is_ptt_down = True
        key_name = getattr(event, 'name', 'PTT').upper()
        print(f"🎙️ [Global Hotkeys] {key_name} pressed -> Starting voice capture...")
        set_bridge_state("listening", "LISTENING")
        threading.Thread(target=stop_active_tts_speech, daemon=True).start()  # Mute/stop any incoming speech immediately!
        start_recording()
    
    def on_ptt_release(event):
        global is_ptt_down
        if not is_ptt_down:
            return
        is_ptt_down = False
        key_name = getattr(event, 'name', 'PTT').upper()
        print(f"🚀 [Global Hotkeys] {key_name} released -> Processing transcript...")
        set_bridge_state("transmitting", "TRANSMITTING")
        threading.Thread(target=stop_recording_and_transcribe, daemon=True).start()
    
    def on_emergency_stop(event=None):
        global is_recording, is_ptt_down
        is_recording = False
        is_ptt_down = False
        print("🛑 [EMERGENCY STOP] Triggered! Halting agent...")
        stop_active_tts_speech()
        dispatch_to_antigravity(
            "EMERGENCY STOP TRIGGERED: Halt all current active tasks immediately.",
            priority="EMERGENCY"
        )
        set_bridge_state("connected", "CONNECTED")
    
    # Both F9 and F8 trigger Push-to-Talk (press to listen, release to transcribe)
    keyboard.on_press_key("F9", on_ptt_press, suppress=False)
    keyboard.on_release_key("F9", on_ptt_release, suppress=False)
    keyboard.on_press_key("F8", on_ptt_press, suppress=False)
    keyboard.on_release_key("F8", on_ptt_release, suppress=False)
    
    # Emergency Stop bound to Shift+F8 and Escape
    try:
        keyboard.add_hotkey("shift+f8", on_emergency_stop, suppress=False)
    except Exception:
        pass
    
    print("🎯 [Global Hotkeys] F8 & F9 = Push-to-Talk (system-wide, works from any app)")
    print("    Shift+F8 = Emergency Stop")


def main():
    print("=" * 70)
    print("  KEYSTONE LOCAL STT DAEMON")
    print("  Faster-Whisper on NVIDIA RTX 5060 Ti (CUDA FP16)")
    print("  F9 = Push-to-Talk (Global) | F8 = Emergency Stop")
    print("=" * 70)

    # Instant Singleton Guard: check if Port 9876 is already bound or in-use
    lock_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock_sock.bind(("127.0.0.1", PORT_9876))
        lock_sock.close()
    except Exception:
        print("⚠️ [SINGLETON GUARD] local_stt_daemon is already running or binding on Port 9876. Exiting duplicate process immediately.")
        sys.exit(0)
    
    # Load Whisper model in background thread
    model_thread = threading.Thread(target=load_whisper_model, daemon=True)
    model_thread.start()
    
    # Start HTTP & Push WebSocket Bridge Server on Port 9876 for Chrome frontend & HUD clients
    ipc_thread = threading.Thread(target=start_ipc_and_ws_server, daemon=True)
    ipc_thread.start()
    
    # Wait for model to finish loading
    print("\n⏳ Waiting for Whisper model to load...")
    model_loaded.wait()
    print("✅ Ready! Initializing OS-wide F8/F9 global hotkeys...")
    try:
        setup_global_hotkeys()
        print("✅ System-wide F9 Push-to-Talk active.\n")
    except Exception as e:
        print(f"⚠️ [Global Hotkeys] Could not bind F9/F8 (detached mode): {e}")
        print("    F9 via HUD HTTP button still works.\n")
    
    # Start audio capture stream using AudioStreamManager
    try:
        init_mic = get_current_mic_setting()
        stream_manager.start_or_switch(init_mic)
        print(f"🔊 [Audio Stream] Active on mic '{init_mic}' at {SAMPLE_RATE}Hz")
        print(f"📁 [Output] Transcripts → {LAST_USER_PROMPT_PATH}")
        print(f"📁 [Log]    Voice log   → {VOICE_LOG_PATH}")
        print()
        
        # Keep daemon alive
        while True:
            time.sleep(0.1)
                
    except KeyboardInterrupt:
        print("\n[Local STT Daemon] Shutting down.")
        stream_manager.stop()
    except Exception as e:
        print(f"❌ [Audio Stream Error]: {e}")
        print("    Make sure your microphone is connected.")
        sys.exit(1)


if __name__ == "__main__":
    main()
