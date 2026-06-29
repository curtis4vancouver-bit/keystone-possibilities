import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

q = json.load(open('learning_queue.json', 'r', encoding='utf-8'))

# All completed topics through Waves 1-3 + partial Wave 4
completed_topics = [
    # Wave 1
    ("hermes_agent_analysis", "Hermes AI agent 2026 complete architecture breakdown features and capabilities"),
    ("hermes_agent_analysis", "Hermes vs Antigravity feature comparison what does Hermes do that we cannot"),
    ("self_correction_tonight", "TikTok Content Posting API v2 complete scope reference video.publish vs video.upload 2026"),
    ("self_correction_tonight", "Instagram Reels publishing API video cover frame thumb_offset and cover_url parameters"),
    ("mcp_ecosystem", "Latest MCP servers released on npm and PyPI May 2026"),
    # Wave 2
    ("mcp_ecosystem", "Most useful MCP servers for business automation and productivity"),
    ("self_learning_patterns", "Error-driven learning loops and correction journal best practices"),
    ("self_correction_tonight", "Automated social media token rotation and expiry monitoring for multi-brand architectures"),
    ("hermes_agent_analysis", "Building a better self-learning agent system than Hermes from scratch"),
    ("self_learning_patterns", "Autonomous skill creation patterns for AI agents"),
    # Wave 3
    ("vector_brain_optimization", "Embedding model comparison: MiniLM-L6-v2 vs newer alternatives 2026"),
    ("self_learning_patterns", "Mock test generation for AI agent self-evaluation"),
    ("chrome_automation", "Chrome DevTools Protocol advanced automation patterns"),
    ("vector_brain_optimization", "Optimal embedding chunk size and overlap for technical markdown documents"),
    ("mcp_ecosystem", "Building custom FastMCP servers in Python advanced patterns"),
    # Wave 4
    ("vector_brain_optimization", "Vector similarity search threshold tuning to eliminate hallucination matches"),
    ("vector_brain_optimization", "Incremental ingestion without wiping existing knowledge"),
    ("chrome_automation", "Google Deep Research API or automation integration methods"),
    ("gemini_platform", "Gemini 3.1 release timeline features and integration guide"),
    ("davinci_resolve", "DaVinci Resolve 19 Python API complete function reference"),
    # Wave 5 (Direct main-chat research runs)
    ("hermes_agent_analysis", "Hermes MEMORY.md self-evolution and DSPy GEPA pipeline deep technical analysis"),
    ("antigravity_skills_discovery", "Best Antigravity skills and plugins available May 2026 community directory"),
    ("davinci_resolve", "Automated timeline assembly from script chunks with Python"),
    ("low_cost_branding", "How to make a construction and health brand mainstream with low budget organic growth"),
    ("shopify_audiobook_marketing", "How to sell and deliver audiobooks via Shopify with high-conversion landing pages"),
    ("antigravity_skills_discovery", "Custom Antigravity skill creation advanced patterns and multi-file skills"),
    ("self_correction_tonight", "YouTube Data API v3 channel switching best practices and OAuth consent screen hardening"),
    ("antigravity_skills_discovery", "Building autonomous overnight agent loops with schedule and cron in Antigravity"),
    ("bc_construction_law", "WorkSafeBC contractor obligations and penalty schedules"),
]

for domain_name, topic in completed_topics:
    for d in q['queue']:
        if d['domain'] == domain_name:
            if topic not in d.get('completed', []):
                d.setdefault('completed', []).append(topic)
            # Check if all topics done
            if len(d.get('completed', [])) >= len(d.get('topics', [])):
                d['status'] = 'completed'
            break

q['completed_topics'] = sum(len(x.get('completed', [])) for x in q['queue'])
q['last_updated'] = '2026-05-22T06:12:00'

json.dump(q, open('learning_queue.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

# Print status summary
print(f"Total completed: {q['completed_topics']}/{q['total_topics']}")
for d in sorted(q['queue'], key=lambda x: x.get('priority', 99)):
    done = len(d.get('completed', []))
    total = len(d.get('topics', []))
    pct = (done / max(total, 1)) * 100
    marker = " [DONE]" if d.get('status') == 'completed' else ""
    print(f"  [{d['priority']}] {d['domain']}: {done}/{total} ({pct:.0f}%){marker}")
