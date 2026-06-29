import os
import time
import subprocess

def main():
    print("Killing existing Chrome processes...")
    os.system("taskkill /F /IM chrome.exe /T")
    time.sleep(3)
    
    print("Starting Chrome with remote debugging on port 9222...")
    # Launch Chrome with --remote-debugging-port=9222 and --remote-allow-origins=*
    # Use standard Chrome path
    chrome_cmd = 'start "" "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --restore-last-session'
    subprocess.Popen(chrome_cmd, shell=True)
    time.sleep(5)
    
    print("Chrome started!")
    # Check if DevToolsActivePort exists and print it
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    if os.path.exists(active_port_file):
        with open(active_port_file, "r") as f:
            print("DevToolsActivePort content:")
            print(f.read())
    else:
        print("Warning: DevToolsActivePort file not found.")

if __name__ == "__main__":
    main()
