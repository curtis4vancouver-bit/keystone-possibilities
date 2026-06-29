import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

BATCH_ITEMS = [
    {
        "domain": "gemini_platform",
        "topic": "Google Spark agent platform capabilities and access methods",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3514\output.txt"
    },
    {
        "domain": "gemini_platform",
        "topic": "Gemini API vs Antigravity vs Chrome deep research comparison",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3602\output.txt"
    },
    {
        "domain": "gemini_platform",
        "topic": "Vertex AI Agent Garden for custom agent deployment",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3524\output.txt"
    }
]

def clean_and_extract_content(filepath):
    print(f"Loading step output from: {filepath}")
    if not os.path.exists(filepath):
        print(f"Error: Step output file {filepath} does not exist!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    content_stripped = content.strip()
    if "Script ran on page and returned:\n" in content_stripped:
        content_stripped = content_stripped.replace("Script ran on page and returned:\n", "")
    
    # Remove code fences
    if content_stripped.startswith("```json"):
        content_stripped = content_stripped.replace("```json", "", 1)
        if content_stripped.endswith("```"):
            content_stripped = content_stripped[:-3]
    content_stripped = content_stripped.strip()

    try:
        research_data = json.loads(content_stripped)
    except Exception as e:
        print(f"Error decoding JSON content: {e}")
        return None

    if isinstance(research_data, dict):
        research_text = research_data.get("reportFull", research_data.get("reportText", ""))
        if not research_text:
            print("Warning: reportFull or reportText key not found in JSON data dictionary.")
            research_text = str(research_data)
    else:
        research_text = research_data

    # Clean off markdown code block prefix/suffix if present inside the text itself
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
        text = clean_and_extract_content(item["step_file"])
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
