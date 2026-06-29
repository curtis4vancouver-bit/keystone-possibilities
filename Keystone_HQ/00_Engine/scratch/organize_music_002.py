"""
MUSIC_002 — Batch Download Organize Script
Matches Flow's auto-generated filenames to clip numbers A1-A24.
Uses os.path.getmtime to sort duplicate-prefix files chronologically.
Run AFTER downloading all 24 clips from Google Flow.
"""

import os
import glob
import shutil

downloads_dir = r"C:\Users\Curtis\Downloads"
dest_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
os.makedirs(dest_dir, exist_ok=True)

def find_files(pattern):
    """Find files matching glob pattern, sorted by modification time (oldest first)."""
    path_pattern = os.path.join(downloads_dir, pattern)
    files = glob.glob(path_pattern)
    files.sort(key=os.path.getmtime)  # oldest first = first generated = lower clip number
    return files

# === STRATEGY ===
# Flow names files with the first few words of the prompt + timestamp.
# Since MUSIC_002 prompts all start differently, we can match by unique keywords.
#
# Clip A1: "Pure black screen" → Pure_black_screen_*
# Clip A2-A24: All start with "The video starts with a rapid..." → The_video_starts_*
#
# Since clips A2-A24 all start the same, we rely on MTIME ordering.
# The oldest "The_video_starts_*" file = A2, next oldest = A3, etc.

# Step 1: Find A1 (unique opening — "Pure black screen")
a1_files = find_files("Pure_black_screen_*.mp4")
if not a1_files:
    # Fallback: might be named differently
    a1_files = find_files("Pure_black_*.mp4")

if a1_files:
    shutil.copy2(a1_files[0], os.path.join(dest_dir, "A1.mp4"))
    print(f"A1 → {os.path.basename(a1_files[0])}")
else:
    print("WARNING: Could not find A1 (Pure black screen). Check Downloads.")

# Step 2: Find A2-A24 (all start with "The video starts...")
# These will be sorted by mtime — oldest first
remaining_files = find_files("The_video_starts_*.mp4")

# Also check for alternate naming patterns Flow might use
if len(remaining_files) < 23:
    # Flow sometimes truncates differently
    alt_files = find_files("The_video_*.mp4")
    # Merge and deduplicate
    all_paths = set(remaining_files + alt_files)
    remaining_files = sorted(all_paths, key=os.path.getmtime)

# Exclude any file we already assigned to A1
if a1_files:
    a1_path = os.path.abspath(a1_files[0])
    remaining_files = [f for f in remaining_files if os.path.abspath(f) != a1_path]

# Assign A2 through A24 in chronological order
for i, filepath in enumerate(remaining_files[:23], start=2):
    target_name = f"A{i}.mp4"
    shutil.copy2(filepath, os.path.join(dest_dir, target_name))
    print(f"A{i} → {os.path.basename(filepath)}")

# === VERIFICATION ===
print("\n" + "="*50)
print("VERIFICATION:")
print("="*50)

expected = 24
found_files = sorted(glob.glob(os.path.join(dest_dir, "A*.mp4")))
found_count = len(found_files)

if found_count == expected:
    print(f"✅ SUCCESS: All {expected} clips present!")
else:
    print(f"⚠️ WARNING: Expected {expected} clips, found {found_count}")
    # Show which are missing
    found_nums = set()
    for f in found_files:
        base = os.path.splitext(os.path.basename(f))[0]
        if base.startswith("A") and base[1:].isdigit():
            found_nums.add(int(base[1:]))
    missing = [f"A{i}" for i in range(1, expected + 1) if i not in found_nums]
    if missing:
        print(f"   Missing: {', '.join(missing)}")

print("\nFiles in destination:")
for f in found_files:
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f"  {os.path.basename(f):10s} — {size_mb:.1f} MB")

print(f"\nTotal size: {sum(os.path.getsize(f) for f in found_files) / (1024*1024):.1f} MB")
print("\nIf all looks good, delete originals from Downloads:")
print(f'  Remove-Item "{downloads_dir}\\The_video_starts_*.mp4" -Force')
print(f'  Remove-Item "{downloads_dir}\\Pure_black_screen_*.mp4" -Force')
