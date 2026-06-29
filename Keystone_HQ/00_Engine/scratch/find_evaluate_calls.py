import json
import os

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\06ca4b70-926e-4492-be53-382883740599\.system_generated\logs\transcript.jsonl"

def main():
    if not os.path.exists(transcript_path):
        print("Transcript not found")
        return
        
    mcp_calls = []
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if 3400 <= step <= 3800:
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        name = tc.get("name")
                        if name == "call_mcp_tool":
                            args = tc.get("args", {})
                            mcp_calls.append((step, args.get("ToolName"), args.get("Arguments")))
            except Exception as e:
                pass
                
    print(f"Found {len(mcp_calls)} chrome calls in step range 3400-3800.")
    for step, tool, arguments in mcp_calls[:30]:
        print(f"Step {step}: Tool={tool}")
        print(f"  Args: {str(arguments)[:200]}")

if __name__ == "__main__":
    main()
