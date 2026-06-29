import json
import os

brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"
brain_id = "69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf"
transcript_path = os.path.join(brain_dir, brain_id, ".system_generated", "logs", "transcript.jsonl")

def main():
    if not os.path.exists(transcript_path):
        print("Transcript not found")
        return
        
    write_step = None
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if "page24_output.json" in line and "write_to_file" in line:
                data = json.loads(line)
                write_step = data.get("step_index")
                break
                
    if write_step is None:
        print("Could not find the write step")
        return
        
    print(f"Found write step at {write_step}. Dumping steps {write_step - 5} to {write_step}...")
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if write_step - 5 <= step <= write_step:
                    print(f"\n=================== Step {step} ===================")
                    print(f"Type: {data.get('type')}, Source: {data.get('source')}")
                    tool_calls = data.get("tool_calls", [])
                    for tc in tool_calls:
                        name = tc.get("name")
                        print(f"  Tool: {name}")
                        args = tc.get("args", {})
                        # Print args in full detail
                        print(f"  Args: {json.dumps(args, indent=2)}")
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
