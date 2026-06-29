import json

file_path = r"C:\Users\Curtis\.gemini\antigravity\brain\21cff3a5-5ad8-4efd-832e-b882b33d65f4\.system_generated\logs\transcript.jsonl"

print("Searching for React fiber snippet...")
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get("step_index")
            if step is not None and 10500 <= step <= 10600:
                content = str(data)
                if ("fiber" in content or "__reactFiber" in content or "subtitle" in content) and data.get("type") == "PLANNER_RESPONSE":
                    print(f"=== Step {step} ===")
                    print(json.dumps(data, indent=2))
        except:
            pass
