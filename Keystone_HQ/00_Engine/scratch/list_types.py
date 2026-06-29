import json

file_path = r"C:\Users\Curtis\.gemini\antigravity\brain\21cff3a5-5ad8-4efd-832e-b882b33d65f4\.system_generated\logs\transcript.jsonl"

types = set()
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            t = data.get("type")
            if t:
                types.add(t)
        except:
            pass

print("Distinct types:", sorted(list(types)))
