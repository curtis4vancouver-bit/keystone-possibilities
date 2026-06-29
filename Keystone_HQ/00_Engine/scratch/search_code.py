import os

scratch_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch"

def main():
    matching_files = []
    for item in os.listdir(scratch_dir):
        if item.endswith(".py"):
            path = os.path.join(scratch_dir, item)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    if "deep_research" in content.lower() or "gemini" in content.lower():
                        matching_files.append(item)
            except:
                pass
                
    print("Files in scratch containing deep_research or gemini:")
    for f in matching_files:
        print(f)

if __name__ == "__main__":
    main()
