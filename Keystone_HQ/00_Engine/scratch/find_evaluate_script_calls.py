import os
import json

path = r"C:\Users\Curtis\.gemini\antigravity\brain\dcfb044f-d157-4191-8dd4-486712240c1d\.system_generated\logs\transcript.jsonl"

def main():
    if not os.path.exists(path):
        print(f"Error: path {path} not found")
        return
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if 3800 <= step <= 3900:
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        name = tc.get("name", "")
                        args = tc.get("args", {})
                        mcp_tool = args.get("ToolName", "")
                        if "evaluate_script" in name or "evaluate_script" in mcp_tool:
                            sub_args = args.get("Arguments", {})
                            if isinstance(sub_args, str):
                                try:
                                    sub_args = json.loads(sub_args)
                                except:
                                    pass
                            js_func = sub_args.get('function', '')
                            if isinstance(js_func, str) and ("message-content" in js_func or "innerText" in js_func or "extended-response" in js_func):
                                print(f"\n================ STEP {step} ==================")
                                print(f"JS:\n{js_func}")
                            if isinstance(js_func, str):
                                print(f"JS:\n{js_func}")
                            else:
                                print(f"JS (Object):\n{json.dumps(js_func, indent=2)}")
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
