# rename_and_move.py
import os
import sys
import json
import time
import re
import string
import shutil
from pathlib import Path

# Reconfigure stdout to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

DOWNLOADS_DIR = Path(r"C:\Users\Curtis\Downloads")
DESKTOP_DIR = Path(r"C:\Users\Curtis\Desktop\LONG_033_GLP1_ANHEDONIA")
PENDING_JSON = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\51cde5f0-bd0e-4277-b8fe-c0e5aeda6f75\scratch\pending_downloads.json")

def clean_words(text):
    if not text:
        return set()
    text = text.lower()
    # Replace non-alphanumeric with spaces
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    # Split and keep words length >= 3, excluding common noise words
    noise = {"says", "keep", "exact", "clothes", "the", "avatar", "not", "change", "them", "standing", "against", "pure", "black", "background", "medium", "shot", "from", "waist", "camera", "pulls", "back", "slowly", "teaching", "mode", "subtitles", "close", "face", "holds", "steady", "serious", "expression", "nod", "with", "slight", "smile", "concerned"}
    words = [w.strip() for w in text.split()]
    return {w for w in words if len(w) >= 3 and w not in noise}

def calculate_match(filename_stem, item):
    file_words = clean_words(filename_stem)
    
    # Clean the prompt
    prompt_words = clean_words(item["prompt"])
    
    # Clean the ID (e.g. A3 has no words, but name does)
    # In some cases the name of the file comes from the dialogue, so let's combine it if present
    # We don't have dialogue in JSON but we can add dialogue in pending_downloads if needed.
    # Wait, let's also search if the filename words match any part of the name in the React state!
    # Wait, the name in React state is a uuid, so it won't match words.
    
    overlap = file_words.intersection(prompt_words)
    return len(overlap)

def get_pending_items():
    if not PENDING_JSON.exists():
        return []
    with open(PENDING_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_pending_items(items):
    with open(PENDING_JSON, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

def main():
    print("[+] Rename and Move daemon started.")
    print(f"[+] Monitoring {DOWNLOADS_DIR} for new files to move to {DESKTOP_DIR}")
    
    processed_files = set()
    
    while True:
        pending = get_pending_items()
        if not pending:
            print("[+] All pending items successfully processed! Exiting.")
            break
            
        # Scan downloads folder
        for file_path in DOWNLOADS_DIR.glob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() in [".crdownload", ".tmp", ".download"]:
                # File is still downloading
                continue
            if file_path.suffix.lower() not in [".mp4", ".jpeg", ".jpg"]:
                continue
            if file_path.name in processed_files:
                continue
                
            # Wait a moment to make sure file is fully written
            initial_size = file_path.stat().st_size
            time.sleep(1)
            if file_path.stat().st_size != initial_size:
                # Still writing
                continue
                
            # Ignore very old files
            # Age of file should be less than 1 hour (3600s)
            file_age = time.time() - file_path.stat().st_mtime
            if file_age > 3600:
                continue
                
            print(f"\n[~] Found newly downloaded file: {file_path.name}")
            
            # Match it against pending items
            stem = file_path.stem
            # Strip off any timestamp like _202606212219
            stem_clean = re.sub(r'_\d{12}$', '', stem)
            
            best_item = None
            best_score = -1
            
            for item in pending:
                # Type must match
                is_video_file = file_path.suffix.lower() == ".mp4"
                is_item_video = item["type"] == "video"
                if is_video_file != is_item_video:
                    continue
                    
                score = calculate_match(stem_clean, item)
                
                # Check for exact matches first
                if score > best_score:
                    best_score = score
                    best_item = item
            
            if best_item and best_score >= 0:
                # Move to target
                target_folder = DESKTOP_DIR / ("Videos" if best_item["type"] == "video" else "Images")
                target_ext = ".mp4" if best_item["type"] == "video" else ".jpeg"
                target_name = f"{best_item['id']}{target_ext}"
                target_path = target_folder / target_name
                
                print(f"  [+] Match found: {best_item['id']} with score {best_score}")
                print(f"  [+] Moving {file_path.name} -> {target_path}")
                
                try:
                    shutil.move(str(file_path), str(target_path))
                    processed_files.add(file_path.name)
                    # Remove from pending list
                    pending.remove(best_item)
                    save_pending_items(pending)
                    print(f"  [+] Success! {len(pending)} items remaining.")
                except Exception as e:
                    print(f"  [-] Error moving file: {e}")
            else:
                print(f"  [-] Could not match file: {file_path.name}")
                # Mark as processed so we don't spam errors
                processed_files.add(file_path.name)
                
        time.sleep(2)

if __name__ == "__main__":
    main()
