# download_script33_assets.py
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
SCRIPT_FILE = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\glp1_anhedonia_8m20s_studio_black.md")
DESKTOP_DIR = Path(r"C:\Users\Curtis\Desktop\LONG_033_GLP1_ANHEDONIA")

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
        clips.append({
            "id": clip_id,
            "speaker": speaker.strip().capitalize(),
            "dialogue": script.strip(),
            "prompt": prompt.strip()
        })
        
    # Match B-rolls
    broll_blocks = re.findall(
        r"#### 🖼️ B(\d+): .*?\n(.*?)(?=\n\n####|\n\n---|\Z)",
        content,
        re.DOTALL
    )
    
    brolls = []
    for broll_id, prompt in broll_blocks:
        brolls.append({
            "id": f"B{broll_id}",
            "prompt": prompt.strip()
        })
        
    return clips, brolls

def calculate_similarity(s1, s2):
    """Simple word-overlap similarity score."""
    def clean(s):
        s = s.lower()
        s = s.replace("he says:", "").replace("she says:", "")
        s = s.replace("victoria says:", "").replace("wayne says:", "")
        return set(w.strip(string.punctuation) for w in s.split() if len(w.strip(string.punctuation)) > 3)
    
    set1 = clean(s1)
    set2 = clean(s2)
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    return len(intersection) / max(len(set1), len(set2))

async def trigger_download(page, card_idx, target_path, is_video):
    cards_locator = page.locator("[aria-roledescription='draggable']")
    target_card = cards_locator.nth(card_idx)
    
    await target_card.scroll_into_view_if_needed()
    await page.wait_for_timeout(300)
    
    inner_btn = target_card.get_by_role("button").first
    if await inner_btn.is_visible():
        await inner_btn.click(button="right", force=True)
    else:
        await target_card.click(button="right", force=True)
    
    await page.wait_for_timeout(600)
    
    download_opt = page.get_by_role("menuitem", name="Download").first
    if not await download_opt.is_visible():
        download_opt = page.get_by_text("Download", exact=True).first
        
    if not await download_opt.is_visible():
        print(f"  [-] Card {card_idx} Download option not found!")
        await page.keyboard.press("Escape")
        return None
        
    await download_opt.hover(force=True)
    await page.wait_for_timeout(300)
    await download_opt.click(force=True)
    await page.wait_for_timeout(500)
    
    if is_video:
        resolution_opt = page.locator("[role='menuitem']").filter(has_text="1080p").first
        if not await resolution_opt.is_visible():
            resolution_opt = page.locator("[role='menuitem']").filter(has_text="Upscaled").first
        if not await resolution_opt.is_visible():
            resolution_opt = page.locator("[role='menuitem']").filter(has_text="720p").first
    else:
        resolution_opt = page.locator("[role='menuitem']").filter(has_text="1K").first
        if not await resolution_opt.is_visible():
            resolution_opt = page.locator("[role='menuitem']").filter(has_text="Original size").first
            
    if not await resolution_opt.is_visible():
        print(f"  [-] Card {card_idx} resolution option not found!")
        await page.keyboard.press("Escape")
        return None
        
    # Start expect_download task
    download_task = asyncio.create_task(page.wait_for_event("download", timeout=180000))
    await resolution_opt.click(force=True)
    
    return download_task, target_path

async def main():
    video_dest = DESKTOP_DIR / "Videos"
    image_dest = DESKTOP_DIR / "Images"
    video_dest.mkdir(parents=True, exist_ok=True)
    image_dest.mkdir(parents=True, exist_ok=True)
    
    clips, brolls = parse_script()
    print(f"[+] Loaded {len(clips)} video clips and {len(brolls)} B-rolls to download.")
    
    test_mode = "--test" in sys.argv
    if test_mode:
        print("[!] TEST MODE ENGAGED: Restricting downloads to first 2 assets of each type.")
        clips = clips[:2]
        brolls = brolls[:2]

    # Connect to Chrome
    try:
        with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
            lines = f.read().splitlines()
        port = lines[0]
        path = lines[1]
        ws_url = f"ws://127.0.0.1:{port}{path}"
        print(f"[+] WebSocket URL: {ws_url}")
    except Exception as e:
        print(f"[-] Cannot read DevToolsActivePort: {e}")
        return

    async with async_playwright() as p:
        try:
            print("[+] Connecting to Chrome...")
            browser = await p.chromium.connect_over_cdp(ws_url)
            context = browser.contexts[0]
            page = None
            for p_ in context.pages:
                if "labs.google/fx/tools/flow/project" in p_.url:
                    page = p_
                    break
            
            if not page:
                print("[-] Flow page not found! Ensure the tab is open.")
                return
                
            print(f"[+] Connected to Flow: {page.url}")
            await page.bring_to_front()
            
            # --- Extract React state mapping of cards ---
            print("[+] Querying React state for media mapping...")
            js_bfs = """
            () => {
                let root = document.querySelector("#__next") || document.body;
                let keys = Object.keys(root);
                let fiberKey = keys.find(k => k.startsWith("__reactContainer") || k.startsWith("__reactFiber"));
                if (!fiberKey) return { error: "No fiber container found" };
                
                let startObj = root[fiberKey];
                let queue = [startObj];
                let visited = new Set();
                let mediaList = null;
                
                while (queue.length > 0) {
                    let curr = queue.shift();
                    if (!curr || visited.has(curr)) continue;
                    visited.add(curr);
                    
                    if (curr.queries && Array.isArray(curr.queries)) {
                        for (let q of curr.queries) {
                            if (q.state?.data?.projectContents?.media) {
                                mediaList = q.state.data.projectContents.media;
                                break;
                            }
                        }
                    }
                    if (mediaList) break;
                    
                    for (let k in curr) {
                        try {
                            let val = curr[k];
                            if (val && typeof val === 'object' && !visited.has(val)) {
                                if (val instanceof Node) continue;
                                queue.push(val);
                            }
                        } catch(e) {}
                    }
                }
                
                if (!mediaList) return { error: "mediaList not found" };
                
                const mediaMap = {};
                mediaList.forEach(item => {
                    if (!item.workflowId) return;
                    const type = item.video ? "video" : (item.image ? "image" : "unknown");
                    let promptText = "";
                    if (item.mediaMetadata?.requestData?.promptInputs?.[0]?.structuredPrompt?.parts?.[0]?.text) {
                        promptText = item.mediaMetadata.requestData.promptInputs[0].structuredPrompt.parts[0].text;
                    } else if (item.mediaMetadata?.mediaTitle) {
                        promptText = item.mediaMetadata.mediaTitle;
                    }
                    
                    mediaMap[item.workflowId] = {
                        name: item.name,
                        type: type,
                        prompt: promptText
                    };
                });
                
                const cards = document.querySelectorAll("[aria-roledescription='draggable']");
                const results = [];
                cards.forEach((card, idx) => {
                    const link = card.querySelector("a")?.href;
                    if (!link) return;
                    const match = link.match(/\\/edit\\/([a-zA-Z0-9\\-]+)/);
                    if (!match) return;
                    const workflowId = match[1];
                    const meta = mediaMap[workflowId] || null;
                    results.push({
                        cardIndex: idx,
                        workflowId: workflowId,
                        meta: meta
                    });
                });
                
                return results;
            }
            """
            
            card_mappings = await page.evaluate(js_bfs)
            if isinstance(card_mappings, dict) and "error" in card_mappings:
                print(f"[-] BFS Error: {card_mappings['error']}")
                return
                
            print(f"[+] Found {len(card_mappings)} active grid cards mapped to React metadata.")
            
            # Group all items that need downloading
            download_queue = []
            
            # Match videos
            for clip in clips:
                clip_id = clip["id"]
                target_path = video_dest / f"{clip_id}.mp4"
                if target_path.exists():
                    continue
                
                best_card_idx = None
                best_score = 0.0
                expected_prompt = f"says: {clip['dialogue']}. {clip['prompt']}"
                
                for card in card_mappings:
                    meta = card.get("meta")
                    if not meta or meta.get("type") != "video":
                        continue
                    score = calculate_similarity(expected_prompt, meta.get("prompt", ""))
                    if score > best_score:
                        best_score = score
                        best_card_idx = card["cardIndex"]
                
                if best_card_idx is not None and best_score > 0.5:
                    download_queue.append({
                        "id": clip_id,
                        "cardIndex": best_card_idx,
                        "path": target_path,
                        "isVideo": True
                    })
                else:
                    print(f"[-] Could not find a match for video {clip_id}")

            # Match B-rolls
            for broll in brolls:
                b_id = broll["id"]
                target_path = image_dest / f"{b_id}.jpeg"
                if target_path.exists():
                    continue
                
                best_card_idx = None
                best_score = 0.0
                
                for card in card_mappings:
                    meta = card.get("meta")
                    if not meta or meta.get("type") != "image":
                        continue
                    score = calculate_similarity(broll["prompt"], meta.get("prompt", ""))
                    if score > best_score:
                        best_score = score
                        best_card_idx = card["cardIndex"]
                
                if best_card_idx is not None and best_score > 0.5:
                    download_queue.append({
                        "id": b_id,
                        "cardIndex": best_card_idx,
                        "path": target_path,
                        "isVideo": False
                    })
                else:
                    print(f"[-] Could not find a match for B-roll {b_id}")

            print(f"[+] Total items pending download: {len(download_queue)}")
            
            # Download in batches of 8
            BATCH_SIZE = 8
            for batch_start in range(0, len(download_queue), BATCH_SIZE):
                batch = download_queue[batch_start:batch_start + BATCH_SIZE]
                batch_ids = [item["id"] for item in batch]
                print(f"\n--- Processing Batch: {', '.join(batch_ids)} ---")
                
                # 1. Trigger all downloads in the batch
                download_promises = []
                for item in batch:
                    print(f"  [~] Triggering {item['id']} on Card {item['cardIndex']}...")
                    res = await trigger_download(page, item["cardIndex"], item["path"], item["isVideo"])
                    if res:
                        download_promises.append(res)
                    # 2 second delay between menu clicks to prevent menu overlap issues
                    await asyncio.sleep(2)
                
                # 2. Wait for all triggered downloads to start and complete
                if download_promises:
                    print(f"  [~] Waiting for batch of {len(download_promises)} downloads to complete...")
                    for task, path in download_promises:
                        try:
                            download = await task
                            await download.save_as(str(path))
                            print(f"  [+] Saved to: {path.name}")
                        except Exception as e:
                            print(f"  [-] Error saving file to {path}: {e}")
                
                # Tiny rest between batches
                await asyncio.sleep(3)
            
            print("\n" + "="*60)
            print("  DOWNLOAD PROCESS COMPLETE!")
            print("="*60)
            
        except Exception as e:
            print(f"[-] Critical execution error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
