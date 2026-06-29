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
STATE_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\flow_generator_state_036.json")
SCRIPT_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\script_036_cjc_ipamorelin.md")

# Video Settings Configuration (Omni Flash, 10s)
VIDEO_MODEL_FAMILY = "abra"  # "abra" is Omni Flash
VIDEO_DURATION = 10         # 10 seconds

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
    
    # Match video clips in script_036 format
    clip_blocks = re.findall(
        r"### 📋 CLIP (A\d+)[^\n]*\r?\nTHIS IS THE SCRIPT:\r?\n(.*?)\r?\n\r?\nTHIS IS THE VIDEO PROMPT:\r?\n(.*?)(?=\r?\n\r?\n###|\r?\n\r?\n---|\r?\n---|\Z)",
        content,
        re.DOTALL
    )

    # Speaker mapping for Script 036
    wayne_clips = {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
        28, 33, 34, 35,
        42, 43, 44, 45,
        46, 47, 48, 49, 50
    }

    clips = []
    for clip_id, script, prompt in clip_blocks:
        num = int(clip_id[1:]) # Extract number from "A1", "A2", etc.
        speaker = "Wayne" if num in wayne_clips else "Victoria"
        clips.append({
            "id": clip_id,
            "speaker": speaker,
            "dialogue": script.strip(),
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
            await page.wait_for_timeout(500)
            
            # Reload page to guarantee a clean Slate editor instance and avoid desync
            print("[+] Reloading Google Flow page for a clean Slate instance...")
            await page.reload()
            await page.wait_for_timeout(5000)
            
            # 1. Open settings drawer with self-healing click and verify settings via UI clicks
            print("[+] Opening settings button...")
            settings_btn = page.locator("button").filter(has_text=re.compile(r'x\d+|\d+x')).first
            
            popover_visible = False
            for attempt in range(5):
                await settings_btn.click(force=True)
                await page.wait_for_timeout(1000)
                
                # Check if video tab is visible
                video_tab = page.locator("button[role='tab']").filter(has_text="Video").first
                if await video_tab.is_visible():
                    popover_visible = True
                    print(f"  [+] Settings popover opened successfully on attempt {attempt+1}!")
                    break
                else:
                    print(f"  [-] Popover not visible yet on attempt {attempt+1}, retrying click...")
            
            if not popover_visible:
                print("[-] ERROR: Settings popover failed to open after 5 attempts.")
                sys.exit(1)
            
            # Click Video tab
            print("[+] Clicking Video tab...")
            video_tab = page.locator("button[role='tab']").filter(has_text="Video").first
            await video_tab.click(force=True)
            await page.wait_for_timeout(1000)
            
            # Select Omni Flash if not selected
            dropdown_btn = page.locator("button").filter(has_text=re.compile("arrow_drop_down")).last
            if await dropdown_btn.is_visible():
                txt = await dropdown_btn.inner_text()
                if "Omni Flash" not in txt:
                    print(f"[+] Clicking model dropdown (current: {repr(txt)})...")
                    await dropdown_btn.click(force=True)
                    await page.wait_for_timeout(1000)
                    
                    # Click Omni Flash option
                    omni_opt = page.locator("[role='option'], [role='menuitem'], button").filter(has_text="Omni Flash").first
                    await omni_opt.click(force=True)
                    await page.wait_for_timeout(1000)
            
            # Select 10s duration if not selected
            duration_btn = page.locator("button").filter(has_text="10s").first
            print("[+] Clicking 10s duration...")
            await duration_btn.click(force=True)
            await page.wait_for_timeout(500)
            
            # Select 1x quantity if not selected
            qty_btn = page.locator("button").filter(has_text="1x").first
            print("[+] Clicking 1x quantity...")
            await qty_btn.click(force=True)
            await page.wait_for_timeout(500)
            
            # Select 16:9 aspect ratio if not selected
            aspect_btn = page.locator("button").filter(has_text="16:9").first
            print("[+] Clicking 16:9 aspect ratio...")
            await aspect_btn.click(force=True)
            await page.wait_for_timeout(500)
            
            # Close settings panel
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(500)

            # Switch settings programmatically via React store to switch to Video Mode (VIDEO_REFERENCES), Omni Flash, 10s, 16:9, and 1x quantity
            print("[+] Locking settings programmatically via React store...")
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
                actions.setMode("VIDEO_REFERENCES");
                actions.setVideoModelFamily("abra");
                actions.setSelectedVideoDuration(10);
                actions.setAspectRatio("LANDSCAPE");
                actions.setOutputsPerPrompt(1);
                return true;
            }""")
            if success:
                print("[+] Settings successfully locked via React store.")
            else:
                print("[-] ERROR: Settings configuration via React store failed.")
                sys.exit(1)


            # Main Generation Loop (4-and-20 Pacing Protocol)
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
                    
                    # 1. Clear prompt box and ingredients programmatically via React store
                    await page.evaluate("""() => {
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
                        if (!store) return;
                        const actions = store.getState().actions;
                        actions.clearPromptBox();
                        actions.clearIngredients();
                        actions.clearCharacterServerIds();
                        actions.clearLikenessIngredients();
                    }""")
                    await page.wait_for_timeout(300)

                    # 2. Focus the editor, clear any text, and type the prompt text using keyboard
                    editor = page.locator("[data-slate-editor]").first
                    await editor.focus()
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.wait_for_timeout(300)
                    await page.keyboard.type(full_prompt, delay=5)
                    await page.wait_for_timeout(300)

                    # 3. Attach character or likeness programmatically via React store dispatches
                    await page.evaluate("""(data) => {
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
                        if (!store) return;
                        const actions = store.getState().actions;
                        
                        if (data.isWayne) {
                            actions.addLikenessIngredient({
                                likenessId: "0278d9a4-7377-08f0-0000-000000000000",
                                source: 'PLUS_BUTTON'
                            });
                        } else {
                            actions.addCharacterIngredient({
                                characterServerId: "f8e9def1-7fe5-42e8-af6b-10f68e977774",
                                source: 'PLUS_BUTTON'
                            });
                        }
                    }""", {
                        "isWayne": speaker.lower() == "wayne"
                    })
                    await page.wait_for_timeout(500)
                    
                    # Record card count
                    cards_before = len(await page.locator("[aria-roledescription='draggable']").all())
                    
                    # 4. Focus editor and submit via Control+Enter
                    await editor.focus()
                    await page.wait_for_timeout(200)
                    await page.keyboard.press("Control+Enter")
                    
                    # 5. Wait for card to appear
                    card_added = False
                    for _ in range(20):  # 10s max
                        await page.wait_for_timeout(500)
                        cards_after = len(await page.locator("[aria-roledescription='draggable']").all())
                        if cards_after > cards_before:
                            card_added = True
                            break
                            
                    if not card_added:
                        print(f"[-] ERROR: Clip {clip_id} was not added to the project grid after clicking submit! Aborting run.")
                        sys.exit(1)
                        
                    # Check for safety violation/failed state on any card
                    new_cards = await page.locator("[aria-roledescription='draggable']").all()
                    for nc in new_cards:
                        try:
                            card_text = await nc.inner_text()
                            if "failed" in card_text.lower() or "violate" in card_text.lower() or "policy" in card_text.lower():
                                print(f"[-] ERROR: Safety policy or failed state detected on card: '{card_text.strip()}'. Aborting run.")
                                sys.exit(1)
                        except Exception:
                            pass
                            
                    # Check for safety violation/error toast messages
                    toasts = await page.locator("[role='status'], [role='alert'], .toast, .notification").all()
                    for t in toasts:
                        try:
                            t_text = await t.inner_text()
                            if "violate" in t_text.lower() or "policy" in t_text.lower() or "error" in t_text.lower():
                                print(f"[-] ERROR: Safety policy or system toast error detected: '{t_text}'. Aborting run.")
                                sys.exit(1)
                        except Exception:
                            pass
                            
                    print(f"        -> Clip {clip_id} successfully queued.")
                    completed.append(clip_id)
                    save_state(state)
                    await page.wait_for_timeout(1000)
                
                # After submitting a batch of 4, wait 20 seconds before starting the next batch (unless it's the last batch)
                if idx_batch < num_batches - 1:
                    print(f"    [+] Batch queued. Waiting 20 seconds before submitting the next batch...")
                    await asyncio.sleep(20)
            
            # Block and Wait for all submitted clips to finish rendering
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
            
            if not success:
                print(f"[!] Warning: Wait timed out before all clips finished! Check progress manually.")
            
            print("\n[+] ALL QUEUED GENERATIONS HAVE COMPLETED OR RESOLVED!")
            await browser.close()
            
        except Exception as e:
            print(f"[-] Critical script exception: {e}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
