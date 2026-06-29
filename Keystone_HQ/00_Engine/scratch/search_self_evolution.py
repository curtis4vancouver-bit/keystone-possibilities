with open("self_evolution.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if "qdrant" in line.lower() or "unified" in line.lower() or "ingest" in line.lower():
        print(f"{i}: {line.strip()}")
