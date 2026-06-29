# Model Alignment & Subagent Routing Rule

To prevent mismatched capability tiers and API pricing overhead, all child agents, subagents, and automated LLM API calls must inherit and use the same Gemini model tier as the parent orchestrating agent.

## Alignment Protocol
- If the parent agent is running on **Gemini Flash** (e.g., Flash 1.5, 2.5, 3.5), all spawned child agents, subagents, and automated LLM API calls must be configured to use the equivalent **Flash** tier.
- If the parent agent is running on **Gemini Pro** (e.g., Pro 1.5, Pro 2.0), all spawned child agents, subagents, and automated LLM API calls must be configured to use the equivalent **Pro** tier.
- No subagents or external LLM scripts may unilaterally upgrade or mismatch model tiers unless explicitly requested by the user.
