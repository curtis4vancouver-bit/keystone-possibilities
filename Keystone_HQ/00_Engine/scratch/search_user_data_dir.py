import os
import re

search_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
pattern = re.compile(r"--remote-debugging-port", re.IGNORECASE)

matches = []
for root, dirs, files in os.walk(search_path):
    if ".git" in root or "node_modules" in root or ".gemini" in root:
        continue
    for file in files:
        if file.endswith(".py") or file.endswith(".ps1") or file.endswith(".bat") or file.endswith(".js"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                if pattern.search(content):
                    matches.append((filepath, len(content)))
            except Exception:
                pass

print(f"Found {len(matches)} files matching --user-data-dir:")
for filepath, size in matches:
    print(f"  {filepath} ({size} bytes)")
