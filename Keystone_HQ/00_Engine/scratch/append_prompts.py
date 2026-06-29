import json

new_prompts = [
  {
    "id": "SYS_019",
    "category": "agent_tool_selection",
    "priority": "critical",
    "prompt": "Deep research into AI agent autonomous tool selection and MCP schema optimization in 2025-2026. How do you design MCP tool schemas, names, and descriptions so an LLM always picks the exact native tool instead of writing custom python scripts or asking the user? What are the best practices for few-shot prompting inside tool definitions? How do you prevent an AI from 'forgetting' it has specialized tools (like 'youtube-manager' or 'upload_quality_gate') when handling complex multi-step workflows? Include concrete examples of highly effective tool description patterns."
  },
  {
    "id": "SYS_020",
    "category": "visual_feedback",
    "priority": "high",
    "prompt": "Deep research into visual feedback loops and 'eyes and ears' for AI coding agents. Are there better alternatives to Chrome DevTools Protocol for browser automation? How do modern 'Computer Use' APIs, Puppeteer MCP, or Playwright MCP integrate with AI agents compared to basic CDP? How do you give an agent reliable visual feedback on what a web page actually looks like (screenshots vs DOM snapshots) so it stops 'flying blind' and breaking UI interactions? Include comparisons of state-of-the-art vision-agent frameworks in 2026."
  },
  {
    "id": "SYS_021",
    "category": "sequential_thinking",
    "priority": "high",
    "prompt": "Deep research into 'Sequential Thinking' (supranormal thinking) MCP and agent reasoning frameworks. How do you configure an AI agent to autonomously invoke sequential thinking or chain-of-thought tools for complex problems BEFORE acting, without the user having to explicitly prompt it? What is the ideal system prompt directive to force an agent to use a sequential thinking MCP when faced with ambiguity? Include examples of 'think-before-you-act' architectures."
  },
  {
    "id": "SYS_022",
    "category": "polling_optimization",
    "priority": "medium",
    "prompt": "Deep research into optimizing AI agent web polling loops to prevent token/credit waste. When an agent needs to wait for a long-running web task (like Deep Research or video generation), how do you implement a 60-second polling loop that doesn't consume massive LLM context tokens? What are the best practices for extracting only the 'completion status' from a DOM instead of feeding the entire HTML body back into the context window? How do systems like Opus handle background waiting efficiently compared to standard agent loops?"
  },
  {
    "id": "SYS_023",
    "category": "agent_memory",
    "priority": "critical",
    "prompt": "Deep research into Persistent Agent Memory vs Context Window dynamics. How do you map the distinction between 'what the agent knows' (stored in a vector DB or skill files) and 'what the agent is currently thinking about' (context window) to prevent having to re-teach the agent basic workflow steps? What are the best patterns for 'context injection' based on intent classification? How do you build an agent that truly 'remembers' your brand rules forever?"
  },
  {
    "id": "SYS_024",
    "category": "self_correction",
    "priority": "high",
    "prompt": "Deep research into Agent Self-Correction and Reflexion loops. If an AI agent's tool call fails (e.g., a web element isn't found or an API returns an error), how do you build an architecture where the agent automatically diagnoses and tries the correct alternative instead of immediately giving up or asking the user for help? What are the specific system prompt structures that encourage autonomous recovery from runtime errors?"
  },
  {
    "id": "SYS_025",
    "category": "system_prompt_overrides",
    "priority": "critical",
    "prompt": "Deep research into System Prompt overrides and 'Master Directives'. How do you write a master directive that successfully overrides a foundational LLM's intrinsic tendency to write custom python scripts when a native MCP tool already exists for the job? What specific keywords or negative constraints (e.g., 'NEVER use python if an MCP tool exists') have the highest compliance rates in production AI agent systems like Antigravity or Claude?"
  },
  {
    "id": "SYS_026",
    "category": "tool_usage_zero_shot",
    "priority": "medium",
    "prompt": "Deep research into zero-shot tool usage improvement. Can we use few-shot examples directly inside MCP tool JSON schema descriptions (e.g., adding an 'examples' field) to guarantee the agent formats its tool calls perfectly on the first try? What is the most effective way to document complex tool arguments so an LLM doesn't hallucinate parameters or use incorrect syntax?"
  },
  {
    "id": "SYS_027",
    "category": "workflow_discipline",
    "priority": "high",
    "prompt": "Deep research into preventing 'lazy' tool usage by AI agents. Why do agents sometimes use a broad, destructive tool (like rewriting a whole file) instead of a precise tool (like multi-line replace), and how do you enforce the use of precise tools? What prompt engineering techniques or tool design choices force an agent to prioritize the safest, most token-efficient tool available?"
  },
  {
    "id": "SYS_028",
    "category": "visual_feedback",
    "priority": "medium",
    "prompt": "Deep research into visual QA for AI agents. When an agent is automating UI tasks, how do you implement a 'look and confirm' step using Vision-Language Models (VLMs)? What are the best practices for taking automated screenshots via CDP or Playwright, passing them to a vision model, and verifying that the screen state matches expectations before clicking buttons? Include production patterns from 2026."
  }
]

with open('learning_queue_system_lockdown.json', 'r') as f:
    data = json.load(f)

data.extend(new_prompts)

with open('learning_queue_system_lockdown.json', 'w') as f:
    json.dump(data, f, indent=2)

print('Successfully added 10 prompts. Total prompts: ', len(data))
