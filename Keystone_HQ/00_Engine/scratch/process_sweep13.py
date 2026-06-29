import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

BATCH_ITEMS = [
    {
        "domain": "low_cost_branding",
        "topic": "Programmatic SEO and viral short-form video correlation for organic brand scaling",
        "output_file": os.path.join(PROJECT_ROOT, "scratch", "page33_output.json")
    },
    {
        "domain": "low_cost_branding",
        "topic": "Programmatic micro-influencer outreach and automated brand ambassador campaigns",
        "output_file": os.path.join(PROJECT_ROOT, "scratch", "page34_output.json")
    },
    {
        "domain": "low_cost_branding",
        "topic": "Automated PR pitching and local media coverage acquisition strategies",
        "output_file": os.path.join(PROJECT_ROOT, "scratch", "page35_output.json")
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
