import os
import sys

def search():
    keywords = ["EAAVQO", "EAAV", "access_token"]
    search_paths = [
        r"C:\Users\Curtis\Desktop",
        r"C:\Users\Curtis\.gemini",
        r"C:\Users\Curtis\New folder"
    ]
    found = []
    
    for base_path in search_paths:
        if not os.path.exists(base_path):
            continue
        print(f"Scanning base path: {base_path}...")
        for root, dirs, files in os.walk(base_path):
            # Skip heavy folders to avoid freezing
            if any(x in root.lower() for x in ["node_modules", ".git", "venv", "__pycache__", "appdata", "local\\microsoft"]):
                continue
            for file in files:
                # Only check small files
                if file.endswith((".py", ".json", ".txt", ".md", ".ini", ".conf", ".cfg")):
                    path = os.path.join(root, file)
                    try:
                        # Check size
                        if os.path.getsize(path) < 1000000: # less than 1MB
                            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                                for kw in keywords:
                                    if kw in content:
                                        found.append((path, kw))
                                        break
                    except Exception:
                        pass
                        
    print(f"\nSearch complete. Found {len(found)} matching files:")
    for path, kw in found:
        print(f" - {path} (matched '{kw}')")

if __name__ == "__main__":
    search()
