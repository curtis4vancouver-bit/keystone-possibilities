import json
import os

src_file = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\steps\2355\output.txt"
dest_file = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Deep_Research_Results\2_2_Local_Citation_Building.md"

if not os.path.exists(src_file):
    print(f"Error: Source file {src_file} not found!")
    exit(1)

with open(src_file, "r", encoding="utf-8") as f:
    content = f.read()

# Clean prefix and suffix if present
if "Script ran on page and returned:" in content:
    content = content.split("Script ran on page and returned:\n")[1]
if content.strip().startswith("```json"):
    content = content.strip()[7:]
if content.strip().endswith("```"):
    content = content.strip()[:-3]

try:
    data = json.loads(content.strip())
    report_text = data.get("reportText", "")
    if not report_text:
        print("Error: reportText is empty or missing!")
        exit(1)
        
    print(f"Loaded report length: {len(report_text)} chars")
    
    # Save as markdown
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    print(f"Successfully saved to {dest_file}")
    
except Exception as e:
    print(f"Error processing JSON: {e}")
    exit(1)
