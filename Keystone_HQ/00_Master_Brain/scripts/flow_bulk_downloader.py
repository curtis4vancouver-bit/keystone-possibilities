import asyncio
from playwright.async_api import async_playwright
import os
import sys
import re
import string
from pathlib import Path

# Reconfigure stdout to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Configurable Paths
SCRIPT_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\short_035_fda_peptide_trial.md")
DESKTOP_DIR = Path(r"C:\Users\Curtis\Desktop\LONG_FORM_PRODUCTION")

def parse_script():
    if not SCRIPT_FILE.exists():
        print(f"[-] Script file not found: {SCRIPT_FILE}")
        return [], []
        
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Match video clips
    clip_blocks = re.findall(
        r"### 📋 CLIP (A\d+) — (WAYNE|VICTORIA).*?\nTHIS IS THE SCRIPT:\r?\n(.*?)\r?\n\r?\nTHIS IS THE VIDEO PROMPT:\r?\n(.*?)(?=\r?\n\r?\n---|\r?\n---|\Z)",
        content,
        re.DOTALL
    )

    clips = []
    for clip_id, speaker, script, prompt in clip_blocks:
        dialogue_match = re.search(r"(Wayne|Victoria) says: (.*)", script, re.DOTALL)
        if dialogue_match:
            dialogue = dialogue_match.group(2).strip()
        else:
            dialogue = script.strip()
            
        clips.append({
            "id": clip_id,
            "speaker": speaker.strip().capitalize(),
            "dialogue": dialogue,
            "prompt": prompt.strip()
        })
        
    # Match B-rolls using the correct format #### 🖼️ B[N]: [TITLE]
    broll_blocks = re.findall(
        r"#### 🖼️ (B\d+):.*?\r?\n(.*?)(?=\r?\n\r?\n####|\r?\n\r?\n##|\Z)",
        content,
        re.DOTALL
    )
    
    brolls = []
    for broll_id, prompt in broll_blocks:
        brolls.append({
            "id": broll_id,
            "prompt": prompt.strip()
        })
        
    return clips, brolls

def score_card_match(card_prompt, speaker, dialogue, prompt):
    card_prompt_lower = card_prompt.lower()
    
    # Check speaker reference
    pronoun = "he says" if speaker.lower() == "wayne" else "she says"
    has_pronoun = pronoun in card_prompt_lower or speaker.lower() in card_prompt_lower
    
    if not has_pronoun:
        return 0
        
    score = 0
    # Score based on words from dialogue
    words = [w.strip(string.punctuation).lower() for w in dialogue.split() if len(w.strip(string.punctuation)) > 3]
    for w in words:
        if w in card_prompt_lower:
            score += 1
            
    # Score based on visual prompt words
    prompt_words = [w.strip(string.punctuation).lower() for w in prompt.split() if len(w.strip(string.punctuation)) > 3]
    for w in prompt_words:
        if w in card_prompt_lower:
            score += 0.5
            
    return score

def score_broll_match(card_prompt, prompt):
    card_prompt_lower = card_prompt.lower()
    
    # Must not have character dialogue indicators to be a B-roll
    if "says:" in card_prompt_lower:
        return 0
        
    score = 0
    # Score based on prompt words
    words = [w.strip(string.punctuation).lower() for w in prompt.split() if len(w.strip(string.punctuation)) > 3]
    for w in words:
        if w in card_prompt_lower:
            score += 1
            
    return score

async def main():
    # Ensure target directories exist
    video_dir = DESKTOP_DIR / "Videos"
    image_dir = DESKTOP_DIR / "Images"
    video_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Target directory ready: {DESKTOP_DIR}")
    
    clips, brolls = parse_script()
    print(f"[+] Parsed {len(clips)} video clips and {len(brolls)} B-rolls from the script.")
    if not clips and not brolls:
        return
        
    async with async_playwright() as p:
        try:
            # Read the DevToolsActivePort file to get the exact WebSocket URL
            try:
                with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
                    lines = f.read().splitlines()
                port = lines[0]
                path = lines[1]
                ws_url = f"ws://127.0.0.1:{port}{path}"
                print(f"[+] Found WebSocket URL: {ws_url}")
            except Exception as e:
                print(f"[-] Error reading DevToolsActivePort: {e}")
                ws_url = "http://127.0.0.1:9222" # fallback
                
            browser = await p.chromium.connect_over_cdp(ws_url)
            context = browser.contexts[0]
            page = None
            for p_ in context.pages:
                if "labs.google/fx/tools/flow/project" in p_.url:
                    page = p_
                    break
            
            if not page:
                print("Flow page not found! Ensure the tab is open.")
                return
                
            print(f"Connected to Flow: {page.url}")
            
            # 1. Retrieve the prompt mappings from the React query cache
            print("[+] Loading prompt mappings from React query cache...")
            uuid_to_prompt = await page.evaluate("""() => {
                const editor = document.querySelector('[data-slate-editor]');
                if (!editor) return {};
                const fiberKey = Object.keys(editor).find(k => k.startsWith('__reactFiber$'));
                let current = editor[fiberKey];
                let client = null;
                while (current) {
                    if (current.memoizedProps && current.memoizedProps.client) {
                        client = current.memoizedProps.client;
                        break;
                    }
                    current = current.return;
                }
                if (!client) return {};
                const query = client.queryCache.queries.find(q => q.queryKey && q.queryKey[0] && q.queryKey[0][0] === 'flow' && q.queryKey[0][1] === 'projectInitialData');
                if (!query || !query.state.data || !query.state.data.projectContents) return {};
                
                const media = query.state.data.projectContents.media || [];
                const mapping = {};
                for (const m of media) {
                    const wId = m.workflowId;
                    if (!wId) continue;
                    let prompt = "";
                    if (m.image && m.image.generatedImage) {
                        prompt = m.image.generatedImage.prompt || "";
                    } else if (m.video && m.video.generatedVideo) {
                        prompt = m.video.generatedVideo.prompt || "";
                    }
                    if (prompt) {
                        mapping[wId] = prompt;
                    }
                }
                return mapping;
            }""")
            
            print(f"  [+] Loaded {len(uuid_to_prompt)} prompt mappings.")
            
            success_count = 0
            
            # Combine items to download: (type, item_id, prompt_data)
            items_to_download = []
            for c in clips:
                items_to_download.append(("video", c["id"], c))
            for b in brolls:
                items_to_download.append(("image", b["id"], b))
                
            for item_type, item_id, item_data in items_to_download:
                print(f"\n--> Matching {item_type.upper()} {item_id}...")
                
                best_uuid = None
                best_score = 0
                
                # Match against the query cache mappings
                for uuid, card_prompt in uuid_to_prompt.items():
                    if item_type == "video":
                        score = score_card_match(card_prompt, item_data["speaker"], item_data["dialogue"], item_data["prompt"])
                    else:
                        score = score_broll_match(card_prompt, item_data["prompt"])
                        
                    if score > best_score:
                        best_score = score
                        best_uuid = uuid
                
                if best_uuid and ((item_type == "video" and best_score >= 3) or (item_type == "image" and best_score >= 2)):
                    print(f"    [+] MATCH: Found card UUID {best_uuid} (score={best_score}): {uuid_to_prompt[best_uuid][:80]}...")
                else:
                    print(f"    [-] NO MATCH: Could not find card for {item_id} (best score={best_score}). Skipping.")
                    continue
                
                try:
                    # Target the draggable card container element that contains our target workflow UUID
                    locator = page.locator(f'[aria-roledescription="draggable"]:has([data-tile-id="fe_id_{best_uuid}"])').first
                    
                    if not await locator.is_visible():
                        print(f"    [-] Card {item_id} is not visible in DOM. Scrolling grid to find it...")
                        # Scroll to bottom and top to trigger virtualization mount
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(1000)
                        await locator.scroll_into_view_if_needed()
                        await page.wait_for_timeout(500)
                        
                    if not await locator.is_visible():
                        print(f"    [!] Warning: Card {item_id} still not visible in DOM. Skipping.")
                        continue
                        
                    await locator.scroll_into_view_if_needed()
                    await page.wait_for_timeout(500)
                    
                    # Hover card
                    await locator.hover()
                    await page.wait_for_timeout(300)
                    
                    # Click 'more_vert' menu button inside the card
                    more_btn = locator.locator('button:has-text("more_vert")').first
                    if await more_btn.is_visible():
                        print("    Clicking 'more_vert' menu button...")
                        await more_btn.click(force=True)
                    else:
                        # Fallback to right click on the container
                        print("    'more_vert' button not visible. Fallback right-clicking card container...")
                        await locator.click(button="right", force=True)
                        
                    await page.wait_for_timeout(1000)
                    
                    # Locate and click Download option in context menu
                    download_opt = page.get_by_role("menuitem", name="Download").first
                    if not await download_opt.is_visible():
                        download_opt = page.get_by_role("button", name="Download").first
                    if not await download_opt.is_visible():
                        download_opt = page.get_by_text("Download", exact=True).first
                        
                    if await download_opt.is_visible():
                        print("    Clicking 'Download' option...")
                        await download_opt.click(force=True)
                        await page.wait_for_timeout(1000)
                        
                        # Find the best upscale button visible on the page
                        upscale_btn = None
                        for btn_text in ["2K", "1080p", "Upscaled", "Original Size", "720p"]:
                            btn = page.get_by_role("button", name=btn_text).first
                            if await btn.is_visible():
                                upscale_btn = btn
                                break
                                
                        if upscale_btn:
                            btn_text = await upscale_btn.inner_text()
                            print(f"    Triggering download with option: {btn_text.strip()}...")
                            
                            async with page.expect_download(timeout=300000) as download_info:
                                await upscale_btn.click(force=True)
                                
                            download = await download_info.value
                            
                            # Determine folder and extension
                            if item_type == "video":
                                target_path = os.path.join(video_dir, f"{item_id}.mp4")
                            else:
                                # Retrieve extension from download suggestion or default to png
                                filename = download.suggested_filename
                                ext = os.path.splitext(filename)[1] or ".png"
                                target_path = os.path.join(image_dir, f"{item_id}{ext}")
                                
                            await download.save_as(target_path)
                            print(f"    [+] SUCCESS: Saved {item_id} to {target_path}")
                            success_count += 1
                        else:
                            print("    [!] No download resolution option button visible!")
                            await page.keyboard.press("Escape")
                            
                        # Wait for UI transition
                        await page.wait_for_timeout(2000)
                    else:
                        print("    [-] Download option not visible in context menu! Escaping menu.")
                        await page.keyboard.press("Escape")
                        await page.wait_for_timeout(1000)
                        
                except Exception as e:
                    print(f"    [!] Error during {item_id} download: {e}")
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(1000)
                    
            print(f"\n--- BATCH DOWNLOAD COMPLETE ---")
            print(f"Successfully processed {success_count}/{len(clips) + len(brolls)} assets.")
            
        except Exception as e:
            print(f"Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
