import json
import os
import re

reports = [
    {
        "id": "11",
        "title": "Shopify_vs_WooCommerce_MCP_Integrations",
        "path": r"C:\Users\Curtis\.gemini\antigravity\brain\dcfb044f-d157-4191-8dd4-486712240c1d\.system_generated\steps\1705\output.txt"
    },
    {
        "id": "12",
        "title": "Music_Metadata_MCP_Integrations",
        "path": r"C:\Users\Curtis\.gemini\antigravity\brain\dcfb044f-d157-4191-8dd4-486712240c1d\.system_generated\steps\1727\output.txt"
    },
    {
        "id": "13",
        "title": "Canadian_Corporate_Tax_Legal_MCPs",
        "path": r"C:\Users\Curtis\.gemini\antigravity\brain\dcfb044f-d157-4191-8dd4-486712240c1d\.system_generated\steps\1715\output.txt"
    }
]

output_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives"
os.makedirs(output_dir, exist_ok=True)

for r in reports:
    with open(r["path"], "r", encoding="utf-8") as f:
        content = f.read()

    # The content is a JSON string of the text. Let's load it.
    try:
        text = json.loads(content)
    except:
        text = content

    out_file = os.path.join(output_dir, f"{r['id']}_{r['title']}.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)
    
    print(f"Saved {out_file}")
