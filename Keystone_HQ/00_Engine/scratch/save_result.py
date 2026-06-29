import sys
import json
import os
sys.path.append('.')
from overnight_research_daemon import OvernightResearchDaemon

text_path = r'C:\Users\Curtis\.gemini\antigravity\brain\f7b9d3bf-f8d4-443c-86d7-3188680ad43f\.system_generated\steps\308\output.txt'
with open(text_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text.startswith('"') and text.endswith('"'):
    try:
        text = json.loads(text)
    except:
        pass

domain = 'AGENT_ARCH'
topic = 'Context Engram Protocol: Deep research into "Context Engrams" for AI agent memory management. How do frameworks like Antigravity SDK, LangGraph, and CrewAI implement persistent memory that survives across conversation sessions without context window overflow? Include implementation patterns for mem_save() and mem_search() functions, compression algorithms for long-term storage, and strategies for preventing memory staleness. Focus on 2026 best practices.'

daemon = OvernightResearchDaemon()
filepath = daemon.save_research_result(domain, topic, text)
daemon.mark_topic_completed(domain, topic, success=True)
daemon.trigger_brain_ingestion()
print('Done. Saved to:', filepath)
