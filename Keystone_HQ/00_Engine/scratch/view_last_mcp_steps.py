import json
import os
import sys

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\logs\transcript.jsonl"

def main():
    if not os.path.exists(transcript_path):
        print(f"Transcript not found at {transcript_path}")
        return

    mcp_calls = []
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                tool_calls = data.get("tool_calls", [])
                
                for tc in tool_calls:
                    name = tc.get("name")
                    if name == "call_mcp_tool" or name == "evaluate_script" or "chrome" in str(name):
                        args = tc.get("args", {})
                        arguments = args.get("Arguments", "")
                        if isinstance(arguments, str):
                            try:
                                arguments = json.loads(arguments)
                            except:
                                pass
                        
                        tool_name = args.get("ToolName", "").replace('"', '')
                        js_func = ""
                        if isinstance(arguments, dict):
                            js_func = arguments.get("function", "")
                        
                        # Look for "Start research" or extraction/done checks
                        if "start" in js_func.lower() or "share" in js_func.lower() or "export" in js_func.lower() or "reportfull" in js_func.lower() or "message-content" in js_func.lower():
                            mcp_calls.append((step, tool_name, arguments))
            except Exception as e:
                pass

    print(f"Found {len(mcp_calls)} matching Deep Research / Upload calls in history.")
    for step, name, args in mcp_calls[-20:]:
        print(f"\n=================== STEP {step} ===================")
        print(f"Tool: {name}")
        print(json.dumps(args, indent=2))

if __name__ == "__main__":
    main()
