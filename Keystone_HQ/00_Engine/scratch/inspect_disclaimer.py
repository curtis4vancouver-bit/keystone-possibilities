import json

with open("post_1149.json", "r", encoding="utf-8") as f:
    d = json.load(f)
content = d.get("content", "")

with open("scratch/post_1149_header.txt", "w", encoding="utf-8") as out:
    out.write(content[:8000])

print("Saved post_1149 header to scratch/post_1149_header.txt")
