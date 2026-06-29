import json
import sys

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\logs\transcript.jsonl"
steps_to_show = [2126, 2128, 2130, 2132, 2166, 2168, 2170, 2172]

def main():
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    for line in lines:
        try:
            data = json.loads(line)
        except Exception:
            continue
            
        step_index = data.get("step_index", 0)
        if step_index in steps_to_show:
            tool_calls = data.get("tool_calls", [])
            if tool_calls:
                print(f"\n=================== Step {step_index} ===================")
                for tc in tool_calls:
                    args = tc.get("args", {})
                    # Load Arguments JSON if it is stringified JSON
                    if 'Arguments' in args:
                        try:
                            sub_args = json.loads(args['Arguments'])
                            print("Arguments:")
                            print(json.dumps(sub_args, indent=2))
                        except Exception:
                            print(f"Arguments: {args['Arguments']}")
                    else:
                        print(f"Args: {args}")

if __name__ == "__main__":
    main()
