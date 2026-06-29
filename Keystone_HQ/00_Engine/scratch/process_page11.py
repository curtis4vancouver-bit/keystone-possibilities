import json
import os
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

BATCH_ITEMS = [
    {
        "domain": "mcp_ecosystem",
        "topic": "MCP server security best practices and access control",
        "step_file": r"C:\Users\Curtis\.gemini\antigravity\brain\f12c78d2-72b4-40e4-afee-7564ea10b735\.system_generated\steps\2646\output.txt"
    }
]

def clean_and_extract_content(filepath):
    print(f"Loading step output from: {filepath}")
    if not os.path.exists(filepath):
        print(f"Error: Step output file {filepath} does not exist!")
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # The MCP output might be JSON-encoded string
    if content.strip().startswith('"') and content.strip().endswith('"'):
        try:
            research_text = json.loads(content.strip())
        except Exception as e:
            print(f"JSON decode failed for raw string: {e}")
            research_text = content.strip()
    else:
        # Check for ```json block
        if "```json" in content:
            parts = content.split("```json")
            json_str = parts[1].split("```")[0].strip()
        else:
            json_str = content.strip()

        try:
            research_text = json.loads(json_str)
        except Exception as e:
            print(f"Error decoding JSON block: {e}")
            research_text = json_str

    if not isinstance(research_text, str) or len(research_text) < 1000:
        print(f"Warning: Extracted content length={len(str(research_text))}")
        if isinstance(research_text, dict):
            research_text = str(research_text)

    return research_text

def main():
    daemon = OvernightResearchDaemon()
    processed_any = False

    for item in BATCH_ITEMS:
        print("\n--------------------------------------------------")
        print(f"Processing Topic: '{item['topic']}'")
        text = clean_and_extract_content(item["step_file"])
        if not text:
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
