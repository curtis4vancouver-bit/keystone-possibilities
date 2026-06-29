import os
import glob
import re
import shutil

downloads_dir = r"C:\Users\Curtis\Downloads"
dest_dir = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
os.makedirs(dest_dir, exist_ok=True)

# Find all mp4 files downloaded today for this project
# They have a timestamp like 202606092022
files = glob.glob(os.path.join(downloads_dir, "*20260609*.mp4"))

# Extract timestamp from filename for sorting
def extract_timestamp(filepath):
    filename = os.path.basename(filepath)
    match = re.search(r'_(\d{12})\.mp4$', filename)
    if match:
        return int(match.group(1))
    return 0

# Sort files by their generation timestamp
sorted_files = sorted(files, key=extract_timestamp)

# Print and move
print(f"Found {len(sorted_files)} files.")
for i, filepath in enumerate(sorted_files, start=1):
    timestamp = extract_timestamp(filepath)
    new_name = f"A{i}.mp4"
    dest_path = os.path.join(dest_dir, new_name)
    print(f"[{timestamp}] {os.path.basename(filepath)} -> {new_name}")
    shutil.copy2(filepath, dest_path)
