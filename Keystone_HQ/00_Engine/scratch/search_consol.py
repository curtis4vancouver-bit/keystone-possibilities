import os

search_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
ignore_dirs = {".git", "node_modules", ".next", "dist", "venv", ".venv", ".system_generated"}

print(f"Searching for 'consol' and 'Console' in: {search_dir}")
matches = []

for root, dirs, files in os.walk(search_dir):
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    for file in files:
        if file.endswith((".py", ".md", ".txt", ".json", ".ps1", ".bat")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, 1):
                        if "consol" in line.lower():
                            matches.append((path, line_num, line.strip()))
            except Exception as e:
                pass

print(f"Found {len(matches)} matches:")
for path, line_num, line in matches[:100]:
    rel_path = os.path.relpath(path, search_dir)
    print(f"[{rel_path}:{line_num}] {line}")
