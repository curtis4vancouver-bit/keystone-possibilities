import re
import os

script_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\keystone_8min_glp1_masterpiece.md"

def count_words(dialogue):
    # Remove punctuation for counting, but preserve hyphenated words as single words
    cleaned = re.sub(r'[^\w\s-]', '', dialogue)
    # Split by whitespace
    words = cleaned.split()
    return words, len(words)

if not os.path.exists(script_path):
    print(f"Error: Script not found at {script_path}")
    exit(1)

with open(script_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

scenes = []
current_scene_num = None

dialogue_pattern = re.compile(r"^\s*`(Wayne says:|Wayne's voiceover says:)\s*(.*?)`")

for idx, line in enumerate(lines):
    # Detect Scene headers
    header_match = re.search(r"### 🎥 SCENE (\d+):", line)
    if header_match:
        current_scene_num = int(header_match.group(1))
    
    # Detect Dialogue lines
    diag_match = dialogue_pattern.match(line)
    if diag_match:
        speaker = diag_match.group(1)
        dialogue = diag_match.group(2)
        words, count = count_words(dialogue)
        scenes.append({
            "scene": current_scene_num,
            "speaker": speaker,
            "dialogue": dialogue,
            "words": words,
            "count": count,
            "line_idx": idx + 1
        })

print(f"--- SCRIPT DIALOGUE WORD COUNT AUDIT ({len(scenes)} Scenes Found) ---\n")
failures = 0
for s in scenes:
    status = "[PASS]" if s["count"] == 15 else "[FAIL]"
    if s["count"] != 15:
        failures += 1
    print(f"Scene {s['scene']:02d} | Count: {s['count']:02d} | {status} | Line {s['line_idx']}")
    if s["count"] != 15:
        print(f"   Dialogue: \"{s['dialogue']}\"")
        print(f"   Words ({s['count']}): {s['words']}\n")

print("\n--- AUDIT SUMMARY ---")
if failures == 0 and len(scenes) == 50:
    print(f"SUCCESS! All {len(scenes)} scenes have exactly 15 words of dialogue!")
else:
    print(f"AUDIT FAILED! Found {failures} invalid scenes. Total scenes detected: {len(scenes)}")
