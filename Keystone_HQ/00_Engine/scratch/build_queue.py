import re
import json

md_path = r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Master_Docs\Gemini_Pro_Instructions\04_SEVENTY_NEW_RESEARCH_TOPICS.md'
queue_path = r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\learning_queue.json'

with open(md_path, 'r', encoding='utf-8') as f:
    content = f.read()

domains = {}
# Find domain tags and topics
# e.g. ### 1. 🔴 [AGENT_ARCH] Context Engram Protocol
# ```
# Deep research into ...
# ```
matches = re.finditer(r'### \d+\.\s+([🔴🟡🟢])\s+\[(.*?)\]\s+(.*?)\n```\n(.*?)\n```', content, re.DOTALL)

for match in matches:
    priority_icon = match.group(1)
    domain = match.group(2)
    topic = match.group(3).strip()
    prompt = match.group(4).strip()
    
    priority_map = {'🔴': 1, '🟡': 2, '🟢': 3}
    priority = priority_map.get(priority_icon, 3)
    
    if domain not in domains:
        domains[domain] = {
            "domain": domain,
            "priority": priority,
            "topics": [],
            "completed": [],
            "status": "pending"
        }
    
    # We just put the topic in the list, the prompt is reconstructed by the daemon
    # Wait, the daemon builds the prompt dynamically from the topic string!
    # So we just pass the full prompt as the "topic" so the daemon can use it?
    # Actually, daemon line 105: f"Activate Deep Research. Thoroughly analyze: {topic}. ..."
    # So if we put the whole text as topic, it works. Or maybe the topic is just the title.
    # Let's put the topic title + prompt in the topic string.
    full_topic = f"{topic}: {prompt}"
    domains[domain]["topics"].append(full_topic)

queue = {
    "last_updated": "",
    "queue": list(domains.values())
}

with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2)
print(f"Queue built with {sum(len(d['topics']) for d in queue['queue'])} topics across {len(domains)} domains.")
