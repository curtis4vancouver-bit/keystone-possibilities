import os
import json

brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"

def main():
    found_steps = []
    for item in os.listdir(brain_dir):
        item_path = os.path.join(brain_dir, item)
        if os.path.isdir(item_path):
            transcript_path = os.path.join(item_path, ".system_generated", "logs", "transcript.jsonl")
            if os.path.exists(transcript_path):
                try:
                    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            if "page24_output.json" in line and "write_to_file" in line:
                                data = json.loads(line)
                                step = data.get("step_index")
                                found_steps.append((item, step))
                                break
                except:
                    pass
            
    print(f"Found page24_output.json in write_to_file in brains:")
    for brain, step in found_steps:
        print(f"Brain: {brain}, Step: {step}")
        t_path = os.path.join(brain_dir, brain, ".system_generated", "logs", "transcript.jsonl")
        with open(t_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    s = data.get("step_index")
                    if step == s:
                        print(f"  Step {s}: Source={data.get('source')}, Type={data.get('type')}")
                        if "tool_calls" in data:
                            for tc in data["tool_calls"]:
                                print(f"    Tool: {tc.get('name')}")
                                print(f"    Args: {str(tc.get('args'))[:500]}")
                except:
                    pass

if __name__ == "__main__":
    main()
