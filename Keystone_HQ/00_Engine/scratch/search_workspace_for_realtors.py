import os

PROJECT_ROOT = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def search_files(directory):
    matches = []
    for root, dirs, files in os.walk(directory):
        if any(ignored in root for ignored in [".git", "__pycache__", ".learnings", "node_modules", "secure_workspace"]):
            continue
        for file in files:
            if file.endswith((".md", ".txt", ".html", ".js", ".py", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "realtor" in content.lower():
                            matches.append(os.path.relpath(path, PROJECT_ROOT))
                except Exception:
                    pass
    return matches

def main():
    print("Searching for 'realtor' in workspace...")
    matches = search_files(PROJECT_ROOT)
    for m in matches:
        print(f"Match: {m}")

if __name__ == "__main__":
    main()
