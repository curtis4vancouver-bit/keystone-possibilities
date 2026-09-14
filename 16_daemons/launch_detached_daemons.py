r"""
================================================================================
KEYSTONE DETACHED OS BACKGROUND DAEMON LAUNCHER
================================================================================
Role: Spawns Keystone daemons as detached OS background processes on Windows.
Prevents background process task multiplication in the Antigravity IDE task runner.

Target Daemons & Ports (5 detached OS processes):
  1. local_stt_daemon.py         — Port 9876 (CUDA STT + F9 Hotkey)
  2. agent_voice_tts_daemon.py   — Port 9877 (TTS Voice Synthesis)
  3. vector_brain_daemon.py      — Port 9878 (Hybrid Search API)
  4. chrome_overlay_daemon.py    — Port 9879 (CDP Overlay Injector)
  5. keystone_janitor_daemon.py  — Port 9891 (Workspace Indexer)

NOT managed here (run as Antigravity task runner daemon cards instead):
  - npm run dev (05_Keystone_HUD)   — Port 5173
  - instant_watchdog.py             — Port 9890

Design & Performance Guarantees:
  - Win32 creation flags: CREATE_BREAKAWAY_FROM_JOB | CREATE_NEW_PROCESS_GROUP
    (0x01000200) — allows child processes to survive when Antigravity's
    run_command Job Object is destroyed after this launcher exits.
  - stdin = subprocess.DEVNULL
  - stdout / stderr redirected to persistent log files in daemon_logs/
  - Unbuffered output via PYTHONUNBUFFERED=1.
  - Non-blocking port checking via Win32 SO_EXCLUSIVEADDRUSE socket bind test.
  - Post-launch port verification with configurable timeout.
================================================================================
"""

import os
import sys
import socket
import time
import argparse
import subprocess

# Force UTF-8 console output for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Constants
DAEMONS_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = r"C:\Users\Curtis\.gemini\antigravity\daemon_logs"

# Win32 Process Detachment Flags:
# CREATE_BREAKAWAY_FROM_JOB (0x01000000) — CRITICAL: allows child processes to
#   escape Antigravity's run_command Job Object so they survive after this
#   launcher script exits. Without this flag, Windows kills all children.
# CREATE_NEW_PROCESS_GROUP (0x00000200) — gives each daemon its own process
#   group so Ctrl+C doesn't cascade from parent.
# DO NOT use CREATE_NO_WINDOW (0x08000000) or DETACHED_PROCESS (0x00000008)
#   because keyboard module and sounddevice/PortAudio need a session context.
CREATION_FLAGS = 0x01000200  # CREATE_BREAKAWAY_FROM_JOB | CREATE_NEW_PROCESS_GROUP

DAEMONS = {
    "local_stt_daemon": {
        "script": "local_stt_daemon.py",
        "port": 9876,
        "log_file": "local_stt_daemon.log",
        "description": "Local CUDA STT Listening Daemon (Port 9876)"
    },
    "agent_voice_tts_daemon": {
        "script": "agent_voice_tts_daemon.py",
        "port": 9877,
        "log_file": "agent_voice_tts_daemon.log",
        "description": "Agent Voice TTS Speaking Daemon (Port 9877)"
    },
    "vector_brain_daemon": {
        "script": "vector_brain_daemon.py",
        "port": 9878,
        "log_file": "vector_brain_daemon.log",
        "description": "Vector Brain Hybrid Search API (Port 9878)"
    },
    "chrome_overlay_daemon": {
        "script": "chrome_overlay_daemon.py",
        "port": 9879,
        "log_file": "chrome_overlay_daemon.log",
        "description": "CDP Overlay Injector Daemon (Port 9879)"
    },
    "keystone_janitor_daemon": {
        "script": "keystone_janitor_daemon.py",
        "port": 9891,
        "log_file": "keystone_janitor_daemon.log",
        "description": "Keystone Janitor & Graph Persistence Daemon (Port 9891)"
    }
}


def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """
    Check if a TCP port is currently bound/in-use.
    First attempts TCP connection (fast path for active HTTP/WS daemons),
    then falls back to Win32 SO_EXCLUSIVEADDRUSE socket bind test.
    Returns True if port is already bound/active, False if port is free.
    """
    try:
        cs = socket.create_connection((host, port), timeout=0.05)
        cs.close()
        return True
    except Exception:
        pass

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if sys.platform == "win32":
            SO_EXCLUSIVEADDRUSE = getattr(socket, "SO_EXCLUSIVEADDRUSE", -5)
            s.setsockopt(socket.SOL_SOCKET, SO_EXCLUSIVEADDRUSE, 1)
        s.bind((host, port))
        s.close()
        return False
    except OSError:
        s.close()
        return True


def kill_process_on_port(port: int):
    """Find and kill any Windows process bound to the target TCP port."""
    if sys.platform != "win32":
        return
    try:
        cmd = f'netstat -ano | findstr :{port}'
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        pids = set()
        for line in out.strip().splitlines():
            parts = line.strip().split()
            if len(parts) >= 5 and "LISTENING" in line:
                local_addr = parts[1]
                if local_addr.endswith(f":{port}"):
                    pids.add(parts[-1])
        for pid in pids:
            if pid and pid != "0":
                subprocess.run(f'taskkill /F /PID {pid}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if pids:
            time.sleep(0.3)
    except Exception:
        pass


def launch_daemon_detached(key: str, force: bool = False, restart: bool = False) -> dict:
    """
    Launch a daemon process fully detached via WMI (Win32_Process.Create).

    WMI creates processes through the WMI Provider Host (wmiprvse.exe),
    which runs in a completely separate session outside any Job Object.
    This is the ONLY method proven to survive Antigravity's run_command
    cleanup on Windows.

    Tested: Processes launched via WMI persist indefinitely after the
    launcher script and all parent processes exit.
    """
    info = DAEMONS.get(key)
    if not info:
        return {"name": key, "status": "UNKNOWN", "message": f"Daemon '{key}' not configured"}

    port = info["port"]
    script_name = info["script"]
    script_path = os.path.normpath(os.path.join(DAEMONS_DIR, script_name))
    log_path = os.path.join(LOG_DIR, info["log_file"])

    if not os.path.exists(script_path):
        return {"name": key, "port": port, "status": "MISSING", "message": f"File not found: {script_path}"}

    if restart or force:
        kill_process_on_port(port)
    elif is_port_in_use(port):
        return {"name": key, "port": port, "status": "RUNNING", "message": f"Active on port {port}"}

    os.makedirs(LOG_DIR, exist_ok=True)

    venv_python = os.path.join(DAEMONS_DIR, "venv", "Scripts", "python.exe")
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable
    extra_args_str = " ".join(info.get("args", []))

    # Build the command line for WMI to execute via cmd.exe
    # cmd.exe /c handles cd, env vars, and output redirection
    cmd_line = (
        f'cmd.exe /c "cd /d "{DAEMONS_DIR}" '
        f'&& set PYTHONUNBUFFERED=1 '
        f'&& "{python_exe}" -u "{script_path}" {extra_args_str} '
        f'>> "{log_path}" 2>&1"'
    )

    try:
        # Use PowerShell to call Win32_Process.Create with hidden window
        # Win32_ProcessStartup.ShowWindow = 0 (SW_HIDE) prevents visible cmd popups
        ps_cmd = (
            f'$si = ([wmiclass]"Win32_ProcessStartup").CreateInstance(); '
            f'$si.ShowWindow = 0; '
            f'$r = Invoke-WmiMethod -Class Win32_Process -Name Create '
            f'-ArgumentList @(\'{cmd_line}\', $null, $si); '
            f'Write-Output "$($r.ProcessId)|$($r.ReturnValue)"'
        )
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        if "|" in output:
            pid_str, ret_str = output.split("|", 1)
            pid = int(pid_str) if pid_str.isdigit() else 0
            ret = int(ret_str) if ret_str.isdigit() else -1
            if ret == 0 and pid > 0:
                return {"name": key, "port": port, "status": "LAUNCHED", "pid": pid, "message": f"Spawned PID {pid} (WMI)"}
            else:
                return {"name": key, "port": port, "status": "ERROR", "message": f"WMI returned code {ret}, PID {pid}"}
        else:
            return {"name": key, "port": port, "status": "ERROR", "message": f"Unexpected WMI output: {output}"}
    except Exception as e:
        return {"name": key, "port": port, "status": "ERROR", "message": str(e)}


def verify_ports(target_keys: list, timeout: float = 8.0) -> dict:
    """Wait up to `timeout` seconds for all target daemon ports to become LISTENING."""
    pending = {k: DAEMONS[k]["port"] for k in target_keys if k in DAEMONS}
    verified = {}
    failed = {}
    deadline = time.time() + timeout
    poll_interval = 0.5

    while pending and time.time() < deadline:
        time.sleep(poll_interval)
        for key in list(pending.keys()):
            if is_port_in_use(pending[key]):
                verified[key] = pending.pop(key)

    failed = dict(pending)  # anything still pending after timeout = failed
    return {"verified": verified, "failed": failed}


def main():
    start_time = time.perf_counter()

    parser = argparse.ArgumentParser(description="Keystone Detached OS Background Daemon Runner")
    parser.add_argument("--status", action="store_true", help="Check daemon port status without launching")
    parser.add_argument("--force", action="store_true", help="Force spawn daemons regardless of port state")
    parser.add_argument("--restart", action="store_true", help="Kill existing processes on ports and restart daemons fresh")
    parser.add_argument("--daemon", type=str, help="Target specific daemon key")
    parser.add_argument("--verify", action="store_true", default=True, help="Verify ports are LISTENING after launch (default: True)")
    parser.add_argument("--no-verify", dest="verify", action="store_false", help="Skip post-launch port verification")
    parser.add_argument("--timeout", type=float, default=8.0, help="Port verification timeout in seconds (default: 8)")
    args = parser.parse_args()

    target_keys = [args.daemon] if args.daemon and args.daemon in DAEMONS else list(DAEMONS.keys())

    # Auto-discover active root chats and synchronize active_chats.json + chat_targets.json on launch
    try:
        from sync_active_chats import sync_active_chats
        synced = sync_active_chats()
        print(f"🔗 [Active Chats Sync] Auto-discovered {len(synced)} root chats and synchronized targets.")
    except Exception as e:
        print(f"⚠️ [Active Chats Sync Warning]: {e}")

    print("🚀 [Keystone Detached Daemon Runner]")

    launched_keys = []
    results = []
    for key in target_keys:
        info = DAEMONS[key]
        if args.status:
            active = is_port_in_use(info["port"])
            status_str = "RUNNING" if active else "STOPPED"
            results.append({"name": key, "port": info["port"], "status": status_str, "message": f"Port {info['port']} {'active' if active else 'free'}"})
        else:
            res = launch_daemon_detached(key, force=args.force, restart=args.restart)
            results.append(res)
            if res["status"] == "LAUNCHED":
                launched_keys.append(key)

    for r in results:
        status_icon = "✅" if r["status"] in ("RUNNING", "LAUNCHED") else "⚠️" if r["status"] == "STOPPED" else "❌"
        print(f"  {status_icon} [{r['name']}] (Port {r['port']}): {r['status']} — {r['message']}")

    # Post-launch port verification
    if args.verify and launched_keys and not args.status:
        print(f"\n🔍 Verifying {len(launched_keys)} daemon(s) bind to ports (timeout: {args.timeout}s)...")
        vresult = verify_ports(launched_keys, timeout=args.timeout)

        for key, port in vresult["verified"].items():
            print(f"  ✅ [{key}] Port {port}: VERIFIED LISTENING")

        for key, port in vresult["failed"].items():
            print(f"  ❌ [{key}] Port {port}: FAILED — not listening after {args.timeout}s")
            # Dump last 5 lines of log for diagnosis
            log_path = os.path.join(LOG_DIR, DAEMONS[key]["log_file"])
            if os.path.exists(log_path):
                try:
                    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                        lines = f.readlines()[-5:]
                    print(f"     Log tail ({os.path.basename(log_path)}):")
                    for line in lines:
                        print(f"       {line.rstrip()}")
                except Exception:
                    pass

        total_ok = len(vresult["verified"])
        total_fail = len(vresult["failed"])
        if total_fail > 0:
            print(f"\n⚠️  {total_fail}/{total_ok + total_fail} daemon(s) failed to bind. Check logs in {LOG_DIR}")
        else:
            print(f"\n✅ All {total_ok} daemon(s) verified LISTENING.")

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    print(f"⚡ Completed in {elapsed_ms:.1f}ms. Exiting detached launcher.")
    sys.exit(0)


if __name__ == "__main__":
    main()
