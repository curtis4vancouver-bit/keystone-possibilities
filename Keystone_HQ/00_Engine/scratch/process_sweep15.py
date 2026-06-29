import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

BATCH_ITEMS = [
    {
        "domain": "youtube_algorithm",
        "topic": "YouTube algorithm changes May 2026 and optimization strategies",
        "output_file": os.path.join(PROJECT_ROOT, "scratch", "page39_output.json")
    },
    {
        "domain": "youtube_algorithm",
        "topic": "Viral hook patterns analysis for health and construction content",
        "output_file": os.path.join(PROJECT_ROOT, "scratch", "page40_output.json")
    },
    {
        "domain": "youtube_algorithm",
        "topic": "YouTube Shorts vs long-form strategy for channel growth 2026",
        "output_file": os.path.join(PROJECT_ROOT, "scratch", "page41_output.json")
    }
]

def clean_and_extract_content(filepath):
    print(f"Loading output from: {filepath}")
    if not os.path.exists(filepath):
        print(f"Error: Output file {filepath} does not exist!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error loading JSON from {filepath}: {e}")
            return None

    research_text = data.get("reportFull", "")
    if not research_text:
        print(f"Warning: reportFull key not found or empty in JSON at {filepath}.")
        return None

    if isinstance(research_text, str):
        if research_text.startswith("```markdown\n"):
            research_text = research_text[len("```markdown\n"):]
        if research_text.endswith("\n```"):
            research_text = research_text[:-4]
        elif research_text.endswith("```"):
            research_text = research_text[:-3]

    return research_text

def main():
    daemon = OvernightResearchDaemon()
    processed_any = False

    for item in BATCH_ITEMS:
        print("\n--------------------------------------------------")
        print(f"Processing Topic: '{item['topic']}'")
        text = clean_and_extract_content(item["output_file"])
        if not text:
            print("Error: Could not extract content for topic.")
            continue

        print(f"Extracted content length: {len(text)}")
        print(f"Saving research result...")
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
