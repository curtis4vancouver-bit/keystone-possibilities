import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def search_files(directory):
    for root, dirs, files in os.walk(directory):
        if ".git" in root or "__pycache__" in root or ".learnings" in root or "node_modules" in root:
            continue
        for file in files:
            if file.endswith((".md", ".txt", ".html", ".js", ".py", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "BC Hydro" in content or "Hydro" in content:
                            print(f"\nMatch in: {os.path.relpath(path, PROJECT_ROOT)}")
                            # Print lines containing the match
                            lines = content.splitlines()
                            for i, line in enumerate(lines, 1):
                                if "BC Hydro" in line or "Hydro" in line:
                                    print(f"  Line {i}: {line.strip()[:150]}")
                except Exception as e:
                    pass

def main():
    print("Searching for 'BC Hydro' or 'Hydro' in workspace files...")
    search_files(PROJECT_ROOT)

if __name__ == "__main__":
    main()
