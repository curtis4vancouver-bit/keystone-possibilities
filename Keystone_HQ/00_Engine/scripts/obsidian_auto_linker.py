import os
import re
import sys
from pathlib import Path

# Force UTF-8 output on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {
    ".git", ".obsidian", ".system_generated", "node_modules",
    "scratch", "__pycache__", "app", "davinci-resolve-mcp", "deprecated_scripts"
}

# Blacklist of filenames/titles that should NOT be used for auto-linking (too generic or system files)
BLACKLIST_TITLES = {
    "index", "agents", "task", "state", "lexicon", "package", "credentials", "main",
    "today", "test", "leads", "short", "scripts", "results", "blueprint", "config",
    "identity", "current_direction", "brand_voice", "brand_visual", "state_of_the_empire",
    "active_projects", "walkthrough", "implementation_plan", "schema", "audit", "report"
}

def get_markdown_files(root_dir: Path):
    """Recursively find all markdown files in the workspace, excluding specific directories."""
    md_files = []
    for path in root_dir.rglob("*.md"):
        # Check if file is in excluded directories
        rel_parts = path.relative_to(root_dir).parts
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue
        md_files.append(path)
    return md_files

def build_title_map(md_files: list, root_dir: Path):
    """
    Build a lookup dictionary of lowercase terms to their target relative paths,
    and a list of terms sorted by length descending.
    """
    title_lookup = {}
    
    for filepath in md_files:
        stem = filepath.stem
        # Skip blacklisted filenames
        if stem.lower() in BLACKLIST_TITLES:
            continue
        
        # Relative path without extension
        rel_path = filepath.relative_to(root_dir).with_suffix("").as_posix()
        
        # Add various ways of referencing this note
        terms = []
        if len(stem) >= 4:
            terms.append(stem)
            
        cleaned_title = stem.replace("_", " ").replace("-", " ")
        cleaned_title_dashes = stem.replace("_", " ")
        
        if len(cleaned_title) >= 4:
            terms.append(cleaned_title)
        if len(cleaned_title_dashes) >= 4:
            terms.append(cleaned_title_dashes)
            
        for term in terms:
            # We map lowercase terms to target path
            title_lookup[term.lower()] = rel_path
            
    # Sort terms by length descending so that longer phrases match first in regex
    sorted_terms = sorted(title_lookup.keys(), key=lambda x: -len(x))
    return title_lookup, sorted_terms

def auto_link_files(md_files: list, title_lookup: dict, sorted_terms: list, root_dir: Path, dry_run: bool = True):
    """Scan and insert links into all files using a single compiled regex."""
    if not sorted_terms:
        print("No terms to link.")
        return 0, 0
        
    # Build a single unified regex matching any of the terms, protecting code blocks and links
    # Group 1: code blocks
    # Group 2: inline code
    # Group 3: existing links
    # Group 4: the terms on word boundaries
    terms_pattern = "|".join(re.escape(t) for t in sorted_terms)
    
    # We compile the master regex
    master_pattern = re.compile(
        r"(```.*?```)|(`.*?`)|(\[\[.*?\]\]|\[.*?\]\(.*?\))|(\b(" + terms_pattern + r")\b)",
        re.IGNORECASE | re.DOTALL
    )
    
    total_links = 0
    linked_files_count = 0
    
    for filepath in md_files:
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"Error reading {filepath.name}: {e}")
            continue
            
        original_content = content
        rel_path_self = filepath.relative_to(root_dir).with_suffix("").as_posix()
        links_added = 0
        
        def replace_match(match):
            nonlocal links_added
            # If any protective group matched, return it unmodified
            if match.group(1):
                return match.group(1)
            if match.group(2):
                return match.group(2)
            if match.group(3):
                return match.group(3)
                
            # Group 4 matched a term
            matched_text = match.group(4)
            term_lower = matched_text.lower()
            target_path = title_lookup.get(term_lower)
            
            # Prevent self-linking
            if target_path == rel_path_self:
                return matched_text
                
            links_added += 1
            return f"[[{target_path}|{matched_text}]]"
            
        content = master_pattern.sub(replace_match, content)
        
        if content != original_content:
            total_links += links_added
            linked_files_count += 1
            if not dry_run:
                try:
                    filepath.write_text(content, encoding="utf-8")
                    print(f"✓ Linked {filepath.name}: Added {links_added} links")
                except Exception as e:
                    print(f"✗ Failed writing {filepath.name}: {e}")
            else:
                print(f"⚙ Would link {filepath.name}: Added {links_added} links (dry-run)")
                
    return linked_files_count, total_links

def main():
    dry_run = "--apply" not in sys.argv
    
    print("=== Optimized Obsidian Auto-Linker ===")
    print(f"Scan Directory: {PROJECT_ROOT}")
    print(f"Mode: {'DRY-RUN (use --apply to write changes)' if dry_run else 'APPLY (writing changes)'}")
    
    md_files = get_markdown_files(PROJECT_ROOT)
    print(f"Found {len(md_files)} markdown files.")
    
    title_lookup, sorted_terms = build_title_map(md_files, PROJECT_ROOT)
    print(f"Compiled {len(sorted_terms)} unique linkable terms.")
    
    linked_files, total_links = auto_link_files(md_files, title_lookup, sorted_terms, PROJECT_ROOT, dry_run=dry_run)
            
    print("\n=== Summary ===")
    print(f"Files Modified: {linked_files} / {len(md_files)}")
    print(f"Total Links Added: {total_links}")
    if dry_run and total_links > 0:
        print("Run with '--apply' to write these changes to the files.")

if __name__ == "__main__":
    main()
