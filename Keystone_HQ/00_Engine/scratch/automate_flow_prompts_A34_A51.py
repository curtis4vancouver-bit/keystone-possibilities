import sys
import os
import time
from playwright.sync_api import sync_playwright

# List of character assignments from A34 to A51:
# A34: Wayne (Avatar: 'me')
# A35: Victoria (Character: 'Victoria')
# A36: Wayne (Avatar: 'me')
# A37: Victoria (Character: 'Victoria')
# A38: Victoria (Character: 'Victoria')
# A39: Wayne (Avatar: 'me')
# A40: Wayne (Avatar: 'me')
# A41: Victoria (Character: 'Victoria')
# A42: Victoria (Character: 'Victoria')
# A43: Wayne (Avatar: 'me')
# A44: Wayne (Avatar: 'me')
# A45: Victoria (Character: 'Victoria')
# A46: Wayne (Avatar: 'me')
# A47: Wayne (Avatar: 'me')
# A48: Wayne (Avatar: 'me')
# A49: Victoria (Character: 'Victoria')
# A50: Wayne (Avatar: 'me')
# A51: Wayne (Avatar: 'me')

CLIPS = [
    {
        "id": "A34",
        "character": "Wayne",  # Avatar: 'me'
        "script": "Wayne says: Skin laxity. Hair thinning. The visible collapse after losing fifty pounds fast. G-H-K copper is the finishing trade after the framing crew.",
        "prompt": "Standing against pure black background Close-up. Camera pushes in slowly. Measured authoritative. No subtitles."
    },
    {
        "id": "A35",
        "character": "Victoria",  # Character: 'Victoria'
        "script": "Victoria says: So the Builder's Protocol. Two hundred grams protein. Heavy resistance training. B-P-C and T-B for tissue repair. G-H-K copper for collagen. Four pillars.",
        "prompt": "Standing against pure black background Medium shot. Camera holds steady. Counting on fingers summarizing. No subtitles."
    },
    {
        "id": "A36",
        "character": "Wayne",
        "script": "Wayne says: Now the supply chain. This is where people make dangerous mistakes. Uncertified concrete shuts a job site down. Gray market peptides are no different.",
        "prompt": "Standing against pure black background Medium close-up. Camera pushes in slowly. Stern serious warning tone. No subtitles."
    },
    {
        "id": "A37",
        "character": "Victoria",
        "script": "Victoria says: Searches for Chinese peptides exploded three hundred times in twelve months. TIME. Scientific American. The Guardian. All running exposés right now.",
        "prompt": "Standing against pure black background Medium close-up. Camera orbits slowly to the left. Concerned data-driven delivery. No subtitles."
    },
    {
        "id": "A38",
        "character": "Victoria",
        "script": "Victoria says: B-S-C-G testing shows thirty percent of gray market peptides fail purity analysis. One in three vials could be contaminated or mislabeled.",
        "prompt": "Standing against pure black background Close-up. Camera holds steady. Grave expression. No subtitles."
    },
    {
        "id": "A39",
        "character": "Wayne",
        "script": "Wayne says: I inject peptides before climbing scaffolding. I cannot afford contamination. I only source from pharmacies under five-oh-three-A federal exemption.",
        "prompt": "Standing against pure black background Medium close-up. Camera orbits slowly to the right. Practical direct no nonsense. No subtitles."
    },
    {
        "id": "A40",
        "character": "Wayne",
        "script": "Wayne says: Verify the certificate of analysis. H-P-L-C purity above ninety-eight percent. Endotoxin testing. Amino acid sequencing. No C-O-A? Walk away.",
        "prompt": "Standing against pure black background Close-up. Camera pushes in slowly. Counting off verification steps. No subtitles."
    },
    {
        "id": "A41",
        "character": "Victoria",
        "script": "Victoria says: And only ly-oph-i-lized powder. If someone sells pre-mixed liquid peptides that is a red flag. Legitimate peptides ship freeze-dried.",
        "prompt": "Standing against pure black background Medium shot. Camera holds steady. Emphatic gestures adding to Wayne's point. No subtitles."
    },
    {
        "id": "A42",
        "character": "Victoria",
        "script": "Victoria says: And there is a regulatory clock ticking. FDA compounding hearings July twenty-third. B-P-C one fifty-seven is on that agenda. Access could disappear.",
        "prompt": "Standing against pure black background Medium close-up. Camera pushes in slowly. Urgent informative. No subtitles."
    },
    {
        "id": "A43",
        "character": "Wayne",
        "script": "Wayne says: If the FDA blocks B-P-C compounding the regulated supply disappears. People flood the gray market. Worst possible outcome for safety.",
        "prompt": "Standing against pure black background Medium close-up. Camera orbits slowly to the left. Frustrated concerned. No subtitles."
    },
    {
        "id": "A44",
        "character": "Wayne",
        "script": "Wayne says: Like banning building permits then acting surprised when people build without inspections. Demand does not vanish. It goes underground. People get hurt.",
        "prompt": "Standing against pure black background Close-up. Camera holds steady. Shaking head passionate. No subtitles."
    },
    {
        "id": "A45",
        "character": "Victoria",
        "script": "Victoria says: So directly. ret-a-tru-tide will be available through compounding soon. Seven more Phase Three readouts this year. Would you switch from tir-zep-a-tide?",
        "prompt": "Standing against pure black background Close-up. Camera pushes in slowly. Direct challenging eye contact. No subtitles."
    },
    {
        "id": "A46",
        "character": "Wayne",
        "script": "Wayne says: Honestly? Not yet. Twenty-six weeks dialing in my protocol. I know my protein timing. My training. My recovery windows. All calibrated.",
        "prompt": "Standing against pure black background Medium close-up. Camera holds steady. Thoughtful genuine. No subtitles."
    },
    {
        "id": "A47",
        "character": "Wayne",
        "script": "Wayne says: Switching compounds mid-build is like changing your engineer during a foundation pour. Two percent more weight loss is not worth the disruption.",
        "prompt": "Standing against pure black background Medium shot. Camera orbits slowly to the right. Builder wisdom measured delivery. No subtitles."
    },
    {
        "id": "A48",
        "character": "Wayne",
        "script": "Wayne says: But starting from scratch today? I would look hard at ret-a-tru-tide. Eating more protein while losing fat. That is a structural advantage.",
        "prompt": "Standing against pure black background Close-up. Camera pushes in slowly. Forward-looking optimistic. No subtitles."
    },
    {
        "id": "A49",
        "character": "Victoria",
        "script": "Victoria says: Bottom line. Whether on sem-a-glu-tide tir-zep-a-tide or waiting for ret-a-tru-tide the Builder's Protocol applies to all of them?",
        "prompt": "Standing against pure black background Medium close-up. Camera holds steady. Clarifying wrapping up. No subtitles."
    },
    {
        "id": "A50",
        "character": "Wayne",
        "script": "Wayne says: Every single one. The compound changes. Demolition power changes. But the engineering stays. Protein. Lifting. Tissue repair. Collagen. Four pillars.",
        "prompt": "Standing against pure black background Medium close-up. Camera orbits slowly to the left. Definitive closing authority. No subtitles."
    },
    {
        "id": "A51",
        "character": "Wayne",
        "script": "Wayne says: Subscribe. Notifications on. Are you considering ret-a-tru-tide or staying on your current protocol? Comment below. I read every one. Let us build.",
        "prompt": "Standing against pure black background Medium close-up. Camera pulls back slowly to medium shot. Warm genuine connecting with audience. No subtitles."
    }
]

def monitor_queue(page):
    print("Checking queue size and compilation status...")
    while True:
        # Re-fetch status of compilations
        compiling_count = 0
        items = page.locator("a[href*='/edit/']").all()
        for idx, item in enumerate(items[:6]):  # look at the first few items which represent recent creations/queued items
            text = item.inner_text() or ""
            # If the item has percentage sign (e.g. 15% or 95%) or is queued (e.g. "Queued")
            if "%" in text or "Queued" in text:
                compiling_count += 1
                
        # Also check for queued cards
        queued_cards = page.locator("button:has-text('Queued')").count()
        compiling_count += queued_cards
        
        print(f"Current active compilations/queued items in UI: {compiling_count}")
        if compiling_count < 3:
            print("Active compilation queue is below 3. Ready to submit next.")
            break
        print("Queue has 3 or more active compilations. Waiting 15 seconds...")
        time.sleep(15)

def run_automation():
    print("Reading Chrome DevTools active port and path...")
    ws_endpoint = None
    try:
        port_file_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\DevToolsActivePort")
        if os.path.exists(port_file_path):
            with open(port_file_path, "r") as f:
                lines = f.read().splitlines()
                if len(lines) >= 2:
                    port = int(lines[0].strip())
                    path = lines[1].strip()
                    ws_endpoint = f"ws://127.0.0.1:{port}{path}"
                    print(f"Found active Chrome WebSocket: {ws_endpoint}")
    except Exception as e:
        print(f"Warning: could not read DevToolsActivePort file: {e}")

    if not ws_endpoint:
        print("Falling back to default HTTP connection...")
        ws_endpoint = "http://127.0.0.1:9222"

    print(f"Connecting to Chrome on endpoint {ws_endpoint}...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(ws_endpoint)
        except Exception as e:
            print(f"Error connecting to Chrome: {e}")
            sys.exit(1)
            
        print("Connected! Scanning pages...")
        flow_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47" in page.url:
                    flow_page = page
                    break
            if flow_page:
                break
                
        if not flow_page:
            print("ERROR: Google Flow project page 827275bd-d7fa-422b-9c90-b67109344d47 not found in Chrome tabs!")
            sys.exit(1)
            
        print(f"Found Google Flow Page: {flow_page.url}")
        flow_page.bring_to_front()
        
        for clip in CLIPS:
            clip_id = clip["id"]
            char_type = clip["character"]
            script_text = clip["script"]
            prompt_text = clip["prompt"]
            
            full_text = f"THIS IS THE SCRIPT:\n{script_text}\n\nTHIS IS THE VIDEO PROMPT:\n{prompt_text}"
            
            print(f"\n==========================================")
            print(f"SUBMITTING {clip_id} ({char_type})...")
            print(f"==========================================")
            
            # Wait for compilation slot before submitting
            monitor_queue(flow_page)
            
            # 1. Clear prompt box first via React state helper or UI click if possible
            # We can select all and delete in the contenteditable text field
            print("Locating textbox...")
            editor = flow_page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=5000)
            editor.focus()
            
            print("Clearing textbox...")
            flow_page.keyboard.press("Control+A")
            flow_page.keyboard.press("Backspace")
            time.sleep(0.5)
            
            # Try clicking the "close Clear prompt" button if it is visible
            try:
                clear_btn = flow_page.locator("button[aria-label*='Clear prompt'], button:has-text('close')").first
                if clear_btn.is_visible():
                    clear_btn.click()
                    time.sleep(0.5)
            except Exception:
                pass
                
            # 2. Select Character/Avatar
            print(f"Opening Character Picker for {char_type}...")
            # Click "+ Create" button
            plus_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "add_2" in t and "Create" in t:
                    plus_btn = btn
                    break
            
            if not plus_btn:
                print("ERROR: + Create button not found!")
                sys.exit(1)
                
            plus_btn.click()
            time.sleep(1.0)
            
            # Switch to Avatar or Character tab
            dialog = flow_page.locator("[role='dialog']").first
            dialog.wait_for(state="visible", timeout=5000)
            
            if char_type == "Wayne":
                # Wayne -> Avatar -> 'me'
                print("Clicking Avatar tab...")
                avatar_tab = dialog.locator("[role='tab']:has-text('Avatar')").first
                avatar_tab.wait_for(state="visible", timeout=5000)
                avatar_tab.click()
                time.sleep(0.8)
                
                print("Selecting 'me' avatar...")
                me_el = dialog.locator("text='me'").first
                me_el.wait_for(state="visible", timeout=5000)
                me_el.click()
                time.sleep(0.5)
            else:
                # Victoria -> Characters -> 'Victoria'
                print("Clicking Characters tab...")
                char_tab = dialog.locator("[role='tab']:has-text('Characters')").first
                char_tab.wait_for(state="visible", timeout=5000)
                char_tab.click()
                time.sleep(0.8)
                
                print("Selecting 'Victoria' character...")
                vic_el = dialog.locator("text='Victoria'").first
                vic_el.wait_for(state="visible", timeout=5000)
                vic_el.click()
                time.sleep(0.5)
                
            # Click "Add to Prompt"
            print("Clicking Add to Prompt...")
            add_btn = dialog.locator("button:has-text('Add to Prompt')").first
            add_btn.wait_for(state="visible", timeout=5000)
            add_btn.click()
            time.sleep(1.0)
            
            # 3. Enter Text
            editor.focus()
            print("Typing full prompt text...")
            editor.type(full_text, delay=2)
            time.sleep(0.8)
            
            # 4. Click Submit Create
            print("Locating Create Submit button...")
            submit_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "arrow_forward" in t and "Create" in t:
                    submit_btn = btn
                    break
                    
            if not submit_btn:
                print("ERROR: Submit button not found!")
                sys.exit(1)
                
            if submit_btn.is_disabled():
                print("WARNING: Submit button is disabled! Waiting...")
                time.sleep(2.0)
                
            if submit_btn.is_disabled():
                print("ERROR: Submit button still disabled. Attempting click anyway...")
            else:
                print("Clicking Submit Create...")
                
            submit_btn.click()
            print(f"SUCCESS: Submitted {clip_id}!")
            time.sleep(5.0)

        print("\nAll remaining prompts A34 to A51 queued and compiling successfully!")

if __name__ == "__main__":
    run_automation()
