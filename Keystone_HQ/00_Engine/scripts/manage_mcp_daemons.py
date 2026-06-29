import os
import sys
import time
import socket
import subprocess
import signal

# Force UTF-8 output on Windows to prevent encoding errors
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Port allocations
SERVERS = {
    "youtube-manager": {
        "script": "youtube_mcp.py",
        "port": 8001,
        "interpreter": "python"
    },
    "youtube-researcher": {
        "script": "youtube_researcher_mcp.py",
        "port": 8002,
        "interpreter": "python"
    },
    "content-engine": {
        "script": "content_engine_mcp.py",
        "port": 8003,
        "interpreter": "python"
    },
    "keystone-brain": {
        "script": "Qdrant_Brain/keystone_brain_v2_mcp.py",
        "port": 8004,
        "interpreter": "python"
    },
    "davinci-resolve-mcp": {
        "script": "davinci-resolve-mcp/src/resolve_mcp_server.py",
        "port": 8005,
        "interpreter": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\davinci-resolve-mcp\venv\Scripts\python.exe"
    }
}

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = r"C:\Users\Curtis\.gemini\antigravity\scratch\logs"

def check_port(port: int) -> bool:
    """Check if a port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:
            s.connect(("127.0.0.1", port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False

def kill_process_on_port(port: int):
    """Find and kill any process listening on the specified port on Windows."""
    try:
        output = subprocess.check_output("netstat -ano", shell=True, text=True)
        pids = set()
        for line in output.splitlines():
            if f":{port}" in line and ("LISTENING" in line or "127.0.0.1" in line or "0.0.0.0" in line):
                parts = line.strip().split()
                if len(parts) >= 5:
                    pids.add(parts[-1])
        
        for pid in pids:
            if pid != "0":
                print(f"[Supervisor] Port {port} occupied by PID {pid}. Terminating...")
                subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(0.5)
    except Exception as e:
        print(f"[Supervisor] Error checking/killing port {port}: {e}")

def run_supervisor():
    """Start all servers and supervise them in a blocking loop."""
    os.makedirs(LOG_DIR, exist_ok=True)
    print("[Supervisor] Starting background MCP SSE servers...")
    
    processes = {}
    log_files = {}
    
    # Clean up ports first
    for name, info in SERVERS.items():
        kill_process_on_port(info["port"])
        
    def spawn_server(name):
        info = SERVERS[name]
        port = info["port"]
        script_abs = os.path.join(WORKSPACE_ROOT, info["script"])
        interpreter = info["interpreter"]
        
        log_path = os.path.join(LOG_DIR, f"mcp_{name}.log")
        log_file = open(log_path, "w", encoding="utf-8", errors="replace")
        log_files[name] = log_file
        
        print(f"[Supervisor] Spawning '{name}' on port {port}...")
        cmd = [interpreter, script_abs, "sse", str(port)]
        
        p = subprocess.Popen(
            cmd,
            cwd=WORKSPACE_ROOT,
            stdout=log_file,
            stderr=log_file,
            env=os.environ.copy()
        )
        processes[name] = p

    # Initial spawn
    for name in SERVERS:
        try:
            spawn_server(name)
        except Exception as e:
            print(f"[Supervisor] Error spawning '{name}': {e}")
            
    # Verification wait
    time.sleep(4.0)
    for name, info in SERVERS.items():
        port = info["port"]
        if check_port(port):
            print(f"[Supervisor] ✅ '{name}' is active on port {port}.")
        else:
            print(f"[Supervisor] ❌ '{name}' failed to start on port {port}.")

    # Supervisor loop
    print("[Supervisor] Entering supervision loop. Press Ctrl+C to terminate.")
    
    try:
        while True:
            time.sleep(5.0)
            for name, p in list(processes.items()):
                poll = p.poll()
                if poll is not None:
                    print(f"[Supervisor] ⚠️ Server '{name}' (PID {p.pid}) exited with code {poll}. Restarting...")
                    # Close old log file
                    if name in log_files:
                        log_files[name].close()
                    # Re-spawn
                    try:
                        spawn_server(name)
                    except Exception as e:
                        print(f"[Supervisor] Error restarting '{name}': {e}")
    except (KeyboardInterrupt, SystemExit):
        print("[Supervisor] Shutdown signal received. Terminating all child processes...")
    finally:
        # Cleanup all processes on exit
        for name, p in processes.items():
            if p.poll() is None:
                print(f"[Supervisor] Terminating '{name}' (PID {p.pid})...")
                p.terminate()
                try:
                    p.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    p.kill()
            if name in log_files:
                log_files[name].close()
        print("[Supervisor] Cleanup complete. Exiting.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_mcp_daemons.py [start|status]")
        sys.exit(1)
        
    action = sys.argv[1].lower()
    if action == "start":
        run_supervisor()
    elif action == "status":
        print("[Supervisor Status Check]")
        all_healthy = True
        for name, info in SERVERS.items():
            port = info["port"]
            if check_port(port):
                print(f"  RUNNING: '{name}' on port {port}.")
            else:
                print(f"  STOPPED: '{name}' on port {port}.")
                all_healthy = False
        if not all_healthy:
            sys.exit(1)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)
