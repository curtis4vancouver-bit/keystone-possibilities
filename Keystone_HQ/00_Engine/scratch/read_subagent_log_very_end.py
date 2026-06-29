import os
import json

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\03db9322-53c9-4c59-9c67-7c7378dde2ea\.system_generated\logs\transcript.jsonl"

if not os.path.exists(log_path):
    print(f"Log path does not exist: {log_path}")
else:
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print(f"Total lines in subagent transcript: {len(lines)}")
    print("Printing last 10 lines in full detail:")
    for idx in range(max(0, len(lines)-10), len(lines)):
        line = lines[idx]
        try:
            data = json.loads(line)
            print(f"\n--- STEP {idx} ---")
            print(f"Type: {data.get('type')}")
            print(f"Source: {data.get('source')}")
            print(f"Status: {data.get('status')}")
            print(f"Content length: {len(data.get('content', '')) if data.get('content') else 0}")
            if data.get('content'):
                print(f"Content: {data.get('content')[:300]}")
            if 'tool_calls' in data:
                print("Tool Calls:")
                for tc in data['tool_calls']:
                    print(f"  Name: {tc.get('name')}")
                    print(f"  Arguments: {str(tc.get('arguments'))[:200]}")
            if 'results' in data:
                print("Results:")
                for r in data['results']:
                    print(f"  Status: {r.get('status')}")
                    print(f"  Output length: {len(r.get('output', '')) if r.get('output') else 0}")
                    print(f"  Output snippet: {str(r.get('output', ''))[:200]}")
        except Exception as e:
            print(f"Error parsing line {idx}: {e}")
