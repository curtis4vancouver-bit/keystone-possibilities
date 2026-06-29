import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

root_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
print("Scanning workspace for port 9222...")

for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file_obj:
                    content = file_obj.read()
                    if "9222" in content:
                        print(f"Match found in: {path}")
            except Exception:
                continue
