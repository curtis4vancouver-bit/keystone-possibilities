import json
import os
import sys

# Define paths
STEP_OUTPUT_PATH = r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\2047\output.txt"
PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    print(f"Loading step output from: {STEP_OUTPUT_PATH}")
    if not os.path.exists(STEP_OUTPUT_PATH):
        print("Error: Step output file does not exist!")
        return

    with open(STEP_OUTPUT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # The file starts with:
    # Script ran on page and returned:
    # ```json
    # "..."
    # ```
    # Let's extract the JSON block.
    if "```json" in content:
        parts = content.split("```json")
        json_str = parts[1].split("```")[0].strip()
    else:
        json_str = content.strip()

    try:
        # Load the JSON string (which is a string containing the text of the research)
        research_text = json.loads(json_str)
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        # Try a direct extract if it's not valid JSON
        research_text = json_str

    if not isinstance(research_text, str) or len(research_text) < 1000:
        print(f"Warning: Extracted content is not a long string (type={type(research_text)}, length={len(str(research_text))})")
        print("Checking if it's a dict...")
        if isinstance(research_text, dict):
            research_text = str(research_text)

    domain = "self_learning_patterns"
    topic = "Prompt self-optimization techniques without human intervention"

    print(f"Creating research result file for topic: '{topic}'")
    daemon = OvernightResearchDaemon()
    filepath = daemon.save_research_result(domain, topic, research_text)
    print(f"Saved to: {filepath}")

    print("Marking topic completed in learning queue...")
    daemon.mark_topic_completed(domain, topic, success=True)

    print("Triggering brain ingestion pipeline...")
    daemon.trigger_brain_ingestion()
    print("Done!")

if __name__ == "__main__":
    main()
