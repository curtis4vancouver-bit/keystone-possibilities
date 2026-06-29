import re

input_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\SCRIPT_001_HEYGEN_OMINI_SEGMENTS.md"
output_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\SCRIPT_001_HEYGEN_OMINI_SEGMENTS.md"

BASE_PROMPT = (
    "Cinematic portrait of a man, mid-40s, athletic build, short hair, clean-shaven or light stubble, "
    "wearing a fitted black crew-neck t-shirt, standing in an active posture against a pure solid black background with "
    "zero visible set elements, zero furniture, and zero wall textures. Single soft key light from a 45-degree angle on the "
    "camera-left, creating dramatic, clinical side-lighting on his face and upper body. Fill light is extremely low, "
    "creating deep, moody, compressed shadows. Muted clinical color grading with a desaturated teal and charcoal gray "
    "palette (#1a3a3a, #111111). Ultra-shallow depth of field with a beautiful, soft bokeh roll-off at the edges. "
    "Volumetric clinical haze is barely visible, catching the key light subtly. Shot on 35mm anamorphic lens, "
    "highly cinematic, premium, authoritative, medical documentary style, 4K resolution, clean. "
    "Expression: severe, focused, authoritative — not smiling. Shoulders squared. {camera_action} "
    "Hands visible at chest/waist level for gesturing."
)

camera_actions = {
    1: "The camera is slowly zooming in on his eyes to capture a tense, serious expression.",
    2: "The camera is static close-up, holding a steady, intense gaze directly into the lens.",
    3: "The camera is medium close-up, slowly zooming out to reveal his shoulders and posture.",
    4: "The camera is medium shot, slowly panning right as he uses hands to gesture active building.",
    5: "The camera is at a 45-degree side profile, slowly panning left as he turns his head back to face the lens.",
    6: "The camera is medium shot, slowly zooming out to reveal his hands gesturing with open palms.",
    7: "The camera is medium close-up, slowly zooming in on his face, creating a tight, serious frame.",
    8: "The camera is static tight close-up, holding a steady, intense look directly into the lens.",
    9: "The camera is medium close-up, slowly zooming in to emphasize the weight of the STEP-one statistics.",
    10: "The camera is tight close-up, slowly zooming in on his eyes to emphasize intense gravity.",
    11: "The camera is medium shot, slowly zooming out as he uses a decisive slicing hand gesture.",
    12: "The camera is medium close-up, slowly panning left as he gestures to outline the study parameters.",
    13: "The camera is at a 45-degree side profile, slowly zooming out as he gestures with hands at chest level.",
    14: "The camera is medium close-up, slowly zooming in as he leans forward with a serious, intense expression.",
    15: "The camera is static medium shot, holding an authoritative, serious explanation posture.",
    16: "The camera is medium close-up, slowly zooming out as he uses hand gestures to explain the scan misreadings.",
    17: "The camera is medium shot, slowly zooming out as he gestures with open palms.",
    18: "The camera is static tight close-up, holding a deeply focused, intense gaze on his face.",
    19: "The camera is at a 45-degree side profile, slowly zooming in on his face, dramatic side-lighting casting deep shadows.",
    20: "The camera is medium close-up, slowly zooming in as his expression hardens with intensity.",
    21: "The camera is medium shot, slowly zooming out to show active, expressive hands.",
    22: "The camera is at a 45-degree side profile, slowly zooming out as he gestures dynamically with both hands.",
    23: "The camera is tight close-up, slowly zooming in on his eyes to capture intense gravity.",
    24: "The camera is medium shot, slowly zooming out as he lifts his hand into a solid fist.",
    25: "The camera is medium close-up, slowly zooming in as he makes direct, unwavering eye contact with the lens.",
    26: "The camera is medium shot, slowly zooming out as he gestures to introduce the first step.",
    27: "The camera is static medium close-up, holding an authoritative, serious explanation posture.",
    28: "The camera is medium shot, slowly zooming out as he raises one finger to count.",
    29: "The camera is medium close-up, slowly zooming in as he delivers the exact protein number with intensity.",
    30: "The camera is static tight close-up, holding a serious, relatable expression.",
    31: "The camera is at a 45-degree side profile, slowly panning right as he gestures dynamically with both hands.",
    32: "The camera is medium shot, slowly zooming out as he gestures to introduce the second step.",
    33: "The camera is medium close-up, slowly zooming in as he delivers the scientific terms with authority.",
    34: "The camera is medium shot, slowly zooming out as he gestures active muscle protection.",
    35: "The camera is at a 45-degree side profile, slowly panning left as he gestures to outline the movements.",
    36: "The camera is tight close-up, slowly zooming in on his face to capture the serious strain and focus.",
    37: "The camera is medium shot, slowly zooming out as he gestures to introduce step three.",
    38: "The camera is medium close-up, slowly zooming in as he explains the scientific validation.",
    39: "The camera is static medium shot, holding an authoritative, serious explanation posture.",
    40: "The camera is at a 45-degree side profile, slowly zooming in as he gestures with hands at waist level.",
    41: "The camera is medium shot, slowly zooming out to introduce the final step.",
    42: "The camera is tight close-up, slowly zooming in on his facial structure.",
    43: "The camera is medium close-up, slowly panning left as he explains the peptide mechanics.",
    44: "The camera is medium shot, slowly zooming out as he gestures with open palms.",
    45: "The camera is medium close-up, slowly zooming in as he makes direct, serious eye contact with the lens.",
    46: "The camera is static medium shot, showing an active, confident posture.",
    47: "The camera is at a 45-degree side profile, slowly panning right as he turns back to the lens with a light grin.",
    48: "The camera is medium shot, slowly zooming out as he gestures with hands moving actively.",
    49: "The camera is medium close-up, slowly zooming in as his expression becomes highly focused and intense.",
    50: "The camera is at a 45-degree side profile, slowly zooming out to wide shot as he gestures to subscribe."
}

with open(input_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Let's parse out the clips
# A clip starts with "### CLIP XX" and contains Dialogue Prompt and Visual Prompt
# Let's replace the visual prompts
for clip_num in range(1, 51):
    clip_str = f"CLIP {clip_num:03d}"
    # find the block for this clip
    # e.g., "### CLIP 001" up to "### CLIP 002" or the end of the file
    start_pos = content.find(f"### {clip_str}")
    if start_pos == -1:
        print(f"Could not find {clip_str}!")
        continue
    
    # find next clip position or end of the file
    next_clip_num = clip_num + 1
    if next_clip_num <= 50:
        next_clip_str = f"### CLIP {next_clip_num:03d}"
        end_pos = content.find(next_clip_str, start_pos)
    else:
        end_pos = content.find("---", start_pos)
        if end_pos == -1:
            end_pos = len(content)
            
    clip_block = content[start_pos:end_pos]
    
    # Now find the Visual Prompt within this block
    # Visual Prompt: `...`
    # Let's extract the exact visual prompt string
    vp_match = re.search(r"\*\s+\*\*Visual Prompt\*\*:\s*\n?\s*`(.*?)`", clip_block)
    if vp_match:
        old_vp = vp_match.group(1)
        camera_action = camera_actions[clip_num]
        new_vp = BASE_PROMPT.format(camera_action=camera_action)
        
        # Replace in the clip_block
        new_clip_block = clip_block.replace(f"`{old_vp}`", f"`{new_vp}`")
        content = content[:start_pos] + new_clip_block + content[end_pos:]
    else:
        print(f"Could not find visual prompt for clip {clip_num}!")

# Update header to V6
content = content.replace(
    "# 🎬 HEYGEN & GOOGLE LABS FLOW OMNI SEGMENTS (V5 — 100% ON-SCREEN STANDING TALKING HEAD)",
    "# 🎬 HEYGEN & GOOGLE LABS FLOW OMNI SEGMENTS (V6 — 100% ON-SCREEN STANDING TALKING HEAD - SELF-CONTAINED PROMPTS)"
)
content = content.replace(
    "## v5.0 | Created: 2026-05-22 | Target Duration: 8 minutes 20 seconds (500 seconds)",
    "## v6.0 | Created: 2026-05-22 | Target Duration: 8 minutes 20 seconds (500 seconds)"
)
content = content.replace(
    "*Script Package 001 Segmented & Structured (V5) | Keystone Recomposition*",
    "*Script Package 001 Segmented & Structured (V6) | Keystone Recomposition*"
)

# Write output
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully generated SCRIPT_001_HEYGEN_OMINI_SEGMENTS.md V6 with 100% self-contained visual prompts!")
