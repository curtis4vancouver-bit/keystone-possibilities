#!/usr/bin/env python3
"""
Sync Brain to Google Drive Payloads.
Runs brain_to_drive_export.py, aggregates the namespace markdowns,
and creates a structured payload file in scratch/sync_doc_payloads.json.
The agent then reads this file and updates Google Docs using Google Workspace MCP.
Also copies the markdown exports directly to the mounted G: drive folder.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Ensure UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORT_DIR = PROJECT_ROOT / "scratch" / "brain_export"
PAYLOAD_FILE = PROJECT_ROOT / "scratch" / "sync_doc_payloads.json"
G_DRIVE_EXPORT_DIR = Path("G:/My Drive/Keystone_Brain_Export")

# Doc ID mapping as defined in brain-drive-sync SKILL.md
DOC_MAPPING = {
    "177cTdJb85WpprCuXW-J4C72LuPq-_XBBV4qsVHwB4B4": {
        "name": "Keystone Brand Identity",
        "namespaces": ["possibilities", "protocol_brand", "music"],
        "type": "qdrant"
    },
    "114MWnoqLub6Evxu2UfBvO2opr4bEKZII621tihWvk88": {
        "name": "Keystone Operations Manual",
        "namespaces": ["master"],
        "type": "qdrant"
    },
    "1oUrYbr7AtUuPNsnss0JqrAaIqSQvYL2oeUza55AiRao": {
        "name": "Keystone Content Pipeline",
        "namespaces": ["content_pipeline"],
        "type": "qdrant"
    },
    "1MtV6hDQ-bFSb_aTEzQDdE82kTKyazFSFnBqKN0pQWVQ": {
        "name": "Keystone Correction Journal",
        "namespaces": [],
        "type": "correction_journal"
    },
    "16U-NWxgFLRHPFO3T3MLCGguOQd8PQJFK1TaRplV90cg": {
        "name": "Keystone SEO Strategy",
        "namespaces": ["local_seo", "webmaster"],
        "type": "qdrant"
    },
    "1N5dpHBe-e_uRraw3tj9ZUyGPpsuhGvSTaL_SJ76YgyU": {
        "name": "Keystone MCP Tool Inventory",
        "namespaces": [],
        "type": "mcp_inventory"
    }
}


def read_namespace_file(ns: str) -> str:
    """Read exported namespace markdown file if it exists."""
    path = EXPORT_DIR / f"{ns}.md"
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"\n\n*Error reading namespace {ns}: {e}*\n\n"
    return ""


def run_export():
    """Execute the export script to dump namespaces to local markdown."""
    print("Running brain_to_drive_export.py...")
    export_script = PROJECT_ROOT / "scripts" / "brain_to_drive_export.py"
    
    # Run the export script
    res = subprocess.run(
        [sys.executable, str(export_script), "--export-dir", str(EXPORT_DIR)],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    
    if res.returncode != 0:
        print(f"Error during export: {res.stderr}")
        return False
        
    print(res.stdout)
    return True


def copy_to_gdrive():
    """Copy exported markdown files to the G: drive directly if mounted."""
    if not G_DRIVE_EXPORT_DIR.exists():
        print(f"G: Drive not mounted or directory {G_DRIVE_EXPORT_DIR} not found. Skipping direct copy.")
        return False
        
    print(f"Copying markdown exports directly to {G_DRIVE_EXPORT_DIR}...")
    import shutil
    
    copied = 0
    # Copy all markdown files in EXPORT_DIR
    for path in EXPORT_DIR.glob("*.md"):
        target_path = G_DRIVE_EXPORT_DIR / path.name
        try:
            shutil.copy2(path, target_path)
            copied += 1
        except Exception as e:
            print(f"Failed to copy {path.name}: {e}")
            
    print(f"✓ Copied {copied} files directly to Google Drive.")
    return True


def compile_correction_journal() -> str:
    """Compile correction journal from local JSON file to Markdown."""
    journal_path = PROJECT_ROOT / ".learnings" / "correction_journal.json"
    if not journal_path.exists():
        return "\n\n*Correction journal file not found.*\n\n"
    try:
        with open(journal_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        lines = [
            "# Keystone Correction Journal",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "Source: Local Correction Journal DB",
            "",
            "---",
            "",
            f"**Total Tracked Errors:** {data.get('stats', {}).get('total_errors', 0)}",
            f"**Total Fixes Applied:** {data.get('stats', {}).get('total_fixes', 0)}",
            "",
            "## Correction History",
            ""
        ]
        
        for idx, entry in enumerate(data.get("entries", [])):
            lines.extend([
                f"### Entry {idx+1}: {entry.get('id', 'N/A')} - {entry.get('category', 'General')}",
                f"- **Date:** {entry.get('date', 'N/A')}",
                f"- **Severity:** {entry.get('severity', 'medium')}",
                f"- **Error Pattern:** `{entry.get('error', 'N/A')}`",
                f"- **Root Cause:** {entry.get('root_cause', 'N/A')}",
                f"- **Fix Applied:** {entry.get('fix_applied', 'N/A')}",
                f"- **Prevention Rule:** *{entry.get('prevention_rule', 'N/A')}*",
                ""
            ])
        return "\n".join(lines)
    except Exception as e:
        return f"\n\n*Error compiling correction journal: {e}*\n\n"


def compile_mcp_tool_inventory() -> str:
    """Compile MCP Tool Inventory from active local configurations."""
    mcp_dir = Path("C:/Users/Curtis/.gemini/antigravity/mcp")
    if not mcp_dir.exists():
        return "\n\n*MCP schema directory not found.*\n\n"
    
    try:
        lines = [
            "# Keystone MCP Tool Inventory",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "Source: Active MCP Config Directories",
            "",
            "---",
            "",
            "This document lists all active Model Context Protocol (MCP) servers and their available tools.",
            ""
        ]
        
        for server_dir in sorted(mcp_dir.iterdir()):
            if not server_dir.is_dir():
                continue
            
            server_name = server_dir.name
            lines.append(f"## Server: `{server_name}`")
            lines.append("")
            lines.append("| Tool Name | Description | Parameters |")
            lines.append("|-----------|-------------|------------|")
            
            tool_count = 0
            for tool_file in sorted(server_dir.glob("*.json")):
                try:
                    with open(tool_file, "r", encoding="utf-8") as tf:
                        schema = json.load(tf)
                    
                    tool_name = schema.get("name", tool_file.stem)
                    desc = schema.get("description", "No description provided.").replace("\n", " ")
                    
                    # Compile params
                    params_info = []
                    props = schema.get("parameters", {}).get("properties", {})
                    req = schema.get("parameters", {}).get("required", [])
                    for p_name, p_val in props.items():
                        req_str = " (required)" if p_name in req else ""
                        params_info.append(f"`{p_name}`: {p_val.get('type', 'any')}{req_str}")
                    
                    params_str = ", ".join(params_info) if params_info else "None"
                    
                    lines.append(f"| `{tool_name}` | {desc} | {params_str} |")
                    tool_count += 1
                except Exception as tool_err:
                    lines.append(f"| `{tool_file.stem}` | *Failed to parse schema: {tool_err}* | N/A |")
            
            if tool_count == 0:
                lines.append("| None | No tools found for this server | N/A |")
            lines.append("")
            
        return "\n".join(lines)
    except Exception as e:
        return f"\n\n*Error compiling MCP tool inventory: {e}*\n\n"


def main():
    if not run_export():
        sys.exit(1)
        
    payloads = {}
    
    # Compile document contents
    for doc_id, info in DOC_MAPPING.items():
        doc_name = info["name"]
        namespaces = info["namespaces"]
        doc_type = info.get("type", "qdrant")
        
        print(f"Compiling document: {doc_name} (ID: {doc_id})...")
        
        if doc_type == "qdrant":
            doc_content = [
                f"# {doc_name}",
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                f"Source Namespaces: {', '.join(namespaces)}",
                "",
                "---",
                ""
            ]
            content_added = False
            for ns in namespaces:
                ns_content = read_namespace_file(ns)
                if ns_content:
                    doc_content.append(ns_content)
                    doc_content.append("\n---\n")
                    content_added = True
                    
            if not content_added:
                doc_content.append("\n*(No vector content found for these namespaces)*\n")
                
            payloads[doc_id] = {
                "name": doc_name,
                "content": "\n".join(doc_content)
            }
        elif doc_type == "correction_journal":
            payloads[doc_id] = {
                "name": doc_name,
                "content": compile_correction_journal()
            }
        elif doc_type == "mcp_inventory":
            payloads[doc_id] = {
                "name": doc_name,
                "content": compile_mcp_tool_inventory()
            }
        
    # Write to local sync payloads JSON
    try:
        os.makedirs(PAYLOAD_FILE.parent, exist_ok=True)
        with open(PAYLOAD_FILE, "w", encoding="utf-8") as f:
            json.dump(payloads, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Generated sync payloads file: {PAYLOAD_FILE}")
    except Exception as e:
        print(f"ERROR: Failed to write payloads file: {e}")
        sys.exit(1)
        
    # Attempt local Google Drive direct copy
    copy_to_gdrive()
    
    print("\nSync compilation finished. The agent can now use this payload file to update Google Docs.")


from datetime import datetime
if __name__ == "__main__":
    main()
