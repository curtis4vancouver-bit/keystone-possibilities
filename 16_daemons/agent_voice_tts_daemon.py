import sys
import os
import time
import json
import socket
import threading
import subprocess
import urllib.request
import queue
from http.server import HTTPServer, BaseHTTPRequestHandler

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Daemon B: Antigravity Response & Instant TTS Playout Daemon running on Port 9877
PORT = 9877
VOICE_OUTBOX_PATH = r"C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt"
SPEAKER_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "gemini_live_speaker.py")

VOICE_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_voice.txt"
SPEAKER_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_speaker.txt"
MIC_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_mic.txt"
VOLUME_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_volume.txt"

def get_current_voice():
    try:
        if os.path.exists(VOICE_CONFIG_PATH):
            with open(VOICE_CONFIG_PATH, "r", encoding="utf-8") as f:
                v = f.read().strip()
                if v: return v
    except Exception:
        pass
    return "Aoede"

def get_current_speaker():
    try:
        if os.path.exists(SPEAKER_CONFIG_PATH):
            with open(SPEAKER_CONFIG_PATH, "r", encoding="utf-8") as f:
                s = f.read().strip()
                if s and s.lower() not in ["default", "system default", "system default (auto-switch)"]:
                    return s
    except Exception:
        pass
    return "default"

def get_default_audio_device():
    try:
        import comtypes
        comtypes.CoInitialize()
        from pycaw.pycaw import AudioUtilities
        from pycaw.constants import EDataFlow, ERole
        enum = AudioUtilities.GetDeviceEnumerator()
        if enum:
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

def get_current_volume():
    try:
        dev = get_default_audio_device()
        if dev and dev.EndpointVolume:
            scalar = dev.EndpointVolume.GetMasterVolumeLevelScalar()
            return max(0, min(100, round(scalar * 100)))
    except Exception:
        pass
    try:
        if os.path.exists(VOLUME_CONFIG_PATH):
            with open(VOLUME_CONFIG_PATH, "r", encoding="utf-8") as f:
                v = int(f.read().strip())
                return max(0, min(100, v))
    except Exception:
        pass
    return 80

def set_current_volume(vol):
    try:
        vol = max(0, min(100, int(vol)))
        try:
            dev = get_default_audio_device()
            if dev and dev.EndpointVolume:
                dev.EndpointVolume.SetMasterVolumeLevelScalar(vol / 100.0, None)
                if vol > 0 and dev.EndpointVolume.GetMute():
                    dev.EndpointVolume.SetMute(0, None)
        except Exception:
            pass
        os.makedirs(os.path.dirname(VOLUME_CONFIG_PATH), exist_ok=True)
        tmp = VOLUME_CONFIG_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(str(vol))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, VOLUME_CONFIG_PATH)
        print(f"[Daemon B] Volume set to {vol}%")
        return vol
    except Exception as e:
        print(f"[Daemon B Volume Error]: {e}")
        return 80

last_mtime = 0
last_spoken_text = ""

current_speaker_process = None
speech_queue = queue.Queue()
queue_lock = threading.Lock()

def stop_active_speech():
    global current_speaker_process
    if current_speaker_process and current_speaker_process.poll() is None:
        try:
            current_speaker_process.kill()
            print("[Daemon B] 🛑 Stopped active TTS speaker process!")
        except Exception:
            pass
    current_speaker_process = None

def clear_speech_queue():
    """Clear all pending speech items and terminate active playback."""
    global current_speaker_process
    with queue_lock:
        while not speech_queue.empty():
            try:
                speech_queue.get_nowait()
                speech_queue.task_done()
            except Exception:
                break
    stop_active_speech()
    print("[Daemon B - FIFO Queue] Cleared speech queue and stopped playback.")

def notify_bridge_state(state: str, badge: str):
    """Notify local_stt_daemon on Port 9876 of speaking/connected states."""
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:9876/api/state",
            data=json.dumps({"state": state, "badge": badge}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=0.8)
    except Exception:
        pass

def enqueue_speech(text: str, voice: str = None, speaker: str = None, volume: int = None, source: str = "outbox"):
    """Enqueue speech item to play in FIFO order without overlapping."""
    text = text.strip()
    if not text:
        return
    v = voice or get_current_voice()
    s = speaker or get_current_speaker()
    vol = volume if volume is not None else get_current_volume()
    speech_queue.put({
        "text": text,
        "voice": v,
        "speaker": s,
        "volume": vol,
        "source": source,
        "timestamp": time.time()
    })
    print(f"[Daemon B - FIFO Queue] Enqueued ({source}) [Queue depth: {speech_queue.qsize()}, Vol: {vol}%]: '{text[:60]}...'")

def speech_queue_worker_loop():
    """Worker thread that executes queued speech items sequentially without overlapping."""
    global current_speaker_process
    print("[Daemon B - FIFO Queue] Sequential Speech Worker thread active.")
    creationflags = 0x08000000 if sys.platform == "win32" else 0

    while True:
        item = None
        try:
            item = speech_queue.get()
            if not item:
                continue

            text = item.get("text", "").strip()
            voice = item.get("voice") or get_current_voice()
            speaker = item.get("speaker") or get_current_speaker()
            volume = item.get("volume") if item.get("volume") is not None else get_current_volume()

            if text:
                try:
                    print(f"[Daemon B - FIFO Playout] Synthesizing (Voice: {voice}, Speaker: {speaker}, Vol: {volume}%): '{text[:80]}'")
                except Exception:
                    pass
                notify_bridge_state("speaking", "SPEAKING")

                try:
                    current_speaker_process = subprocess.Popen(
                        [PYTHON_EXE, SPEAKER_SCRIPT_PATH, text, voice, speaker, str(volume)],
                        creationflags=creationflags,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    current_speaker_process.wait()
                except Exception as ex:
                    try:
                        print(f"⚠️ [Daemon B - Playout Error]: {ex}")
                    except Exception:
                        pass
                finally:
                    current_speaker_process = None

                # 400ms conversational cadence pause between sequential speech items
                time.sleep(0.4)

            # When queue is fully drained, transition back to connected state
            if speech_queue.empty():
                notify_bridge_state("connected", "CONNECTED")
        except Exception as e:
            try:
                print(f"[Daemon B - Queue Worker Error]: {e}")
            except Exception:
                pass
            time.sleep(0.2)
        finally:
            if item is not None:
                try:
                    speech_queue.task_done()
                except Exception:
                    pass

PYTHON_VENV_EXE = r"C:\Users\Curtis\Desktop\Keystone Brain\16_daemons\venv\Scripts\python.exe"
PYTHON_EXE = PYTHON_VENV_EXE if os.path.exists(PYTHON_VENV_EXE) else sys.executable

class AgentVoiceTTSHandler(BaseHTTPRequestHandler):
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
        if self.path in ["/api/status", "/api/stats", "/health"]:
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"daemon": "Daemon B (Agent TTS)", "port": PORT, "status": "ONLINE", "queue_depth": speech_queue.qsize()}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        elif self.path in ["/api/volume", "/api/audio/volume"]:
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            vol = get_current_volume()
            response = {"status": "SUCCESS", "volume": vol}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global current_speaker_process, last_spoken_text
        if self.path == "/api/shutdown":
            clear_speech_queue()
            notify_bridge_state("connected", "CONNECTED")
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "SHUTTING_DOWN"}')
            print("🛑 [Agent TTS Daemon] Graceful shutdown signal received. Terminating.")
            threading.Thread(target=lambda: (time.sleep(0.1), os._exit(0)), daemon=True).start()
            return
        elif self.path in ["/api/volume", "/api/audio/volume"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            vol_val = data.get("volume")
            if vol_val is None:
                vol_val = data.get("level", 80)
            new_vol = set_current_volume(vol_val)
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "volume": new_vol}).encode("utf-8"))
        elif self.path == "/api/stop":
            clear_speech_queue()
            notify_bridge_state("connected", "CONNECTED")
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "STOPPED"}).encode("utf-8"))
        elif self.path == "/api/speak":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            text_to_speak = data.get("text", "").strip()
            if text_to_speak:
                last_spoken_text = text_to_speak
                active_voice = data.get("voice") or get_current_voice()
                active_speaker = data.get("speaker") or get_current_speaker()
                active_vol = data.get("volume")
                enqueue_speech(text_to_speak, voice=active_voice, speaker=active_speaker, volume=active_vol, source="api_speak")

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"status": "ENQUEUED", "text": text_to_speak, "queue_depth": speech_queue.qsize()}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        elif self.path in ["/api/chime", "/api/audio/chime"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            speaker_name = data.get("device_name", get_current_speaker())
            cur_vol = get_current_volume()
            stop_active_speech()
            creationflags = 0x08000000 if sys.platform == "win32" else 0
            proc = subprocess.Popen(
                [PYTHON_EXE, SPEAKER_SCRIPT_PATH, "--chime", speaker_name, str(cur_vol)],
                creationflags=creationflags,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            current_speaker_process = proc
            threading.Thread(target=proc.wait, daemon=True).start()
            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "CHIME_PLAYED", "device": speaker_name, "volume": cur_vol}).encode("utf-8"))
        elif self.path in ["/api/audio/select", "/api/select_device"]:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body) if body else {}
            device_type = data.get("type", "speaker").lower()
            device_name = data.get("device_name", "").strip()

            target_path = SPEAKER_CONFIG_PATH if device_type == "speaker" else MIC_CONFIG_PATH

            try:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                tmp_path = target_path + ".tmp"
                with open(tmp_path, "w", encoding="utf-8") as f:
                    f.write(device_name)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, target_path)
                print(f"[Daemon B] Updated {os.path.basename(target_path)} -> '{device_name}'")
            except Exception as e:
                print(f"[Daemon B Error]: {e}")

            if device_type == "speaker":
                stop_active_speech()
                cur_vol = get_current_volume()
                creationflags = 0x08000000 if sys.platform == "win32" else 0
                subprocess.Popen(
                    [PYTHON_EXE, SPEAKER_SCRIPT_PATH, "--chime", device_name, str(cur_vol)],
                    creationflags=creationflags,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            self.send_response(200)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "SUCCESS", "type": device_type, "selected": device_name}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def outbox_monitor_loop():
    global last_mtime, last_spoken_text
    print(f"[Daemon B - Agent Voice TTS] Outbox Watchdog active on {VOICE_OUTBOX_PATH}")
    while True:
        try:
            if os.path.exists(VOICE_OUTBOX_PATH):
                mtime = os.path.getmtime(VOICE_OUTBOX_PATH)
                if mtime > last_mtime:
                    last_mtime = mtime
                    with open(VOICE_OUTBOX_PATH, "r", encoding="utf-8-sig") as f:
                        text = f.read().strip()
                    if text and text != last_spoken_text:
                        last_spoken_text = text
                        enqueue_speech(text, source="voice_outbox")
        except Exception as e:
            print(f"[Daemon B - Error]: {e}")
        time.sleep(0.1)

class ReusableHTTPServer(HTTPServer):
    """HTTPServer with SO_EXCLUSIVEADDRUSE on Windows. Bypasses Python 3.14 SO_REUSEADDR crash."""
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

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0

def run_daemon_b():
    # Singleton check: If port 9877 is already responsive, exit duplicate process cleanly
    if is_port_in_use(PORT):
        try:
            req = urllib.request.Request(f"http://127.0.0.1:{PORT}/api/status")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    print(f"⚠️ [SINGLETON GUARD] agent_voice_tts_daemon already active and healthy on Port {PORT}. Exiting duplicate cleanly.")
                    sys.exit(0)
        except Exception:
            pass

    t_outbox = threading.Thread(target=outbox_monitor_loop, daemon=True)
    t_outbox.start()
    t_worker = threading.Thread(target=speech_queue_worker_loop, daemon=True)
    t_worker.start()
    for attempt in range(10):
        try:
            server = ReusableHTTPServer(("127.0.0.1", PORT), AgentVoiceTTSHandler)
            print(f"[Daemon B - Agent Voice TTS] Active on http://127.0.0.1:{PORT}")
            server.serve_forever()
            return
        except OSError as e:
            print(f"[Daemon B] Port {PORT} busy (attempt {attempt+1}/10): {e}")
            import time
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ [Daemon B Error]: {e}")
            return
    print(f"❌ [Daemon B] Failed to bind port {PORT} after 10 attempts")

if __name__ == "__main__":
    run_daemon_b()
