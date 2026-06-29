import os
import json

path = r"C:\Users\Curtis\.gemini\antigravity\brain\dcfb044f-d157-4191-8dd4-486712240c1d\.system_generated\logs\transcript.jsonl"
calls = []
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if data.get("tool_calls"):
                    for tc in data["tool_calls"]:
                        if tc.get("name") == "call_mcp_tool":
                            args = tc.get("args", {})
                            sname = args.get("ServerName", "")
                            tname = args.get("ToolName", "")
                            if "chrome-devtools-mcp" in sname or "playwright" in sname:
                                calls.append((step, tname, args.get("Arguments")))
            except Exception as e:
                pass

for c in calls:
    if 3270 <= c[0] <= 3315:
        print(f"Step {c[0]}: Tool={c[1]} | Args={c[2]}")
