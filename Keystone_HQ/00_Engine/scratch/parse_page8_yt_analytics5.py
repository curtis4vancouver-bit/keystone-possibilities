import os
import sys
import json

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    topic = "Deep research into YouTube channel growth strategies that work in 2026. What changed with the algorithm? How important is watch time vs. engagement vs. subscriber velocity? What posting frequency is optimal? How do Shorts feed into long-form growth? Include case studies of channels that grew from 0 to 100K in 12 months."
    filepath = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd\.system_generated\steps\2655\output.txt"
    
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()
        
    # Extract the JSON block
    # The file starts with "Script ran on page and returned:\n```json\n" and ends with "\n```"
    start_idx = raw.find('```json\n')
    if start_idx != -1:
        json_str = raw[start_idx + 8:]
        end_idx = json_str.rfind('\n```')
        if end_idx != -1:
            json_str = json_str[:end_idx]
    else:
        json_str = raw
        
    try:
        content = json.loads(json_str)
    except Exception as e:
        print("Failed to parse JSON directly, trying standard string conversion")
        json_str_clean = json_str.strip()
        if json_str_clean.startswith('"') and json_str_clean.endswith('"'):
            content = json.loads(json_str_clean)
        else:
            content = json_str_clean

    daemon = OvernightResearchDaemon()
    saved_path = daemon.save_research_result("YT_ANALYTICS", topic, content)
    daemon.mark_topic_completed("YT_ANALYTICS", topic, success=True)
    daemon.trigger_brain_ingestion()
    print("SUCCESS:", saved_path)

if __name__ == "__main__":
    main()
