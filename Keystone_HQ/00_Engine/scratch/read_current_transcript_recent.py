import json
import os

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\logs\transcript.jsonl"

def main():
    if not os.path.exists(transcript_path):
        print(f"Transcript not found at: {transcript_path}")
        return
        
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                if data.get("type") == "USER_INPUT":
                    step = data.get("step_index")
                    content = data.get("content")
                    print(f"Step {step} | User Input: {content}")
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
