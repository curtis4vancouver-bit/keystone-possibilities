import os
import json

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\03db9322-53c9-4c59-9c67-7c7378dde2ea\.system_generated\logs\transcript.jsonl"

if not os.path.exists(log_path):
    print(f"Log path does not exist: {log_path}")
else:
    print("Reading last 50 lines of log...")
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
        for line in lines[-50:]:
            try:
                data = json.loads(line)
                print(f"[{data.get('type', 'UNKNOWN')}] {data.get('content', '')[:150]}")
            except Exception as e:
                print(f"Line error: {e}")
