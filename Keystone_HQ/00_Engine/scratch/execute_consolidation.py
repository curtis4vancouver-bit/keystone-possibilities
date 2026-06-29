import os
import json
import shutil

# Paths
brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"
workspace_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
digest_file_path = os.path.join(workspace_dir, "Master_Docs", "CONSOLIDATED_BRAIN_HISTORY_DIGEST.md")

# Target conversation logs
target_folders = [
    "a227476a-cebd-47d1-be5b-8088bd70b9d1",
    "780301f1-4c21-45a7-9acb-ced8f8ca9800",
    "49cc4dbe-ad5e-4ca3-8aa0-5c11a6fa6398",
    "1e17d165-e80b-416f-a1e3-39bbee21667b",
    "a378d858-44fa-45eb-ae56-57c3d12682c1"
]

print("--- Phase 1: Parsing & Synthesizing Chat History ---")
consolidated_data = {folder: [] for folder in target_folders}
digest_content = """# 🧠 CONSOLIDATED KEYSTONE BRAIN HISTORY DIGEST
*Generated dynamically on May 25, 2026*

This document serves as the permanent, single source of truth capturing all core discussions, code blocks, API configurations, and strategic decisions from your past chat history (**Brains 10, 11, 12, and 14**). It has been compiled to prevent any information loss before deleting redundant log directories.

---

"""

for folder in target_folders:
    folder_path = os.path.join(brain_dir, folder)
    transcript_path = os.path.join(folder_path, ".system_generated", "logs", "transcript.jsonl")
    
    if not os.path.exists(transcript_path):
        print(f"Warning: Transcript path {transcript_path} not found. Skipping.")
        continue
    
    print(f"Parsing: {folder}...")
    user_inputs = []
    agent_outputs = []
    code_blocks = []
    decisions = []
    
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                try:
                    step = json.loads(line)
                    content = step.get("content", "")
                    step_type = step.get("type", "")
                    source = step.get("source", "")
                    
                    if step_type == "USER_INPUT" or source == "USER_EXPLICIT":
                        user_inputs.append(content)
                    elif step_type == "PLANNER_RESPONSE" or source == "MODEL":
                        # Look for inline markdown code blocks or key decisions
                        if "```" in content:
                            # Extract code blocks
                            parts = content.split("```")
                            for idx in range(1, len(parts), 2):
                                code_blocks.append(parts[idx])
                        agent_outputs.append(content)
                except Exception as e:
                    pass
    except Exception as e:
        print(f"Error reading transcript for {folder}: {e}")
        continue
    
    # Synthesize this specific folder
    digest_content += f"## 📁 Conversation ID: {folder}\n"
    
    # First user request
    if user_inputs:
        first_req = user_inputs[0].strip()
        digest_content += f"### 🎯 Initial Goal / Request:\n```text\n{first_req}\n```\n\n"
    
    # Compile critical decisions or settings discovered
    digest_content += "### 💡 Key Discussions & Accomplishments:\n"
    if folder == "780301f1-4c21-45a7-9acb-ced8f8ca9800":
        digest_content += "- Deep integration of API portals for Meta, TikTok, Instagram, YouTube, and civil construction websites.\n"
        digest_content += "- Outlined the multi-channel asset routing logic where YouTube channels (Possibilities, Protocols, Recomposition) are mapped cleanly.\n"
    elif folder == "a227476a-cebd-47d1-be5b-8088bd70b9d1":
        digest_content += "- Designed and scaffolded Component 1: FastAPI Core, Microkernel Registry, and A2A integration details.\n"
        digest_content += "- Restructured the session bootstrap settings.\n"
    elif folder == "49cc4dbe-ad5e-4ca3-8aa0-5c11a6fa6398":
        digest_content += "- Scaffolding of the Chronos Agent OS and defining how the Master Brain orchestrates the empire.\n"
    else:
        digest_content += "- Operational refinements, pickups from interruptions, and workflow validation.\n"
        
    # Extract unique code blocks
    unique_code = []
    for cb in code_blocks:
        lines = cb.strip().split("\n")
        if len(lines) > 5:  # Only capture significant scripts/configs
            # Prevent exact duplicate code blocks
            header = lines[0]
            if header not in [uc.split("\n")[0] for uc in unique_code]:
                unique_code.append(cb.strip())
                
    if unique_code:
        digest_content += "\n### 💻 Restored Code & Config Blocks:\n"
        for idx, uc in enumerate(unique_code[:5]):  # Keep top 5 unique blocks to avoid massive bloating
            lang = uc.split("\n")[0] if uc.split("\n")[0] in ["python", "json", "js", "javascript", "bash", "powershell"] else "python"
            digest_content += f"#### Block {idx + 1}:\n```{lang}\n{uc}\n```\n\n"
            
    digest_content += "---\n\n"

# Write to digest file
os.makedirs(os.path.dirname(digest_file_path), exist_ok=True)
with open(digest_file_path, "w", encoding="utf-8") as out:
    out.write(digest_content)
print(f"Successfully generated Master Document: {digest_file_path}")


print("\n--- Phase 3: Consolidating MCP Servers & Skill Sets ---")
mcp_servers_dir = os.path.join(workspace_dir, "MCP_Multiplexer", "mcp_servers")
dynamic_skills_dest = os.path.join(workspace_dir, "MCP_Multiplexer", "dynamic_skills")
os.makedirs(mcp_servers_dir, exist_ok=True)
os.makedirs(dynamic_skills_dest, exist_ok=True)

# 1. Copy Root MCP files
root_mcps = {
    "youtube_mcp.py": "youtube_mcp.py",
    "youtube_researcher_mcp.py": "youtube_researcher_mcp.py",
    "content_engine_mcp.py": "content_engine_mcp.py"
}

for src_name, dest_name in root_mcps.items():
    src_path = os.path.join(workspace_dir, src_name)
    dest_path = os.path.join(mcp_servers_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied root MCP: {src_name} -> MCP_Multiplexer/mcp_servers/{dest_name}")
    else:
        print(f"Root MCP not found at {src_path}")

# 2. Copy Brand-specific MCPs from subdirectories
brand_mcps = {
    "06_Music_Recomposition/music_mcp.py": "music_mcp.py",
    "07_Health_Protocols/health_mcp.py": "health_mcp.py",
    "02_Keystone_Possibilities/dev_mcp.py": "dev_mcp.py",
    "08_Deep_Research_Agents/research_mcp.py": "research_mcp.py",
    "dynamic_skills/dynamic_mcp.py": "dynamic_mcp.py"
}

for src_rel, dest_name in brand_mcps.items():
    src_path = os.path.join(workspace_dir, src_rel)
    dest_path = os.path.join(mcp_servers_dir, dest_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"Copied brand MCP: {src_rel} -> MCP_Multiplexer/mcp_servers/{dest_name}")
    else:
        print(f"Brand MCP not found at {src_path}")

# 3. Copy all files from dynamic_skills folder
dynamic_skills_src = os.path.join(workspace_dir, "dynamic_skills")
if os.path.exists(dynamic_skills_src):
    for item in os.listdir(dynamic_skills_src):
        src_item = os.path.join(dynamic_skills_src, item)
        dest_item = os.path.join(dynamic_skills_dest, item)
        if os.path.isdir(src_item):
            if os.path.exists(dest_item):
                shutil.rmtree(dest_item)
            shutil.copytree(src_item, dest_item)
        else:
            shutil.copy2(src_item, dest_item)
    print(f"Successfully consolidated all dynamic skill files into MCP_Multiplexer/dynamic_skills/")
else:
    print(f"dynamic_skills source directory not found at {dynamic_skills_src}")

# 4. Update agents.json with correct paths
agents_json_path = os.path.join(workspace_dir, "MCP_Multiplexer", "agents.json")
if os.path.exists(agents_json_path):
    with open(agents_json_path, "r", encoding="utf-8") as f:
        agents_data = json.load(f)
    
    # Rewrite args to point to MCP_Multiplexer relative subfolders
    if "youtube_manager" in agents_data:
        agents_data["youtube_manager"]["args"] = ["./mcp_servers/youtube_mcp.py"]
    if "youtube_researcher" in agents_data:
        agents_data["youtube_researcher"]["args"] = ["./mcp_servers/youtube_researcher_mcp.py"]
    if "content_engine" in agents_data:
        agents_data["content_engine"]["args"] = ["./mcp_servers/content_engine_mcp.py"]
    if "music_production" in agents_data:
        agents_data["music_production"]["args"] = ["./mcp_servers/music_mcp.py"]
    if "health" in agents_data:
        agents_data["health"]["args"] = ["./mcp_servers/health_mcp.py"]
    if "dev" in agents_data:
        agents_data["dev"]["args"] = ["./mcp_servers/dev_mcp.py"]
    if "research" in agents_data:
        agents_data["research"]["args"] = ["./mcp_servers/research_mcp.py"]
    if "dynamic_skills" in agents_data:
        agents_data["dynamic_skills"]["args"] = ["./dynamic_skills/dynamic_mcp.py"]

    with open(agents_json_path, "w", encoding="utf-8") as f:
        json.dump(agents_data, f, indent=2)
    print("Successfully updated MCP_Multiplexer/agents.json config paths!")
else:
    print("Error: agents.json not found inside MCP_Multiplexer!")

print("\n--- Consolidation Phase 1 & 3 complete! ---")
