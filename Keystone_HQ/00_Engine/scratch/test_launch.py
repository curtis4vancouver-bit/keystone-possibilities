import os

def search():
    root = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
    print(f"Searching for 'Starting Chrome in remote debugging' in {root}...")
    for dirpath, _, filenames in os.walk(root):
        if ".git" in dirpath or "node_modules" in dirpath or "__pycache__" in dirpath:
            continue
        for fn in filenames:
            if not fn.endswith((".py", ".bat", ".ps1", ".txt", ".md", ".json")):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                if "Starting Chrome in remote debugging" in content:
                    print(f"FOUND IN: {path}")
            except Exception:
                pass

if __name__ == "__main__":
    search()
