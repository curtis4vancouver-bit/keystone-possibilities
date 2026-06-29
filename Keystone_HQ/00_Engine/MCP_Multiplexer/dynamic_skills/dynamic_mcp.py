import os
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
