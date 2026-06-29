import os
from playwright.sync_api import sync_playwright

def test_connect():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    if not os.path.exists(active_port_file):
        print(f"File not found: {active_port_file}")
        return
        
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
        
    if len(lines) < 2:
        print("Invalid DevToolsActivePort file content")
        return
        
    port = lines[0].strip()
    ws_path = lines[1].strip()
    ws_url = f"ws://127.0.0.1:{port}{ws_path}"
    print(f"Constructed WebSocket URL: {ws_url}")
    
    with sync_playwright() as p:
        try:
            print("Connecting...")
            browser = p.chromium.connect_over_cdp(ws_url)
            print("Connected successfully!")
            
            flow_page = None
            for context in browser.contexts:
                for page in context.pages:
                    print(f"Page URL: {page.url}")
                    if "labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47" in page.url:
                        flow_page = page
            if flow_page:
                print(f"Flow page found: {flow_page.title()}")
            else:
                print("Flow page NOT found")
                
            browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_connect()
