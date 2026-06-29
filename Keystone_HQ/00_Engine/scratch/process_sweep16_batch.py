import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

BATCH_ITEMS = [
    {
        "domain": "VIDEO_PROD",
        "topic": "Deep research into color grading workflows for AI-generated video content in DaVinci Resolve. How do you create a consistent visual look across 24+ AI-generated clips that may have slightly different lighting and color? What LUTs, color matching tools, and grading techniques work best?",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\5229\output.txt"
    },
    {
        "domain": "VIDEO_PROD",
        "topic": "Research the legal and copyright status of AI-generated video content in 2026. What are the current regulations around AI-generated content on YouTube? Do AI videos need disclosure labels? What are the monetization policies? How does this differ between US, Canada, and EU?",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\5235\output.txt"
    },
    {
        "domain": "VIDEO_PROD",
        "topic": "Deep research into 9:16 vertical video production best practices for YouTube Shorts, TikTok, and Instagram Reels. What are the optimal frame compositions, text safe zones, and attention hotspots for vertical content? How should AI-generated vertical content differ from horizontal?",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\5223\output.txt"
    }
]

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
    processed_any = False

    for item in BATCH_ITEMS:
        print("\n--------------------------------------------------")
        print(f"Processing Topic: '{item['topic'][:80]}...'")
        text = clean_and_extract_content(item["step_file"])
        if not text:
            continue

        print(f"Creating research result file for topic...")
        filepath = daemon.save_research_result(item["domain"], item["topic"], text)
        print(f"Saved to: {filepath}")

        print("Marking topic completed in learning queue...")
        daemon.mark_topic_completed(item["domain"], item["topic"], success=True)
        processed_any = True

    if processed_any:
        print("\nTriggering brain ingestion pipeline...")
        daemon.trigger_brain_ingestion()
        print("Brain ingestion complete!")
    else:
        print("No items were processed.")

if __name__ == "__main__":
    main()
