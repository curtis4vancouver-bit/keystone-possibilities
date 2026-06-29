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
STATE_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\flow_generator_state.json")
SCRIPT_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\short_035_fda_peptide_trial.md")

# References Mapping (Detected dynamically on startup, or fallback to these)
WAYNE_WARDROBE_REF = ""
VICTORIA_WARDROBE_REF = ""
BACKGROUND_REF = ""

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
            
            # Dynamically detect reference photo mappings
            print("[+] Detecting reference media IDs dynamically...")
            refs = await page.evaluate("""() => {
                const editor = document.querySelector('[data-slate-editor]');
                if (!editor) return null;
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
                if (!client) return null;
                const query = client.queryCache.queries.find(q => q.queryKey && q.queryKey[0] && q.queryKey[0][0] === 'flow' && q.queryKey[0][1] === 'projectInitialData');
                if (!query || !query.state.data || !query.state.data.projectContents) return null;
                
                const workflows = query.state.data.projectContents.workflows || [];
                let wayne_wardrobe = null;
                let victoria_wardrobe = null;
                let background = null;
                
                for (const w of workflows) {
                    const metadata = w.metadata || {};
                    const displayName = metadata.displayName || "";
                    const primaryMediaId = metadata.primaryMediaId;
                    if (!primaryMediaId) continue;
                    
                    if (displayName === "1") {
                        wayne_wardrobe = primaryMediaId;
                    } else if (displayName === "2") {
                        victoria_wardrobe = primaryMediaId;
                    } else if (displayName.toLowerCase().includes("whistler") || displayName.toLowerCase().includes("cabin")) {
                        background = primaryMediaId;
                    }
                }
                
                return { wayne_wardrobe, victoria_wardrobe, background };
            }""")
            
            global WAYNE_WARDROBE_REF, VICTORIA_WARDROBE_REF, BACKGROUND_REF
            if refs and not isinstance(refs, str) and "error" not in refs:
                WAYNE_WARDROBE_REF = refs.get("wayne_wardrobe") or ""
                VICTORIA_WARDROBE_REF = refs.get("victoria_wardrobe") or ""
                BACKGROUND_REF = refs.get("background") or ""
                print(f"  [+] Detected Wayne Wardrobe: {WAYNE_WARDROBE_REF}")
                print(f"  [+] Detected Victoria Wardrobe: {VICTORIA_WARDROBE_REF}")
                print(f"  [+] Detected Background: {BACKGROUND_REF}")
            else:
                print("  [-] Warning: Dynamic reference detection failed or returned invalid data. Using manual overrides.")

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
                    
                    # Determine speaker settings
                    character_id = None
                    likeness_id = None
                    if speaker.lower() == "wayne":
                        likeness_id = "2e00f1a0-b785-467d-8d86-9b0f2cea70e7" # Wayne's likeness ID
                    else:
                        # Find matching character ID dynamically
                        character_id = await page.evaluate("""() => {
                            const editor = document.querySelector('[data-slate-editor]');
                            if (!editor) return null;
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
                            if (!client) return null;
                            const query = client.queryCache.queries.find(q => q.queryKey && q.queryKey[0] && q.queryKey[0][0] === 'flow' && q.queryKey[0][1] === 'projectInitialData');
                            if (!query || !query.state.data || !query.state.data.projectContents) return null;
                            const char = (query.state.data.projectContents.workflows || [])
                                .filter(w => w.type === 'CHARACTER')
                                .find(w => w.title && w.title.toLowerCase().includes('victoria'));
                            return char ? char.id : null;
                        }""")
                        if not character_id:
                            character_id = "fc82097f-7d54-4d1c-88da-aa8e68018148"
                    
                    # Prepare reference image IDs
                    ref_image_ids = []
                    if speaker.lower() == "wayne" and WAYNE_WARDROBE_REF:
                        ref_image_ids.append(WAYNE_WARDROBE_REF)
                    elif speaker.lower() == "victoria" and VICTORIA_WARDROBE_REF:
                        ref_image_ids.append(VICTORIA_WARDROBE_REF)
                    if BACKGROUND_REF:
                        ref_image_ids.append(BACKGROUND_REF)

                    # Clear and type prompt via React store to keep things clean
                    await page.evaluate("""({promptText, characterId, likenessId, referenceImageIds}) => {
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
                        
                        // 1. Clear everything
                        actions.clearPromptBox();
                        actions.clearIngredients();
                        actions.clearCharacterServerIds();
                        actions.clearLikenessIngredients();
                        
                        // 2. Set prompt
                        actions.setPrompt(promptText);
                        
                        // 3. Attach character/likeness
                        if (characterId) {
                            actions.addCharacterIngredient({
                                characterServerId: characterId,
                                source: 'PLUS_BUTTON'
                            });
                        }
                        if (likenessId) {
                            actions.addLikenessIngredient({
                                likenessId: likenessId,
                                source: 'PLUS_BUTTON'
                            });
                        }
                        
                        // 4. Attach reference images using official addImageIngredient
                        if (referenceImageIds && referenceImageIds.length > 0) {
                            referenceImageIds.forEach(id => {
                                if (id) {
                                    actions.addImageIngredient({
                                        imageId: id,
                                        preferredIngredientType: 'REFERENCE',
                                        source: 'PLUS_BUTTON'
                                    });
                                }
                            });
                        }
                    }""", {
                        "promptText": full_prompt,
                        "characterId": character_id,
                        "likenessId": likeness_id,
                        "referenceImageIds": ref_image_ids
                    })
                    
                    await page.wait_for_timeout(800)
                    
                    # Click submit
                    submit_btn = page.get_by_role("button", name="arrow_forward").first
                    if not await submit_btn.is_visible():
                        submit_btn = page.get_by_role("button", name="Create").first
                    await submit_btn.click(force=True, timeout=5000)
                    
                    print(f"        -> Clip {clip_id} submitted to Google Flow with references: {ref_image_ids}")
                    await page.wait_for_timeout(1500)
                
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
