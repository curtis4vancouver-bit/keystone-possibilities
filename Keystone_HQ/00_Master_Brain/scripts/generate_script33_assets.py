# generate_script33_assets.py
import asyncio
from playwright.async_api import async_playwright
import os
import json
import re
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Paths
STATE_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\flow_generator_state_33.json")
SCRIPT_FILE = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\glp1_anhedonia_8m20s_studio_black.md")
DESKTOP_DIR = Path(r"C:\Users\Curtis\Desktop\LONG_033_GLP1_ANHEDONIA")

# References Mapping (Paste fe_id_<mediaName> here if using reference photos/wardrobes/backgrounds)
WAYNE_WARDROBE_REF = ""
VICTORIA_WARDROBE_REF = ""
BACKGROUND_REF = ""

# Detect aspect ratio based on project directory name
IS_SHORT = "SHORT" in str(DESKTOP_DIR).upper()
ASPECT_RATIO = "9:16" if IS_SHORT else "16:9"
print(f"[+] Configuration: {'Shorts (9:16)' if IS_SHORT else 'Long-Form (16:9)'} aspect ratio detected.")

# Ensure target directories exist
(DESKTOP_DIR / "Videos").mkdir(parents=True, exist_ok=True)
(DESKTOP_DIR / "Images").mkdir(parents=True, exist_ok=True)

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"completed_clips": [], "completed_brolls": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

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

async def submit_video_clip(page, clip):
    """Submit a single video clip. Attaches avatar/character (face) + clothing and background references."""
    clip_id = clip["id"]
    speaker = clip["speaker"]
    dialogue = clip["dialogue"]
    visual_prompt = clip["prompt"]
    
    # Build full prompt: generic pronoun + dialogue + visual directions
    # DO NOT use real names — triggers Google Flow policy violations.
    pronoun = "He" if speaker.lower() == "wayne" else "She"
    full_prompt = f"{pronoun} says: {dialogue}. {visual_prompt}"
    
    print(f"  [{clip_id}] Submitting ({speaker})...")
    
    # Escape any open dialogs
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(500)
    
    # Determine speaker settings
    character_id = None
    likeness_id = None
    if speaker.lower() == "wayne":
        likeness_id = "2e00f1a0-b785-467d-8d86-9b0f2cea70e7" # Wayne's likeness ID
    else:
        # Find matching character ID from project context
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
            # Fallback to standard Victoria character ID if not found dynamically
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
        
        // 4. Attach reference images (wardrobe, background)
        if (referenceImageIds && referenceImageIds.length > 0) {
            const currentIngredients = store.getState().ingredients || [];
            const newIngredients = [...currentIngredients];
            referenceImageIds.forEach(id => {
                if (id) {
                    newIngredients.push({
                        ingredientId: id,
                        isLoading: false,
                        addedTime: new Date(),
                        modifiedTime: new Date(),
                        preferredIngredientType: 'REFERENCE'
                    });
                }
            });
            store.setState({ ingredients: newIngredients });
        }
    }""", {
        "promptText": full_prompt,
        "characterId": character_id,
        "likenessId": likeness_id,
        "referenceImageIds": ref_image_ids
    })
    
    await page.wait_for_timeout(800)
    
    # Click the submit arrow button
    submit_btn = page.locator("button:has-text('arrow_forward')").first
    if not await submit_btn.is_visible():
        submit_btn = page.locator("button:has-text('Create')").last
    await submit_btn.click(force=True, timeout=3000)
    
    print(f"  [{clip_id}] Submitted successfully with references: {ref_image_ids}")
    await page.wait_for_timeout(2000)

async def submit_broll(page, broll):
    """Submit a single B-roll image generation. No avatar needed."""
    b_id = broll["id"]
    prompt = broll["prompt"]
    
    print(f"  [{b_id}] Submitting B-roll...")
    
    # Escape any open dialogs
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(500)
    
    # Clear reference chips
    try:
        cancel_btns = page.locator("button:has-text('cancel')")
        btn_count = await cancel_btns.count()
        for _ in range(min(btn_count, 5)):
            try:
                await cancel_btns.first.click(force=True, timeout=1000)
                await page.wait_for_timeout(300)
            except Exception:
                break
    except Exception:
        pass
    
    # Clear text box
    textbox = page.locator("div[contenteditable='true'], textarea").first
    await textbox.click(force=True)
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await page.wait_for_timeout(300)
    
    # Type prompt
    await page.keyboard.insert_text(prompt)
    await page.wait_for_timeout(500)
    
    # Submit directly (no avatar/character needed for B-roll images)
    submit_btn = page.locator("button:has-text('arrow_forward')").first
    if not await submit_btn.is_visible():
        submit_btn = page.locator("button:has-text('Create')").last
    await submit_btn.click(force=True, timeout=3000)
    
    print(f"  [{b_id}] Submitted successfully.")
    await page.wait_for_timeout(1500)

async def wait_for_batch(page, initial_count, batch_size, timeout_per_item=120, poll_interval=10):
    """Wait for a batch of generations to complete."""
    target = initial_count + batch_size
    max_wait = batch_size * timeout_per_item
    elapsed = 0
    
    while elapsed < max_wait:
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
        
        items = await page.locator("[aria-roledescription='draggable']").all()
        finished = 0
        for it in items:
            try:
                text = await it.inner_text()
                has_play = "play_circle" in text
                has_image = "Generated image" in text
                is_loading = bool(re.search(r'\d+%', text))
                is_failed = "Failed" in text or "violate" in text or "cancelled" in text or "refunded" in text or "Error" in text
                if (has_play or has_image or is_failed) and not is_loading:
                    finished += 1
            except Exception:
                pass
        
        done = finished - initial_count
        print(f"    Progress: {done}/{batch_size} completed ({elapsed}s elapsed)")
        
        if finished >= target:
            return True
    
    return False

async def count_finished(page):
    """Count finished (non-loading) items in the grid."""
    items = await page.locator("[aria-roledescription='draggable']").all()
    finished = 0
    for it in items:
        try:
            text = await it.inner_text()
            has_play = "play_circle" in text
            has_image = "Generated image" in text
            is_loading = bool(re.search(r'\d+%', text))
            is_failed = "Failed" in text or "violate" in text or "cancelled" in text or "refunded" in text or "Error" in text
            if (has_play or has_image or is_failed) and not is_loading:
                finished += 1
        except Exception:
            pass
    return finished

async def count_loading(page):
    """Count currently loading/generating items in the grid."""
    items = await page.locator("[aria-roledescription='draggable']").all()
    loading = 0
    for it in items:
        try:
            text = await it.inner_text()
            is_loading = bool(re.search(r'\d+%', text)) or "Generating" in text or "loading" in text.lower()
            if is_loading:
                loading += 1
        except Exception:
            pass
    return loading

async def wait_for_loading_complete(page, timeout=120, poll_interval=5):
    """Wait until there are no loading items in the grid."""
    elapsed = 0
    while elapsed < timeout:
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval
        loading = await count_loading(page)
        print(f"    Waiting for images to finish... ({loading} loading, {elapsed}s elapsed)")
        if loading == 0:
            return True
    return False

async def switch_to_video_mode(page):
    """Ensure the settings are: Video, Omni Flash, 10s, ASPECT_RATIO."""
    expected_ratio_str = f"crop_{ASPECT_RATIO.replace(':', '_')}"
    print(f"[+] Setting mode to Video / Omni Flash / 10s / {ASPECT_RATIO} (expecting {expected_ratio_str})...")
    
    # Escape any open dialogs first
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(500)
    
    # 1. Switch to Video Mode / Omni Flash if not active
    try:
        settings_btn = page.locator("button:has-text('crop_'), button:has-text('1x')").first
        if await settings_btn.is_visible():
            btn_text = await settings_btn.inner_text()
            if "Banana" in btn_text or "Image" in btn_text:
                await settings_btn.click(force=True)
                await page.wait_for_timeout(1000)
                video_tab = page.locator("button:has-text('Video'), [role='tab']:has-text('Video')").first
                if await video_tab.is_visible():
                    await video_tab.click(force=True)
                    await page.wait_for_timeout(500)
                omni_btn = page.locator("button:has-text('Omni'), [role='tab']:has-text('Omni')").first
                if await omni_btn.is_visible():
                    await omni_btn.click(force=True)
                    await page.wait_for_timeout(500)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)
    except Exception as e:
        print(f"  [-] Model selection error: {e}")

    # 2. Configure Duration and Aspect Ratio
    for attempt in range(3):
        settings_btn = page.locator("button:has-text('crop_'), button:has-text('1x')").first
        if not await settings_btn.is_visible():
            print("  [-] Settings button not visible, cannot configure settings.")
            break
            
        btn_text = await settings_btn.inner_text()
        needs_duration = "10s" not in btn_text
        needs_ratio = expected_ratio_str not in btn_text
        
        if not (needs_duration or needs_ratio):
            print(f"  [+] Settings are correct: {btn_text.strip().replace(chr(10), ' ')}")
            return
            
        print(f"  [Attempt {attempt+1}] Configuring (current: {btn_text.strip().replace(chr(10), ' ')})...")
        await settings_btn.click(force=True)
        await page.wait_for_timeout(1000)
        
        # Set duration to 10s
        if needs_duration:
            duration_10s = page.locator("button:has-text('10s'), [role='tab']:has-text('10s')").first
            if await duration_10s.is_visible():
                await duration_10s.click(force=True)
                print("    [+] Duration set to 10s.")
                await page.wait_for_timeout(500)
        
        # Set aspect ratio
        if needs_ratio:
            ratio_tab = page.locator(f"[role='tab']:has-text('{ASPECT_RATIO}'), button:has-text('{ASPECT_RATIO}')").first
            if not await ratio_tab.is_visible():
                ratio_tab = page.locator(f"[role='tab']:has-text('{expected_ratio_str}'), button:has-text('{expected_ratio_str}')").first
            if await ratio_tab.is_visible():
                await ratio_tab.click(force=True)
                print(f"    [+] Aspect ratio clicked for {ASPECT_RATIO}.")
                await page.wait_for_timeout(500)
            else:
                print(f"    [-] Could not locate {ASPECT_RATIO} tab in menu.")
        
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)
        
    # Final check
    btn_text = await settings_btn.inner_text()
    if expected_ratio_str not in btn_text or "10s" not in btn_text:
        raise Exception(f"CRITICAL: Failed to configure settings to Video / 10s / {ASPECT_RATIO}. Current settings button: {repr(btn_text)}")
    print("[+] Video mode configured.")

async def switch_to_image_mode(page):
    """Ensure the settings are: Image, Nano Banana Pro, ASPECT_RATIO."""
    expected_ratio_str = f"crop_{ASPECT_RATIO.replace(':', '_')}"
    print(f"[+] Switching to Image / Nano Banana Pro / {ASPECT_RATIO} (expecting {expected_ratio_str})...")
    
    # Escape any open dialogs first
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(500)
    
    for attempt in range(3):
        settings_btn = page.locator("button:has-text('crop_'), button:has-text('1x')").first
        if not await settings_btn.is_visible():
            print("  [-] Settings button not visible, cannot configure settings.")
            break
            
        btn_text = await settings_btn.inner_text()
        needs_switch = "Banana" not in btn_text or "Image" not in btn_text
        needs_ratio = expected_ratio_str not in btn_text
        
        if not (needs_switch or needs_ratio):
            print(f"  [+] Image settings are correct: {btn_text.strip().replace(chr(10), ' ')}")
            return
            
        print(f"  [Attempt {attempt+1}] Configuring Image settings (current: {btn_text.strip().replace(chr(10), ' ')})...")
        await settings_btn.click(force=True)
        await page.wait_for_timeout(1000)
        
        if needs_switch:
            # Click Image tab
            image_tab = page.locator("button:has-text('Image'), [role='tab']:has-text('Image')").first
            if await image_tab.is_visible():
                await image_tab.click(force=True)
                await page.wait_for_timeout(500)
            
            # Select Banana Pro
            banana_btn = page.locator("button:has-text('Banana'), button:has-text('Nano Banana Pro')").first
            if await banana_btn.is_visible():
                await banana_btn.click(force=True)
                await page.wait_for_timeout(500)
        
        # Set aspect ratio
        if needs_ratio:
            ratio_tab = page.locator(f"[role='tab']:has-text('{ASPECT_RATIO}'), button:has-text('{ASPECT_RATIO}')").first
            if not await ratio_tab.is_visible():
                ratio_tab = page.locator(f"[role='tab']:has-text('{expected_ratio_str}'), button:has-text('{expected_ratio_str}')").first
            if await ratio_tab.is_visible():
                await ratio_tab.click(force=True)
                print(f"    [+] Aspect ratio clicked for {ASPECT_RATIO}.")
                await page.wait_for_timeout(500)
            else:
                print(f"    [-] Could not locate {ASPECT_RATIO} tab in menu.")
                
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)
        
    # Final check
    btn_text = await settings_btn.inner_text()
    if expected_ratio_str not in btn_text or ("Banana" not in btn_text and "Image" not in btn_text):
        raise Exception(f"CRITICAL: Failed to configure settings to Image / Banana Pro / {ASPECT_RATIO}. Current settings button: {repr(btn_text)}")
    print("[+] Image mode configured.")

async def main():
    clips, brolls = parse_script()
    print(f"[+] Parsed {len(clips)} video clips and {len(brolls)} B-roll images.")
    
    if len(clips) == 0:
        print("[-] No clips found! Check script file format.")
        return
    
    state = load_state()
    # Resume state
    print(f"[+] Resuming state: {len(state['completed_clips'])} clips, {len(state['completed_brolls'])} B-rolls already completed.")
    
    # Check for test flag
    test_mode = "--test" in sys.argv
    if test_mode:
        print("[!] TEST MODE ENGAGED: Restricting run to first 2 clips.")
        clips = clips[:2]
        brolls = brolls[:2]
    
    # Connect to Chrome
    try:
        with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
            lines = f.read().splitlines()
        port = lines[0]
        path = lines[1]
        ws_url_local = f"ws://localhost:{port}{path}"
        ws_url_ip = f"ws://127.0.0.1:{port}{path}"
        print(f"[+] WebSocket options: {ws_url_local} or {ws_url_ip}")
    except Exception as e:
        print(f"[-] Cannot read DevToolsActivePort: {e}")
        return

    async with async_playwright() as p:
        try:
            # Try connecting via localhost first
            try:
                print("[+] Connecting to Chrome via localhost...")
                browser = await p.chromium.connect_over_cdp(ws_url_local)
            except Exception as e_local:
                print(f"[-] Connection via localhost failed ({e_local}). Retrying via 127.0.0.1...")
                browser = await p.chromium.connect_over_cdp(ws_url_ip)
                
            context = browser.contexts[0]
            
            page = None
            for p_ in context.pages:
                if "labs.google/fx/tools/flow/project" in p_.url:
                    page = p_
                    break
            
            if not page:
                print("[-] Google Flow project tab not found!")
                return
            
            # If in edit view, navigate back to project root
            if "/edit/" in page.url or "/character/" in page.url:
                project_url = page.url.split("/edit/")[0].split("/character/")[0]
                print(f"[+] Navigating back to project root: {project_url}")
                await page.goto(project_url)
                await page.wait_for_timeout(3000)
            
            print(f"[+] Connected to Flow: {page.url}")
            await page.bring_to_front()
            
            # ═══════════════════════════════════════════════
            # PHASE 1: GENERATE ALL VIDEO CLIPS
            # ═══════════════════════════════════════════════
            print("\n" + "=" * 60)
            print(f"  PHASE 1: GENERATING VIDEO CLIPS (Omni Flash, 10s)")
            print("=" * 60)
            
            # Filter out already completed clips
            remaining_clips = [c for c in clips if c["id"] not in state["completed_clips"]]
            print(f"[+] Remaining video clips to generate: {len(remaining_clips)}")
            
            if len(remaining_clips) > 0:
                await switch_to_video_mode(page)
                
                BATCH_SIZE = 4  # Wayne requested 4 at a time
                for batch_start in range(0, len(remaining_clips), BATCH_SIZE):
                    batch = remaining_clips[batch_start:batch_start + BATCH_SIZE]
                    batch_ids = [c["id"] for c in batch]
                    print(f"\n--- Batch: {', '.join(batch_ids)} ---")
                    
                    for clip in batch:
                        await submit_video_clip(page, clip)
                    
                    # Mark as completed/submitted in state so we don't submit them again if we resume
                    state["completed_clips"].extend(batch_ids)
                    save_state(state)
                    print(f"  ✓ Batch {', '.join(batch_ids)} submitted.")
                    
                    # Wayne's specific request: "do 4 and then wait 20 seconds and then do another 4"
                    if batch_start + BATCH_SIZE < len(remaining_clips):
                        print(f"  Waiting 20 seconds before starting the next batch...")
                        await asyncio.sleep(20)
                
                # Now wait for all submitted/generating videos to finish
                print("\nWaiting for all video clips to finish generating...")
                wait_time = 0
                while True:
                    loading_count = await count_loading(page)
                    if loading_count == 0:
                        print("[+] All videos finished generating.")
                        break
                    print(f"    [{wait_time}s] {loading_count} video(s) still generating. Waiting 15 seconds...")
                    await asyncio.sleep(15)
                    wait_time += 15
                    if wait_time > 2400: # 40 minutes safety timeout
                        print("[-] Safety timeout reached while waiting for videos to finish.")
                        break
            
            print(f"\n✓ VIDEO CLIPS GENERATION PHASE COMPLETE!")
            
            # ═══════════════════════════════════════════════
            # PHASE 2: GENERATE ALL B-ROLL IMAGES
            # ═══════════════════════════════════════════════
            print("\n" + "=" * 60)
            print(f"  PHASE 2: GENERATING B-ROLL IMAGES (Banana Pro)")
            print("=" * 60)
            
            await switch_to_image_mode(page)
            
            # Filter out already completed B-rolls
            remaining_brolls = [b for b in brolls if b["id"] not in state["completed_brolls"]]
            print(f"[+] Remaining B-rolls to generate: {len(remaining_brolls)}")
            
            BROLL_BATCH = 5  # Images are free + fast, can do larger batches
            for batch_start in range(0, len(remaining_brolls), BROLL_BATCH):
                batch = remaining_brolls[batch_start:batch_start + BROLL_BATCH]
                batch_ids = [b["id"] for b in batch]
                print(f"\n--- Batch: {', '.join(batch_ids)} ---")
                
                for broll in batch:
                    await submit_broll(page, broll)
                
                print(f"  Waiting for batch {', '.join(batch_ids)} to finish generating...")
                await page.wait_for_timeout(3000)
                
                success = await wait_for_loading_complete(page, timeout=120, poll_interval=5)
                
                if success:
                    state["completed_brolls"].extend(batch_ids)
                    save_state(state)
                    print(f"  ✓ B-roll batch {', '.join(batch_ids)} DONE")
                else:
                    print(f"  ⚠ B-roll batch timed out.")
                    state["completed_brolls"].extend(batch_ids)
                    save_state(state)
            
            print(f"\n✓ B-ROLL IMAGES GENERATION PHASE COMPLETE!")
            print("\n" + "=" * 60)
            print("  ALL ASSET GENERATION COMPLETE!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[-] CRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
