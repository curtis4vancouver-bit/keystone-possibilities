import sys
import json
import os
sys.path.append('.')
from overnight_research_daemon import OvernightResearchDaemon

text_path = r'C:\Users\Curtis\.gemini\antigravity\brain\f7b9d3bf-f8d4-443c-86d7-3188680ad43f\.system_generated\steps\395\output.txt'
with open(text_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('"') and text.endswith('"'):
    try:
        text = json.loads(text)
    except:
        pass

domain = 'AGENT_ARCH'
topic = 'PreToolUse Hook Security Patterns: Deep research into PreToolUse and PostToolUse lifecycle hooks for AI agents in 2026. How to implement synchronous tool-call interception that blocks dangerous commands, mutates tool arguments for safety (e.g., injecting --dry-run), and logs all tool executions for audit trails. Include implementation specs for Claude Code hooks, Antigravity SDK hooks, and ADK 2.0 hooks. Focus on patterns that prevent prompt injection attacks via tool arguments.'

daemon = OvernightResearchDaemon()
filepath = daemon.save_research_result(domain, topic, text)
daemon.mark_topic_completed(domain, topic, success=True)
daemon.trigger_brain_ingestion()
print('Done Topic 2. Saved to:', filepath)
