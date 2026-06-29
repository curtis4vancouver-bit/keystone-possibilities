import json

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\logs\transcript.jsonl"

def main():
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "insertText" in line and '"ToolName":"\\\"evaluate_script\\\""' in line:
                data = json.loads(line)
                print(f"\n=================== Step {data.get('step_index')} ===================")
                tool_calls = data.get("tool_calls", [])
                for tc in tool_calls:
                    args = tc.get("args", {})
                    if 'Arguments' in args:
                        try:
                            sub_args = json.loads(args['Arguments'])
                            print("JS function:")
                            print(sub_args.get("function"))
                        except Exception:
                            print(args['Arguments'])

if __name__ == "__main__":
    main()
