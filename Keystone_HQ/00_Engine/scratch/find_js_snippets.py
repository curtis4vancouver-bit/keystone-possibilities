import os
import json

brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"

def main():
    found_snippets = []
    for item in os.listdir(brain_dir):
        item_path = os.path.join(brain_dir, item)
        if os.path.isdir(item_path):
            transcript_path = os.path.join(item_path, ".system_generated", "logs", "transcript.jsonl")
            if os.path.exists(transcript_path):
                try:
                    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            if "evaluate_script" in line and ("gemini" in line or "spark" in line):
                                data = json.loads(line)
                                step = data.get("step_index")
                                tool_calls = data.get("tool_calls", [])
                                for tc in tool_calls:
                                    name = tc.get("name")
                                    args = tc.get("args", {})
                                    if "evaluate_script" in str(tc.get("name")) or "evaluate_script" in str(args.get("ToolName")):
                                        arguments = args.get("Arguments")
                                        if isinstance(arguments, str):
                                            try:
                                                arguments = json.loads(arguments)
                                            except:
                                                pass
                                        found_snippets.append((item, step, arguments))
                                        if len(found_snippets) >= 20:
                                            break
                except:
                    pass
        if len(found_snippets) >= 20:
            break
            
    print(f"Found {len(found_snippets)} JS evaluation snippets:")
    for brain, step, args in found_snippets:
        print(f"\n================ Brain: {brain}, Step: {step} ================")
        print(json.dumps(args, indent=2))

if __name__ == "__main__":
    main()
