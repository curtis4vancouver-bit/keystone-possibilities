import sys
import os
from playwright.sync_api import sync_playwright

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    if not os.path.exists(active_port_file):
        raise FileNotFoundError(f"DevToolsActivePort file not found at {active_port_file}")
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
    port = lines[0].strip()
    ws_path = lines[1].strip()
    return f"ws://127.0.0.1:{port}{ws_path}"

def main():
    try:
        ws_url = get_websocket_url()
        print(f"Connecting to WS URL: {ws_url}")
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws_url)
            print(f"Connected! Contexts: {len(browser.contexts)}")
            for c_idx, context in enumerate(browser.contexts):
                print(f"Context {c_idx} has {len(context.pages)} pages:")
                for p_idx, page in enumerate(context.pages):
                    print(f"  Page {p_idx}: URL={page.url} Title={page.title()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
