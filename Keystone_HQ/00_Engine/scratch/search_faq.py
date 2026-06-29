import json
import glob
import re

for filename in glob.glob("post_*.json"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            d = json.load(f)
        content = d.get("content", "")
        if "FAQPage" in content or "faq" in content.lower():
            print(f"Found FAQ in {filename}")
            # Search for JSON blocks
            faqs = re.findall(r'FAQPage', content)
            print(f"  FAQPage occurrences: {len(faqs)}")
    except Exception as e:
        print(f"Error reading {filename}: {e}")
