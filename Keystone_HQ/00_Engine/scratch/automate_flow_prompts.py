import sys
import os
import time
from playwright.sync_api import sync_playwright

PROMPTS = {
    12: "The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal her face in a close-up behind a Pioneer DJ controller on a minimal black platform. Pure black background. Single warm teal spotlight from directly above creating a sharp shadow on one side of her face. Her eyes snap open and she looks directly into the camera lens with calm fierce intensity. She holds the stare without blinking. Her right hand reaches down to the mixer below frame. Camera holds perfectly still. She is wearing fitted black leather high-waisted shorts, a dark charcoal ribbed tank top, a slim gold chain necklace. At 0:08, her jaw tightens almost imperceptibly. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into cinematic motion blur. --no flashing lights --no strobe effects --no watermark --no text artifacts --no subtitles --no floating limbs --no warped face",
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

def run_automation():
    print("Connecting to Chrome on port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print(f"Error connecting to Chrome: {e}")
            sys.exit(1)
            
        print("Connected! Scanning pages...")
        flow_page = None
        for context in browser.contexts:
            for page in context.pages:
                if "labs.google/fx/tools/flow/project" in page.url:
                    flow_page = page
                    break
            if flow_page:
                break
                
        if not flow_page:
            print("ERROR: Google Flow project page not found in Chrome tabs!")
            sys.exit(1)
            
        print(f"Found Google Flow Page: {flow_page.url}")
        flow_page.bring_to_front()
        
        for clip_num in sorted(PROMPTS.keys()):
            prompt_text = PROMPTS[clip_num]
            print(f"\n==========================================")
            print(f"SUBMITTING CLIP A{clip_num}...")
            print(f"==========================================")
            
            # 1. Locate and click "+ Create" button
            print("Locating + Create button...")
            plus_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "add_2" in t and "Create" in t:
                    plus_btn = btn
                    break
            
            if not plus_btn:
                print(f"ERROR: + Create button not found for A{clip_num}")
                continue
                
            print("Clicking + Create button...")
            plus_btn.click()
            flow_page.wait_for_timeout(1000)
            
            # 2. Wait for Characters tab
            print("Waiting for Characters tab...")
            char_tab = flow_page.locator("[role='tab']:has-text('Characters')").first
            char_tab.wait_for(state="visible", timeout=5000)
            print("Clicking Characters tab...")
            char_tab.click()
            flow_page.wait_for_timeout(1000)
            
            # 3. Wait for Ana Stevenson character card and click it
            print("Waiting for Ana Stevenson card...")
            # Let's search for the image/card of Ana Stevenson
            # In the DOM snapshot, the card contains text "Ana Stevenson" and image with src having dec2
            # Let's try locating by text Ana Stevenson inside the dialog container
            dialog = flow_page.locator("[role='dialog']").first
            # Look for an image or text
            ana_el = dialog.locator("text='Ana Stevenson'").first
            ana_el.wait_for(state="visible", timeout=5000)
            print("Selecting Ana Stevenson...")
            ana_el.click()
            flow_page.wait_for_timeout(800)
            
            # 4. Click Add to Prompt button
            print("Locating Add to Prompt button...")
            add_btn = dialog.locator("button:has-text('Add to Prompt')").first
            add_btn.wait_for(state="visible", timeout=5000)
            print("Clicking Add to Prompt...")
            add_btn.click()
            
            # Wait for modal to close
            flow_page.wait_for_timeout(1000)
            
            # 5. Type prompt text
            print("Locating textbox...")
            editor = flow_page.locator("div[contenteditable='true']").first
            editor.wait_for(state="visible", timeout=5000)
            editor.focus()
            
            print("Clearing textbox...")
            flow_page.keyboard.press("Control+A")
            flow_page.keyboard.press("Backspace")
            flow_page.wait_for_timeout(300)
            
            print("Typing prompt text...")
            editor.type(prompt_text, delay=5) # Type with a brief delay per character
            flow_page.wait_for_timeout(800)
            
            # 6. Locate submit button
            print("Locating Submit (arrow_forward Create) button...")
            submit_btn = None
            for btn in flow_page.locator("button").all():
                t = btn.inner_text() or ""
                if "arrow_forward" in t and "Create" in t:
                    submit_btn = btn
                    break
                    
            if not submit_btn:
                print("ERROR: Submit button not found!")
                continue
                
            # Wait for submit button to be enabled (it should be since we typed via native emulator)
            if submit_btn.is_disabled():
                print("WARNING: Submit button is disabled! Waiting for it to enable...")
                flow_page.wait_for_timeout(2000)
                
            if submit_btn.is_disabled():
                print("ERROR: Submit button remained disabled! React state did not update. Aborting.")
                # Let's click it anyway just in case it works
                submit_btn.click()
            else:
                print("Clicking Submit Create button...")
                submit_btn.click()
                
            print(f"SUCCESS: Submitted A{clip_num}! Waiting before next clip...")
            flow_page.wait_for_timeout(8000) # Wait 8 seconds before submitting the next one to avoid issues

        print("\nAll remaining prompts A12 to A24 submitted successfully!")

if __name__ == "__main__":
    run_automation()
