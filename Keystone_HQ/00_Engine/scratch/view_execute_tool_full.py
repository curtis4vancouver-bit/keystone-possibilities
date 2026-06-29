import json

with open(r"C:\Users\Curtis\.gemini\antigravity\brain\c47c6452-cc70-4117-9f16-571f8aabc598\.system_generated\steps\1265\output.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

# The keys in data are search_console, google_workspace, etc.
# Wait, let's search for "mcp_multiplexer_execute_tool" in all lists of tools
for agent, tools in data.items():
    for tool in tools:
        if "execute" in tool.get("name", "") or "multiplexer" in tool.get("name", ""):
            print(f"Agent: {agent}")
            print(json.dumps(tool, indent=2))
