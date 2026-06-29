import os
import sys
import json

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    topic = "Research how to use the YouTube Data API v3 for competitive intelligence. What endpoints reveal the most useful data about competitor channels? How do you programmatically track upload frequency, view velocity, engagement ratios, and topic trends? Include Python code examples for building an automated competitor tracker."
    filepath = os.path.join(PROJECT_ROOT, "scratch", "page8_output.json")
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = json.load(f)
        
    if isinstance(content, str) and content.startswith('"') and content.endswith('"'):
        try:
            content = json.loads(content)
        except:
            pass
            
    daemon = OvernightResearchDaemon()
    saved_path = daemon.save_research_result("YT_ANALYTICS", topic, content)
    daemon.mark_topic_completed("YT_ANALYTICS", topic, success=True)
    print("SUCCESS:", saved_path)

if __name__ == "__main__":
    main()
