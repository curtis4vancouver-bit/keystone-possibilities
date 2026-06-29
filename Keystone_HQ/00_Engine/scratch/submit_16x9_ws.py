import os
import sys
import time
import re
from playwright.sync_api import sync_playwright

def parse_prompts(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    prompts = {}
    
    # Matches ### CLIP A<num> ... followed by a codeblock
    pattern = re.compile(r'### CLIP A(\d+).*?```(.*?)```', re.DOTALL)
    for match in pattern.finditer(content):
        clip_num = int(match.group(1))
        prompt_text = match.group(2).strip()
        # Remove linebreaks within the prompt to make it a single continuous paragraph
        prompt_text = " ".join(prompt_text.splitlines())
        prompts[clip_num] = prompt_text
        
    return prompts

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    if not os.path.exists(active_port_file):
        raise FileNotFoundError(f"Chrome active port file not found at: {active_port_file}")
        
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
        
    if len(lines) < 2:
        raise ValueError("Invalid DevToolsActivePort file format")
        
    port = lines[0].strip()
    ws_path = lines[1].strip()
    return f"ws://127.0.0.1:{port}{ws_path}"

def run():
    md_file = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\MUSIC_002_ANA_STEVENSON_DJ_SET_V2.md"
    prompts = parse_prompts(md_file)
    print(f"Parsed {len(prompts)} prompts from markdown file.")
    
    if len(prompts) == 0:
        print("ERROR: No prompts found.")
        return

    ws_url = get_websocket_url()
    print(f"Connecting to Chrome via WebSocket: {ws_url}...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(ws_url)
            print("Connected!")
        except Exception as e:
            print(f"FAILED to connect: {e}")
            return
            
        print("Searching for Google Flow project page...")
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
            
        print(f"Found Page: {flow_page.url}")
        flow_page.bring_to_front()
        
        for clip_num, text in sorted(prompts.items()):
            print(f"\n==========================================")
            print(f"SUBMITTING CLIP A{clip_num}...")
            print(f"==========================================")
            
            # Click prompt box to focus
            print("Focusing prompt textbox...")
            editor = flow_page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=10000)
            editor.focus()
            
            # Clear text
            print("Clearing textbox...")
            flow_page.keyboard.press("Control+A")
            flow_page.keyboard.press("Backspace")
            flow_page.wait_for_timeout(400)
            
            # Type prompt text
            print("Typing prompt...")
            editor.type(text)
            flow_page.wait_for_timeout(800)
            
            # Click "+ Create" button (Ingredients / Characters dialog)
            print("Opening characters dialog...")
            plus_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "add_2" in t and "Create" in t:
                    plus_btn = btn
                    break
            if not plus_btn:
                print("ERROR: + Create button not found!")
                continue
            plus_btn.click()
            flow_page.wait_for_timeout(1000)
            
            # Wait for dialog and select Characters tab
            dialog = flow_page.locator("[role='dialog']").first
            dialog.wait_for(state="visible", timeout=5000)
            
            char_tab = dialog.locator("[role='tab']:has-text('Characters')").first
            char_tab.wait_for(state="visible", timeout=5000)
            char_tab_selected = char_tab.get_attribute("aria-selected")
            if char_tab_selected != "true":
                print("Clicking Characters tab...")
                char_tab.click()
                flow_page.wait_for_timeout(600)
                
            # Select Ana Stevenson's image card inside modal
            print("Selecting Ana Stevenson character image...")
            ana_img = dialog.locator("img[alt*='Ana'], img[src*='ee567222-dec2']").first
            ana_img.wait_for(state="visible", timeout=5000)
            ana_img.click()
            flow_page.wait_for_timeout(600)
            
            # Click Add to Prompt
            print("Clicking Add to Prompt...")
            add_btn = dialog.locator("button:has-text('Add to Prompt')").first
            add_btn.wait_for(state="visible", timeout=5000)
            add_btn.click()
            flow_page.wait_for_timeout(1000) 
            
            # Locate and click submit Create button
            print("Locating Create submit button...")
            submit_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "arrow_forward" in t and "Create" in t:
                    submit_btn = btn
                    break
                    
            if not submit_btn:
                print("ERROR: Create submit button not found!")
                continue
                
            if submit_btn.is_disabled():
                print("WARNING: Create button is disabled! Waiting for state sync...")
                flow_page.wait_for_timeout(2000)
                
            if submit_btn.is_disabled():
                print("ERROR: Create button remained disabled! React state desync.")
                continue
                
            print("Clicking Create submit button...")
            submit_btn.click()
            print(f"SUCCESS: Submitted clip A{clip_num}!")
            
            # Wait 8 seconds before next prompt to let queueing register
            time.sleep(8)

        print("\nAll 24 clips successfully queued!")
        browser.close()

if __name__ == "__main__":
    run()
