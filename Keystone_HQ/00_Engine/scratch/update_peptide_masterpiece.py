import re
import os

script_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\keystone_8min_glp1_masterpiece.md"

if not os.path.exists(script_path):
    print(f"Error: {script_path} not found.")
    exit(1)

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Mexico in description
old_desc = "Finally, we explore my 100% AI avatar transition experiment, our biophilic construction expansion into Mexico, and how we flow tax-free dividends under Stevenson Holdings Ltd. to protect our primary construction credentials"
new_desc = "Finally, we explore my 100% AI avatar transition experiment, our local Squamish biophilic sauna builds and future Mexico design plans, and how we flow tax-free dividends under Stevenson Holdings Ltd. to protect our primary construction credentials"

# Scene 3: Shoulder & Stretching, Natural backdrop
old_scene_3 = """#### 🎥 SCENE 3: [0:20 - 0:30] DETAIL B-ROLL (TIMBER FRAMING CLOSE-UP)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: Joint decay threatened my career, forcing a deep dive into advanced molecular joint repair protocols.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light to reveal a cinematic close-up of a massive hand-peeled cedar log frame. Dust motes drift in the warm golden hour side-lighting. No humans or faces are visible. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no humans --no watermark --no text artifacts --no subtitles`"""

new_scene_3 = """#### 🎥 SCENE 3: [0:20 - 0:30] DETAIL B-ROLL (CLINICAL STRETCHING)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: My shoulder is feeling better after adding daily clinical stretching and targeted molecular recovery protocols.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light to reveal a cinematic, close-up shot of heavy resistance bands and leather stretching straps hanging from a branch in an old-growth cedar forest. Mood PNW morning side-lighting. No humans or faces are visible. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no humans --no watermark --no text artifacts --no subtitles`"""

# Scene 4: Standing against rugged cliff overlooking ocean instead of cabin wall
old_scene_4 = """#### 🎥 SCENE 4: [0:30 - 0:40] WAYNE ON-CAMERA (PEPTIDE OVERVIEW)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: That is when I stacked metabolic compound B P C with tissue compound T B.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic medium shot of Wayne, looking stoic in premium Pacific Northwest workwear, standing against a rustic cedar-sided cabin wall. Camera slow dollies in. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_4 = """#### 🎥 SCENE 4: [0:30 - 0:40] WAYNE ON-CAMERA (PEPTIDE OVERVIEW)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: That is when I stacked metabolic compound B P C with tissue compound T B.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic medium shot of Wayne, looking stoic in premium Pacific Northwest workwear, standing on a rugged granite ledge overlooking the misty Howe Sound, surrounded by towering pine trees. Camera slow dollies in. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 6: Natural platform in forest instead of completed cedar sauna cabin
old_scene_6 = """#### 🎥 SCENE 6: [0:50 - 1:00] WAYNE ON-CAMERA (ECOSYSTEM METHODOLOGY)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: We pair physical body rebuilding with original deep house frequencies to optimize nervous system recovery.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur. A cinematic medium shot of Wayne, looking calm and authoritative, standing inside a completed cedar sauna cabin. Warm wood textures, desaturated grading. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_6 = """#### 🎥 SCENE 6: [0:50 - 1:00] WAYNE ON-CAMERA (ECOSYSTEM METHODOLOGY)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: We pair physical body rebuilding with original deep house frequencies to optimize nervous system recovery.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur. A cinematic medium shot of Wayne, looking calm and authoritative, standing on a clean granite platform nestled deep within a mossy old-growth cedar forest. Dappled morning sunlight filters through the forest canopy, creating a peaceful, natural setting. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 11: High granite peak overlooking river canyon instead of office overlook
old_scene_11 = """#### 🎥 SCENE 11: [1:40 - 1:50] WAYNE ON-CAMERA (REGULATORY CONTEXT)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: Compounding pharmacies are currently facing extreme regulatory pressure from the F D A bulk list.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A medium cinematic shot of Wayne, looking professional and stoic, standing inside a sleek modern office with massive glass windows overlooking the Squamish forest. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_11 = """#### 🎥 SCENE 11: [1:40 - 1:50] WAYNE ON-CAMERA (REGULATORY CONTEXT)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: Compounding pharmacies are currently facing extreme regulatory pressure from the F D A bulk list.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A medium cinematic shot of Wayne, looking professional and stoic, standing on a high granite peak overlooking a vast river canyon with dramatic Squamish mountains in the distance. Overcast sky, clean natural light. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 23: Natural gravel path instead of cedar/concrete studio
old_scene_23 = """#### 🎥 SCENE 23: [3:40 - 3:50] WAYNE ON-CAMERA (THE SARCOPENIA RISK)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: However, rapid weight loss often triggers severe lean mass loss, inducing early onset muscular sar-co-pe-ni-a.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A cinematic medium shot of Wayne, looking serious and focused, standing in a high-end personal training studio constructed of dark cedar and concrete. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_23 = """#### 🎥 SCENE 23: [3:40 - 3:50] WAYNE ON-CAMERA (THE SARCOPENIA RISK)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: However, rapid weight loss often triggers severe lean mass loss, inducing early onset muscular sar-co-pe-ni-a.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A cinematic medium shot of Wayne, looking serious and focused, standing on a natural gravel path at the edge of a dense Squamish pine forest in the misty morning light. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 29: Wayne recomposition stats, 210 lbs, muscle, slight gut, meadow instead of clinic
old_scene_29 = """#### 🎥 SCENE 29: [4:40 - 4:50] WAYNE ON-CAMERA (COMPOSITION MEASUREMENT)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: We track this exact muscle composition using weekly high-fidelity bio-impedance scans and blood panel markers.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A medium cinematic shot of Wayne, looking focused and calm, standing next to a sleek bio-electrical impedance analysis machine inside a modern wellness clinic. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_29 = """#### 🎥 SCENE 29: [4:40 - 4:50] WAYNE ON-CAMERA (COMPOSITION MEASUREMENT)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: Currently I am holding at two hundred ten pounds while building muscle and reducing gut.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A medium cinematic shot of Wayne's avatar, standing on an open grassy meadow with snow-capped granite peaks in the far background. Wayne exhibits a realistic, highly improved recomposition physique: broad muscular shoulders and arms, holding a stable two-hundred-ten-pound frame with a natural, slight midsection gut. Camera slow dollies in. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 31: Rocky shore instead of wood workshop
old_scene_31 = """#### 🎥 SCENE 31: [5:00 - 5:10] WAYNE ON-CAMERA (THE AI AVATAR ANNOUNCEMENT)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: For the next few months, I am transitioning my content to a complete AI-avatar experiment.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur. A premium, highly desaturated 8k cinematic shot of Wayne, wearing a premium charcoal-colored canvas work jacket, standing inside a beautiful open-air wood workshop. Camera slow dollies in. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_31 = """#### 🎥 SCENE 31: [5:00 - 5:10] WAYNE ON-CAMERA (THE AI AVATAR ANNOUNCEMENT)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: For the next few months, I am transitioning my content to a complete AI-avatar experiment.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur. A premium, highly desaturated 8k cinematic shot of Wayne, wearing a premium charcoal-colored canvas work jacket, standing on a rocky shore with waves crashing against grey granite cliffs in the background. Pure wilderness environment, soft misty weather. Camera slow dollies in. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 35: Mexico decoupling (blueprints instead of active coastal sweep)
old_scene_35 = """#### 🎥 SCENE 35: [5:40 - 5:50] SCENIC B-ROLL (MEXICAN BEACHFRONT TRANSITION)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: As we transition, we also expand our custom biophilic wellness building footprint directly to Mexico.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal a cinematic, highly desaturated drone sweep over a pristine, white-sand beach in Baja, Mexico. Deep blue ocean waves breaking on the shore. A minimal modern concrete and timber retreat is integrated into the dry coast landscape. At 0:09, the camera executes a rapid 1-second camera tilt-up to the sunset sky, dissolving into light. --no humans --no watermark --no text artifacts --no subtitles`"""

new_scene_35 = """#### 🎥 SCENE 35: [5:40 - 5:50] SCENIC B-ROLL (MEXICAN DESIGN STAGE)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: While our Baja resort expansion is a long term three to five year design plan.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur to reveal a slow-slider cinematic shot of a modern architectural drafting table nestled in an open-air forest workspace. Blueprints, sketches, and a sleek tablet screen display clean 3D CAD models of a future beachfront wellness sanctuary. At 0:09, the camera executes a rapid 1-second camera tilt-up to the morning sky, dissolving into light. --no humans --no watermark --no text artifacts --no subtitles`"""

# Scene 36: Squamish local timber framing instead of Mexico beach sauna
old_scene_36 = """#### 🎥 SCENE 36: [5:50 - 6:00] DETAIL B-ROLL (OFF GRID TIMBER BEACH SAUNA)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: We are designing modern off-grid sanctuaries integrating solar arrays, salt pools, and cedar beach saunas.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A gorgeous, desaturated slider shot of an off-grid beachfront cedar sauna, with black solar panels mounted beautifully on its flat roof. Clean design, modern lines. No humans. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no humans --no watermark --no text artifacts --no subtitles`"""

new_scene_36 = """#### 🎥 SCENE 36: [5:50 - 6:00] DETAIL B-ROLL (SQUAMISH TIMBER FRAME)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: This year we are building premium biophilic timber frame saunas locally in Squamish British Columbia.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A gorgeous, desaturated slider shot of a premium custom wood-burning cedar sauna built on a steep granite cliffside in Squamish, surrounded by towering, wet pine trees. Moss and dew on the rocks. No humans. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no humans --no watermark --no text artifacts --no subtitles`"""

# Scene 37: Open slate platform instead of cedar/concrete kitchen
old_scene_37 = """#### 🎥 SCENE 37: [6:00 - 6:10] WAYNE ON-CAMERA (NUTRITIONAL ARCHITECTURE)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: True health requires aligning your external recovery architecture with clean, nutrient dense whole organic foods.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic medium shot of Wayne, looking focused and calm, standing in a high-end minimal concrete and raw cedar kitchen. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_37 = """#### 🎥 SCENE 37: [6:00 - 6:10] WAYNE ON-CAMERA (NUTRITIONAL ARCHITECTURE)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: True health requires aligning your external recovery architecture with clean, nutrient dense whole organic foods.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic medium shot of Wayne, looking focused and calm, standing on an open-air natural slate platform overlooking a cascading mountain stream. Lush ferns and moss-covered boulders surround him. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 40: Rugged timber deck over fjord instead of Suna Spa cabin under construction
old_scene_40 = """#### 🎥 SCENE 40: [6:30 - 6:40] WAYNE ON-CAMERA (THE BULLETPROOF FRAMEWORK)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: By combining physical shelter with biochemical fuel, we create a bulletproof framework for peak longevity.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A medium cinematic shot of Wayne, looking determined and stoic, standing inside a premium, fully-custom Suna Spa cabin under construction. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_40 = """#### 🎥 SCENE 40: [6:30 - 6:40] WAYNE ON-CAMERA (THE BULLETPROOF FRAMEWORK)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: By combining physical shelter with biochemical fuel, we create a bulletproof framework for peak longevity.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A medium cinematic shot of Wayne, looking determined and stoic, standing on a rugged timber deck overlooking a deep, misty fjord, surrounded by vast wilderness. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the right. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 46: quiet moss-covered granite glade instead of home spa cedar wall panels
old_scene_46 = """#### 🎥 SCENE 46: [7:30 - 7:40] WAYNE ON-CAMERA (THE SOUND FREQUENCY KEY)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: To enhance biological relaxation, we pair our physical resorts with custom designed audio frequency structures.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic medium shot of Wayne, looking direct and calm, standing next to customized natural cedar acoustic wall panels inside a high-end home spa. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_46 = """#### 🎥 SCENE 46: [7:30 - 7:40] WAYNE ON-CAMERA (THE SOUND FREQUENCY KEY)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: To enhance biological relaxation, we pair our physical resorts with custom designed audio frequency structures.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic medium shot of Wayne, looking direct and calm, standing in a quiet, moss-covered granite glade under a canopy of ancient fir trees. Soft, filtered forest light. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 48: Anti-sales music recovery instead of Spotify subscription push
old_scene_48 = """#### 🎥 SCENE 48: [7:50 - 8:00] DETAIL B-ROLL (SPOTIFY & OAC CHANNELS)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: Stream our full music collection on the official KeyStone Recomposition Spotify and YouTube music channels.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A premium, high-contrast flat-lay close-up of a high-end designer smartphone displaying our custom "KeyStone Recomposition" Spotify artist profile page. Elegant desaturated UI. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no humans --no watermark --no text artifacts --no subtitles`"""

new_scene_48 = """#### 🎥 SCENE 48: [7:50 - 8:00] DETAIL B-ROLL (RECOVERY TRACKS)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: I stream my custom electronic music library during recovery to balance my autonomic nervous system.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A premium, high-contrast close-up of a high-end smartphone lying on a flat mossy granite stone, displaying an elegant, desaturated audio player interface showing track wave patterns. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no humans --no watermark --no text artifacts --no subtitles`"""

# Scene 49: Anti-sales case study close instead of subscription CTA
old_scene_49 = """#### 🎥 SCENE 49: [8:00 - 8:10] WAYNE ON-CAMERA (THE SOVEREIGN SUBSCRIPTION CTA)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: Subscribe now to join our sovereign journey of health, biophilic building, and financial structural freedom.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic close-up of Wayne standing on a granite peak overlooking a vast, desaturated mountain range. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

new_scene_49 = """#### 🎥 SCENE 49: [8:00 - 8:10] WAYNE ON-CAMERA (THE CASE STUDY CLOSE)
*   **Audio (Spoken Dialogue):**  
    `Wayne says: I am documenting this raw transition to share my personal cellular health and structural achievements.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the left, emerging from motion blur. A cinematic close-up of Wayne standing on a granite peak overlooking a vast, desaturated mountain range. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`"""

# Scene 50: Outro logo prompt
old_scene_50 = """#### 🎥 SCENE 50: [8:10 - 8:20] DETAIL B-ROLL (FINAL SCIENTIFIC DISCLAIMER)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: This scientific case study is not medical advice. Always consult your own licensed healthcare professional.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur. A clean, premium slate-grey background screen displaying our clinical disclaimer. Modern minimalist typography. Cold, elegant side-lighting. [On-Screen Graphic: SCIENTIFIC CASE STUDY ONLY. NOT MEDICAL ADVICE. CONSULT A LICENSED PROFESSIONAL.] --no humans --no watermark --no text artifacts --no subtitles`"""

new_scene_50 = """#### 🎥 SCENE 50: [8:10 - 8:20] DETAIL B-ROLL (OUTRO & CLINICAL DISCLAIMER)
*   **Audio (Spoken Dialogue):**  
    `Wayne's voiceover says: This scientific case study is not medical advice. Always consult your own licensed healthcare professional.`
*   **Google Flow (Omni) Prompt:**  
    `The video starts with a rapid whip-pan from the right, emerging from motion blur. A clean, premium slate-grey background screen displaying our clinical disclaimer. Modern minimalist typography. Cold, elegant side-lighting. At 0:08, a clean transition introduces the Keystone custom brand logo and "Scribe" outro graphic. [On-Screen Graphic / Video Editor Note: **PROMPT FOR WAYNE**: INSERT YOUR CUSTOM BRAND LOGO AND "SCRIBE" OUTRO GRAPHIC HERE FOR THE LAST 2 SECONDS OF THIS CLIP. Text: SCIENTIFIC CASE STUDY ONLY. NOT MEDICAL ADVICE. CONSULT A LICENSED PROFESSIONAL.] --no humans --no watermark --no text artifacts --no subtitles`"""


replacements = [
    (old_desc, new_desc),
    (old_scene_3, new_scene_3),
    (old_scene_4, new_scene_4),
    (old_scene_6, new_scene_6),
    (old_scene_11, new_scene_11),
    (old_scene_23, new_scene_23),
    (old_scene_29, new_scene_29),
    (old_scene_31, new_scene_31),
    (old_scene_35, new_scene_35),
    (old_scene_36, new_scene_36),
    (old_scene_37, new_scene_37),
    (old_scene_40, new_scene_40),
    (old_scene_46, new_scene_46),
    (old_scene_48, new_scene_48),
    (old_scene_49, new_scene_49),
    (old_scene_50, new_scene_50)
]

print("Applying replacements...")
success_count = 0
for idx, (old_text, new_text) in enumerate(replacements):
    if old_text in content:
        content = content.replace(old_text, new_text)
        print(f"[{idx+1}/{len(replacements)}] Replacement succeeded!")
        success_count += 1
    else:
        print(f"[{idx+1}/{len(replacements)}] Replacement FAILED! (Target text not found)")

if success_count == len(replacements):
    print("All replacements successful! Writing updated content to file.")
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(content)
else:
    print(f"Failed. Only {success_count} out of {len(replacements)} replacements succeeded. Check target matches.")
    exit(1)
