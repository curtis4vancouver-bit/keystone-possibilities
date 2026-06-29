import asyncio
import json
import os
import requests
from playwright.async_api import async_playwright

NOTEBOOKLM_URL = "https://notebooklm.google.com"
CDP_PORT = 9222 # Standard CDP port

async def extract_notebooklm_cookies():
    """Extracts Google session cookies using CDP without launching a new visible browser."""
    print(f"Attempting to connect to Chrome CDP on port {CDP_PORT}...")
    
    try:
        async with async_playwright() as p:
            # Connect to the existing Chrome instance
            browser = await p.chromium.connect_over_cdp(f"http://localhost:{CDP_PORT}")
            context = browser.contexts[0]
            
            # Get all cookies for NotebookLM
            cookies = await context.cookies([NOTEBOOKLM_URL])
            
            # Extract the specific authentication cookies needed for batchexecute
            auth_cookies = {c['name']: c['value'] for c in cookies if 'SID' in c['name'] or 'OSID' in c['name']}
            
            if not auth_cookies:
                print("Error: Could not find Google authentication cookies. Ensure you are logged into NotebookLM in Chrome.")
                return None
                
            cookie_string = "; ".join([f"{k}={v}" for k, v in auth_cookies.items()])
            print("Successfully extracted NotebookLM session cookies via CDP.")
            return cookie_string
            
    except Exception as e:
        print(f"CDP Connection Failed: {e}")
        print("Make sure Chrome is running with the flag: --remote-debugging-port=9222")
        return None

def trigger_batchexecute_rpc(cookie_string, notebook_id):
    """Fires a direct backend RPC call to NotebookLM to force an update/sync."""
    print(f"Triggering background RPC sync for Notebook ID: {notebook_id}...")
    
    headers = {
        "cookie": cookie_string,
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "origin": NOTEBOOKLM_URL,
        "referer": f"{NOTEBOOKLM_URL}/notebook/{notebook_id}"
    }
    
    # Internal Google batchexecute payload structure for forcing a source refresh
    # This bypasses the UI and talks directly to the NotebookLM backend
    payload = f'f.req=[[["NotebookService.SyncSources","[\\"{notebook_id}\\"]",null,"generic"]]]'
    
    try:
        response = requests.post(
            f"{NOTEBOOKLM_URL}/_/NotebookService/data/batchexecute",
            headers=headers,
            data=payload
        )
        if response.status_code == 200:
            print("Successfully triggered background sync. NotebookLM is updating instantly.")
            return True
        else:
            print(f"Failed to trigger sync. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"RPC Call failed: {e}")
        return False

async def main():
    print("--- NotebookLM Instant Sync (CDP + RPC) ---")
    
    cookie_string = await extract_notebooklm_cookies()
    if not cookie_string:
        return
        
    # The Notebook ID for the "Keystone Master Brain" Notebook
    # Extracted from the brain_drive_sync SKILL.md
    NOTEBOOK_ID = "a0d3ba69-e793-43e2-9e0b-f3cbc03abccf"
    
    trigger_batchexecute_rpc(cookie_string, NOTEBOOK_ID)

if __name__ == "__main__":
    asyncio.run(main())
