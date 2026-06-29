import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

STEP_FILE = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\2323\output.txt"
DOMAIN = "hermes_agent_analysis"
TOPIC = "Hermes autonomous skill creation and tool discovery patterns implementation guide"

def clean_and_extract_content(filepath):
    print(f"Loading step output from: {filepath}")
    if not os.path.exists(filepath):
        print(f"Error: Step output file {filepath} does not exist!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract JSON block if present
    if "```json" in content:
        parts = content.split("```json")
        json_str = parts[1].split("```")[0].strip()
    else:
        json_str = content.strip()

    try:
        research_text = json.loads(json_str)
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        research_text = json_str

    if not isinstance(research_text, str) or len(research_text) < 1000:
        print(f"Warning: Extracted content is not a long string (type={type(research_text)}, length={len(str(research_text))})")
        if isinstance(research_text, dict):
            research_text = str(research_text)

    return research_text

def main():
    daemon = OvernightResearchDaemon()
    text = clean_and_extract_content(STEP_FILE)
    if not text:
        return

    print(f"Creating research result file for topic...")
    filepath = daemon.save_research_result(DOMAIN, TOPIC, text)
    print(f"Saved to: {filepath}")

    print("Marking topic completed in learning queue...")
    daemon.mark_topic_completed(DOMAIN, TOPIC, success=True)

    print("\nTriggering brain ingestion pipeline...")
    daemon.trigger_brain_ingestion()
    print("Brain ingestion complete!")

if __name__ == "__main__":
    main()
