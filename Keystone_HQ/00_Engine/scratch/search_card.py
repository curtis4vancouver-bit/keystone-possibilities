import os

root_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ"
keyword = "kr-entity-card"

for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(p in dirpath for p in [".git", "node_modules", "vendor", ".gemini", "wp-admin", "wp-includes"]):
        continue
    for filename in filenames:
        if filename.endswith(('.php', '.html', '.css', '.js', '.json', '.md', '.txt')):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, 1):
                        if keyword in line.lower():
                            print(f"{filepath}:{line_num}: {line.strip()}")
            except Exception as e:
                pass
