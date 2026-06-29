import os
import subprocess
import sys
import psutil
import threading
import logging
from logging.handlers import RotatingFileHandler

class VoiceBridgeAPI:
    def __init__(self):
        self.master_brain = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
        self.voice_bridge_script = os.path.join(self.master_brain, "scripts", "voice_bridge.py")
        self.voice_outbox = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "voice_outbox.txt")
        self.voice_log = os.path.join(self.master_brain, "scripts", "voice_bridge.log")
        self.lock = threading.RLock()
        self.is_starting = False

        # Setup Rotating Logger to handle voice bridge logs without locking the file on Windows
        self.logger = logging.getLogger("VoiceBridgeAPI")
        if not self.logger.handlers:
            # Rotate at 5MB, keep 3 backups
            handler = RotatingFileHandler(self.voice_log, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def is_running(self) -> bool:
        # 1. Check if the process we started in this session is running via Popen reference
        with self.lock:
            if hasattr(self, 'proc') and self.proc is not None:
                if self.proc.poll() is None:
                    return True

        # 2. Check the status file for the process PID to verify directly without looping all processes
        status_path = os.path.join(
            os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_status.json"
        )
        if os.path.exists(status_path):
            try:
                import json
                with open(status_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    pid = data.get("pid")
                    if pid:
                        if psutil.pid_exists(pid):
                            try:
                                proc = psutil.Process(pid)
                                name = proc.name().lower()
                                if "python" in name or "aida" in name:
                                    return True
                            except (psutil.NoSuchProcess, psutil.AccessDenied):
                                pass
            except Exception:
                pass

        return False

    def get_status(self) -> str:
        if not self.is_running():
            return "disconnected"
            
        # Check json status file first for live status
        status_path = os.path.join(
            os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_status.json"
        )
        if os.path.exists(status_path):
            try:
                import json
                with open(status_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    status = data.get("status")
                    if status:
                        return status
            except Exception:
                pass
                
        # Check logs for detailed status if available

        if os.path.exists(self.voice_log):
            try:
                # Read last 5 lines
                with open(self.voice_log, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.readlines()[-5:]
                log_text = "".join(lines).lower()
                if "reconnecting" in log_text or "websocket closed" in log_text:
                    return "reconnecting"
                elif "connected" in log_text or "ready" in log_text or "started" in log_text:
                    return "connected"
            except Exception:
                pass
                
        return "connected"  # Default if running but log unreadable

    def get_status_data(self) -> dict:
        if not self.is_running():
            return {"status": "disconnected", "rms": 0.0, "pitch": 0.0}
            
        status_path = os.path.join(
            os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_status.json"
        )
        if os.path.exists(status_path):
            try:
                import json
                with open(status_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return {
                        "status": data.get("status", "connected"),
                        "rms": float(data.get("rms", 0.0)),
                        "pitch": float(data.get("pitch", 0.0))
                    }
            except Exception:
                pass
        return {"status": self.get_status(), "rms": 0.0, "pitch": 0.0}

    def start_bridge(self) -> bool:
        with self.lock:
            if self.is_starting:
                print("Voice bridge start already in progress...")
                return True
            if self.is_running():
                print("Voice bridge is already running.")
                return True
            self.is_starting = True

        try:
            # Stop any existing bridge (stale or visible) to ensure a clean slate and fresh config load
            self.stop_bridge()
                
            if not os.path.exists(self.voice_bridge_script):
                print(f"Voice bridge script not found at {self.voice_bridge_script}")
                return False

            # In a PyInstaller bundle, sys.executable is the compiled AIDA.exe.
            # We must run voice_bridge.py using the real python interpreter, not AIDA.exe!
            python_exe = sys.executable
            if "aida" in python_exe.lower() or not (python_exe.lower().endswith("python.exe") or python_exe.lower().endswith("pythonw.exe")):
                import shutil
                python_exe = shutil.which("pythonw") or shutil.which("python") or r"C:\Users\Curtis\AppData\Local\Programs\Python\Python314\pythonw.exe"

            # Start voice_bridge.py in the background (hidden) with pipe consumption.
            # Because AIDA.exe is running in your interactive user session (Session 1),
            # this background process inherits Session 1 access, and global keyboard hooks work perfectly!
            proc = subprocess.Popen(
                [python_exe, self.voice_bridge_script],
                creationflags=subprocess.CREATE_NO_WINDOW,
                cwd=os.path.dirname(self.voice_bridge_script),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
                text=True,
                bufsize=1,
                close_fds=True
            )

            # Consume output in a background thread to prevent blocking and write to rotating log
            def log_reader(process, logger):
                try:
                    for line in iter(process.stdout.readline, ''):
                        if line:
                            logger.info(line.strip())
                except Exception as e:
                    logger.error(f"Error reading voice bridge stdout: {e}")
                finally:
                    try:
                        process.stdout.close()
                    except Exception:
                        pass
                    try:
                        process.wait()
                    except Exception:
                        pass

            reader_thread = threading.Thread(target=log_reader, args=(proc, self.logger), daemon=True)
            reader_thread.start()
            return True
        except Exception as e:
            print(f"Failed to start voice bridge: {e}")
            return False
        finally:
            with self.lock:
                self.is_starting = False

    def stop_bridge(self) -> bool:
        try:
            status_path = os.path.join(
                os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_status.json"
            )
            if os.path.exists(status_path):
                import json
                with open(status_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    pid = data.get("pid")
                    if pid:
                        import psutil
                        try:
                            proc = psutil.Process(pid)
                            proc.kill()
                            return True
                        except Exception:
                            pass
            return False
        except Exception as e:
            print(f"Error stopping voice bridge: {e}")
            return False

    def speak(self, text: str) -> bool:
        try:
            os.makedirs(os.path.dirname(self.voice_outbox), exist_ok=True)
            with open(self.voice_outbox, "w", encoding="utf-8") as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error writing to voice outbox: {e}")
            return False

    def trigger_press(self) -> bool:
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"press", ("127.0.0.1", 55443))
            return True
        except Exception as e:
            self.logger.error(f"Error sending press trigger: {e}")
            return False

    def trigger_release(self) -> bool:
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"release", ("127.0.0.1", 55443))
            return True
        except Exception as e:
            self.logger.error(f"Error sending release trigger: {e}")
            return False

    def abort(self) -> bool:
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"abort", ("127.0.0.1", 55443))
            # Also clear the voice outbox file to prevent immediate re-trigger on read
            if os.path.exists(self.voice_outbox):
                try:
                    with open(self.voice_outbox, "w", encoding="utf-8") as f:
                        f.write("")
                except Exception:
                    pass
            return True
        except Exception as e:
            self.logger.error(f"Error sending abort trigger: {e}")
            return False
