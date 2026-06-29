import os
import sys
import json

# Add project root to path
PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

# Paths
brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain\55ece092-8436-4c83-924a-2121703c17bd"
output_path = os.path.join(brain_dir, ".system_generated", "steps", "1799", "output.txt")

with open(output_path, "r", encoding="utf-8") as f:
    text = f.read()

# Find the json block if it exists, otherwise use the whole text
start_marker = "```json"
end_marker = "```"

start_idx = text.find(start_marker)
if start_idx != -1:
    content_str = text[start_idx + len(start_marker):]
    end_idx = content_str.rfind(end_marker)
    if end_idx != -1:
        content_str = content_str[:end_idx]
    
    # Clean up and load the JSON string
    json_val = content_str.strip()
    try:
        content = json.loads(json_val)
    except Exception as e:
        print(f"Warning: could not parse json from block: {e}")
        content = json_val
else:
    content = text

# Strip JSON double-quotes if it parsed as a string containing double-quotes
if isinstance(content, str) and content.startswith('"') and content.endswith('"'):
    try:
        content = json.loads(content)
    except:
        pass

daemon = OvernightResearchDaemon()
domain = "YOUTUBE_SCRIPTS"
topic = "Research the top 10 highest-performing health and wellness YouTube channels (Dr. Eric Berg, Thomas DeLauer, Andrew Huberman, etc.) and analyze their exact script structure. How do they open? What is their hook-to-content ratio? How do they handle transitions between topics? What is their words-per-minute delivery rate? What makes viewers stay for 8+ minutes?"

filepath = daemon.save_research_result(domain, topic, content)
daemon.mark_topic_completed(domain, topic, success=True)
print(f"SUCCESS: Saved to {filepath}")
