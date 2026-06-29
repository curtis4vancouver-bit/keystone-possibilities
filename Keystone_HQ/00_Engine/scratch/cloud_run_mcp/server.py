import os
import re
import json
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

security = TransportSecuritySettings(enable_dns_rebinding_protection=False)
mcp = FastMCP("Brand Brain remote", host="0.0.0.0", transport_security=security)
MOUNT_PATH = "/gcs/brand-brain"

@mcp.tool()
def list_brain_files(directory_path: str = ""):
    """
    List contents of the Brand Brain directory on the Cloud Run remote GCS mount.
    directory_path: Relative path from the root of the Brand Brain.
    """
    target_path = os.path.abspath(os.path.join(MOUNT_PATH, directory_path))
    if not target_path.startswith(MOUNT_PATH):
        return "ERROR: Path is outside the brand brain boundary."
    
    if not os.path.exists(target_path):
        return f"ERROR: Path {directory_path} does not exist."
        
    items = []
    try:
        for entry in os.scandir(target_path):
            rel = os.path.relpath(entry.path, MOUNT_PATH)
            # Normalize path separator
            rel = rel.replace(os.sep, "/")
            is_dir = entry.is_dir()
            size = entry.stat().st_size if not is_dir else 0
            items.append({
                "name": entry.name,
                "relative_path": rel,
                "type": "directory" if is_dir else "file",
                "size_bytes": size
            })
        return json.dumps(items, indent=2)
    except Exception as e:
        return f"ERROR: Failed to list directory: {e}"

@mcp.tool()
def view_brain_file(relative_path: str):
    """
    Read the contents of a specific text file inside the Brand Brain.
    relative_path: The relative path to the file.
    """
    target_path = os.path.abspath(os.path.join(MOUNT_PATH, relative_path))
    if not target_path.startswith(MOUNT_PATH):
        return "ERROR: Path is outside the brand brain boundary."
        
    if not os.path.exists(target_path):
        return f"ERROR: File {relative_path} does not exist."
        
    if os.path.isdir(target_path):
        return f"ERROR: {relative_path} is a directory, not a file."
        
    # Check if text file by checking extension
    _, ext = os.path.splitext(target_path)
    # Ignored binary files to prevent reading giant bin files
    if ext.lower() in {".mov", ".mp4", ".avi", ".mkv", ".mp3", ".wav", ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg", ".gif", ".pdf"}:
        return f"ERROR: Cannot read binary/media file of type {ext} as text."
        
    try:
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(100000) # limit to first 100k chars for safety
            if len(content) >= 100000:
                content += "\n\n... [TRUNCATED due to length limit of 100KB] ..."
            return content
    except Exception as e:
        return f"ERROR: Failed to read file: {e}"

@mcp.tool()
def search_brain(query: str):
    """
    Perform a case-insensitive text search across all files in the Brand Brain.
    query: The term or phrase to search for.
    """
    results = []
    # Compile a regex search pattern
    try:
        pattern = re.compile(query, re.IGNORECASE)
    except Exception as e:
        return f"ERROR: Invalid search query regex: {e}"
        
    # Walk the mount path
    count = 0
    max_results = 50
    for root, dirs, files in os.walk(MOUNT_PATH):
        # In-place modify dirs to skip ignored directories
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".system_generated", "scratch", "node_modules", ".next", "dist", "build", ".cache"}]
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in {".tmp", ".swp", ".log", ".mov", ".mp4", ".avi", ".mkv", ".mp3", ".wav", ".zip", ".tar", ".gz", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".db"}:
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, MOUNT_PATH).replace(os.sep, "/")
            
            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if pattern.search(line):
                            results.append({
                                "file": rel_path,
                                "line_number": i,
                                "line_content": line.strip()
                            })
                            count += 1
                            if count >= max_results:
                                break
            except Exception:
                continue
            if count >= max_results:
                break
        if count >= max_results:
            break
            
    if not results:
        return f"No results found for query: '{query}'"
    return json.dumps(results, indent=2)

if __name__ == "__main__":
    # If run directly, run in SSE mode binding to all interfaces and matching the PORT env var
    port = int(os.environ.get("PORT", 8080))
    import uvicorn
    from starlette.middleware.cors import CORSMiddleware
    
    app = mcp.sse_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    uvicorn.run(app, host="0.0.0.0", port=port)
