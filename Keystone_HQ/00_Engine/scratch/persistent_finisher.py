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

def get_latest_download(after_time):
    downloads_dir = r"C:\Users\Curtis\Downloads"
    mp4_files = glob.glob(os.path.join(downloads_dir, "*.mp4"))
    if not mp4_files:
        return None
    latest_file = max(mp4_files, key=os.path.getctime)
    if os.path.getctime(latest_file) > after_time:
        return latest_file
    return None

def run_davinci_assembly():
    print("Starting DaVinci Resolve Assembly...")
    os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    
    modules_path = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
    if modules_path not in sys.path:
        sys.path.append(modules_path)

    try:
        import DaVinciResolveScript as dvr
        resolve = dvr.scriptapp("Resolve")
        if not resolve:
            print("ERROR: Resolve not open")
            return
            
        pm = resolve.GetProjectManager()
        project = pm.GetCurrentProject()
        media_pool = project.GetMediaPool()
        
        media_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
        files = []
        for i in range(1, 25):
            fpath = os.path.join(media_dir, f"A{i}.mp4")
            if os.path.exists(fpath):
                files.append(fpath)
                
        if not files:
            print("No files found!")
            return
            
        media_items = media_pool.ImportMediaFiles(files)
        
        def get_num(name):
            match = re.match(r'^A(\d+)\.mp4$', name)
            return int(match.group(1)) if match else 999
            
        media_items.sort(key=lambda x: get_num(x.GetName()))
        
        timeline = media_pool.CreateEmptyTimeline("Auto_Assembly_Music_002")
        project.SetCurrentTimeline(timeline)
        
        media_pool.AppendToTimeline(media_items)
        
        pm.SaveProject()
        print("DaVinci Assembly COMPLETE!")
    except Exception as e:
        print("DaVinci script failed:", e)

def run():
    md_file = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\MUSIC_002_ANA_STEVENSON_DJ_SET_V2.md"
    prompts = parse_prompts(md_file)
    print("Killing existing Chrome processes to free the profile lock...")
    os.system("taskkill /F /IM chrome.exe /T")
    time.sleep(3)
    
    dest_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
    os.makedirs(dest_dir, exist_ok=True)
    
    missing_clips = []
    with sync_playwright() as p:
        print("Launching Chrome manually with remote debugging...")
        os.system('cmd /c "start chrome --remote-debugging-port=9225 --restore-last-session"')
        time.sleep(5)
        
        ws_url = "http://127.0.0.1:9225"
        print(f"Connecting to Chrome on {ws_url}...")
        browser = p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        
        flow_page = None
        for page in context.pages:
            if "labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47" in page.url:
                flow_page = page
                break
                
        if not flow_page:
            print("Flow page not found in existing tabs, opening a new one...")
            flow_page = context.new_page()
            flow_page.goto("https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47", timeout=60000)
            
        flow_page.bring_to_front()
        flow_page.wait_for_timeout(2000)
        
        for clip_num in missing_clips:
            print(f"Submitting A{clip_num}...")
            editor = flow_page.locator("div[contenteditable='true']").first
            safe_text = prompts[clip_num].replace("Ana", "the woman").replace("Pioneer", "professional").replace("Ana's", "the woman's")
            
            editor.focus()
            flow_page.keyboard.press("Control+A")
            flow_page.keyboard.press("Backspace")
            flow_page.wait_for_timeout(400)
            editor.type(safe_text)
            flow_page.wait_for_timeout(800)
            
            plus_btn = None
            for b in flow_page.locator("button").all():
                t = b.inner_text() or ""
                if "add_2" in t and "Create" in t: plus_btn = b; break
            if plus_btn: plus_btn.click()
            flow_page.wait_for_timeout(1000)
            
            dialog = flow_page.locator("[role='dialog']").first
            char_tab = dialog.locator("[role='tab']:has-text('Characters')").first
            if char_tab.count() > 0 and char_tab.get_attribute("aria-selected") != "true":
                char_tab.click()
                flow_page.wait_for_timeout(600)
                
            ana_img = dialog.locator("img[alt*='Ana'], img[src*='ee567222-dec2']").first
            if ana_img.count() > 0: ana_img.click()
            flow_page.wait_for_timeout(600)
            
            add_btn = dialog.locator("button:has-text('Add to Prompt')").first
            if add_btn.count() > 0: add_btn.click()
            flow_page.wait_for_timeout(1500)
            
            submit_btn = None
            for _ in range(10):
                for b in flow_page.locator("button").all():
                    t = b.inner_text() or ""
                    if "arrow_forward" in t and "Create" in t: submit_btn = b; break
                if submit_btn: break
                flow_page.wait_for_timeout(1000)
                
            if submit_btn:
                for _ in range(10):
                    if not submit_btn.is_disabled(): break
                    flow_page.wait_for_timeout(1000)
                submit_btn.click()
                print(f"Submitted A{clip_num}")
            time.sleep(5)
            
        print("Waiting for generations to complete (10 mins max)...")
        for _ in range(60):
            thumbnails = flow_page.locator("a[href*='/edit/']").all()
            if len(thumbnails) >= 24:
                print(f"Found {len(thumbnails)} completed clips!")
                break
            time.sleep(10)
            
        time.sleep(15) 
            
        found_clips = set()
        thumbnails = flow_page.locator("a[href*='/edit/']").all()
        for i in range(len(thumbnails)):
            print(f"Processing clip {i+1}...")
            try:
                current_thumbnails = flow_page.locator("a[href*='/edit/']").all()
                if i >= len(current_thumbnails): continue
                thumb = current_thumbnails[i]
                
                thumb.scroll_into_view_if_needed()
                flow_page.wait_for_timeout(500)
                thumb.click()
                flow_page.wait_for_timeout(3000)
                
                page_text = flow_page.evaluate("document.body.innerText")
                page_text_clean = " ".join(page_text.splitlines())
                
                best_ratio = 0
                matched_clip = None
                
                for clip_num, text in prompts.items():
                    words = set(text.split())
                    page_words = set(page_text_clean.split())
                    overlap = len(words.intersection(page_words))
                    
                    if overlap > best_ratio:
                        best_ratio = overlap
                        matched_clip = clip_num
                        
                if matched_clip:
                    print(f"Matched to: A{matched_clip}! (Score: {best_ratio})")
                    found_clips.add(matched_clip)
                    
                    dest_path = os.path.join(dest_dir, f"A{matched_clip}.mp4")
                    if os.path.exists(dest_path):
                        print(f"A{matched_clip} already exists, skipping download.")
                    else:
                        start_time = time.time()
                        panel = flow_page.locator("[role='dialog']").last
                        if panel.count() == 0: panel = flow_page.locator("body")
                            
                        more_btn = panel.locator("button:has-text('More options'), button[aria-label='More options']").first
                        if more_btn.count() > 0:
                            more_btn.click()
                            flow_page.wait_for_timeout(1000)
                            dl_menu = flow_page.locator("li:has-text('Download'), [role='menuitem']:has-text('Download')").first
                            if dl_menu.count() > 0:
                                dl_menu.hover()
                                flow_page.wait_for_timeout(1000)
                                upscale = flow_page.locator("li:has-text('1080p Upscaled'), [role='menuitem']:has-text('1080p Upscaled')").first
                                if upscale.count() > 0:
                                    upscale.click()
                                    print("Clicked 1080p Upscaled! Waiting for download...")
                                else:
                                    print("No upscaled option, clicking normal download.")
                                    dl_menu.click()
                                    
                                downloaded = False
                                for wait_idx in range(45): 
                                    time.sleep(5)
                                    latest_file = get_latest_download(start_time)
                                    if latest_file and not latest_file.endswith(".crdownload"):
                                        shutil.move(latest_file, dest_path)
                                        print(f"Successfully saved to {dest_path}")
                                        downloaded = True
                                        break
                                if not downloaded:
                                    print("WARNING: Download timed out.")
                            else:
                                print("Download menu missing")
                        else:
                            print("More options missing")
                
                close_btn = flow_page.locator("button:has-text('Close'), button[aria-label='Close'], button[aria-label='Go Back']").first
                if close_btn.count() > 0: close_btn.click()
                else: flow_page.keyboard.press("Escape")
                flow_page.wait_for_timeout(1500)
                
            except Exception as e:
                print("Error:", e)
                flow_page.keyboard.press("Escape")
                flow_page.wait_for_timeout(1500)
                
        context.close()
        
    print(f"Downloaded exactly {len(found_clips)} unique clips.")
    print("Running advanced DaVinci Assembly script...")
    os.system('python "c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\scratch\\davinci_assemble_music_002.py"')

if __name__ == "__main__":
    run()
