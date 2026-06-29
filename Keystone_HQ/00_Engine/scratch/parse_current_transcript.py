import json
import os

file_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\steps\2189\output.txt"

if not os.path.exists(file_path):
    print(f"Error: Output file not found at {file_path}")
    exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Clean prefix and suffix if present
if "Script ran on page and returned:" in content:
    content = content.split("Script ran on page and returned:\n")[1]
if content.startswith("```json\n"):
    content = content[8:]
if content.endswith("\n```"):
    content = content[:-4]
elif content.endswith("```"):
    content = content[:-3]

try:
    data = json.loads(content.strip())
    print(f"Total elements: {data.get('totalElements')}")
    matches = data.get('matches', [])
    print(f"Total matches: {len(matches)}")
    
    # Filter matches
    filtered = []
    for m in matches:
        tag = m.get('tagName')
        if tag in ['SCRIPT', 'STYLE', 'HEAD', 'HTML']:
            continue
        filtered.append(m)
        
    print(f"Filtered matches (no script/style): {len(filtered)}")
    for i, m in enumerate(filtered[:20]):
        print(f"[{i}] Tag: {m.get('tagName')} | Class: {m.get('className')} | Parent: {m.get('parentTag')}")
        print(f"    Text: {m.get('innerText')[:200]}")
except Exception as e:
    print(f"Error loading JSON: {e}")
