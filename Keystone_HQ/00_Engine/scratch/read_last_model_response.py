import json
import os
import sys

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\logs\transcript.jsonl"

def main():
    # Force standard output to use utf-8
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.exists(transcript_path):
        print("Transcript not found")
        return
        
    responses = []
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("source") == "MODEL" and data.get("type") == "PLANNER_RESPONSE":
                    content = data.get("content")
                    if content and not content.strip().startswith("I will"):
                        responses.append((data.get("step_index"), content))
            except Exception as e:
                pass
                
    print(f"Total responses found: {len(responses)}")
    for idx, (step, content) in enumerate(responses[-5:]):
        print(f"\n--- RESPONSE (Step {step}) ---")
        # print with error handling
        print(content[:1500].encode('utf-8', errors='replace').decode('utf-8'))

if __name__ == "__main__":
    main()
