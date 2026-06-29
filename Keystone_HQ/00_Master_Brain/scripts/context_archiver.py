import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
import json

# Ensure sys.stdout handles UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Add Qdrant Brain path to sys.path to import MCP tools
ENGINE_PATH = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\Qdrant_Brain")
if str(ENGINE_PATH) not in sys.path:
    sys.path.append(str(ENGINE_PATH))

try:
    from keystone_brain_v2_mcp import ingest_to_brain
except ImportError as e:
    print(f"[Warning] Failed to import ingest_to_brain: {e}", file=sys.stderr)
    ingest_to_brain = None

def get_working_memory_path():
    # Try to resolve conversation ID from voice_bridge_config.json
    config_path = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
    )
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            conv_id = config.get("conversation_id")
            if conv_id:
                path = os.path.join(
                    os.path.expanduser("~"), ".gemini", "antigravity", "brain", conv_id, "working_memory.md"
                )
                if os.path.exists(path):
                    return path
        except Exception:
            pass

    # Fallback to the target parent conversation ID from prompt
    parent_id = "b352331d-7ad0-45d8-9daa-058939da47d3"
    path = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "brain", parent_id, "working_memory.md"
    )
    return path

def archive_context(summary: str, objectives: list, pending_actions: list):
    """
    Updates the local working_memory.md with the latest objectives and pending actions,
    and ingests the summary to Qdrant brain under the 'session_archive' namespace.
    """
    print(f"Archiving context...")
    filepath = get_working_memory_path()
    print(f"Target working_memory.md path: {filepath}")

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if not os.path.exists(filepath):
        # Create a new working_memory.md from template
        conv_id = os.path.basename(os.path.dirname(filepath))
        objs_str = "\n".join(f"{i+1}. {obj}" for i, obj in enumerate(objectives))
        acts_str = "\n".join(f"{i+1}. {act}" for i, act in enumerate(pending_actions))
        now_str = datetime.utcnow().isoformat() + "Z"
        content = f"""# 🧠 AGENT WORKING MEMORY STATE

**Last Updated:** {now_str}
**Conversation ID:** {conv_id}
**Purpose:** This file is read at the start of every message to ensure 100% context retention even after system-level chat compactions.

---

## 🎯 Current Objectives
{objs_str}

---

## 📊 Deep Research Status (ALL COMPLETE)
- (None)

---

## 📋 Pending Actions Queue
{acts_str}

---

## 🔑 Operational Configurations
- (None)
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Created new working_memory.md file.")
    else:
        # Read and update existing file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update Last Updated timestamp
        now_str = datetime.utcnow().isoformat() + "Z"
        content = re.sub(
            r"\*\*Last Updated:\*\* .*",
            f"**Last Updated:** {now_str}",
            content
        )

        # Helper to replace section
        def replace_section(text, header, new_list):
            new_list_str = "\n".join(f"{i+1}. {item}" for i, item in enumerate(new_list))
            pattern = r"(## " + re.escape(header) + r"\s*?\n)(.*?)(\n---|\n##|\Z)"
            replacement = r"\g<1>" + new_list_str + r"\n\g<3>"
            return re.sub(pattern, replacement, text, flags=re.DOTALL)

        content = replace_section(content, "🎯 Current Objectives", objectives)
        content = replace_section(content, "📋 Pending Actions Queue", pending_actions)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated existing working_memory.md file.")

    # Ingest the summary to Qdrant brain under the 'session_archive' namespace
    if ingest_to_brain:
        source_id = f"session_archive_{int(time.time())}"
        print(f"Ingesting summary to Qdrant ('session_archive' namespace, source_id: {source_id})...")
        try:
            res = ingest_to_brain(
                source_id=source_id,
                content=summary,
                namespace="session_archive",
                memory_layer="semantic"
            )
            print(f"Ingestion result: {res}")
        except Exception as e:
            print(f"Error during Qdrant ingestion: {e}", file=sys.stderr)
    else:
        print("[Error] Qdrant ingest_to_brain function not available. Ingestion skipped.", file=sys.stderr)

if __name__ == "__main__":
    # If run directly, run a quick self-test or allow command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Archive context to working_memory.md and Qdrant")
    parser.add_argument("--summary", type=str, help="Text summary of the context", default="Test context archiving execution.")
    parser.add_argument("--objectives", type=str, nargs="+", help="Current objectives list", default=["Test objective 1", "Test objective 2"])
    parser.add_argument("--pending", type=str, nargs="+", help="Pending actions queue", default=["Test pending action 1"])
    args = parser.parse_args()

    archive_context(args.summary, args.objectives, args.pending)
