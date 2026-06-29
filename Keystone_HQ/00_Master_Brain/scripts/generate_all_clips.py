import asyncio
from playwright.async_api import async_playwright
import urllib.request
import json
from pathlib import Path

# Paths
SCREENSHOT_DIR = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\d929c3a3-3922-4448-91fe-b63a060484d1")

clips_to_generate = [
    # A1-A4: Introduction
    {
        "id": "A1",
        "speaker": "He",
        "text": "You know you are getting older when just bending over to tie your shoes feels like an absolute Olympic sport. But what if it didn't?",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Camera slowly zooms in. He speaks bluntly, hands moving naturally. No subtitles."
    },
    {
        "id": "A2",
        "speaker": "He",
        "text": "What if the creaks and the joint pain were just a lack of raw materials? I am sitting at two hundred ten pounds right now.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, slight 20-degree rotation. Builder persona, hands emphasizing points. No subtitles."
    },
    {
        "id": "A3",
        "speaker": "She",
        "text": "That is an amazing personal case study. But just a reminder to everyone watching, we are not doctors and this is certainly not medical advice.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Professional posture, camera zooms out slightly. Speaking clearly. No subtitles."
    },
    {
        "id": "A4",
        "speaker": "She",
        "text": "Always consult your physician before starting any new protocol. Now, explain exactly what you mean by needing the right raw materials for your aging joints.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Direct eye contact, analytical expression. No subtitles."
    },

    # A5-A10: Wayne's Log (Builder Metaphor, CJC/Ibutamoren)
    {
        "id": "A5",
        "speaker": "He", 
        "text": "Think about it like framing a custom house. You absolutely cannot build a solid foundation with rotten wood. Your body is the exact same way.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Speaking bluntly with a builder persona, hands shaping a box. No subtitles."
    },
    {
        "id": "A6",
        "speaker": "He", 
        "text": "Bending over used to be a chore. Now, it feels completely easy again. The absolute secret for my structure has been the Wolverine stack protocol.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Looking excited, slight camera pan left. No subtitles."
    },
    {
        "id": "A7",
        "speaker": "He", 
        "text": "I am running C-J-C twelve ninety five without D-A-C, combined with Ibutamoren. It physically provides the scaffolding my body needs to repair itself properly today.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on face, slow zoom-out. Intense, blunt delivery. No subtitles."
    },
    {
        "id": "A8",
        "speaker": "He", 
        "text": "At two hundred ten pounds, carrying that kind of mass around the job site takes a massive toll on your connective tissue and recovery times.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, camera rotates 20 degrees right. Expressive hand gestures. No subtitles."
    },
    {
        "id": "A9",
        "speaker": "He", 
        "text": "This stack optimizes the natural growth pulses. It is not masking the pain at all, it is actually physically repairing the micro tears every night.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, authoritative builder persona. Camera slowly pushes in. No subtitles."
    },
    {
        "id": "A10",
        "speaker": "He", 
        "text": "So my mobility is totally back. I am moving fluidly, and honestly, feeling like I am twenty years old again when I wake up morning.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Cinematic shot. Looking very happy, relaxed body language. No subtitles."
    },
    
    # A11-A20: Victoria Deep Dive on MOTS-c
    {
        "id": "A11",
        "speaker": "She", 
        "text": "That structural repair is truly fascinating. The C-J-C and Ibutamoren combination clearly works for your specific biological scaffolding. But let us shift our gears completely.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, analytical expression. Slight zoom out. No subtitles."
    },
    {
        "id": "A12",
        "speaker": "She", 
        "text": "Structure is one thing, but what about the power grid? The biohacking space is currently blowing up over a brand new mitochondrial derived peptide compound.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-key lighting, professional posture. Camera pans slightly left. No subtitles."
    },
    {
        "id": "A13",
        "speaker": "She", 
        "text": "It is called MOTS-c. If the Wolverine stack is the scaffolding, MOTS-c is the electrical grid keeping the lights on inside your actual cells today.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Hand gestures emphasizing energy. Slow zoom in. No subtitles."
    },
    {
        "id": "A14",
        "speaker": "She", 
        "text": "There is actually a massive clinical trial happening right now, looking at how MOTS-c acts like literal exercise in a bottle for the human body.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on eyes and face. Highly engaged expression. No subtitles."
    },
    {
        "id": "A15",
        "speaker": "He", 
        "text": "Exercise in a bottle. That sounds like a complete cheat code. How exactly does a peptide target the mitochondria directly like that in the body?",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees left. Curious, blunt tone. No subtitles."
    },
    {
        "id": "A16",
        "speaker": "She", 
        "text": "It prevents cellular senescence. Basically, it stops your cells from acting old and tired, restoring mitochondrial respiration so you naturally produce far more metabolic energy.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Speaking with authority, slow dolly push-in. No subtitles."
    },
    {
        "id": "A17",
        "speaker": "He", 
        "text": "So while my personal stack is physically rebuilding the joints and muscles, MOTS-c would theoretically provide the pure cellular energy to fuel that massive rebuilding.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Excited builder persona, hands moving. No subtitles."
    },
    {
        "id": "A18",
        "speaker": "She", 
        "text": "Exactly right. It improves insulin sensitivity and directly combats aging related diseases. The published data on PubMed right now is honestly absolutely staggering to read.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, analytical expression. Camera holds steady. No subtitles."
    },
    {
        "id": "A19",
        "speaker": "He", 
        "text": "That is the ultimate metabolic remodeling. You handle the structure with the Wolverine stack, and you handle the entire engine with the MOTS-c peptide. Incredible.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Very happy, expressive hand gestures, slow zoom-out. No subtitles."
    },
    {
        "id": "A20",
        "speaker": "She", 
        "text": "We will keep monitoring the clinical trials closely on MOTS-c. For now, your case study proves that getting the right raw materials changes absolutely everything.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Cinematic shot, slow dolly push-in. Smiling slightly. No subtitles."
    },

    # A21-A44: Detailed Custom Conversational Flow
    {
        "id": "A21",
        "speaker": "He",
        "text": "And when you are training, you are not just lifting weights. You are building the infrastructure. If the scaffolding is weak, the whole structure collapses.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees right. Blunt delivery, expressive hands. No subtitles."
    },
    {
        "id": "A22",
        "speaker": "She",
        "text": "Exactly. That is why clinical focus on peptides like C-J-C twelve ninety five is about supporting that cellular scaffold, not forcing unnatural growth pulses.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Camera slowly zooms in. Analytical expression. No subtitles."
    },
    {
        "id": "A23",
        "speaker": "He",
        "text": "Right. It is a titration schedule, a gradual building process. We are not looking for a quick fix here. It is about long term sustainability.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Builder persona, talking blunt. No subtitles."
    },
    {
        "id": "A24",
        "speaker": "She",
        "text": "And titration is key to avoiding receptor desensitization. If you run it too hard, too fast, your body simply stops responding properly over time.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Professional posture, looking slightly off-camera. Speaking clearly. No subtitles."
    },
    {
        "id": "A25",
        "speaker": "He",
        "text": "Like over stressing a beam on a job site. You exceed the load capacity, and something is going to snap. You have to titrate the stress.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Blunt delivery, hand making a snapping motion. No subtitles."
    },
    {
        "id": "A26",
        "speaker": "She",
        "text": "Correct. And when you look at the research on MOTS-c, it is doing the same thing for the metabolic side. It titrates the energy production.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Direct eye contact. No subtitles."
    },
    {
        "id": "A27",
        "speaker": "He",
        "text": "So we are optimizing the metabolic blueprint. Rebuilding the scaffolding with C-J-C and Ibutamoren, and optimizing the power grid with the MOTS-c peptide.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees left. Excited tone, hands moving. No subtitles."
    },
    {
        "id": "A28",
        "speaker": "She",
        "text": "Exactly. But remember, the clinical data on MOTS-c is still developing. We are looking at rodent models and very early human trials right now.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-key lighting, professional posture. Slow zoom out. No subtitles."
    },
    {
        "id": "A29",
        "speaker": "He",
        "text": "Which is why we frame this as a personal case study. What works for my two hundred ten pound frame might not work for someone else.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Blunt delivery, pointing to chest. No subtitles."
    },
    {
        "id": "A30",
        "speaker": "She",
        "text": "Precisely. Individual biochemistry is highly variable. What we are showing is the conceptual framework of structural repair combined with cellular energy production.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, analytical expression. Camera holds steady. No subtitles."
    },
    {
        "id": "A31",
        "speaker": "He",
        "text": "And that conceptual framework is what is missing in most standard anti aging protocols. People focus on one hormone without looking at mitochondria.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Blunt delivery. No subtitles."
    },
    {
        "id": "A32",
        "speaker": "She",
        "text": "Right. Without mitochondrial respiration, you cannot synthesize the proteins needed for tissue repair. The engine needs fuel to build the house properly.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Speaking clearly. No subtitles."
    },
    {
        "id": "A33",
        "speaker": "He",
        "text": "Beautifully put. You need the power on site before you start framing. Otherwise, you are just standing in the dark with a hammer.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Excited builder persona, laughing slightly. No subtitles."
    },
    {
        "id": "A34",
        "speaker": "She",
        "text": "And the research shows MOTS-c actually promotes mitochondrial biogenesis. It is literally building more power plants inside your actual cells today.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, professional posture. Slow zoom in. No subtitles."
    },
    {
        "id": "A35",
        "speaker": "He",
        "text": "Building more power plants. That is how we fight cellular senescence. We keep the cellular power grid expanding instead of decaying slowly.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on face, slow zoom-out. Blunt delivery. No subtitles."
    },
    {
        "id": "A36",
        "speaker": "She",
        "text": "Exactly. And a robust power grid means better insulin sensitivity, less inflammation, and faster recovery from intense physical training in the gym.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up. Camera slowly pushes in. No subtitles."
    },
    {
        "id": "A37",
        "speaker": "He",
        "text": "Which directly correlates to how I am feeling. Moving easily, bending over, no morning stiffness. It is all connected to that cellular energy.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, rotating 20 degrees right. Happy expression. No subtitles."
    },
    {
        "id": "A38",
        "speaker": "She",
        "text": "It is. But safety is paramount. Any case study needs to emphasize clean sources and regular blood work to monitor systemic health closely.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-key lighting, professional posture. No subtitles."
    },
    {
        "id": "A39",
        "speaker": "He",
        "text": "Absolutely. You don't build a custom house without inspecting the foundation regularly. Blood work is your essential structural inspection.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, camera rotates 20 degrees left. Blunt builder persona. No subtitles."
    },
    {
        "id": "A40",
        "speaker": "She",
        "text": "And that is the core takeaway. Remodeling the aging machine requires a highly systematic, data driven approach, not random guesswork.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, analytical expression. No subtitles."
    },
    {
        "id": "A41",
        "speaker": "He",
        "text": "Systematic approach. We check the blueprints, we measure the loads, and we adjust the protocols based on real feedback.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, natural hand gestures. No subtitles."
    },
    {
        "id": "A42",
        "speaker": "She",
        "text": "Exactly. And we share this data for educational study, hoping it inspires men to look deeper into their own metabolic health.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Speaking clearly. No subtitles."
    },
    {
        "id": "A43",
        "speaker": "He",
        "text": "That is the goal. Rebuilding the machine while it is still running. It is hard work, but the results speak for themselves.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Smiling, hands moving. No subtitles."
    },
    {
        "id": "A44",
        "speaker": "She",
        "text": "It is a continuous process. And we will keep tracking the science as new clinical trials on mitochondrial peptides emerge.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, professional posture. No subtitles."
    },

    # A45-A47: Music Promo
    {
        "id": "A45",
        "speaker": "He",
        "text": "Speaking of keeping the engine running perfectly, you have to lock in your mental focus when you actually get into the gym to do the work.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot. Excited persona, hands gesturing widely. No subtitles."
    },
    {
        "id": "A46",
        "speaker": "He",
        "text": "I have been bumping our new Keystone Recomposition deep house mix on Spotify. It is the perfect training soundscape to completely soundtrack your entire workout.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Extreme close-up on face, slow zoom-out. Happy expression. No subtitles."
    },
    {
        "id": "A47",
        "speaker": "He",
        "text": "The link is down in the description below. Hit subscribe right now if you are following the journey, and drop a comment on our next topic.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium close-up, camera rotates 20 degrees left. Blunt delivery. No subtitles."
    },

    # A48-A50: Outro
    {
        "id": "A48",
        "speaker": "She",
        "text": "Stay consistent, stay curious, and always verify the science behind the protocol. Thanks for tuning in to another episode of the Recomposition case studies right now.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Medium shot, professional posture. Slow zoom out. No subtitles."
    },
    {
        "id": "A49",
        "speaker": "He",
        "text": "Build the foundation correctly, and the rest of the house will absolutely stand the test of time. Keep putting in the work every single day guys.",
        "direction": "A man. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Low-angle cinematic shot. Smiling, builder persona, hands moving. No subtitles."
    },
    {
        "id": "A50",
        "speaker": "She",
        "text": "We will see you in the next breakdown where we dive even deeper into cellular energy and metabolic remodeling. Check the links below for the soundscapes.",
        "direction": "A professional woman. KEEP EXACT CLOTHES ON THE AVATAR, DO NOT CHANGE THEM. Solid matte black studio room. Premium cinematic medium close-up. Friendly, engaging expression. No subtitles."
    }
]

async def main():
    print(f"[+] Starting UI-based Playwright generator for {len(clips_to_generate)} clips (starting from A1)...")
    
    # Read DevToolsActivePort
    try:
        with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
            lines = f.read().splitlines()
        port = lines[0]
        path = lines[1]
        ws_url = f"ws://127.0.0.1:{port}{path}"
        print(f"[+] Found WebSocket URL: {ws_url}")
    except Exception as e:
        print(f"[-] Error reading DevToolsActivePort: {e}")
        return

    async with async_playwright() as p:
        print("[+] Connecting to Chrome...")
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        
        page = None
        for p_ in context.pages:
            if "labs.google/fx/tools/flow/project" in p_.url:
                page = p_
                break
                
        if not page:
            print("[-] Google Flow tab not found!")
            return
            
        print(f"[+] Connected to Flow project: {page.url}")
        await page.bring_to_front()
        # Escape potential open dialogs
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
        
        BATCH_SIZE = 4
        num_batches = (len(clips_to_generate) + BATCH_SIZE - 1) // BATCH_SIZE
        
        for idx_batch in range(num_batches):
            start_idx = idx_batch * BATCH_SIZE
            batch = clips_to_generate[start_idx:start_idx+BATCH_SIZE]
            batch_ids = [c["id"] for c in batch]
            print(f"\n[===] PROCESSING BATCH {idx_batch+1}/{num_batches}: {', '.join(batch_ids)} [===]")
            
            for clip in batch:
                clip_id = clip["id"]
                speaker = clip["speaker"]
                dialogue = clip["text"]
                visual_prompt = clip["direction"]
                pronoun = "He" if speaker.lower() == "he" else "She"
                full_prompt = f"{pronoun} says: {dialogue}. {visual_prompt}"
                
                print(f"    [+] Running Clip {clip_id} ({speaker})...")
                
                # 1. Focus textbox
                box = page.locator('[role="textbox"]')
                await box.click()
                await page.wait_for_timeout(300)
                
                # 2. Clear text using Ctrl+A and Backspace
                await box.press("Control+A")
                await page.wait_for_timeout(100)
                await box.press("Backspace")
                await page.wait_for_timeout(200)
                
                # 3. Type prompt text
                await box.type(full_prompt, delay=5)
                await page.wait_for_timeout(300)
                
                # 4. Open asset picker Dialog (+ Create button)
                add_btn = page.locator('[aria-haspopup="dialog"]').first
                await add_btn.click(force=True)
                await page.wait_for_timeout(1500) # Wait for dialog to open fully
                
                # 5. Click the correct category tab inside the dialog, then click the image card container
                # Selecting the card wrapper inside the dialog will select it and dismiss/close the dialog.
                if speaker.lower() == "he":
                    # Click Avatar tab
                    avatar_tab = page.locator('[role="dialog"]').locator('[role="tab"]:has-text("Avatar")').first
                    await avatar_tab.click(force=True)
                    await page.wait_for_timeout(800)
                    
                    # Click the 'me' likeness image's card container (scoped inside dialog)
                    await page.evaluate("""() => {
                        const dialog = document.querySelector('[role="dialog"]');
                        if (dialog) {
                            const img = dialog.querySelector('img[alt="me"]');
                            if (img) {
                                const card = img.closest('[class*="sc-64c4dea-"]') || img.closest('button') || img.parentElement;
                                card.click();
                            }
                        }
                    }""")
                else:
                    # Click Characters tab
                    char_tab = page.locator('[role="dialog"]').locator('[role="tab"]:has-text("Characters")').first
                    await char_tab.click(force=True)
                    await page.wait_for_timeout(800)
                    
                    # Click the 'Victoria' character image's card container (scoped inside dialog)
                    await page.evaluate("""() => {
                        const dialog = document.querySelector('[role="dialog"]');
                        if (dialog) {
                            const img = dialog.querySelector('img[alt="Victoria"]');
                            if (img) {
                                const card = img.closest('a') || img.closest('button') || img.parentElement;
                                card.click();
                            }
                        }
                    }""")
                
                # Wait 1.5 seconds to let the dialog close and the UI settle
                await page.wait_for_timeout(1500)
                
                # 6. Click submit Create button (arrow_forward) on the main page
                submit_btn = page.locator('button:has-text("arrow_forward")').first
                await submit_btn.click(force=True)
                print(f"        -> Submitted Clip {clip_id}")
                await page.wait_for_timeout(1500)
                
            # Wait 20 seconds between batches, taking progress screenshot at 17s
            print(f"    [+] Batch submitted. Waiting 20 seconds...")
            await asyncio.sleep(17)
            
            # Save screenshot
            screenshot_path = SCREENSHOT_DIR / f"screenshot_batch_{idx_batch+1}.png"
            await page.screenshot(path=str(screenshot_path))
            print(f"    [+] Saved progress screenshot: {screenshot_path}")
            await asyncio.sleep(3)

        print("\n[+] All batches successfully submitted!")

if __name__ == "__main__":
    asyncio.run(main())
