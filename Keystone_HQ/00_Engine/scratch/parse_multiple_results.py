import os
import sys
import json

# Add project root to path
PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def parse_and_save(file_path, domain, topic):
    print(f"\nProcessing {file_path}...")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
        
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            content = json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            # Fallback to reading file directly
            f.seek(0)
            content = f.read()

    # If it loaded as a string, check if it starts and ends with double quotes
    if isinstance(content, str) and content.startswith('"') and content.endswith('"'):
        try:
            content = json.loads(content)
        except:
            pass

    daemon = OvernightResearchDaemon()
    filepath = daemon.save_research_result(domain, topic, content)
    daemon.mark_topic_completed(domain, topic, success=True)
    print(f"SUCCESS: Saved to {filepath}")
    return True

if __name__ == "__main__":
    # Page 7: Topic 3
    topic3 = "Deep research into conversational interview-style YouTube scripts. How do channels like Joe Rogan, Lex Fridman, and Steven Bartlett create natural-sounding back-and-forth dialogue? What is the ratio of questions to answers? How do they script vs. improvise? How can an AI write dialogue that sounds like two people genuinely talking?"
    parse_and_save(
        os.path.join(PROJECT_ROOT, "scratch", "page7_output.json"),
        "YOUTUBE_SCRIPTS",
        topic3
    )

    # Page 8: Topic 4
    topic4 = "Research how to write YouTube scripts that pass AI detection. What specific writing patterns trigger AI detectors? How do professional ghostwriters for YouTubers make AI-assisted scripts undetectable? What vocabulary, sentence variation, and structural techniques create genuinely human-sounding content?"
    parse_and_save(
        os.path.join(PROJECT_ROOT, "scratch", "page8_output.json"),
        "YOUTUBE_SCRIPTS",
        topic4
    )
