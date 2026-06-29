import os
import sys
import time
import re
import glob
import shutil
from difflib import SequenceMatcher
from playwright.sync_api import sync_playwright

def parse_prompts(md_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    prompts = {}
    pattern = re.compile(r'### CLIP A(\d+).*?```(.*?)```', re.DOTALL)
    for match in pattern.finditer(content):
        clip_num = int(match.group(1))
        prompt_text = " ".join(match.group(2).strip().splitlines())
        prompts[clip_num] = prompt_text
    return prompts

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
    port = lines[0].strip()
    ws_path = lines[1].strip()
    return f"ws://127.0.0.1:{port}{ws_path}"

def get_latest_download():
    downloads_dir = r"C:\Users\Curtis\Downloads"
    mp4_files = glob.glob(os.path.join(downloads_dir, "*.mp4"))
    if not mp4_files:
        return None
    latest_file = max(mp4_files, key=os.path.getctime)
    if time.time() - os.path.getctime(latest_file) < 120:
        return latest_file
    return None

def run():
    md_file = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\MUSIC_002_ANA_STEVENSON_DJ_SET_V2.md"
    prompts = parse_prompts(md_file)
    
    ws_url = get_websocket_url()
    dest_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
    os.makedirs(dest_dir, exist_ok=True)
    
    found_clips = []
    
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
                
        flow_page.bring_to_front()
        flow_page.wait_for_timeout(2000)
        
        thumbnails = flow_page.locator("a[href*='/edit/']").all()
        print(f"Found {len(thumbnails)} generated clips in the feed.")
        
        for i in range(len(thumbnails)):
            print(f"\nProcessing clip {i+1}/{len(thumbnails)}...")
            try:
                current_thumbnails = flow_page.locator("a[href*='/edit/']").all()
                if i >= len(current_thumbnails): continue
                thumb = current_thumbnails[i]
                
                thumb.scroll_into_view_if_needed()
                flow_page.wait_for_timeout(500)
                thumb.click()
                flow_page.wait_for_timeout(2000) 
                
                # Get text from the side panel prompt text area
                # Flow usually has the prompt text in a div or paragraph
                # But document.body.innerText gets everything. Let's try to isolate it.
                # Actually, SequenceMatcher is robust even with extra UI text.
                page_text = flow_page.evaluate("document.body.innerText")
                page_text_clean = " ".join(page_text.splitlines())
                
                best_ratio = 0
                matched_clip = None
                
                for clip_num, text in prompts.items():
                    # We only care about the similarity of the text inside the page
                    # Let's find the substring in page_text that matches best
                    # SequenceMatcher is slow for large strings, so let's use a heuristic:
                    # check how many unique words from the prompt are in the page text
                    words = set(text.split())
                    page_words = set(page_text_clean.split())
                    overlap = len(words.intersection(page_words))
                    
                    if overlap > best_ratio:
                        best_ratio = overlap
                        matched_clip = clip_num
                        
                if matched_clip:
                    print(f"Matched to: CLIP A{matched_clip}! (Score: {best_ratio})")
                    found_clips.append(matched_clip)
                    
                    # DOWNLOAD LOGIC
                    # Look for 3-dots "More options" inside the side panel
                    # Usually the side panel is a <div role="dialog"> or similar
                    panel = flow_page.locator("[role='dialog']").last
                    if panel.count() == 0:
                        panel = flow_page.locator("body")
                        
                    more_btn = panel.locator("button:has-text('More options'), button[aria-label='More options']").first
                    if more_btn.count() > 0:
                        more_btn.click()
                        flow_page.wait_for_timeout(1000)
                        
                        dl_menu = flow_page.locator("li:has-text('Download'), [role='menuitem']:has-text('Download')").first
                        if dl_menu.count() > 0:
                            dl_menu.hover()
                            flow_page.wait_for_timeout(500)
                            upscale = flow_page.locator("li:has-text('1080p Upscaled'), [role='menuitem']:has-text('1080p Upscaled')").first
                            if upscale.count() > 0:
                                upscale.click()
                                print(f"Downloading A{matched_clip} at 1080p...")
                                time.sleep(12)
                                
                                latest_file = get_latest_download()
                                if latest_file:
                                    dest_path = os.path.join(dest_dir, f"A{matched_clip}.mp4")
                                    shutil.move(latest_file, dest_path)
                                    print(f"Successfully saved to {dest_path}")
                                else:
                                    print("WARNING: Download failed or took too long.")
                            else:
                                print("WARNING: 1080p Upscaled option not found in menu.")
                                # Maybe clicking "Download" directly downloads it?
                                dl_menu.click()
                                time.sleep(12)
                        else:
                            print("WARNING: Download menu item not found.")
                    else:
                        print("WARNING: More options button not found.")
                else:
                    print("WARNING: Could not match this clip.")
                    
                # Close panel
                close_btn = flow_page.locator("button:has-text('Close'), button[aria-label='Close'], button[aria-label='Go Back']").first
                if close_btn.count() > 0:
                    close_btn.click()
                else:
                    flow_page.keyboard.press("Escape")
                flow_page.wait_for_timeout(1000)
                
            except Exception as e:
                print(f"Error processing clip {i+1}: {e}")
                flow_page.keyboard.press("Escape")
                flow_page.wait_for_timeout(1000)
                
        all_clips = set(range(1, 25))
        missing = sorted(list(all_clips - set(found_clips)))
        print("\n==========================================")
        print(f"FINISHED PROCESSING. Found {len(found_clips)} clips.")
        print(f"SUCCESSFUL CLIPS: {sorted(found_clips)}")
        print(f"MISSING CLIPS (Failed): {missing}")
        print("==========================================")
        
        browser.close()

if __name__ == "__main__":
    run()
