import os
import sys
import json

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    topic = "Research YouTube script pacing for different content formats: 60-second Shorts, 3-minute explainers, 8-minute deep dives, 30-minute full albums. What is the optimal words-per-minute for each format? How does pacing change between talking-head, interview, and B-roll heavy content?"
    filepath = os.path.join(PROJECT_ROOT, "scratch", "page9_output.json")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = json.load(f)
        
    if isinstance(content, str) and content.startswith('"') and content.endswith('"'):
        try:
            content = json.loads(content)
        except:
            pass
            
    daemon = OvernightResearchDaemon()
    saved_path = daemon.save_research_result("YOUTUBE_SCRIPTS", topic, content)
    daemon.mark_topic_completed("YOUTUBE_SCRIPTS", topic, success=True)
    print("SUCCESS:", saved_path)

if __name__ == "__main__":
    main()
