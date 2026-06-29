import os

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def search():
    found_mentions = []
    keywords = ["61583823506176"]
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(x in root for x in ["node_modules", ".git", "venv", "__pycache__"]):
            continue
        for file in files:
            path = os.path.join(root, file)
            if not file.endswith((".py", ".json", ".md", ".ps1", ".bat", ".txt")):
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for kw in keywords:
                        if kw in content:
                            found_mentions.append(path)
            except Exception:
                pass
                
    print(f"Found {len(found_mentions)} files containing page ID '61583823506176':")
    for path in found_mentions:
        rel = os.path.relpath(path, ROOT_DIR)
        print(f" - {rel}")

if __name__ == "__main__":
    search()
