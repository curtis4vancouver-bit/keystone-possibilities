import json

file_path = r"C:\Users\Curtis\.gemini\antigravity\brain\21cff3a5-5ad8-4efd-832e-b882b33d65f4\.system_generated/logs/transcript.jsonl"

with open(file_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        try:
            data = json.loads(line)
            if data.get("step_index") == 11473:
                print(f"Step 11473: {data}")
                break
        except Exception as e:
            pass
