import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

BATCH_ITEMS = [
    {
        "domain": "chrome_automation",
        "topic": "Browser tab lifecycle management for long-running automation",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3146\output.txt"
    },
    {
        "domain": "social_media_automation",
        "topic": "TikTok Content Posting API v2 direct publish flow complete guide 2026",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3152\output.txt"
    },
    {
        "domain": "social_media_automation",
        "topic": "Facebook Reels publishing via Graph API video upload from URL",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\3166\output.txt"
    }
]

def clean_and_extract_content(filepath):
    print(f"Loading step output from: {filepath}")
    if not os.path.exists(filepath):
        print(f"Error: Step output file {filepath} does not exist!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # The MCP output is JSON-encoded string or text containing json blocks
    content_stripped = content.strip()
    if content_stripped.startswith('"') and content_stripped.endswith('"'):
        try:
            research_text = json.loads(content_stripped)
        except Exception as e:
            print(f"JSON decode failed for raw string: {e}")
            research_text = content_stripped
    else:
        # Check for ```json block
        if "```json" in content:
            parts = content.split("```json")
            json_str = parts[1].split("```")[0].strip()
        else:
            json_str = content_stripped

        try:
            research_text = json.loads(json_str)
        except Exception as e:
            print(f"Error decoding JSON block: {e}")
            # Try to strip lead-in or lead-out if it says "Script ran on page and returned:"
            if "Script ran on page and returned:\n```json\n" in json_str:
                json_str = json_str.replace("Script ran on page and returned:\n```json\n", "")
                if json_str.endswith("\n```"):
                    json_str = json_str[:-4]
                try:
                    research_text = json.loads(json_str)
                except Exception as ex:
                    print(f"Second decode attempt failed: {ex}")
                    research_text = json_str
            else:
                research_text = json_str

    if not isinstance(research_text, str) or len(research_text) < 1000:
        print(f"Warning: Extracted content length={len(str(research_text))}")
        if isinstance(research_text, dict):
            research_text = str(research_text)

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
