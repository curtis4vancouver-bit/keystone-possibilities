import os
import time
import glob
import shutil
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def get_latest_download(after_time):
    downloads_dir = r"C:\Users\Curtis\Downloads"
    mp4_files = glob.glob(os.path.join(downloads_dir, "*.mp4"))
    if not mp4_files:
        return None
    latest_file = max(mp4_files, key=os.path.getctime)
    if os.path.getctime(latest_file) > after_time:
        return latest_file
    return None

def run():
    print("Killing existing Chrome processes to free the profile lock...")
    os.system("taskkill /F /IM chrome.exe /T")
    time.sleep(3)

    user_data_dir = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data_Link"
    dest_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
    os.makedirs(dest_dir, exist_ok=True)

    options = Options()
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument("profile-directory=Default")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    print("Launching Chrome via Selenium...")
    driver = webdriver.Chrome(options=options)

    try:
        url = "https://labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47"
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(15) # Wait for page to fully load and state to populate

        print("Extracting project state from __NEXT_DATA__...")
        next_data = driver.execute_script("return window.__NEXT_DATA__")
        
        dehydrated = next_data["props"]["pageProps"]["trpcState"]["json"]["queries"]
        components = None
        for query in dehydrated:
            if query["queryKey"][0] == "project" and query["queryKey"][1] == "get":
                components = query["state"]["data"]["components"]
                break
                
        if not components:
            print("Failed to find components in __NEXT_DATA__")
            return
            
        print(f"Found {len(components)} components.")
        
        # Parse prompts to map them to A1-A24
        md_file = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\MUSIC_002_ANA_STEVENSON_DJ_SET_V2.md"
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        prompts = {}
        pattern = re.compile(r'### CLIP A(\d+).*?```(.*?)```', re.DOTALL)
        for match in pattern.finditer(content):
            clip_num = int(match.group(1))
            prompt_text = " ".join(match.group(2).strip().splitlines())
            prompts[clip_num] = prompt_text
            
        from difflib import SequenceMatcher
        found_clips = set()
        
        for comp in components:
            if "prompt" in comp and "media" in comp and comp["media"] is not None:
                comp_prompt = comp["prompt"]["text"].strip()
                comp_prompt_flat = " ".join(comp_prompt.splitlines())
                uuid = comp["media"]["name"]
                
                best_match = None
                best_ratio = 0
                for clip_num, target_prompt in prompts.items():
                    ratio = SequenceMatcher(None, comp_prompt_flat[:150], target_prompt[:150]).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = clip_num
                        
                if best_ratio > 0.85:
                    print(f"Matched A{best_match} (UUID: {uuid})")
                    found_clips.add(best_match)
                    
                    dest_path = os.path.join(dest_dir, f"A{best_match}.mp4")
                    if os.path.exists(dest_path):
                        print(f"A{best_match} already downloaded.")
                        continue
                        
                    dl_url = f"https://labs.google/fx/api/trpc/media.getMediaUrlRedirect?name={uuid}&mediaUrlType=MEDIA_URL_TYPE_VIDEO_UPSCALED_1080P"
                    print(f"Downloading A{best_match}...")
                    start_time = time.time()
                    
                    # Navigate to trigger the download
                    driver.execute_script(f"window.open('{dl_url}', '_blank');")
                    
                    downloaded = False
                    for _ in range(45):
                        time.sleep(5)
                        latest_file = get_latest_download(start_time)
                        if latest_file and not latest_file.endswith(".crdownload"):
                            shutil.move(latest_file, dest_path)
                            print(f"Saved to {dest_path}")
                            downloaded = True
                            break
                            
                    if not downloaded:
                        print(f"Failed to download A{best_match}!")
                        
    except Exception as e:
        print("Error during automation:", e)
    finally:
        driver.quit()
        
    print(f"Finished processing. Downloaded exactly {len(found_clips)} unique clips.")
    if len(found_clips) == 24:
        print("Running advanced DaVinci Assembly script...")
        os.system('python "c:\\Users\\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\scratch\\davinci_assemble_music_002.py"')
    else:
        print("Not all 24 clips were found, skipping DaVinci assembly.")

if __name__ == "__main__":
    run()
