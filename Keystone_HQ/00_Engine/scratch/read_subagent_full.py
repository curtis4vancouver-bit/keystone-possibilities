import json
import os

path = r"C:\Users\Curtis\.gemini\antigravity\brain\231c6914-89c5-4c61-99bf-e20300ea490f\.system_generated\logs\transcript.jsonl"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    found = False
    for line in reversed(lines):
        try:
            d = json.loads(line)
            if "tool_calls" in d:
                for tc in d["tool_calls"]:
                    if tc.get("name") == "send_message":
                        msg = tc["args"].get("Message", "")
                        if "COMPREHENSIVE WEBSITE" in msg:
                            print(f"Found report in send_message! Length: {len(msg)}")
                            with open("scratch/subagent_full_report.txt", "w", encoding="utf-8") as out:
                                out.write(msg)
                            print("Wrote full report to scratch/subagent_full_report.txt")
                            found = True
                            break
                if found:
                    break
        except Exception as e:
            pass
    if not found:
        print("Could not find report content in tool_calls.")
else:
    print("Transcript not found.")
