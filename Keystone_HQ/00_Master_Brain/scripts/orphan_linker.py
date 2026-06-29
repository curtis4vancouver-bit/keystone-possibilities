"""
Orphan Linker — Phase 5
========================
Loops through all Obsidian orphan pages, finds the _INDEX.md in their
parent directory, and injects a [[wikilink]] into that index.
If no _INDEX.md exists, creates one.
Tags 1-block stubs with #needs_expansion.
"""

import json
import subprocess
import re
from pathlib import Path

MASTER_BRAIN = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")

# ── Step 1: Get orphans from graphthulhu ──────────────────────
# We'll call list_orphans via the MCP manually isn't possible from a script,
# so we'll scan the vault ourselves for pages with zero inbound links.

def get_all_md_files():
    """Get all .md files in the vault."""
    return list(MASTER_BRAIN.rglob("*.md"))

def extract_wikilinks(text):
    """Extract all [[wikilinks]] from text."""
    return set(re.findall(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]', text))

def find_orphans():
    """Find pages that are never linked to from any other page."""
    all_files = get_all_md_files()
    
    # Build a set of all page names (stems) that are linked to
    linked_targets = set()
    file_contents = {}
    
    for f in all_files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            file_contents[f] = text
            links = extract_wikilinks(text)
            for link in links:
                # Normalize: take the last part if it's a path
                clean = link.split("/")[-1].strip()
                linked_targets.add(clean)
        except Exception:
            pass
    
    # An orphan is a file whose stem is never in linked_targets
    orphans = []
    for f in all_files:
        stem = f.stem
        if stem not in linked_targets and stem != "_INDEX" and not stem.startswith("."):
            orphans.append(f)
    
    return orphans, file_contents

def find_index_for(orphan_path):
    """Find the nearest _INDEX.md in the orphan's directory or parent."""
    d = orphan_path.parent
    while d >= MASTER_BRAIN:
        idx = d / "_INDEX.md"
        if idx.exists():
            return idx
        d = d.parent
    return None

def main():
    print("Scanning vault for orphan pages...")
    orphans, file_contents = find_orphans()
    print(f"Found {len(orphans)} orphan pages.\n")
    
    linked_count = 0
    tagged_count = 0
    created_indexes = 0
    skipped = 0
    
    # Group orphans by their parent directory
    by_dir = {}
    for o in orphans:
        parent = o.parent
        by_dir.setdefault(parent, []).append(o)
    
    for directory, dir_orphans in sorted(by_dir.items()):
        index_path = directory / "_INDEX.md"
        
        # Create _INDEX.md if it doesn't exist
        if not index_path.exists():
            rel = directory.relative_to(MASTER_BRAIN)
            index_path.write_text(
                f"# {directory.name}\n\nIndex for `{rel}`\n\n## Contents\n\n",
                encoding="utf-8"
            )
            created_indexes += 1
        
        # Read current index content
        index_text = index_path.read_text(encoding="utf-8", errors="ignore")
        
        new_links = []
        for orphan in dir_orphans:
            stem = orphan.stem
            link = f"[[{stem}]]"
            
            # Skip if already linked in the index
            if stem in extract_wikilinks(index_text):
                skipped += 1
                continue
            
            # Check if this is a stub (very small content)
            content = file_contents.get(orphan, "")
            is_stub = len(content.strip()) < 50
            
            if is_stub:
                # Tag the stub file itself
                if "#needs_expansion" not in content:
                    with open(orphan, "a", encoding="utf-8") as f:
                        f.write("\n\n#needs_expansion\n")
                    tagged_count += 1
            
            new_links.append(f"- {link}")
            linked_count += 1
        
        # Append new links to the index
        if new_links:
            with open(index_path, "a", encoding="utf-8") as f:
                f.write("\n" + "\n".join(new_links) + "\n")
    
    print(f"Results:")
    print(f"  Linked into _INDEX files: {linked_count}")
    print(f"  Tagged as #needs_expansion: {tagged_count}")
    print(f"  New _INDEX.md files created: {created_indexes}")
    print(f"  Already linked (skipped): {skipped}")
    print(f"Done.")

if __name__ == "__main__":
    main()
