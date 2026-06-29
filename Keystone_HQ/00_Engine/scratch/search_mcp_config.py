import os
import json

search_paths = [
    r"C:\Users\Curtis\.gemini",
    r"C:\Users\Curtis\AppData\Local\Google",
    r"C:\Users\Curtis\AppData\Roaming\Google"
]

def search_configs():
    found = []
    for base in search_paths:
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            if "node_modules" in root or ".git" in root or "brain" in root:
                continue
            for file in files:
                if file.endswith((".json", ".pbtxt", ".config", ".yaml", ".yml")):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        if "keystone_multiplexer" in content or "MCP_Multiplexer" in content or "keystone-brain" in content:
                            found.append({
                                "path": filepath,
                                "size": len(content),
                                "snippet": content[:300]
                            })
                    except Exception:
                        pass
    return found

if __name__ == "__main__":
    print("Searching for IDE MCP configurations...")
    configs = search_configs()
    for c in configs:
        print(f"Path: {c['path']}")
        print(f"Size: {c['size']} bytes")
        print(f"Snippet: {c['snippet']}")
        print("-" * 50)
