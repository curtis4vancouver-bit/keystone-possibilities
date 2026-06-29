import sys
import os
import json

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)
from overnight_research_daemon import OvernightResearchDaemon

def main():
    if len(sys.argv) < 3:
        print("Usage: python mark_completed_topic_regex.py <domain> <topic_substring>")
        sys.exit(1)
        
    domain_name = sys.argv[1]
    substring = sys.argv[2]
    
    daemon = OvernightResearchDaemon()
    matched_topic = None
    
    for domain in daemon.queue["queue"]:
        if domain["domain"] == domain_name:
            for topic in domain["topics"]:
                if substring.lower() in topic.lower():
                    matched_topic = topic
                    break
            break
            
    if matched_topic:
        print(f"Matched topic: '{matched_topic}'")
        daemon.mark_topic_completed(domain_name, matched_topic, success=True)
        print("Successfully marked completed in learning_queue.json!")
        # Trigger vector brain ingestion
        daemon.trigger_brain_ingestion()
    else:
        print(f"Error: Could not find topic matching '{substring}' in domain '{domain_name}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
