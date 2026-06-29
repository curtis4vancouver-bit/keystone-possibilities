import sys
import os
import json

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    if len(sys.argv) < 4:
        print("Usage: python process_completed_topic.py <domain> <topic_name> <txt_filepath>")
        sys.exit(1)
        
    domain = sys.argv[1]
    topic = sys.argv[2]
    filepath = sys.argv[3]
    
    if not os.path.exists(filepath):
        print(f"Error: Text file not found at {filepath}")
        sys.exit(1)
        
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        content = f.read().strip()
        
    if not content:
        print("Error: Extracted content is empty")
        sys.exit(1)
        
    print(f"Loaded {len(content)} characters of research for '{topic}'")
    daemon = OvernightResearchDaemon()
    
    # Save the result
    saved_path = daemon.save_research_result(domain, topic, content)
    print(f"Saved report to: {saved_path}")
    
    # Mark topic completed
    daemon.mark_topic_completed(domain, topic, success=True)
    print("Marked completed in learning_queue.json")
    
    # Trigger vector brain ingestion
    daemon.trigger_brain_ingestion()
    print("Brain ingestion complete!")

if __name__ == "__main__":
    main()
