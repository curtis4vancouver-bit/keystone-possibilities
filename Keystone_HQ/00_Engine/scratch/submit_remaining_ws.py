import os
import sys
import time
from playwright.sync_api import sync_playwright

PROMPTS = {
    13: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a wide shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera slowly pushes in from wide toward medium. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Thin haze thickens slightly around her. Both her hands move across the decks with faster more confident movements. Her head bobs with building energy. The wide shot shows the full dramatic scale of the minimal booth against pure black. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she shifts her weight forward leaning into the decks. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    14: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium-close shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. She pauses for a beat. Both hands rest flat on the mixer. She takes a slow deliberate breath. Camera holds steady on her face. Her expression is one of focused anticipation. Complete control. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace. At 0:08, her fingers curl slightly on the mixer edge. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    15: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. She brings both hands decisively onto the controller and begins working the mixer with sharp precise movements. Camera slowly pushes in from medium to medium-close. Her head nods with authority. Her expression shifts to a subtle confident smirk. Maximum energy but complete control. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she lifts her chin slightly. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    16: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a wide shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera holds the wide shot showing the full booth and figure. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Thick haze drifts through the light beams. She is in full performance mode with her hands moving fluidly across the mixer. Her body moves with aggressive controlled energy. She owns the space. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she glances up from the decks directly at the camera. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    17: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera smoothly moves around her from left to right in a continuous slow arc. Single warm teal spotlight from directly above follows as the camera moves. Soft steady amber accent shifts as the angle changes. As the camera passes in front of her she locks eyes with the lens with a fierce composed expression. Her hands never stop moving on the decks. Cinematic and powerful. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she breaks eye contact and looks back down at the decks. At 0:09, the camera executes a rapid 1-second whip-pan continuing to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    18: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium-close shot from slightly camera-right behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left catches her profile. She leans forward slightly into the decks, one hand adjusting the high EQ while the other holds the crossfader. Her chin drops and she watches her own hands work with total focus. Camera slowly pushes in. Her gold chain hangs forward. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she tilts her head slightly to one side. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    19: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Camera holds steady. Both hands work the mixer with fluid practiced movements. She looks up from the decks and stares directly into the camera with an intense knowing smirk. She is completely in her element. Peak confidence. Camera slowly pushes in to medium-close. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she gives the slightest nod to camera. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    20: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Camera holds steady at medium distance. Her expression is calm and satisfied. Her head nods rhythmically at a steady pace. She looks down at the decks briefly then back up with a slight knowing smile. She has found her stride. Thin haze drifts gently. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she exhales visibly and her shoulders drop slightly in relaxation. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    21: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera slowly pulls back from medium to medium-wide. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. Her left hand slides the crossfader while her right hand reaches across to adjust the incoming channel EQ. The movement is fluid and practiced. Professional and effortless. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, she finishes the transition and both hands settle on the mixer. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    22: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above. Soft steady amber accent from camera-left. She finishes a mix transition and nods once to herself in quiet approval. She rolls her shoulders once then leans back into the decks with renewed easy energy. Camera holds steady. She glances to camera-left briefly as if acknowledging someone then looks back to the decks with a half-smile. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, her gaze returns to center. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    23: "The video starts with a rapid whip-pan from the left, emerging from motion blur to reveal the woman in a medium shot behind a Pioneer DJ controller on a minimal black platform. Pure black background. Camera slowly pulls back from medium to wide. Single warm teal spotlight from directly above begins to dim very gradually. Soft steady amber accent from camera-left softens. She makes one last smooth adjustment to the mixer and lets the track ride. She takes one hand off the controller and rests it on the edge of the booth. Her head still nods gently. The energy is winding down naturally. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace, and black chunky rings on both hands. At 0:08, her remaining hand lifts from the mixer. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
    24: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal the woman in a wide shot standing behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above is dim. Soft amber accent is barely visible. She lifts both hands off the controller and lets them rest at her sides. She looks up from the decks directly into the camera with a calm powerful stare. The teal spotlight slowly dims further. Her silhouette becomes darker and darker. She gives one final slow nod. The light fades until only the faintest outline of her face is visible against pure black. No subtitles. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face"
}

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    if not os.path.exists(active_port_file):
        raise FileNotFoundError(f"Chrome active port file not found at: {active_port_file}")
        
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
        
    if len(lines) < 2:
        raise ValueError("Invalid DevToolsActivePort file format")
        
    port = lines[0].strip()
    ws_path = lines[1].strip()
    return f"ws://127.0.0.1:{port}{ws_path}"

def run():
    ws_url = get_websocket_url()
    print(f"Connecting to Chrome via WebSocket: {ws_url}...")
    
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(ws_url)
            print("Connected!")
        except Exception as e:
            print(f"FAILED to connect: {e}")
            return
            
        print("Searching for Google Flow project page...")
        flow_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "labs.google/fx/tools/flow/project/827275bd-d7fa-422b-9c90-b67109344d47" in page.url:
                    flow_page = page
                    break
            if flow_page:
                break
                
        if not flow_page:
            print("ERROR: Flow project page not found!")
            browser.close()
            return
            
        print(f"Found Page: {flow_page.url}")
        flow_page.bring_to_front()
        
        for clip_num, text in sorted(PROMPTS.items()):
            print(f"\n==========================================")
            print(f"SUBMITTING CLIP A{clip_num}...")
            print(f"==========================================")
            
            # Click prompt box to focus
            print("Focusing prompt textbox...")
            editor = flow_page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=10000)
            editor.focus()
            
            # Clear text
            print("Clearing textbox...")
            flow_page.keyboard.press("Control+A")
            flow_page.keyboard.press("Backspace")
            flow_page.wait_for_timeout(400)
            
            # Type prompt text
            print("Typing prompt...")
            editor.type(text)
            flow_page.wait_for_timeout(800)
            
            # Click "+ Create" button (Ingredients / Characters dialog)
            print("Opening characters dialog...")
            plus_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "add_2" in t and "Create" in t:
                    plus_btn = btn
                    break
            if not plus_btn:
                print("ERROR: + Create button not found!")
                continue
            plus_btn.click()
            flow_page.wait_for_timeout(1000)
            
            # Wait for dialog and select Characters tab
            dialog = flow_page.locator("[role='dialog']").first
            dialog.wait_for(state="visible", timeout=5000)
            
            char_tab = dialog.locator("[role='tab']:has-text('Characters')").first
            char_tab.wait_for(state="visible", timeout=5000)
            char_tab_selected = char_tab.get_attribute("aria-selected")
            if char_tab_selected != "true":
                print("Clicking Characters tab...")
                char_tab.click()
                flow_page.wait_for_timeout(600)
                
            # Select Ana Stevenson's image card inside modal
            print("Selecting Ana Stevenson character image...")
            # We must click the actual img element or the thumbnail, not just the text label
            ana_img = dialog.locator("img[alt*='Ana'], img[src*='ee567222-dec2']").first
            ana_img.wait_for(state="visible", timeout=5000)
            ana_img.click()
            flow_page.wait_for_timeout(600)
            
            # Click Add to Prompt
            print("Clicking Add to Prompt...")
            add_btn = dialog.locator("button:has-text('Add to Prompt')").first
            add_btn.wait_for(state="visible", timeout=5000)
            add_btn.click()
            flow_page.wait_for_timeout(1000) # Wait for dialog to close
            
            # Locate and click submit Create button
            print("Locating Create submit button...")
            submit_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "arrow_forward" in t and "Create" in t:
                    submit_btn = btn
                    break
                    
            if not submit_btn:
                print("ERROR: Create submit button not found!")
                continue
                
            if submit_btn.is_disabled():
                print("WARNING: Create button is disabled! Waiting for state sync...")
                flow_page.wait_for_timeout(2000)
                
            if submit_btn.is_disabled():
                print("ERROR: Create button remained disabled! React state desync.")
                continue
                
            print("Clicking Create submit button...")
            submit_btn.click()
            print(f"SUCCESS: Submitted clip A{clip_num}!")
            
            # Wait 8 seconds before next prompt to let queueing register
            time.sleep(8)

        print("\nAll remaining prompts A13-A24 successfully queued!")
        browser.close()

if __name__ == "__main__":
    run()
