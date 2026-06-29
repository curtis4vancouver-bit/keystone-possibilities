import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

STEP_FILE = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\3493\output.txt"
DOMAIN = "VIDEO_PROD"
TOPIC = "Deep research into Google Flow batch processing and automation. What are the API endpoints for programmatic video generation? How do you queue 70+ prompts without manual intervention? What are the rate limits, credit costs, and concurrent job limits? Is there an official API or is browser automation the only option?"

def main():
    print(f"Loading step output from: {STEP_FILE}")
    if not os.path.exists(STEP_FILE):
        print(f"Error: Step file {STEP_FILE} does not exist!")
        return

    with open(STEP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract JSON string
    if "```json" in content:
        parts = content.split("```json")
        json_str = parts[1].split("```")[0].strip()
    else:
        json_str = content.strip()

    try:
        text = json.loads(json_str)
    except Exception as e:
        # Try direct decode if it failed
        try:
            text = json.loads('"' + json_str + '"')
        except Exception as e2:
            print(f"Error decoding JSON block: {e}, backup: {e2}")
            return

    daemon = OvernightResearchDaemon()
    print("Saving research result...")
    filepath = daemon.save_research_result(DOMAIN, TOPIC, text)
    print(f"Saved to: {filepath}")

    print("Marking topic completed in learning queue...")
    daemon.mark_topic_completed(DOMAIN, TOPIC, success=True)

    print("Triggering brain ingestion pipeline...")
    daemon.trigger_brain_ingestion()
    print("Brain ingestion complete!")

if __name__ == "__main__":
    main()
