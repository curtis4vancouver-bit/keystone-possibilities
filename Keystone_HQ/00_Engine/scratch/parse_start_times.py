import json
import os

path = r'C:\Users\Curtis\.gemini\antigravity\brain\e0c6e90d-f4d6-474b-9f6a-fbe1416672e1\.system_generated\logs\transcript.jsonl'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Search lines around 1045 for type_text or navigate_page
for idx in range(1030, 1070):
    if idx < len(lines):
        line = lines[idx]
        try:
            data = json.loads(line)
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                method = tc.get('method') or tc.get('ToolName') or ''
                args = tc.get('args') or tc.get('Arguments') or {}
                if 'type_text' in method or 'type_text' in json.dumps(tc):
                    print(f"Line {idx+1} (Step {data.get('step_index')}): Tool={method}, Text={args.get('text')}")
        except Exception as e:
            pass
