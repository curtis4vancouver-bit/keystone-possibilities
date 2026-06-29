import os

root_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def main():
    matching_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip node_modules, .git, venv
        if any(skip in root for skip in ["node_modules", ".git", "venv", ".learnings", "deprecated_scripts"]):
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        if "reportFull" in f.read():
                            matching_files.append(os.path.relpath(path, root_dir))
                except:
                    pass
                    
    print("Files containing 'reportFull':")
    for f in matching_files:
        print(f)

if __name__ == "__main__":
    main()
