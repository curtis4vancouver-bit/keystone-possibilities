import os
import sys
import time
from playwright.sync_api import sync_playwright

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    if not os.path.exists(active_port_file):
        raise FileNotFoundError(f"Chrome active port file not found at: {active_port_file}")
        
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
        
    port = lines[0].strip()
    ws_path = lines[1].strip()
    return f"ws://127.0.0.1:{port}{ws_path}"

def run():
    ws_url = get_websocket_url()
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url)
        
        flow_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47" in page.url:
                    flow_page = page
                    break
            if flow_page:
                break
                
        if not flow_page:
            print("ERROR: Flow project page not found!")
            browser.close()
            return
            
        flow_page.bring_to_front()
        
        while True:
            # Query for the first available Reuse Prompt button
            reuse_btn = flow_page.locator("button:has-text('Reuse Prompt')").first
            if reuse_btn.count() == 0:
                print("No more failed prompts found!")
                break
                
            print("\n==========================================")
            print("RETRYING A FAILED CLIP...")
            print("==========================================")
            
            # Click Reuse Prompt
            print("Clicking Reuse Prompt...")
            reuse_btn.click()
            flow_page.wait_for_timeout(1000)
            
            # Now delete that specific failed alert so it doesn't loop
            # The delete button is usually right next to reuse prompt
            try:
                # Find the parent div or alert and click its delete button
                parent_alert = flow_page.locator("button:has-text('Reuse Prompt')").first.locator("..")
                del_btn = parent_alert.locator("button:has-text('Delete')").first
                if del_btn.count() > 0:
                    del_btn.click()
                    flow_page.wait_for_timeout(1000)
                else:
                    # Fallback just click the first delete button visible
                    flow_page.locator("button:has-text('Delete')").first.click()
                    flow_page.wait_for_timeout(1000)
            except Exception as e:
                print("Could not delete alert:", e)
            
            editor = flow_page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=5000)
            old_text = editor.inner_text()
            
            # Fix the prompt
            new_text = old_text.replace("Ana", "the woman").replace("Pioneer", "professional").replace("Ana's", "the woman's")
            
            print("Fixing prompt text...")
            editor.focus()
            flow_page.keyboard.press("Control+A")
            flow_page.keyboard.press("Backspace")
            flow_page.wait_for_timeout(400)
            
            editor.type(new_text)
            flow_page.wait_for_timeout(800)
            
            print("Opening characters dialog...")
            plus_btn = None
            for b in flow_page.locator("button").all():
                t = b.inner_text() or ""
                if "add_2" in t and "Create" in t:
                    plus_btn = b
                    break
            if plus_btn:
                plus_btn.click()
                flow_page.wait_for_timeout(1000)
                
                dialog = flow_page.locator("[role='dialog']").first
                dialog.wait_for(state="visible", timeout=5000)
                
                char_tab = dialog.locator("[role='tab']:has-text('Characters')").first
                char_tab.wait_for(state="visible", timeout=5000)
                if char_tab.get_attribute("aria-selected") != "true":
                    char_tab.click()
                    flow_page.wait_for_timeout(600)
                    
                print("Selecting Ana Stevenson character image...")
                ana_img = dialog.locator("img[alt*='Ana'], img[src*='ee567222-dec2']").first
                if ana_img.count() > 0:
                    ana_img.click()
                    flow_page.wait_for_timeout(600)
                    
                    add_btn = dialog.locator("button:has-text('Add to Prompt')").first
                    add_btn.wait_for(state="visible", timeout=5000)
                    add_btn.click()
                    flow_page.wait_for_timeout(1000)
            
            print("Locating Create submit button...")
            submit_btn = None
            for b in flow_page.locator("button").all():
                t = b.inner_text() or ""
                if "arrow_forward" in t and "Create" in t:
                    submit_btn = b
                    break
                    
            if submit_btn and submit_btn.is_disabled():
                flow_page.wait_for_timeout(2000)
                
            if submit_btn and not submit_btn.is_disabled():
                print("Clicking Create submit button...")
                submit_btn.click()
                print("SUCCESS: Resubmitted failed clip!")
            else:
                print("ERROR: Create button remained disabled!")
                
            time.sleep(8)

        print("\nAll failed prompts have been fixed and resubmitted!")
        browser.close()

if __name__ == "__main__":
    run()
