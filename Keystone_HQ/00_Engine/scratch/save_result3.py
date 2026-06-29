import sys
import json
import os
sys.path.append('.')
from overnight_research_daemon import OvernightResearchDaemon

text_path = r'C:\Users\Curtis\.gemini\antigravity\brain\f7b9d3bf-f8d4-443c-86d7-3188680ad43f\.system_generated\steps\423\output.txt'
with open(text_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('"') and text.endswith('"'):
    try:
        text = json.loads(text)
    except:
        pass

domain = 'AGENT_ARCH'
topic = 'Circuit Breaker Patterns for Autonomous Agents: Deep research into circuit breaker algorithms for autonomous AI agents. How to detect infinite loops, no-progress states, and repeated error fingerprints in long-running agent tasks. Include the three diagnostic heuristics: No-Progress Trigger, Same-Error Fingerprint (hash-based), and Token Decline Metric. Compare implementations in LangGraph, ADK 2.0, and the-architect system. Include code examples for Python.'

daemon = OvernightResearchDaemon()
filepath = daemon.save_research_result(domain, topic, text)
daemon.mark_topic_completed(domain, topic, success=True)
daemon.trigger_brain_ingestion()

# Now close the sweep
daemon.record_prompts_used(3)
credit_check = daemon.should_wait_for_credits()

print('Done Topic 3. Saved to:', filepath)
print('Credit Check:', json.dumps(credit_check))
