import json

with open("learning_queue.json", "r", encoding="utf-8") as f:
    q = json.load(f)

for domain in q["queue"]:
    completed = domain.get("completed", [])
    total = len(domain.get("topics", []))
    print(f"\n=== {domain['domain']} ({len(completed)}/{total}) ===")
    for i, t in enumerate(completed, 1):
        short = t[:100] + "..." if len(t) > 100 else t
        print(f"  {i}. {short}")
