import os

def find_qdrant_writes():
    workspace = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
    print("Searching for Qdrant write operations in Python files...")
    
    keywords = ["upsert", "upload_points", "upload_records", "add_point", "add_points"]
    
    for root, dirs, files in os.walk(workspace):
        dirs[:] = [d for d in dirs if d not in [".git", ".obsidian", "node_modules", "scratch", "__pycache__"]]
        
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "client" in content or "qdrant" in content:
                            lines = content.split("\n")
                            for idx, line in enumerate(lines):
                                if any(kw in line for kw in keywords) and ("unified" in line or "UNIFIED" in line or "collection" in line or "points" in line):
                                    print(f"Found in: {path} (Line {idx+1})")
                                    print(f"  {line.strip()}")
                except Exception as e:
                    pass

if __name__ == "__main__":
    find_qdrant_writes()
