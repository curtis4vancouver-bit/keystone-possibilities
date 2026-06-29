#!/usr/bin/env python3
"""
Obsidian Vault AI Metadata Enrichment & Optimization.
Adds YAML frontmatter, unique IDs, entity lists, and hidden context anchors to all markdown notes.
Generates a global wiki/index.md index and wiki/hot.md active session cache.
"""

import os
import sys
import re
import uuid
import json
from pathlib import Path
from datetime import datetime
import yaml

# Ensure UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TARGET_DIRS = [
    PROJECT_ROOT / "Master_Docs",
    PROJECT_ROOT / "Brand_Constitution"
]
WIKI_DIR = PROJECT_ROOT / "wiki"
EXCLUDE_FILES = {"INDEX.md", "README.md"}

# Predefined entities to auto-detect
ENTITIES_LIBRARY = [
    "Wayne Stevenson", "BPC-157", "GHK-Cu", "GLP-1", "Ozempic", "CCPC",
    "Bill 44", "Step Code", "Sea-to-Sky", "DaVinci Resolve", "DaVinci",
    "Suno", "Udio", "ElevenLabs", "Kling", "Runway", "YouTube", "Spotify",
    "GMB", "GCS", "NotebookLM", "Gemini Spark", "Squamish", "Whistler",
    "Vancouver", "Keystone Possibilities", "Keystone Recomposition"
]

# Regexes
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
HEADER_RE = re.compile(r"^(#{2,3})\s+(.+)$", re.MULTILINE)
CONTEXT_ANCHOR_RE = re.compile(r"<!--\s*CONTEXT:\s*(.*?)\s*-->")


def slugify(text):
    """Generate a clean kebab-case string from text."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text.strip("-")


def extract_fallback_summary(content_body):
    """Extract a 1-sentence fallback summary from the first text paragraph."""
    lines = content_body.split("\n")
    for line in lines:
        line = line.strip()
        # Skip headers, HTML comments, tables, frontmatter
        if not line or line.startswith("#") or line.startswith("<") or line.startswith("|") or line.startswith("-"):
            continue
        # Clean markdown formatting from the paragraph
        clean_line = re.sub(r"[\*\_`\[\]]", "", line)
        if len(clean_line) > 30:
            if len(clean_line) > 150:
                return clean_line[:147] + "..."
            return clean_line
    return "Consolidated documentation for Wayne Stevenson's dual-brand empire."


def enrich_note_file(file_path, dry_run=False):
    """Enrich a single markdown file with YAML frontmatter and context anchors."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine title from filename
    title = file_path.stem
    if title.startswith("0") or title.startswith("1") or title.startswith("2"):
        # Strip prefixes like '02_' or '24_'
        clean_title = re.sub(r"^\d+_", "", title).replace("_", " ").title()
    else:
        clean_title = title.replace("_", " ").title()

    # 1. Parse YAML Frontmatter
    frontmatter_match = FRONTMATTER_RE.match(content)
    frontmatter_data = {}
    body_content = content

    if frontmatter_match:
        yaml_text = frontmatter_match.group(1)
        body_content = content[frontmatter_match.end():]
        try:
            frontmatter_data = yaml.safe_load(yaml_text) or {}
        except Exception as e:
            print(f"  Warning: Failed to parse frontmatter in {file_path.name}: {e}")
            frontmatter_data = {}

    # Ensure stable ID
    if "id" not in frontmatter_data:
        frontmatter_data["id"] = f"doc-{slugify(title)}"
    
    # Ensure title
    if "title" not in frontmatter_data:
        frontmatter_data["title"] = clean_title

    # Ensure type
    if "type" not in frontmatter_data:
        # Determine based on directory
        parent_name = file_path.parent.name
        if parent_name == "Brand_Constitution":
            frontmatter_data["type"] = "brand"
        else:
            frontmatter_data["type"] = "document"

    # Ensure summary
    if "summary" not in frontmatter_data:
        frontmatter_data["summary"] = extract_fallback_summary(body_content)

    # Detect entities in body and frontmatter title/summary
    full_text_to_scan = f"{frontmatter_data['title']} {frontmatter_data['summary']} {body_content}"
    detected_entities = []
    for entity in ENTITIES_LIBRARY:
        # Scan with word boundaries
        if re.search(r"\b" + re.escape(entity) + r"\b", full_text_to_scan, re.IGNORECASE):
            detected_entities.append(entity)
            
    frontmatter_data["entities"] = sorted(list(set(detected_entities)))

    # Dates
    now_iso = datetime.now().isoformat()
    if "created" not in frontmatter_data:
        # Use file birthtime if available, else now
        try:
            mtime = os.path.getctime(file_path)
            frontmatter_data["created"] = datetime.fromtimestamp(mtime).isoformat()
        except Exception:
            frontmatter_data["created"] = now_iso
    frontmatter_data["updated"] = now_iso

    # 2. Inject context anchors in body content
    body_lines = body_content.split("\n")
    new_body_lines = []
    
    i = 0
    while i < len(body_lines):
        line = body_lines[i]
        header_match = HEADER_RE.match(line)
        if header_match:
            header_text = header_match.group(2).strip()
            # Check if previous non-empty line was a context anchor
            has_anchor = False
            # Look back up to 3 lines to see if there's a context anchor
            lookback = 1
            while lookback <= 3 and len(new_body_lines) - lookback >= 0:
                prev_line = new_body_lines[-lookback].strip()
                if prev_line:
                    if CONTEXT_ANCHOR_RE.match(prev_line):
                        has_anchor = True
                    break
                lookback += 1
                
            if not has_anchor:
                # Insert context anchor line preceding the header
                anchor_text = f"<!-- CONTEXT: {clean_title} / {header_text} -->"
                new_body_lines.append(anchor_text)
                
        new_body_lines.append(line)
        i += 1

    new_body_content = "\n".join(new_body_lines)

    # 3. Assemble full document
    new_yaml_text = yaml.dump(frontmatter_data, sort_keys=False, default_flow_style=False, allow_unicode=True).strip()
    new_full_content = f"---\n{new_yaml_text}\n---\n{new_body_content}"

    modified = (new_full_content != content)

    if modified and not dry_run:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_full_content)

    return frontmatter_data, modified


def generate_global_index(notes_registry, dry_run=False):
    """Generate global index file listing all documents and metadata summaries."""
    print("Generating wiki/index.md...")
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    index_file = WIKI_DIR / "index.md"

    lines = [
        "# 🎯 Global Knowledge Index",
        "",
        "> This is the auto-generated index of distilled documents and systems in Wayne Stevenson's dual-brand empire.",
        "> Updated: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
        "",
        "---",
        "",
        "## 📚 Documents Repository",
        "",
        "| Document Title | Type | Stable ID | Key Entities | Summary |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    for title, info in sorted(notes_registry.items()):
        entities_str = ", ".join([f"`{e}`" for e in info.get("entities", [])[:4]]) or "None"
        # Create Obsidian wikilink representation relative to vault root
        rel_path = info["rel_path"].replace("\\", "/")
        wikilink = f"[[{rel_path.replace('.md', '')}\\|{info['title']}]]"
        
        lines.append(
            f"| {wikilink} | `{info['type']}` | `{info['id']}` | {entities_str} | {info['summary']} |"
        )

    lines.append("")

    full_text = "\n".join(lines)

    if not dry_run:
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(full_text)
        print("✓ Index generated successfully.")
    else:
        print("[DRY RUN] Would write index file.")


def compile_hot_cache(dry_run=False):
    """Compile active session hot cache based on active projects and correction logs."""
    print("Compiling wiki/hot.md...")
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    hot_file = WIKI_DIR / "hot.md"

    # 1. Read active projects
    active_projects_content = "*No active projects loaded.*"
    projects_path = PROJECT_ROOT / "Master_Docs" / "ACTIVE_PROJECTS.md"
    if projects_path.exists():
        try:
            with open(projects_path, "r", encoding="utf-8") as f:
                active_projects_content = f.read()
            # Grab just the relevant section if too long
            # Let's take the first 40 lines of the file
            lines = active_projects_content.split("\n")
            active_projects_content = "\n".join(lines[:35]) + "\n\n*(Truncated for space)*"
        except Exception as e:
            active_projects_content = f"*Error reading active projects: {e}*"

    # 2. Read latest correction journal entries
    journal_entries_text = "*No recent corrections logged.*"
    journal_path = PROJECT_ROOT / ".learnings" / "correction_journal.json"
    if journal_path.exists():
        try:
            with open(journal_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data.get("entries", [])
            if entries:
                lines = []
                # Take last 3 entries
                for entry in entries[-3:]:
                    lines.extend([
                        f"- **Category:** `{entry.get('category', 'General')}`",
                        f"  - **Error:** `{entry.get('error', 'N/A')}`",
                        f"  - **Prevention Rule:** *{entry.get('prevention_rule', 'N/A')}*",
                        ""
                    ])
                journal_entries_text = "\n".join(lines)
        except Exception as e:
            journal_entries_text = f"*Error parsing correction journal: {e}*"

    # 3. Read active tasks
    tasks_text = "*No tasks logged.*"
    task_path = PROJECT_ROOT / "task.md"
    if task_path.exists():
        try:
            with open(task_path, "r", encoding="utf-8") as f:
                tasks_text = f.read()
        except Exception:
            pass

    hot_content = f"""# 🔥 Active Session Hot Cache

> **Purpose**: A session-level cache summarizing active projects, recent system errors, and priorities to bootstrap agent sessions.
> **Last Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 🚀 Active Projects & Direction

{active_projects_content}

---

## 🛠️ Recent Learnings & Correction Journal Rules

{journal_entries_text}

---

## 📋 Run Queue Tasks

{tasks_text}
"""

    if not dry_run:
        with open(hot_file, "w", encoding="utf-8") as f:
            f.write(hot_content)
        print("✓ Hot cache compiled successfully.")
    else:
        print("[DRY RUN] Would compile hot cache file.")


def main():
    dry_run = "--dry-run" in sys.argv
    print(f"Scanning directories for metadata enrichment...")
    if dry_run:
        print("--- RUNNING IN DRY-RUN MODE ---")

    notes_registry = {}
    enriched_count = 0
    modified_count = 0

    for target_dir in TARGET_DIRS:
        if not target_dir.exists():
            continue
        print(f"Scanning: {target_dir.name}...")
        for path in target_dir.rglob("*.md"):
            # Skip excluded files
            if path.name in EXCLUDE_FILES or any(part.startswith(".") for part in path.parts):
                continue
                
            rel_path = path.relative_to(PROJECT_ROOT)
            try:
                frontmatter, modified = enrich_note_file(path, dry_run=dry_run)
                enriched_count += 1
                if modified:
                    modified_count += 1
                    
                notes_registry[path.stem] = {
                    "title": frontmatter.get("title", path.stem),
                    "id": frontmatter.get("id", ""),
                    "type": frontmatter.get("type", "document"),
                    "summary": frontmatter.get("summary", ""),
                    "entities": frontmatter.get("entities", []),
                    "rel_path": str(rel_path)
                }
            except Exception as e:
                print(f"Error enriching {path.name}: {e}")

    print(f"\nMetadata sweep completed.")
    print(f"  Processed: {enriched_count} notes")
    print(f"  Modified/Enriched: {modified_count} notes")

    if enriched_count > 0:
        generate_global_index(notes_registry, dry_run=dry_run)
        compile_hot_cache(dry_run=dry_run)


if __name__ == "__main__":
    main()
