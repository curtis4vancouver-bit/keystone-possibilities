import json
import glob
import re

with open("inspect_results.txt", "w", encoding="utf-8") as out:
    for filename in glob.glob("post_*.json"):
        out.write(f"=== {filename} ===\n")
        try:
            with open(filename, "r", encoding="utf-8") as f:
                d = json.load(f)
            content = d.get("content", "")
            
            # Search for "twin" case-insensitive
            twins = re.findall(r'.{0,100}twin.{0,100}', content, re.IGNORECASE)
            out.write(f"Found {len(twins)} occurrences of 'twin':\n")
            for t in twins:
                out.write(f"  - {t.strip()}\n")
                
            # Search for "hidden" or "display:none" or "display: none"
            hiddens = re.findall(r'.{0,100}display:\s*none.{0,100}', content, re.IGNORECASE)
            out.write(f"Found {len(hiddens)} occurrences of 'display: none':\n")
            for h in hiddens:
                out.write(f"  - {h.strip()}\n")
                
            # Search for "kr-disclaimer-box" or similar elements
            disclaimers = re.findall(r'.{0,100}disclaimer.{0,100}', content, re.IGNORECASE)
            out.write(f"Found {len(disclaimers)} occurrences of 'disclaimer':\n")
            for dc in disclaimers:
                out.write(f"  - {dc.strip()}\n")
        except Exception as e:
            out.write(f"Error: {e}\n")
        out.write("\n")
print("Saved search results to inspect_results.txt")
