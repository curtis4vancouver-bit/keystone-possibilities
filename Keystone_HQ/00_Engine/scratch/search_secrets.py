import os
import sys
import json

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def search():
    keywords = ["61583823506176", "15126924864337868", "EAAVQO"]
    found = {}
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(x in root for x in ["node_modules", ".git", "venv", "__pycache__"]):
            continue
        for file in files:
            path = os.path.join(root, file)
            if not file.endswith((".py", ".json", ".md", ".ps1", ".bat", ".txt")):
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines, 1):
                        for kw in keywords:
                            if kw in line:
                                rel = os.path.relpath(path, ROOT_DIR)
                                if rel not in found:
                                    found[rel] = []
                                found[rel].append((idx, kw, line.strip()[:100]))
            except Exception:
                pass
                
    print(f"Search found {len(found)} matching files:")
    for file, matches in found.items():
        print(f"\nFile: {file}")
        for line_num, kw, line_text in matches:
            print(f"  Line {line_num} [{kw}]: {line_text}")

if __name__ == "__main__":
    search()
