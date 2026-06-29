import os
import json

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def search():
    found_files = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip node_modules, .git, venv
        if any(x in root for x in ["node_modules", ".git", "venv", "__pycache__"]):
            continue
        for file in files:
            path = os.path.join(root, file)
            # Look for JSON files or files containing token, credential, oauth, secret
            file_lower = file.lower()
            if ".json" in file_lower or "token" in file_lower or "credential" in file_lower or "secret" in file_lower or "oauth" in file_lower:
                found_files.append(path)
                
    print(f"Found {len(found_files)} potential secret files:")
    for path in sorted(found_files):
        rel = os.path.relpath(path, ROOT_DIR)
        size = os.path.getsize(path)
        print(f" - {rel} ({size} bytes)")

if __name__ == "__main__":
    search()
