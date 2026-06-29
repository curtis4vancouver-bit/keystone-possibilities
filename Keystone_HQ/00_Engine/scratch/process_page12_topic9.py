import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

STEP_FILE = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\2957\output.txt"
DOMAIN = "YT_ANALYTICS"
TOPIC = "Deep research into YouTube Shorts strategy for channel growth in 2026. What is the current algorithm behavior for Shorts? How do Shorts viewers convert to long-form subscribers? What is the optimal Shorts posting frequency? How do you repurpose long-form content into Shorts effectively?"

def main():
    print(f"Loading step output from: {STEP_FILE}")
    if not os.path.exists(STEP_FILE):
        print(f"Error: Step file {STEP_FILE} does not exist!")
        return

    with open(STEP_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # The step file starts with "Script ran on page and returned:" followed by ```json
    if "```json" in content:
        parts = content.split("```json")
        json_str = parts[1].split("```")[0].strip()
    else:
        json_str = content.strip()

    try:
        obj = json.loads(json_str)
        text = obj["text"]
    except Exception as e:
        print(f"Error decoding JSON block: {e}")
        return

    # Extract starting from the report header
    marker = "Algorithmic Dynamics and Automated Content Pipelines for YouTube Shorts: A 2026 Strategic Blueprint"
    if marker in text:
        report_content = text.split(marker, 1)[1]
        report_content = marker + "\n" + report_content
    else:
        # Fallback to the whole text
        print("Warning: report marker not found, using full text.")
        report_content = text

    daemon = OvernightResearchDaemon()
    print("Saving research result...")
    filepath = daemon.save_research_result(DOMAIN, TOPIC, report_content)
    print(f"Saved to: {filepath}")

    print("Marking topic completed in learning queue...")
    daemon.mark_topic_completed(DOMAIN, TOPIC, success=True)

    print("Triggering brain ingestion pipeline...")
    daemon.trigger_brain_ingestion()
    print("Brain ingestion complete!")

if __name__ == "__main__":
    main()
