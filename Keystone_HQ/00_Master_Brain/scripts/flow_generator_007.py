import asyncio
from playwright.async_api import async_playwright
import os
import json
import re
import urllib.request
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Paths
STATE_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\flow_generator_state_007.json")
SCRIPT_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Content_Production\SCRIPT_007_NEW_FLOW.md")

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"completed_clips": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

async def get_finished_count(page):
    items = await page.locator("[aria-roledescription='draggable']").all()
    finished = 0
    for it in items:
        try:
            text = await it.inner_text()
            is_completed = "play_circle" in text and not re.search(r'\d+%', text)
            is_failed = "Failed" in text or "violate" in text or "policy" in text
            if is_completed or is_failed:
                finished += 1
        except Exception:
            pass
    return finished

def parse_script():
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
        # Extract dialogue
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
    return clips

async def main():
    clips = parse_script()
    print(f"[+] Parsed {len(clips)} clips from the script.")
    if not clips:
        print("[-] No clips found in the script file. Check regex/formatting.")
        return
        
    state = load_state()
    completed = state["completed_clips"]
    print(f"[+] Loaded state: {len(completed)} clips already completed.")

    # Establish CDP connection to Chrome
    ws_url = None
    cdp_connected = False
    
    # Try connecting directly to debugging port 9222 first
    print("[+] Checking remote debugging port 9222...")
    try:
        req = urllib.request.Request("http://127.0.0.1:9222/json/version")
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            ws_url = data.get("webSocketDebuggerUrl")
            if ws_url:
                print(f"[+] Found active remote debugging session on port 9222: {ws_url}")
                cdp_connected = True
    except Exception as e:
        print(f"[-] Debugging port 9222 not directly reachable: {e}")

    # Fallback: Read DevToolsActivePort file
    if not cdp_connected:
        print("[+] Falling back to DevToolsActivePort file...")
        try:
            with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
                lines = f.read().splitlines()
            port = lines[0]
            path = lines[1]
            ws_url = f"ws://127.0.0.1:{port}{path}"
            print(f"[+] Found WebSocket URL from DevToolsActivePort: {ws_url}")
        except Exception as e:
            print(f"[-] Error reading DevToolsActivePort: {e}")
            print("[-] Please ensure Chrome is running with --remote-debugging-port=9222")
            return

    async with async_playwright() as p:
        try:
            print("[+] Connecting to Chrome via Playwright...")
            browser = await p.chromium.connect_over_cdp(ws_url)
            print("[+] Connection successful!")
            context = browser.contexts[0]
            
            page = None
            for p_ in context.pages:
                if "labs.google/fx/tools/flow/project" in p_.url:
                    page = p_
                    break
                    
            if not page:
                print("[-] Flow project page not found! Please open Google Flow in Chrome first.")
                return
                
            print(f"[+] Connected to Flow project: {page.url}")
            await page.bring_to_front()
            
            # Reset UI state (Escape) to close any leftover open dialogs from previous runs
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(1000)

            # --- 2. Switch model, duration, and aspect ratio programmatically via React store ---
            print("[+] Configuring settings (10s, 16:9, Omni Flash)...")
            success = await page.evaluate("""() => {
                const editor = document.querySelector('[data-slate-editor]');
                const fiberKey = Object.keys(editor).find(k => k.startsWith('__reactFiber$'));
                let current = editor[fiberKey];
                let store = null;
                while (current) {
                    if (current.memoizedProps && current.memoizedProps.promptBoxStore) {
                        store = current.memoizedProps.promptBoxStore;
                        break;
                    }
                    current = current.return;
                }
                if (!store) return false;
                const actions = store.getState().actions;
                actions.setMode("VIDEO");
                actions.setVideoModelFamily("abra");
                actions.setSelectedVideoDuration(10);
                actions.setAspectRatio("LANDSCAPE");
                return true;
            }""")
            if success:
                print("  [+] Video settings configured programmatically via React store.")
                await page.wait_for_timeout(500)
            else:
                print("  [-] Settings configuration failed.")

            # --- 3. Main Generation Loop (4-and-20 Pacing Protocol) ---
            pending_clips = [clip for clip in clips if clip["id"] not in completed]
            print(f"[+] Total pending clips: {len(pending_clips)}")
            
            if not pending_clips:
                print("[+] All clips already generated!")
                return
                
            # Get initial finished count
            initial_finished = await get_finished_count(page)
            print(f"    Initial finished cards count in project: {initial_finished}")
            
            BATCH_SIZE = 4
            num_batches = (len(pending_clips) + BATCH_SIZE - 1) // BATCH_SIZE
            
            for idx_batch in range(num_batches):
                start_idx = idx_batch * BATCH_SIZE
                batch = pending_clips[start_idx:start_idx+BATCH_SIZE]
                batch_ids = [c["id"] for c in batch]
                print(f"\n[===] QUEUEING BATCH {idx_batch+1}/{num_batches}: {', '.join(batch_ids)} [===]")
                
                # Submit all prompts in this batch
                for clip in batch:
                    clip_id = clip["id"]
                    speaker = clip["speaker"]
                    dialogue = clip["dialogue"]
                    visual_prompt = clip["prompt"]
                    pronoun = "He" if speaker.lower() == "wayne" else "She"
                    full_prompt = f"{pronoun} says: {dialogue}. {visual_prompt}"
                    
                    print(f"    [+] Submitting Clip {clip_id} ({speaker})...")
                    
                    # 1. Focus and clear the prompt textbox
                    prompt_locator = page.locator("div[contenteditable='true'], textarea").first
                    await prompt_locator.focus()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.wait_for_timeout(200)

                    # Click cancel button on any existing avatar/character ingredient if visible
                    cancel_btn = page.locator("button:has-text('cancel')").first
                    if await cancel_btn.is_visible():
                        await cancel_btn.click()
                        await page.wait_for_timeout(300)
                    
                    # Fallback: click close Clear prompt button if visible
                    clear_btn = page.locator("button:has-text('close'), button:has-text('Clear prompt')").first
                    if await clear_btn.is_visible():
                        await clear_btn.click()
                        await page.wait_for_timeout(300)

                    # 2. Type prompt
                    await page.keyboard.type(full_prompt)
                    await page.wait_for_timeout(300)

                    # 3. Open Asset Picker Dialog using native Playwright click
                    create_dialog_btn = page.locator("button:has-text('add_2 Create')").first
                    await create_dialog_btn.click()
                    await page.wait_for_selector("div[role='dialog']", timeout=10000)
                    await page.wait_for_timeout(800)

                    # 4. Attach Avatar or Character using native Playwright clicks
                    if speaker.lower() == "wayne":
                        # Click "Avatar" tab in dialog
                        avatar_tab = page.locator("div[role='dialog'] [role='tab']:has-text('face'), div[role='dialog'] [role='tab']:has-text('Avatar')").first
                        await avatar_tab.click()
                        await page.wait_for_timeout(800)

                        # Select "me" avatar and click "Add to Prompt"
                        await page.locator("div[role='dialog'] img[alt='me']").first.click()
                        await page.wait_for_timeout(500)
                        
                        await page.locator("div[role='dialog'] button:has-text('Add to Prompt')").first.click()
                        await page.wait_for_timeout(800)
                    else:
                        # Click "Characters" tab in dialog
                        char_tab = page.locator("div[role='dialog'] [role='tab']:has-text('Characters'), div[role='dialog'] [role='tab']:has-text('accessibility_new')").first
                        await char_tab.click()
                        await page.wait_for_timeout(800)

                        # Type "Victoria" in Search assets box
                        search_box = page.locator("div[role='dialog'] input[placeholder='Search assets']").first
                        await search_box.focus()
                        await page.keyboard.press("Control+A")
                        await page.keyboard.press("Backspace")
                        await page.keyboard.type("Victoria")
                        await page.keyboard.press("Enter")
                        await page.wait_for_timeout(800)

                        # Select Victoria and click "Add to Prompt"
                        await page.locator("div[role='dialog'] img[alt='Victoria']").first.click()
                        await page.wait_for_timeout(500)
                        
                        await page.locator("div[role='dialog'] button:has-text('Add to Prompt')").first.click()
                        await page.wait_for_timeout(800)

                    # 5. MANDATORY: Close the Asset Picker dialog before submitting!
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(800)

                    # 6. Click submit button using native Playwright click
                    submit_btn = page.locator("button:has-text('arrow_forward')").first
                    await submit_btn.click()
                    print(f"        -> Clip {clip_id} submitted to Google Flow via native UI click.")
                    await page.wait_for_timeout(3000)
                
                # After submitting a batch of 4, wait 20 seconds before starting the next batch (unless it's the last batch)
                if idx_batch < num_batches - 1:
                    print(f"    [+] Batch queued. Waiting 20 seconds before submitting the next batch...")
                    await asyncio.sleep(20)
            
            # --- 4. Block and Wait for all submitted clips to finish rendering ---
            target_finished = initial_finished + len(pending_clips)
            print(f"\n[+] All {len(pending_clips)} clips queued! Waiting for all to finish rendering (target finished count: {target_finished})...")
            
            success = False
            max_polls = (len(pending_clips) * 180) // 10
            for poll in range(max_polls):
                await asyncio.sleep(10)
                current_finished = await get_finished_count(page)
                completed_total = current_finished - initial_finished
                print(f"    -> Poll {poll+1}/{max_polls}: {completed_total}/{len(pending_clips)} clips finished rendering...")
                
                if current_finished >= target_finished:
                    print(f"[+] All clips finished rendering successfully!")
                    success = True
                    break
            
            if success:
                completed.extend([c["id"] for c in pending_clips])
                save_state(state)
            else:
                print(f"[!] Warning: Wait timed out before all clips finished! Saving completed ones...")
                current_finished = await get_finished_count(page)
                completed_total = current_finished - initial_finished
                for idx in range(min(completed_total, len(pending_clips))):
                    completed.append(pending_clips[idx]["id"])
                save_state(state)
            
            print("\n[+] ALL QUEUED GENERATIONS HAVE COMPLETED OR RESOLVED!")
            
        except Exception as e:
            print(f"[-] Critical script exception: {e}")

if __name__ == "__main__":
    asyncio.run(main())
