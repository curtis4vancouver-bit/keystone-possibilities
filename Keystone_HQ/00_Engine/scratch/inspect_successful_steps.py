import json

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\d1671347-49b6-43c0-852f-31e4bb435851\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            step = json.loads(line)
            step_idx = step.get("step_index")
            if step_idx is not None and 373 <= step_idx <= 537:
                source = step.get("source", "")
                stype = step.get("type", "")
                status = step.get("status", "")
                content = step.get("content", "")
                tool_calls = step.get("tool_calls", [])
                
                # Print only relevant MCP calls
                if tool_calls:
                    for tc in tool_calls:
                        name = tc.get("name")
                        args = str(tc.get("args"))
                        if name in ["click", "type_text", "call_mcp_tool"]:
                            print(f"Step {step_idx}: {name} | {args}")
        except Exception as e:
            pass
