# prepare_downloads.py
import re
import json
import string
from pathlib import Path

SCRIPT_FILE = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved\glp1_anhedonia_8m20s_studio_black.md")
DESKTOP_DIR = Path(r"C:\Users\Curtis\Desktop\LONG_033_GLP1_ANHEDONIA")
MAPS_FILE = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\51cde5f0-bd0e-4277-b8fe-c0e5aeda6f75\.system_generated\steps\1311\output.txt")
OUTPUT_JSON = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\51cde5f0-bd0e-4277-b8fe-c0e5aeda6f75\scratch\pending_downloads.json")

def parse_script():
    with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    
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
            "prompt": prompt.strip(),
            "type": "video"
        })
        
    broll_blocks = re.findall(
        r"#### 🖼️ B(\d+): .*?\n(.*?)(?=\n\n####|\n\n---|\Z)",
        content,
        re.DOTALL
    )
    brolls = []
    for broll_id, prompt in broll_blocks:
        brolls.append({
            "id": f"B{broll_id}",
            "prompt": prompt.strip(),
            "type": "image"
        })
        
    return clips, brolls

def calculate_similarity(s1, s2):
    def clean(s):
        s = s.lower()
        s = s.replace("he says:", "").replace("she says:", "")
        s = s.replace("victoria says:", "").replace("wayne says:", "")
        return set(w.strip(string.punctuation) for w in s.split() if len(w.strip(string.punctuation)) > 3)
    
    set1 = clean(s1)
    set2 = clean(s2)
    if not set1 or not set2:
        return 0.0
    intersection = set1.intersection(set2)
    return len(intersection) / max(len(set1), len(set2))

def main():
    clips, brolls = parse_script()
    
    # Read card mappings from output.txt
    with open(MAPS_FILE, "r", encoding="utf-8") as f:
        log_content = f.read()
    
    # Extract json block
    json_match = re.search(r"```json\s*(.*?)\s*```", log_content, re.DOTALL)
    card_mappings = json.loads(json_match.group(1))
    
    # Check already downloaded files
    video_dest = DESKTOP_DIR / "Videos"
    image_dest = DESKTOP_DIR / "Images"
    video_dest.mkdir(parents=True, exist_ok=True)
    image_dest.mkdir(parents=True, exist_ok=True)
    
    existing_videos = {f.stem for f in video_dest.glob("*.mp4")}
    existing_images = {f.stem for f in image_dest.glob("*.jpeg")}
    
    pending = []
    
    # Match clips
    for clip in clips:
        clip_id = clip["id"]
        if clip_id in existing_videos:
            continue
            
        best_card = None
        best_score = 0.0
        expected_prompt = f"says: {clip['dialogue']}. {clip['prompt']}"
        
        for card in card_mappings:
            meta = card.get("meta")
            if not meta or meta.get("type") != "video":
                continue
            score = calculate_similarity(expected_prompt, meta.get("prompt", ""))
            if score > best_score:
                best_score = score
                best_card = card
                
        if best_card and best_score > 0.5:
            pending.append({
                "id": clip_id,
                "cardIndex": best_card["cardIndex"],
                "type": "video",
                "name": best_card["meta"]["name"],
                "prompt": f"{clip['dialogue']} {clip['prompt']}"
            })
        else:
            print(f"[-] No match for clip {clip_id}")

    # Match B-rolls
    for broll in brolls:
        b_id = broll["id"]
        if b_id in existing_images:
            continue
            
        best_card = None
        best_score = 0.0
        
        for card in card_mappings:
            meta = card.get("meta")
            if not meta or meta.get("type") != "image":
                continue
            score = calculate_similarity(broll["prompt"], meta.get("prompt", ""))
            if score > best_score:
                best_score = score
                best_card = card
                
        if best_card and best_score > 0.5:
            pending.append({
                "id": b_id,
                "cardIndex": best_card["cardIndex"],
                "type": "image",
                "name": best_card["meta"]["name"],
                "prompt": broll["prompt"]
            })
        else:
            print(f"[-] No match for B-roll {b_id}")
            
    # Save the output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(pending, f, indent=2)
        
    print(f"[+] Prepared {len(pending)} pending downloads. Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
