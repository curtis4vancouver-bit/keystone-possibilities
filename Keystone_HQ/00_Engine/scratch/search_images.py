import os
import re

artifacts_dir = r"C:\Users\Curtis\.gemini\antigravity\brain\21cff3a5-5ad8-4efd-832e-b882b33d65f4"
for name in os.listdir(artifacts_dir):
    if name.endswith(".md"):
        path = os.path.join(artifacts_dir, name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
            if matches:
                print(f"File: {name}")
                for m in matches:
                    print(f"  {m}")
