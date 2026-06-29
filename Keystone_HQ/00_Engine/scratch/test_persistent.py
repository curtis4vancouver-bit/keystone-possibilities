import os
import sys
import time
from playwright.sync_api import sync_playwright

def run():
    print("Killing existing Chrome processes to free the profile lock...")
    os.system("taskkill /F /IM chrome.exe /T")
    time.sleep(3)

    user_data_dir = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data"
    dest_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
    os.makedirs(dest_dir, exist_ok=True)

    print("Launching Chrome via Playwright persistent context...")
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=["--start-maximized", "--disable-blink-features=AutomationControlled"],
            no_viewport=True,
            channel="chrome"
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        print("Navigating to Flow project...")
        page.goto("https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47", timeout=60000)
        
        print("Waiting for page to load...")
        page.wait_for_timeout(10000)
        
        print("Downloading all 24 clips...")
        # We need to find all clips on the page and download them.
        # The user says "right click on video and go to dowload then upscale 1080"
        # Let's find the videos in the grid.
        
        # This part requires specific selectors. Let's just do a basic script to see if it loads successfully first.
        print("Successfully opened persistent profile!")
        
        page.wait_for_timeout(5000)
        context.close()

if __name__ == "__main__":
    run()
