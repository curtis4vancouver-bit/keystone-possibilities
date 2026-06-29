import json

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\logs\transcript.jsonl"

with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            data = json.loads(line)
            step = data.get("step_index")
            if 5755 <= step <= 5768:
                print(f"\n=== Step {step} ({data.get('source')}, {data.get('type')}) ===")
                content = data.get("content", "")
                if content:
                    print(content[:1500])
                tool_calls = data.get("tool_calls", [])
                if tool_calls:
                    print("Tool Calls:", json.dumps(tool_calls, indent=2)[:1000])
        except Exception as e:
            pass
