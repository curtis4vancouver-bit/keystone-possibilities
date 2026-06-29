import json
import os

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\e0c6e90d-f4d6-474b-9f6a-fbe1416672e1\.system_generated\logs\transcript.jsonl"

if not os.path.exists(transcript_path):
    print(f"File not found: {transcript_path}")
    exit(1)

print("Searching transcript.jsonl lines 400 to 1200...")
matches = []
with open(transcript_path, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i < 400:
            continue
        if i > 1200:
            break
        try:
            data = json.loads(line)
            tool_calls = data.get("tool_calls", [])
            for tc in tool_calls:
                method = tc.get("method") or tc.get("ToolName") or ""
                args = tc.get("args") or tc.get("Arguments") or {}
                args_str = json.dumps(args)
                if "new_page" in args_str or "select_page" in args_str or "click" in args_str or "type_text" in args_str:
                    matches.append((i+1, method, args_str))
        except Exception as e:
            pass

for m in matches[:40]:
    print(f"Line {m[0]}: Tool={m[1]}, Args={m[2][:400]}")
