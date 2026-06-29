import os

def find_create_collection():
    workspace = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
    print("Searching for 'create_collection' in Python files...")
    
    for root, dirs, files in os.walk(workspace):
        # Skip excluded dirs
        dirs[:] = [d for d in dirs if d not in [".git", ".obsidian", "node_modules", "scratch", "__pycache__"]]
        
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "create_collection" in content or "recreate_collection" in content:
                            print(f"Found in: {path}")
                            # Print lines containing it
                            lines = content.split("\n")
                            for idx, line in enumerate(lines):
                                if "create_collection" in line or "recreate_collection" in line:
                                    print(f"  Line {idx+1}: {line.strip()}")
                except Exception as e:
                    pass

if __name__ == "__main__":
    find_create_collection()
