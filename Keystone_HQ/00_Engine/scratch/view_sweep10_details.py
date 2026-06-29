import json
import os

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\logs\transcript.jsonl"

def main():
    if not os.path.exists(transcript_path):
        print("Transcript not found")
        return
        
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if step in [3675, 3677, 3729]:
                    print(f"\n=================== Step {step} ===================")
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        args = tc.get("args", {})
                        sub_args = args.get("Arguments", {})
                        if isinstance(sub_args, str):
                            sub_args = json.loads(sub_args)
                        print(f"ServerName: {args.get('ServerName')}")
                        print(f"ToolName: {args.get('ToolName')}")
                        print("Arguments:")
                        print(json.dumps(sub_args, indent=2))
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
