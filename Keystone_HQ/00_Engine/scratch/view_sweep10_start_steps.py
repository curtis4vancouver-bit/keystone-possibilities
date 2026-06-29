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
                if 3620 <= step <= 3730:
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        name = tc.get("name")
                        args = tc.get("args", {})
                        if name == "call_mcp_tool":
                            sub_args = args.get("Arguments", {})
                            print(f"Step {step}: call_mcp_tool Server={args.get('ServerName')}, Tool={args.get('ToolName')}")
                            if isinstance(sub_args, str):
                                try:
                                    sub_args = json.loads(sub_args)
                                except:
                                    pass
                            print(f"  Args: {str(sub_args)[:500]}")
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
