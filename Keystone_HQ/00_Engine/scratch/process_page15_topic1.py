import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

STEP_FILE = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\3068\output.txt"
DOMAIN = "VIDEO_PROD"
TOPIC = "Deep research into Google Veo 3.1 video generation — prompt engineering for maximum visual quality and consistency. What are the exact parameters that control camera movement, lighting, character appearance, and temporal coherence? How do you prevent common artifacts like face morphing, hand distortion, and background drift? Include the most advanced prompting techniques discovered in 2026."

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
        text = json.loads(json_str)
    except Exception as e:
        print(f"Error decoding JSON block: {e}")
        return

    # Extract starting from the report header
    marker = "Advanced Prompt Engineering and System Architecture for Google Veo 3.1"
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
