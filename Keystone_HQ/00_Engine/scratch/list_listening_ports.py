import subprocess
import json
import re

def main():
    print("Finding listening TCP connections...")
    netstat_out = subprocess.check_output("netstat -ano", shell=True).decode("utf-8", errors="ignore")
    listening_pids = {}
    for line in netstat_out.splitlines():
        if "LISTENING" in line:
            # Match local address and PID
            parts = line.strip().split()
            if len(parts) >= 4:
                addr = parts[1]
                pid = int(parts[-1])
                # Extract port from local address
                port_match = re.search(r':(\d+)$', addr)
                if port_match:
                    port = int(port_match.group(1))
                    listening_pids[pid] = port

    print(f"Found {len(listening_pids)} listening PIDs.")

    print("Querying Chrome processes via PowerShell...")
    ps_cmd = 'powershell -Command "Get-CimInstance Win32_Process -Filter \\"name=\'chrome.exe\'\\" | Select-Object ProcessId, CommandLine | ConvertTo-Json"'
    try:
        ps_out = subprocess.check_output(ps_cmd, shell=True).decode("utf-8", errors="ignore")
        if ps_out.strip():
            processes = json.loads(ps_out)
            if not isinstance(processes, list):
                processes = [processes]
            for p in processes:
                pid = p.get("ProcessId")
                cmd = p.get("CommandLine", "")
                if pid in listening_pids:
                    print(f"MATCH: PID {pid} is listening on Port {listening_pids[pid]}")
                    print(f"  Command: {cmd}")
                else:
                    # Let's search if any of its parent/child is listening or if it has debugging port in cmd
                    if "remote-debugging-port" in (cmd or ""):
                        print(f"INFO: PID {pid} has remote-debugging-port in command line, but not directly listening. Command: {cmd}")
        else:
            print("No chrome.exe processes returned by PowerShell.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
