import json
import os

path = r"C:\Users\Curtis\.gemini\antigravity\brain\231c6914-89c5-4c61-99bf-e20300ea490f\.system_generated\logs\transcript.jsonl"
if os.path.exists(path):
    print("Found subagent transcript. Reading last few lines...")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for line in lines[-20:]:
        try:
            d = json.loads(line)
            # Print if type is PLANNER_RESPONSE or MODEL_RESPONSE or similar
            if d.get("source") == "MODEL" or "content" in d:
                print(f"[{d.get('type')}] content preview:")
                print(d.get("content")[:2000])
                print("="*40)
        except Exception as e:
            print("Error parsing line:", e)
else:
    print("Subagent transcript not found at", path)
