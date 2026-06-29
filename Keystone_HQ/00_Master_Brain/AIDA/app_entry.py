import os
import sys
import time
import threading
import subprocess

# Redirect stdout/stderr/stdin in windowed mode for logging and crash prevention
class DummyWriter:
    encoding = 'utf-8'
    errors = 'strict'
    def write(self, data): pass
    def flush(self): pass
    def isatty(self): return False
    def writable(self): return True
    def readable(self): return False
    def seekable(self): return False

class DummyReader:
    def read(self, *args, **kwargs): return ""
    def readline(self, *args, **kwargs): return ""
    def readlines(self, *args, **kwargs): return []
    def __iter__(self): return self
    def __next__(self): raise StopIteration

try:
    log_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AIDA"
    os.makedirs(log_dir, exist_ok=True)
    sys.stdout = open(os.path.join(log_dir, "aida_stdout.log"), "a", encoding="utf-8", buffering=1)
    sys.stderr = open(os.path.join(log_dir, "aida_stderr.log"), "a", encoding="utf-8", buffering=1)
    sys.stdout.write("LOG START: app_entry.py started\n")
    sys.stdout.flush()
except Exception:
    sys.stdout = DummyWriter()
    sys.stderr = DummyWriter()

if sys.stdin is None:
    sys.stdin = DummyReader()

# Add paths to sys.path so imports work correctly
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(base_dir)
sys.path.append(os.path.join(base_dir, "backend"))

def start_backend():
    import uvicorn
    # Import from backend.server
    try:
        from backend.server import app
    except ImportError:
        from server import app
    print("[AIDA App] Starting backend server on http://127.0.0.1:8421...")
    uvicorn.run(app, host="127.0.0.1", port=8421, log_level="warning")

def get_chrome_path():
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for p in chrome_paths:
        if os.path.exists(p):
            return p
    return "chrome.exe" # rely on PATH

if __name__ == '__main__':
    # 1. Start backend server in a daemon thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # Wait briefly for FastAPI to initialize
    time.sleep(1.5)
    
    # 2. Configure and launch Chrome in Standalone App Mode
    print("[AIDA App] Launching Chrome window in App Mode...")
    chrome_path = get_chrome_path()
    user_data_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "aida_chrome_profile")
    
    chrome_cmd = [
        chrome_path,
        "--app=http://127.0.0.1:8421",
        f"--user-data-dir={user_data_dir}",
        "--window-size=1340,820",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-session-crashed-bubble",
        "--disable-sync",
        "--new-window"
    ]
    
    try:
        chrome_process = subprocess.Popen(chrome_cmd)
        # Wait for Chrome process to close
        chrome_process.wait()
    except Exception as e:
        print(f"[AIDA App] Error launching or waiting for Chrome: {e}")
    
    # 3. Clean up background voice bridge process on window close
    print("[AIDA App] Shutting down Voice Bridge...")
    try:
        try:
            from backend.voice_bridge_api import VoiceBridgeAPI
        except ImportError:
            from voice_bridge_api import VoiceBridgeAPI
        VoiceBridgeAPI().stop_bridge()
    except Exception as e:
        print(f"[AIDA App] Error during cleanup: {e}")
