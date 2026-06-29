import os
import sys

def search_files(directory, search_terms):
    print(f"=== Searching {directory} for terms: {search_terms} ===")
    for root, dirs, files in os.walk(directory):
        if any(x in root for x in ["node_modules", ".git", "__pycache__"]):
            continue
        for file in files:
            if not file.endswith((".py", ".json", ".md", ".txt", ".bat", ".ps1")):
                continue
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for term in search_terms:
                        if term in content:
                            print(f"Found '{term}' in: {path}")
            except Exception as e:
                pass

if __name__ == "__main__":
    search_files(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain", 
                 ["UCxURlqMNhAtxUTpdXmlOYaw", "youtube_token", "Keystone Protocols"])
