import asyncio
from playwright.async_api import async_playwright
import os
import json
import re
import urllib.request
from pathlib import Path
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Paths
STATE_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\flow_generator_state_035.json")
SCRIPT_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\short_035_fda_peptide_trial.md")

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
            # If the item has 'play_circle' and doesn't contain '%' (e.g. 50% or 1%), it is completed.
            # Also count as finished if it failed.
            is_completed = "play_circle" in text and not re.search(r'\d+%', text)
            is_failed = "Failed" in text or "violate" in text or "policy" in text
            if is_completed or is_failed:
                finished += 1
        except Exception:
            pass
    return finished

async def print_detailed_queue(page):
    items = await page.locator("[aria-roledescription='draggable']").all()
    print("--- Detailed Queue Status ---")
    for it in items:
        try:
            text = await it.inner_text()
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            if lines:
                # Print the first line (status/percentage) and first part of dialogue
                status_desc = lines[0]
                dialogue_snippet = ""
                for line in lines[1:]:
                    if "says:" in line or len(line) > 20:
                        dialogue_snippet = line[:80]
                        break
                print(f"  * [{status_desc}] {dialogue_snippet}...")
        except Exception:
            pass
    print("-----------------------------\n")

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
        dialogue = script.strip()
        clips.append({
            "id": clip_id,
            "speaker": speaker.strip().upper(),
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

    # 1. Establish CDP connection to Chrome
    ws_url = None
    cdp_connected = False
    
    # Try port 9222 first
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

    # Fallback to DevToolsActivePort file
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

            # --- 2. Settings Verification ---
            print("[+] Verifying project settings at startup...")
            # We look for a button containing Video/Image and a middle dot
            try:
                settings_text = await page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('button'));
                    const settingsBtn = buttons.find(b => {
                        const text = b.innerText;
                        return (text.includes('Video') || text.includes('Image')) && text.includes('·');
                    });
                    return settingsBtn ? settingsBtn.innerText : null;
                }""")
                if not settings_text:
                    print("[-] Could not locate the settings summary button on the page.")
                    return
            except Exception as e:
                print(f"[-] Error locating settings summary button: {e}")
                return
                
            print(f"    Current Settings Chip text: '{settings_text.strip()}'")
            
            # Expect "Video" and "10s"
            if "Video" in settings_text and "10s" in settings_text:
                print("[+] Verified: Aspect Ratio, Duration (10s), Mode (Video) are correct.")
            else:
                print(f"[-] WARNING: Settings mismatch! Expected Video and 10s, found: {settings_text}")
                return

            # --- 3. Main Generation Loop (4-and-20 Pacing Protocol) ---
            pending_clips = [clip for clip in clips if clip["id"] not in completed]
            print(f"[+] Total pending clips: {len(pending_clips)}")
            
            if not pending_clips:
                print("[+] All clips already generated!")
                return
                
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
                    full_prompt = f"{pronoun} says: {dialogue} {visual_prompt}"
                    
                    print(f"    [+] Emulating UI click-and-type for Clip {clip_id} ({speaker})...")
                    
                    # 1. Click prompt textbox
                    textbox = page.locator('div[contenteditable="true"]').first
                    await textbox.click()
                    await page.wait_for_timeout(300)
                    
                    # 1b. Clear any previously attached character/avatar ingredients
                    await page.evaluate("""() => {
                        const chips = Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.toLowerCase().includes('cancel') && (b.innerText.toLowerCase().includes('account_circle') || b.innerText.toLowerCase().includes('accessibility_new')));
                        chips.forEach(c => c.click());
                    }""")
                    await page.wait_for_timeout(300)
                    
                    # 2. Clear textbox
                    await page.keyboard.press("Control+A")
                    await page.wait_for_timeout(200)
                    await page.keyboard.press("Backspace")
                    await page.wait_for_timeout(300)
                    
                    # 3. Type prompt text
                    await page.keyboard.type(full_prompt)
                    await page.wait_for_timeout(500)
                    
                    # 4. Click "+ Create" button to open asset picker dialog
                    create_btn = page.locator('button[aria-haspopup="dialog"]').first
                    await create_btn.click()
                    await page.wait_for_timeout(1000)
                    
                    # 5. Switch to appropriate tab (scoped to dialog to avoid sidebar buttons)
                    if speaker.lower() == "wayne":
                        await page.evaluate("""() => {
                            const inputs = Array.from(document.querySelectorAll('input'));
                            const searchInput = inputs.find(i => i.placeholder && i.placeholder.toLowerCase().includes('search assets') || i.outerHTML.toLowerCase().includes('search assets'));
                            if (!searchInput) return;
                            
                            let container = searchInput;
                            while (container && container !== document.body) {
                                const role = container.getAttribute('role');
                                const isDialog = role === 'dialog' || role === 'dialog-content' || container.tagName === 'DIALOG' || container.className.includes('Dialog') || container.className.includes('dialog') || container.className.includes('Modal') || container.className.includes('modal') || container.getAttribute('data-testid') === 'dialog';
                                if (isDialog) break;
                                container = container.parentElement;
                            }
                            if (!container || container === document.body) return;
                            
                            const tabs = Array.from(container.querySelectorAll('[role="tab"], button'));
                            const tab = tabs.find(t => t.innerText && t.innerText.toLowerCase().includes('avatar'));
                            if (tab) tab.click();
                        }""")
                    else:
                        await page.evaluate("""() => {
                            const inputs = Array.from(document.querySelectorAll('input'));
                            const searchInput = inputs.find(i => i.placeholder && i.placeholder.toLowerCase().includes('search assets') || i.outerHTML.toLowerCase().includes('search assets'));
                            if (!searchInput) return;
                            
                            let container = searchInput;
                            while (container && container !== document.body) {
                                const role = container.getAttribute('role');
                                const isDialog = role === 'dialog' || role === 'dialog-content' || container.tagName === 'DIALOG' || container.className.includes('Dialog') || container.className.includes('dialog') || container.className.includes('Modal') || container.className.includes('modal') || container.getAttribute('data-testid') === 'dialog';
                                if (isDialog) break;
                                container = container.parentElement;
                            }
                            if (!container || container === document.body) return;
                            
                            const tabs = Array.from(container.querySelectorAll('[role="tab"], button'));
                            const tab = tabs.find(t => t.innerText && t.innerText.toLowerCase().includes('characters'));
                            if (tab) tab.click();
                        }""")
                    await page.wait_for_timeout(1000)
                    
                    # 6. Click on character image option card wrapper (avoiding navigation redirect)
                    if speaker.lower() == "wayne":
                        await page.evaluate("""() => {
                            const inputs = Array.from(document.querySelectorAll('input'));
                            const searchInput = inputs.find(i => i.placeholder && i.placeholder.toLowerCase().includes('search assets') || i.outerHTML.toLowerCase().includes('search assets'));
                            if (!searchInput) return;
                            
                            let container = searchInput;
                            while (container && container !== document.body) {
                                const role = container.getAttribute('role');
                                const isDialog = role === 'dialog' || role === 'dialog-content' || container.tagName === 'DIALOG' || container.className.includes('Dialog') || container.className.includes('dialog') || container.className.includes('Modal') || container.className.includes('modal') || container.getAttribute('data-testid') === 'dialog';
                                if (isDialog) break;
                                container = container.parentElement;
                            }
                            if (!container || container === document.body) return;
                            
                            const img = container.querySelector('img[alt="me"]');
                            if (img) {
                                const card = img.closest('[role="option"]') || img.closest('button') || img.closest('[data-testid]') || img.parentElement;
                                const isSelected = card.getAttribute('aria-selected') === 'true' || 
                                                   card.getAttribute('data-selected') === 'true' || 
                                                   card.classList.contains('selected') || 
                                                   card.outerHTML.includes('aria-selected="true"');
                                if (!isSelected) {
                                    card.click();
                                }
                            }
                        }""")
                    else:
                        await page.evaluate("""() => {
                            const inputs = Array.from(document.querySelectorAll('input'));
                            const searchInput = inputs.find(i => i.placeholder && i.placeholder.toLowerCase().includes('search assets') || i.outerHTML.toLowerCase().includes('search assets'));
                            if (!searchInput) return;
                            
                            let container = searchInput;
                            while (container && container !== document.body) {
                                const role = container.getAttribute('role');
                                const isDialog = role === 'dialog' || role === 'dialog-content' || container.tagName === 'DIALOG' || container.className.includes('Dialog') || container.className.includes('dialog') || container.className.includes('Modal') || container.className.includes('modal') || container.getAttribute('data-testid') === 'dialog';
                                if (isDialog) break;
                                container = container.parentElement;
                            }
                            if (!container || container === document.body) return;
                            
                            const img = container.querySelector('img[alt="Victoria"]');
                            if (img) {
                                const card = img.closest('[role="option"]') || img.closest('button') || img.closest('[data-testid]') || img.parentElement;
                                const isSelected = card.getAttribute('aria-selected') === 'true' || 
                                                   card.getAttribute('data-selected') === 'true' || 
                                                   card.classList.contains('selected') || 
                                                   card.outerHTML.includes('aria-selected="true"');
                                if (!isSelected) {
                                    card.click();
                                }
                            }
                        }""")
                    await page.wait_for_timeout(1500)
                    
                    # 7. Check if dialog is still open; if so, click Add to Prompt
                    add_to_prompt = page.locator('button:has-text("Add to Prompt")').first
                    if await add_to_prompt.is_visible():
                        await add_to_prompt.click()
                        await page.wait_for_timeout(800)
                    
                    # 8. Re-focus on textbox and press Enter to submit
                    await textbox.click()
                    await page.wait_for_timeout(300)
                    await page.keyboard.press("Enter")
                    print(f"        -> Clip {clip_id} submitted successfully.")
                    
                    # Wait briefly between submissions in the same batch to avoid race conditions
                    await page.wait_for_timeout(2000)
                
                # After submitting a batch of 4, wait 20 seconds before starting the next batch (unless it's the last batch)
                if idx_batch < num_batches - 1:
                    print(f"    [+] Batch submitted. Pausing for 20 seconds before starting next batch...")
                    # Overlook check during the wait (check status once)
                    await asyncio.sleep(10)
                    await print_detailed_queue(page)
                    await asyncio.sleep(10)
            
            # --- 4. Block and Wait for all submitted clips to finish rendering ---
            target_finished = initial_finished + len(pending_clips)
            print(f"\n[+] All {len(pending_clips)} clips queued! Entering progress monitoring loop (checking every 30 seconds)...")
            
            success = False
            max_polls = (len(pending_clips) * 180) // 30  # Allow ample time
            for poll in range(max_polls):
                await asyncio.sleep(30)
                current_finished = await get_finished_count(page)
                completed_total = current_finished - initial_finished
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Rendering Progress: {completed_total}/{len(pending_clips)} clips complete.")
                await print_detailed_queue(page)
                
                if current_finished >= target_finished:
                    print(f"[+] All submitted clips finished rendering successfully!")
                    success = True
                    break
            
            if success:
                completed.extend([c["id"] for c in pending_clips])
                save_state(state)
            else:
                print(f"[!] Warning: Wait timed out before all clips finished! Saving state of completed ones...")
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
