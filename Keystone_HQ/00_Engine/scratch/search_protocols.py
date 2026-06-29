import os
import re

pattern = re.compile(r"keystoneprotocols", re.IGNORECASE)
matches = []

for root, dirs, files in os.walk("."):
    # Avoid python virtual environments or build folders if any
    if "venv" in root or "node_modules" in root or ".git" in root:
        continue
    for file in files:
        if file.endswith((".py", ".php", ".js", ".json", ".md", ".txt")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for idx, line in enumerate(f):
                        if pattern.search(line):
                            matches.append((path, idx + 1, line.strip()))
            except Exception as e:
                pass

with open("scratch/search_protocols_results.txt", "w", encoding="utf-8") as out:
    out.write(f"Found {len(matches)} matches for 'keystoneprotocols':\n")
    for path, line_num, content in matches:
        out.write(f"{path}:{line_num}: {content}\n")

print("Saved protocols search results to scratch/search_protocols_results.txt")
