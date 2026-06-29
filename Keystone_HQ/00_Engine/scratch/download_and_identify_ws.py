import os
import sys
import time
import re
import glob
import shutil
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
    if not os.path.exists(active_port_file):
        raise FileNotFoundError(f"Chrome active port file not found at: {active_port_file}")
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
    # Check if it was created in the last 2 minutes
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
                
        if not flow_page:
            print("ERROR: Flow project page not found!")
            browser.close()
            return
            
        flow_page.bring_to_front()
        flow_page.wait_for_timeout(2000)
        
        # Get all video thumbnails in the feed
        thumbnails = flow_page.locator("a[href*='/edit/']").all()
        print(f"Found {len(thumbnails)} generated clips in the feed.")
        
        for i in range(len(thumbnails)):
            print(f"\nProcessing clip {i+1}/{len(thumbnails)}...")
            try:
                # Re-query to avoid stale elements
                current_thumbnails = flow_page.locator("a[href*='/edit/']").all()
                if i >= len(current_thumbnails):
                    continue
                thumb = current_thumbnails[i]
                
                # Click the thumbnail to open the side panel
                thumb.scroll_into_view_if_needed()
                flow_page.wait_for_timeout(500)
                thumb.click()
                flow_page.wait_for_timeout(2000) # Wait for side panel to load
                
                # The side panel should have the prompt text inside a specific container
                # Usually it's in a div or textarea. Let's get all text and match it.
                page_text = flow_page.evaluate("document.body.innerText")
                page_text_clean = " ".join(page_text.splitlines())
                
                matched_clip = None
                for clip_num, text in prompts.items():
                    # The exact text might be slightly different if it was fixed,
                    # so let's match a large chunk of it (e.g. first 50 chars of the actual unique part)
                    # Alternatively, since we know it's A1-A24, let's just find the best match
                    chunk = text[30:80].replace("Ana", "the woman")
                    chunk2 = text[-50:]
                    if chunk in page_text_clean or chunk2 in page_text_clean or text[:50] in page_text_clean:
                        matched_clip = clip_num
                        break
                        
                if not matched_clip:
                    # Try harder: maybe it's the exact text
                    for clip_num, text in prompts.items():
                        if text[:100] in page_text_clean:
                            matched_clip = clip_num
                            break
                            
                if matched_clip:
                    print(f"Matched to: CLIP A{matched_clip}!")
                    found_clips.append(matched_clip)
                    
                    # Now click the more options (3 dots) on the side panel header and click Download
                    # Or find a button with 'Download' text
                    dl_btn = flow_page.locator("button:has-text('Download')").first
                    if dl_btn.count() > 0:
                        dl_btn.click()
                        flow_page.wait_for_timeout(1000)
                        
                        # Click 1080p Upscaled
                        upscale_btn = flow_page.locator("span:has-text('1080p Upscaled')").first
                        if upscale_btn.count() > 0:
                            upscale_btn.click()
                            print(f"Downloading A{matched_clip} at 1080p...")
                            # Wait for download to finish
                            time.sleep(10)
                            
                            # Find the latest downloaded file
                            latest_file = get_latest_download()
                            if latest_file:
                                dest_path = os.path.join(dest_dir, f"A{matched_clip}.mp4")
                                shutil.move(latest_file, dest_path)
                                print(f"Successfully saved to {dest_path}")
                            else:
                                print("WARNING: Could not find downloaded file.")
                        else:
                            print("WARNING: 1080p Upscaled option not found.")
                    else:
                        print("WARNING: Download button not found on side panel.")
                else:
                    print("WARNING: Could not match this clip to A1-A24 based on text.")
                    
                # Close the side panel to return to the feed
                # There is usually a close button (X) or back arrow
                close_btn = flow_page.locator("button:has-text('Close'), button[aria-label='Close']").first
                if close_btn.count() > 0:
                    close_btn.click()
                else:
                    flow_page.keyboard.press("Escape")
                flow_page.wait_for_timeout(1000)
                
            except Exception as e:
                print(f"Error processing clip {i+1}: {e}")
                flow_page.keyboard.press("Escape")
                flow_page.wait_for_timeout(1000)
                
        # Determine missing clips
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
