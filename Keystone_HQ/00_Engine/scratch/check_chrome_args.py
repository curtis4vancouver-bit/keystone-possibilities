import subprocess

try:
    out = subprocess.check_output("wmic process where name='chrome.exe' get commandline", shell=True)
    lines = out.decode("utf-8", errors="ignore").splitlines()
    for line in lines:
        line = line.strip()
        if line and "remote-debugging-port" in line:
            print(line[:200]) # Print first 200 chars of matching processes
except Exception as e:
    print(f"Error checking processes: {e}")
