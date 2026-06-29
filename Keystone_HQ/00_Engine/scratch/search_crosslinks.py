import json

for pid in [1149, 1178]:
    try:
        with open(f"post_{pid}.json", "r", encoding="utf-8") as f:
            d = json.load(f)
        content = d.get("content", "")
        if "fda-peptide-ban-ending-2026" in content:
            print(f"Post {pid} ALREADY has a link to Episode 3 blog!")
        else:
            print(f"Post {pid} does NOT have a link to Episode 3 blog.")
    except Exception as e:
        print(f"Error reading post_{pid}.json: {e}")
