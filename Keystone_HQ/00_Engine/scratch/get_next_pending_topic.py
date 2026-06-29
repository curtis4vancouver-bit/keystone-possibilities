import sys
import os
import json

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    daemon = OvernightResearchDaemon()
    
    # 1. Check credit gate
    gate = daemon.should_wait_for_credits()
    if not gate.get("can_continue", True):
        print(json.dumps({
            "status": "credits_exhausted",
            "wait_seconds": gate.get("wait_seconds", 3600),
            "recommendation": gate.get("recommendation", "Wait for credit refresh")
        }))
        return

    # 2. Get currently running topics from deep_research_state.json
    running_topics = set()
    state_file = os.path.join(PROJECT_ROOT, "scratch", "deep_research_state.json")
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
                for page in state_data.get("pages", []):
                    if page.get("status") == "running" and page.get("topic"):
                        running_topics.add(page.get("topic"))
        except Exception:
            pass

    # 3. Find next pending topic not running
    next_item = None
    sorted_domains = sorted(daemon.queue["queue"], key=lambda d: d.get("priority", 99))
    
    for domain in sorted_domains:
        completed = set(domain.get("completed", []))
        for topic in domain.get("topics", []):
            if topic not in completed and topic not in running_topics:
                # Build the prompt
                prompt = daemon._build_research_prompt(domain["domain"], topic)
                next_item = {
                    "status": "success",
                    "domain": domain["domain"],
                    "topic": topic,
                    "prompt": prompt
                }
                break
        if next_item:
            break
            
    if not next_item:
        print(json.dumps({"status": "no_topics_remaining"}))
    else:
        print(json.dumps(next_item, indent=2))

if __name__ == "__main__":
    main()
