import os
import re

# File Paths
segments_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Content_Production\SCRIPT_001_HEYGEN_OMINI_SEGMENTS.md"
broll_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Content_Production\SCRIPT_001_BROLL_SHOT_LIST.md"
output_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Content_Production\SCRIPT_001_FINAL_FLOW.md"

# 1. Read input files
with open(segments_path, "r", encoding="utf-8") as f:
    segments_content = f.read()

with open(broll_path, "r", encoding="utf-8") as f:
    broll_content = f.read()

# 2. Parse Video Clips
clips = []
# Match ### CLIP 001 ... up to next ### CLIP or ---
clip_matches = re.finditer(r"### CLIP (\d+) \((.*?)\)\s*\n\*\*Dialogue:\*\*\s*\n`Wayne says: (.*?)`\s*\n\*\*Visual:\*\*\s*\n`(.*?)`", segments_content, re.DOTALL)

for m in clip_matches:
    clip_num = int(m.group(1))
    time_range = m.group(2)
    dialogue = m.group(3).strip()
    visual = m.group(4).strip()
    
    # Apply Wayne's personal updates and zinc/CJC discovery in clips 45-48
    if clip_num == 45:
        dialogue = "Let me share what implementing this full protocol has looked like in my own case study... thirty-two weeks into my tir-zep-a-tide protocol... forty-eight pounds down... currently at two hundred ten pounds..."
        visual = "Standing against pure black background. Camera static medium shot. Confident posture."
    elif clip_num == 46:
        dialogue = "And my lean muscle mass has remained completely stable... while my back is stretching better and my shoulder injury is finally recovering..."
        visual = "Standing against pure black background. Camera slowly zooms out. Open palm gestures."
    elif clip_num == 47:
        dialogue = "But here is a critical lesson I learned... while on c-j-c twelve ninety-five... you need to supplement zinc... I did not take it at the beginning... and only found out later..."
        visual = "Standing against pure black background. Camera slowly zooms in. Serious direct gaze."
    elif clip_num == 48:
        dialogue = "Growth hormone is stored in the pituitary using zinc... so continuous stimulation can deplete it... I am actually coming off the c-j-c right now... just to hold on to the zinc status..."
        visual = "Standing against pure black background. Camera at 45-degree side profile slowly panning right. Turning back to lens."

    # Format the prompt following PR-019 and formatting rules
    # Visual action description: e.g. "Camera slowly zooms in on face. Serious intense expression."
    # We clean visual prompt text, removing "Standing against pure black background" to avoid redundancy
    cleaned_visual_action = visual.replace("Standing against pure black background.", "").strip()
    if cleaned_visual_action.startswith("Camera"):
        cleaned_visual_action = cleaned_visual_action[0].lower() + cleaned_visual_action[1:]
    
    video_prompt = f"Wayne. Reference the picture for my face and clothes. Standing at a 30-degree angle or less, facing mostly front. Pure black background. {cleaned_visual_action} No subtitles."
    
    clips.append({
        "num": clip_num,
        "time": time_range,
        "dialogue": dialogue,
        "prompt": video_prompt
    })

# 3. Parse B-Roll Prompts
brolls = []
# Match ### B-ROLL 001 — Overlays CLIP 001 (0:00–0:10) ... up to next ### B-ROLL or ---
# Note: Prompt is in a ``` block
broll_matches = re.finditer(r"### B-ROLL (\d+) — Overlays CLIP \d+ \((.*?)\).*?```\s*\n(.*?)\n```", broll_content, re.DOTALL)

for m in broll_matches:
    broll_num = int(m.group(1))
    time_mark = m.group(2).split("–")[0].strip()  # get start time mark (e.g. 0:00)
    prompt = m.group(3).strip()
    
    # Make sure prompt ends with 16:9
    if not prompt.endswith("16:9."):
        prompt = prompt.rstrip() + " 16:9."
        
    brolls.append({
        "num": broll_num,
        "time": time_mark,
        "prompt": prompt
    })

# 4. Generate the consolidated SCRIPT_001_FINAL_FLOW.md
output_text = """# 🎬 SCRIPT 001 — GLP-1 MUSCLE LOSS: THE BUILDER'S RECOMPOSITION PROTOCOL
## Keystone Recomposition | Long-Form Podcast (Wayne Solo)
## Target Duration: 8 minutes 20 seconds (500 seconds)
## Format: 100% Talking Head on V1, B-Roll overlays on V2, T1 Thumbnail

---

## 📋 PRODUCTION OVERVIEW
| Field | Value |
|-------|-------|
| **Script ID** | SCRIPT_001 |
| **Title** | I Lost 40 Lbs on Ozempic — Here's How Much Was Muscle \| Men Over 40 |
| **Format** | Talking Head (Wayne Stevenson) |
| **Channel** | Keystone Recomposition |
| **Style** | Pure black background, standing at 30-degree angle or less, active hand movements |
| **Video Model** | Omni Flash · 10s · 16:9 · 1x |
| **Image Model** | 🍌 Nano Banana Pro · 16:9 · 1x |
| **Output Folder** | `C:\\Users\\Curtis\\Desktop\\LONG_FORM_PRODUCTION` |

---

## 🎬 SECTION 1: VIDEO CLIPS (Omni Flash · 10s · 16:9)

> **Settings**: Video mode → Omni Flash → 10 seconds → 16:9 → 1x
> **Wayne clips**: Attach avatar ("me"). No chair.
> **Pacing**: Standing throughout, 30-degree max angle, frequent zooms, and high hand-gesture activity.
> **Phonetics**: `sema-gloo-tide`, `tir-zep-a-tide`, `c-j-c twelve ninety-five`, `g-h-k copper`, `b-p-c one fifty-seven` verified.

"""

for c in clips:
    output_text += f"### 📋 CLIP A{c['num']} ({c['time']})\n\n"
    output_text += "```\n"
    output_text += f"THIS IS THE SCRIPT:\nWayne says: {c['dialogue']}\n\n"
    output_text += f"THIS IS THE VIDEO PROMPT:\n{c['prompt']}\n"
    output_text += "```\n\n"

output_text += """---

## 🖼️ SECTION 2: B-ROLL IMAGES (🍌 Nano Banana Pro · 16:9)

> **Settings**: Image mode → 🍌 Nano Banana Pro → 16:9 → 1x
> **NO AVATARS IN B-ROLL**. Save images to `C:\\Users\\Curtis\\Desktop\\LONG_FORM_PRODUCTION\\Images\\`

"""

for b in brolls:
    # E.g. 10s mark transition, 20s mark transition...
    seconds = (b['num'] - 1) * 10
    output_text += f"### 🖼️ B-ROLL PICTURE B{b['num']} ({seconds}s mark transition)\n\n"
    output_text += "```text\n"
    output_text += f"THIS IS THE B-ROLL PICTURE PROMPT:\n{b['prompt']}\n"
    output_text += "```\n\n"

output_text += """---

## 🎨 SECTION 3: THUMBNAIL (🍌 Nano Banana Pro · 16:9)

### 🎨 THUMBNAIL: The Muscle Wasting Blueprint

```text
High-contrast thumbnail. Left side: Victoria looking shocked and holding a DEXA scan report. Right side: Wayne looking serious and confident in a black crew-neck t-shirt. Center: Bold gold typography reading 'OZEMPIC TOOK 45% OF MY MUSCLE'. Pure black background. Reference the picture for my face and clothes. 16:9.
```

---

## 📦 SECTION 4: YOUTUBE METADATA

### 📋 YOUTUBE TITLE OPTIONS
```
I Lost 48 Lbs on Ozempic — Here's How Much Was Muscle | Men Over 40
Ozempic Took 45% of My Weight From Muscle — The Data Nobody Shows You
The Ozempic Muscle Loss Fix: A Construction Worker's 90-Day Recomp Protocol
```

### 📋 YOUTUBE DESCRIPTION
```
Are you losing active skeletal muscle tissue on GLP-1 receptor agonists? Clinical trials show that up to forty percent of weight lost during rapid semaglutide or tirzepatide therapy is actually active, functional lean mass. This muscle leak triggers early-onset sarcopenia and damages your baseline metabolic rate, leading to metabolic rebound. In this educational case study, Wayne Stevenson shares his personal recomposition protocol designed for men over forty to combat muscle wasting. By combining a protein nutrition floor titrated to two grams per kilogram of lean body mass with a high-tension progressive resistance training regimen four times per week, the body signals active muscle hypertrophy. Additionally, this research analysis breaks down the cellular science behind growth hormone secretagogues CJC-1295 and Ipamorelin, which work cooperatively to trigger lipid oxidation while amplifying protein synthesis. We also touch upon structural tissue recovery using joint-healing compounds like BPC-157 and TB-500. Discover how a systematic titration schedule, clean whole-food nutrition (like grass-fed beef and wild salmon), and biomarker-tracked lab work can rebuild a strong physical engine. All protocols are conducted under direct clinical physician supervision for research and longevity science analysis.

#GLP1 #Sarcopenia #MuscleLoss #PeptideProtocols #MenOver40 #LongevityBuilder #BiohackingBuilder #KeystoneProtocols #Semaglutide #Tirzepatide #CJC1295 #Ipamorelin

---
🎵 Training Soundscapes — Lock in your deep-focus workout with the official Keystone Recomposition Deep House Mix: https://www.youtube.com/watch?v=LNlAiAu5YOo

---
🔗 CONNECT:
• Instagram: https://www.instagram.com/keystonerecomposition
• Facebook: https://www.facebook.com/166025896601563
• Spotify: https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y

---
🏗️ Building a new custom home? Multiplexes and commercial developments in the Sea-to-Sky Corridor: https://keystonepossibilities.ca

⚖️ MEDICAL DISCLAIMER:
The information in this video is for scientific study, educational analysis, and general research purposes only. It does not constitute medical advice, diagnosis, or treatment. Compounded peptides such as CJC-1295, Ipamorelin, BPC-157, and TB-500 are not FDA-approved for human administration, are banned by WADA, and are classified as unauthorized drugs by Health Canada. GLP-1 receptor agonists like semaglutide and tirzepatide should only be used under direct, licensed clinical medical supervision. Salt formulations of semaglutide (such as semaglutide sodium or semaglutide acetate) have no established safety profiles and should be avoided. Consult your physician before starting any new protocol.

🤖 SYNTHETIC MEDIA / AI DIGITAL TWIN DISCLOSURE:
The host is a photorealistic digital representation of Wayne Stevenson, synthesized using advanced visual networks. All personal health metrics, real B-roll footage, and audio journals are authentic.
```

### 📋 YOUTUBE TAGS
```
glp-1 muscle loss, glp-1 sarcopenia, semaglutide muscle loss, tirzepatide muscle preservation, how to prevent muscle loss on semaglutide, prevent sarcopenia on ozempic, body recomposition peptide protocol, cjc 1295 ipamorelin muscle gain, cjc-1295 ipamorelin weight loss, growth hormone secretagogues muscle, growth hormone secretagogue recomposition, preventing muscle wasting on wegovy, protein intake on glp-1, peptides for muscle preservation, sarcopenic obesity men over 40, muscle hypertrophy on glp-1, wayne stevenson recomposition, keystone protocols peptides, cellular recovery protocol, bpc-157 tb-500 joint health, joint repair peptides, compounded semaglutide safety, cjc 1295 ipamorelin titration schedule, men over 40 peptide stack, peptide therapy for fat loss, lipid oxidation peptides, protein synthesis peptides, builder recovery protocol, clinical longevity science, biomarker tracked recomposition, peptide science case study, how to maintain muscle on ozempic, lean mass preservation semaglutide, peptide stack for fat loss, cellular hypertrophy peptides
```
"""

# Write the output file
with open(output_path, "w", encoding="utf-8") as f:
    f.write(output_text)

print(f"SUCCESS: Compiled SCRIPT_001_FINAL_FLOW.md with {len(clips)} clips and {len(brolls)} B-rolls.")
