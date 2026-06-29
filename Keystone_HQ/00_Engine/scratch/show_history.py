import json
import sys

# Force UTF-8 output
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

log_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\logs\transcript.jsonl"

def main():
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Failed to read file: {e}")
        return

    print(f"Total lines in transcript: {len(lines)}")
    for line in lines:
        try:
            data = json.loads(line)
        except Exception:
            continue
            
        step_index = data.get("step_index", 0)
        if 2950 <= step_index <= 3010:
            tool_calls = data.get("tool_calls", [])
            content = data.get("content", "")
            if tool_calls:
                print(f"\n--- Step {step_index} ---")
                if content:
                    print(f"Content: {content[:300]}...")
                for tc in tool_calls:
                    print(f"  Tool: {tc.get('name')}")
                    args = tc.get("args", {})
                    if 'Arguments' in args:
                        try:
                            sub_args = json.loads(args['Arguments'])
                            print("    Arguments:")
                            print(json.dumps(sub_args, indent=2, ensure_ascii=False))
                        except Exception:
                            print(f"    Arguments: {args['Arguments']}")
                    else:
                        print(f"    Args: {args}")

if __name__ == "__main__":
    main()
