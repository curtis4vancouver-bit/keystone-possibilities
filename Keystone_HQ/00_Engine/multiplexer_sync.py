import os
import json
import subprocess
import sys

MULTIPLEXER_DIR = os.path.join(os.getcwd(), "MCP_Multiplexer")
AGENTS_CONFIG = os.path.join(MULTIPLEXER_DIR, "agents.json")
DYNAMIC_SKILLS_DIR = os.path.join(os.getcwd(), "dynamic_skills")
DYNAMIC_MCP_PATH = os.path.join(DYNAMIC_SKILLS_DIR, "dynamic_mcp.py")

# FastMCP Dynamic Multi-Tool Server Template
DYNAMIC_MCP_TEMPLATE = """import os
import sys
import importlib
import inspect
from mcp.server.fastmcp import FastMCP

# Align execution CWD
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, os.path.dirname(SCRIPT_DIR))
sys.path.insert(0, SCRIPT_DIR)

mcp = FastMCP("Keystone Sovereign Dynamic Skills")

print("Keystone Dynamic Skills MCP Server Booting...", file=sys.stderr)

# Scan and dynamic import all validated skills in this directory
for filename in os.listdir(SCRIPT_DIR):
    if filename.endswith(".py") and filename != "dynamic_mcp.py" and not filename.startswith("__"):
        module_name = filename[:-3]
        try:
            mod = importlib.import_module(module_name)
            # Find all public functions defined within the module itself (excluding imports)
            for name, func in inspect.getmembers(mod, inspect.isfunction):
                if func.__module__ == mod.__name__ and not name.startswith("_"):
                    print(f"Dynamically loading evolved skill tool: {module_name}.{name}", file=sys.stderr)
                    # Register tool dynamically using FastMCP's decorator wrapper
                    mcp.tool(name=f"dynamic_{module_name}_{name}")(func)
        except Exception as e:
            print(f"Error loading dynamic module {module_name}: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    mcp.run()
"""

def sync_dynamic_skills_to_multiplexer():
    """
    Registers the dynamic skills sub-agent within MCP_Multiplexer/agents.json 
    and regenerates the dynamic tools cache schema.
    """
    os.makedirs(DYNAMIC_SKILLS_DIR, exist_ok=True)
    
    # 1. Write the dynamic MCP agent template if missing
    if not os.path.exists(DYNAMIC_MCP_PATH):
        with open(DYNAMIC_MCP_PATH, "w", encoding="utf-8") as f:
            f.write(DYNAMIC_MCP_TEMPLATE)
        print(f"[Multiplexer Sync] Synthesized dynamic skills bridge at: {DYNAMIC_MCP_PATH}")
        
    # Create empty __init__.py for module imports
    init_path = os.path.join(DYNAMIC_SKILLS_DIR, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w") as f:
            pass
            
    # 2. Add sub-agent configuration to agents.json
    if os.path.exists(AGENTS_CONFIG):
        with open(AGENTS_CONFIG, "r", encoding="utf-8") as f:
            agents = json.load(f)
            
        if "dynamic_skills" not in agents:
            print("[Multiplexer Sync] Exposing dynamic_skills agent inside agents.json...")
            agents["dynamic_skills"] = {
                "command": "python",
                "args": [
                    "./dynamic_skills/dynamic_mcp.py"
                ],
                "enabled": True
            }
            with open(AGENTS_CONFIG, "w", encoding="utf-8") as f:
                json.dump(agents, f, indent=2)
                
    # 3. Refresh tool cache to update cached_tools.json
    print("[Multiplexer Sync] Refreshing the dynamic multiplexer cached schemas...")
    try:
        # Runs Node to refresh the cache dynamically using Multiplexer diagnostic_refresh.js
        node_script = os.path.join(MULTIPLEXER_DIR, "diagnostic_refresh.js")
        
        # We run standard Node command
        result = subprocess.run(
            ["node", node_script],
            cwd=MULTIPLEXER_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        print(f"[Multiplexer Sync] Refresh result: {result.stdout.strip()} {result.stderr.strip()}")
        print("[Multiplexer Sync] Evolved capabilities successfully hot-reloaded and accessible!")
    except Exception as e:
        print(f"[Multiplexer Sync] Warning: Failed to trigger node refresh daemon: {str(e)}")

if __name__ == "__main__":
    sync_dynamic_skills_to_multiplexer()
