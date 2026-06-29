import json

with open(r"C:\Users\Curtis\.gemini\antigravity\brain\c47c6452-cc70-4117-9f16-571f8aabc598\.system_generated\steps\1265\output.txt", "r", encoding="utf-8") as f:
    data = json.load(f)

# Find the execute_tool in multiplexer
for tool in data.get("keystone_multiplexer", []):
    if tool.get("name") == "mcp_multiplexer_execute_tool":
        print(json.dumps(tool, indent=2))
