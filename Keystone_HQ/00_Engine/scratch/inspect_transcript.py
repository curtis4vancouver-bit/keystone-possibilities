import json

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\d1671347-49b6-43c0-852f-31e4bb435851\.system_generated\logs\transcript.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        try:
            step = json.loads(line)
            step_idx = step.get("step_index")
            if step_idx == 961:
                print(f"Step {step_idx} status: {step.get('status')}")
                print(f"Content: {step.get('content')}")
        except Exception as e:
            pass
