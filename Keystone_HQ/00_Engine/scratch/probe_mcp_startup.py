import subprocess
import time
import sys

def probe():
    cmd = ["node", "c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\10_Vector_DB_Architecture\\brain_feeder\\mcp_server.js"]
    print("Starting node process...")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Wait a few seconds for initialization
    time.sleep(3)
    
    # Kill the process
    process.terminate()
    
    # Read stdout and stderr
    stdout_lines = []
    stderr_lines = []
    
    # Poll outputs
    try:
        stdout, stderr = process.communicate(timeout=2)
        stdout_lines = stdout.splitlines()
        stderr_lines = stderr.splitlines()
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        stdout_lines = stdout.splitlines()
        stderr_lines = stderr.splitlines()
        
    print("\n--- CAPTURED STDOUT ---")
    for i, line in enumerate(stdout_lines):
        print(f"STDOUT[{i}]: {repr(line)}")
        
    print("\n--- CAPTURED STDERR ---")
    for i, line in enumerate(stderr_lines):
        print(f"STDERR[{i}]: {repr(line)}")

if __name__ == "__main__":
    probe()
