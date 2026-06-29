import subprocess
import json

def main():
    print("Searching for node processes...")
    try:
        out = subprocess.check_output([
            "powershell", 
            "-Command", 
            "Get-CimInstance Win32_Process -Filter \"name = 'node.exe'\" | Select-Object ProcessId, CommandLine | ConvertTo-Json"
        ])
        data = json.loads(out.decode("utf-8", errors="ignore"))
        if not isinstance(data, list):
            data = [data]
        for item in data:
            cmd = item.get('CommandLine') or ""
            print(f"FOUND PID: {item.get('ProcessId')}")
            print(f"  Cmd: {cmd}")
            print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
