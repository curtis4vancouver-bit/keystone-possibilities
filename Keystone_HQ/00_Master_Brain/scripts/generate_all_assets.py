"""
LONG_001 — Google Flow Asset Generator (Black Background Edition)
Generates all 50 video clips FIRST (Omni Flash, 10s, 16:9)
Then generates all 50 B-roll images SECOND (Nano Banana Pro, 16:9)

Videos: Attach avatar/character only (face reference for consistency).
        No file uploads. The prompt itself specifies solid black background.
B-rolls: No avatar needed. Just the text prompt.

Uses chrome-devtools-mcp style Playwright automation.
"""
import asyncio
from playwright.async_api import async_playwright
import os
import json
import re
from pathlib import Path
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Paths
STATE_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\flow_generator_state.json")
SCRIPT_FILE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\short_035_fda_peptide_trial.md")
DESKTOP_DIR = Path(r"C:\Users\Curtis\Desktop\LONG_FORM_PRODUCTION")

# References Mapping (Detected dynamically on startup, or fallback to these)
WAYNE_WARDROBE_REF = ""
VICTORIA_WARDROBE_REF = ""
BACKGROUND_REF = ""

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
        # Check if we can find Wayne character or likeness. Wayne uses likeness.
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
    await page.wait_for_timeout(300)
    
    # Clear and set B-roll prompt via React store to keep things clean
    await page.evaluate("""({promptText}) => {
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
    }""", {
        "promptText": prompt
    })
    
    await page.wait_for_timeout(500)
    
    # Submit directly
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
                is_failed = "Failed" in text or "violate" in text
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
            is_failed = "Failed" in text or "violate" in text
            if (has_play or has_image or is_failed) and not is_loading:
                finished += 1
        except Exception:
            pass
    return finished

async def switch_to_video_mode(page):
    """Ensure the settings are: Video, Omni Flash, 10s, 16:9."""
    print("[+] Programmatically setting mode to Video / Omni Flash / 10s / 16:9...")
    try:
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
            print("  [+] Video mode configured programmatically via React store.")
            await page.wait_for_timeout(250)
        else:
            print("  [-] Could not access promptBoxStore to configure video settings.")
    except Exception as e:
        print(f"  [-] Settings error: {e}")

async def switch_to_image_mode(page):
    """Ensure the settings are: Image, Banana Pro, 16:9."""
    print("[+] Programmatically setting mode to Image / Banana Pro / 16:9...")
    try:
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
            actions.setMode("IMAGE");
            actions.setImageModelFamily("nano_banana_pro");
            actions.setAspectRatio("LANDSCAPE");
            return true;
        }""")
        if success:
            print("  [+] Image mode configured programmatically via React store.")
            await page.wait_for_timeout(250)
        else:
            print("  [-] Could not access promptBoxStore to configure image settings.")
    except Exception as e:
        print(f"  [-] Settings error: {e}")

async def main():
    clips, brolls = parse_script()
    print(f"[+] Parsed {len(clips)} video clips and {len(brolls)} B-roll images.")
    
    if len(clips) == 0:
        print("[-] No clips found! Check script file format.")
        return
    
    state = load_state()
    # Initialize keys if missing
    if "completed_clips" not in state:
        state["completed_clips"] = []
    if "completed_brolls" not in state:
        state["completed_brolls"] = []
        
    print(f"[+] Resuming state: {len(state['completed_clips'])} clips, {len(state['completed_brolls'])} B-rolls already completed.")
    
    # Connect to Chrome
    try:
        with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
            lines = f.read().splitlines()
        port = lines[0]
        path = lines[1]
        ws_url = f"ws://127.0.0.1:{port}{path}"
        print(f"[+] WebSocket: {ws_url}")
    except Exception as e:
        print(f"[-] Cannot read DevToolsActivePort: {e}")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(ws_url)
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
            
            # ═══════════════════════════════════════════════
            # PHASE 1: GENERATE ALL 50 VIDEO CLIPS
            # ═══════════════════════════════════════════════
            print("\n" + "=" * 60)
            print("  PHASE 1: GENERATING VIDEO CLIPS (Omni Flash, 10s)")
            print("=" * 60)
            
            # Filter out already completed clips
            remaining_clips = [c for c in clips if c["id"] not in state["completed_clips"]]
            print(f"[+] Remaining video clips to generate: {len(remaining_clips)}")
            
            if remaining_clips:
                await switch_to_video_mode(page)
                
                BATCH_SIZE = 4  # 4 at a time
                num_video_batches = (len(remaining_clips) + BATCH_SIZE - 1) // BATCH_SIZE
                
                initial_finished_videos = await count_finished(page)
                print(f"    Initial finished cards count before video generation: {initial_finished_videos}")
                
                for idx_batch in range(num_video_batches):
                    start_idx = idx_batch * BATCH_SIZE
                    batch = remaining_clips[start_idx:start_idx + BATCH_SIZE]
                    batch_ids = [c["id"] for c in batch]
                    print(f"\n--- Queueing Video Batch {idx_batch+1}/{num_video_batches}: {', '.join(batch_ids)} ---")
                    
                    for clip in batch:
                        await submit_video_clip(page, clip)
                    
                    if idx_batch < num_video_batches - 1:
                        print("  Waiting 20 seconds before queueing next video batch...")
                        await asyncio.sleep(20)
                
                # Now wait for all to finish
                target_finished_videos = initial_finished_videos + len(remaining_clips)
                print(f"\n[+] All {len(remaining_clips)} videos queued. Waiting for all of them to finish rendering (target finished count: {target_finished_videos})...")
                
                success = await wait_for_batch(page, initial_finished_videos, len(remaining_clips), timeout_per_item=150)
                if success:
                    state["completed_clips"].extend([c["id"] for c in remaining_clips])
                    save_state(state)
                    print("  ✓ All video clips are DONE!")
                else:
                    print("  ⚠ Some video clips timed out rendering. Saving current state anyway...")
                    curr_fin = await count_finished(page)
                    completed_count = curr_fin - initial_finished_videos
                    for idx in range(min(completed_count, len(remaining_clips))):
                        state["completed_clips"].append(remaining_clips[idx]["id"])
                    save_state(state)
            else:
                print("[+] All video clips already marked completed.")
            
            # ═══════════════════════════════════════════════
            # PHASE 2: GENERATE ALL B-ROLL IMAGES
            # ═══════════════════════════════════════════════
            print("\n" + "=" * 60)
            print("  PHASE 2: GENERATING B-ROLL IMAGES (Banana Pro)")
            print("=" * 60)
            
            # Filter out already completed B-rolls
            remaining_brolls = [b for b in brolls if b["id"] not in state["completed_brolls"]]
            print(f"[+] Remaining B-rolls to generate: {len(remaining_brolls)}")
            
            if remaining_brolls:
                await switch_to_image_mode(page)
                
                BROLL_BATCH = 5  # Images are free + fast, can do larger batches
                num_broll_batches = (len(remaining_brolls) + BROLL_BATCH - 1) // BROLL_BATCH
                
                initial_finished_brolls = await count_finished(page)
                print(f"    Initial finished cards count before B-roll generation: {initial_finished_brolls}")
                
                for idx_batch in range(num_broll_batches):
                    start_idx = idx_batch * BROLL_BATCH
                    batch = remaining_brolls[start_idx:start_idx + BROLL_BATCH]
                    batch_ids = [b["id"] for b in batch]
                    print(f"\n--- Queueing B-Roll Batch {idx_batch+1}/{num_broll_batches}: {', '.join(batch_ids)} ---")
                    
                    for broll in batch:
                        await submit_broll(page, broll)
                    
                    if idx_batch < num_broll_batches - 1:
                        print("  Waiting 10 seconds before queueing next B-roll batch...")
                        await asyncio.sleep(10)
                
                # Now wait for all B-rolls to finish
                target_finished_brolls = initial_finished_brolls + len(remaining_brolls)
                print(f"\n[+] All {len(remaining_brolls)} B-rolls queued. Waiting for all to finish generating...")
                
                success = await wait_for_batch(page, initial_finished_brolls, len(remaining_brolls), timeout_per_item=30, poll_interval=5)
                if success:
                    state["completed_brolls"].extend([b["id"] for b in remaining_brolls])
                    save_state(state)
                    print("  ✓ All B-roll images are DONE!")
                else:
                    print("  ⚠ Some B-roll images timed out. Saving current state anyway...")
                    curr_fin = await count_finished(page)
                    completed_count = curr_fin - initial_finished_brolls
                    for idx in range(min(completed_count, len(remaining_brolls))):
                        state["completed_brolls"].append(remaining_brolls[idx]["id"])
                    save_state(state)
            else:
                print("[+] All B-rolls already marked completed.")
            
            print("\n" + "=" * 60)
            print("  ALL ASSET GENERATION COMPLETE!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n[-] CRITICAL ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
