import os
import time
import psutil
import subprocess

def main():
    print("Finding all chrome processes...")
    killed_count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                print(f"Killing process {proc.info['pid']} ({proc.info['name']})...")
                proc.kill()
                killed_count += 1
        except Exception as e:
            print(f"Failed to kill {proc.info['pid']}: {e}")
            
    print(f"Killed {killed_count} chrome processes.")
    time.sleep(5) # Wait for OS to clean up socket and lock handles
    
    user_data_dir = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data"
    lock_files = [
        os.path.join(user_data_dir, "lock"),
        os.path.join(user_data_dir, "SingletonLock"),
        os.path.join(user_data_dir, "Default", "SingletonLock"),
        os.path.join(user_data_dir, "Default", "lock"),
    ]
    
    for filepath in lock_files:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"Deleted lock file: {filepath}")
            except Exception as e:
                print(f"Failed to delete lock file {filepath}: {e}")
                
    print("Starting Chrome in remote debugging mode...")
    chrome_cmd = 'start "" "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --remote-allow-origins=* --restore-last-session'
    subprocess.Popen(chrome_cmd, shell=True)
    time.sleep(5)
    
    print("Done restarting.")
    if os.path.exists(os.path.join(user_data_dir, "DevToolsActivePort")):
        with open(os.path.join(user_data_dir, "DevToolsActivePort"), "r") as f:
            print("DevToolsActivePort:")
            print(f.read())

if __name__ == "__main__":
    main()
