import json
import os
import sys

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\logs\transcript.jsonl"

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.exists(transcript_path):
        print("Transcript not found")
        return
        
    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                data = json.loads(line)
                step = data.get("step_index")
                if 3715 <= step <= 3856:
                    source = data.get("source")
                    type_ = data.get("type")
                    print(f"\n--- STEP {step} | Source: {source} | Type: {type_} ---")
                    content = data.get("content")
                    if content:
                        print(f"Content: {content[:800].encode('utf-8', errors='replace').decode('utf-8')}")
                    if "tool_calls" in data:
                        print("Tool Calls:")
                        for tc in data["tool_calls"]:
                            print(f"  Name: {tc.get('name')}")
                            print(f"  Args: {str(tc.get('args'))[:400]}")
            except Exception as e:
                pass

if __name__ == "__main__":
    main()
