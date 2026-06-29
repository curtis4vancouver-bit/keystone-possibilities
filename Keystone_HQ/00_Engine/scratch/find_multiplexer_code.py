import os

MULTIPLEXER_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\MCP_Multiplexer"

def search():
    for root, dirs, files in os.walk(MULTIPLEXER_DIR):
        for file in files:
            if file.endswith((".js", ".ts", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if "mcp_multiplexer_execute_tool" in content or "execute_tool" in content:
                            print(f"File: {os.path.relpath(path, MULTIPLEXER_DIR)}")
                            # Print matching lines
                            for line in content.splitlines():
                                if "execute_tool" in line or "executeTool" in line or "agent" in line:
                                    print(f"  {line[:120]}")
                except Exception:
                    pass

if __name__ == "__main__":
    search()
