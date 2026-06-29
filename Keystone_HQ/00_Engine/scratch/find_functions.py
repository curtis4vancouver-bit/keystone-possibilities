import os

def find_files(root_dir, filename):
    matches = []
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            matches.append(os.path.join(root, filename))
    return matches

for path in ["c:\\Users\\Curtis\\New folder\\second-website", "c:\\Users\\Curtis\\New folder\\construction-website"]:
    print(f"Searching in: {path}")
    for f in find_files(path, "functions.php"):
        print(f"Found: {f} (Size: {os.path.getsize(f)} bytes)")
