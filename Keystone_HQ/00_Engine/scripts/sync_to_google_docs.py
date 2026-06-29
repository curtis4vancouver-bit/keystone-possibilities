#!/usr/bin/env python3
"""
Sync compiled brain markdowns to live Google Docs in the cloud.
Converts Markdown to HTML locally, translates wiki-links to native Google Doc hyperlinks,
and performs in-place updates using Google Drive API to preserve File IDs for NotebookLM.
"""

import os
import sys
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaInMemoryUpload
    import markdown
except ImportError as e:
    print(f"ERROR: Missing dependencies: {e}. Run: pip install google-auth google-api-python-client markdown")
    sys.exit(1)

# Ensure UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PAYLOAD_FILE = PROJECT_ROOT / "scratch" / "sync_doc_payloads.json"
TOKEN_FILE = Path("C:/Users/Curtis/.google_workspace_mcp/credentials/curtis4vancouver@gmail.com.json")
STATE_FILE = PROJECT_ROOT / "scratch" / "doc_sync_state.json"

# Regex for wiki links [[Note Name]] or [[Note Name|Alias]]
WIKI_LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
# Regex for hashtags #tag_name (starts with word boundary, then #, then letters/numbers/underscores)
TAG_RE = re.compile(r"\b#([a-zA-Z0-9_-]+)\b")


def load_credentials():
    """Load cached OAuth credentials from MCP directory."""
    if not TOKEN_FILE.exists():
        print(f"ERROR: Google Workspace MCP token file not found at: {TOKEN_FILE}")
        return None
        
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            token_data = json.load(f)
            
        creds = Credentials(
            token=token_data.get("access_token"),
            refresh_token=token_data.get("refresh_token"),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=token_data.get("client_id"),
            client_secret=token_data.get("client_secret")
        )
        return creds
    except Exception as e:
        print(f"ERROR: Failed to load credentials from token file: {e}")
        return None


def load_sync_state():
    """Load MD5 state dictionary to track delta changes."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_sync_state(state):
    """Save MD5 state dictionary."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Warning: Failed to save sync state: {e}")


def calculate_content_hash(text):
    """Calculate MD5 hash of string content."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def translate_wiki_links(content, title_to_id):
    """Translate [[Wiki-Links]] to HTML hyperlinks targeting the mapped Google Doc IDs."""
    def replace_link(match):
        target_title = match.group(1).strip()
        alias = match.group(2) or target_title
        
        # Look for exact or case-insensitive match in title_to_id
        target_id = None
        for key, val in title_to_id.items():
            if key.lower() == target_title.lower():
                target_id = val
                break
                
        if target_id:
            return f'<a href="https://docs.google.com/document/d/{target_id}/edit">{alias}</a>'
        return alias
        
    return WIKI_LINK_RE.sub(replace_link, content)


def format_hashtags(content):
    """Convert #hashtag to styled HTML tag badges."""
    # Only replace hashtags that are not inside markdown links or code blocks
    # A simple replacement is fine for our compiled export formats
    tag_style = (
        'background-color: #f1f5f9; '
        'color: #475569; '
        'padding: 1px 5px; '
        'border-radius: 4px; '
        'font-family: monospace; '
        'font-size: 0.9em;'
    )
    return TAG_RE.sub(f'<span style="{tag_style}">#\\1</span>', content)


def sync_document(drive_service, doc_id, doc_name, markdown_content, title_to_id, dry_run=False):
    """Upload formatted HTML content to Google Drive in-place preserving Doc ID."""
    print(f"Syncing: {doc_name} (ID: {doc_id})...")
    
    # 1. Translation passes
    translated_md = translate_wiki_links(markdown_content, title_to_id)
    styled_md = format_hashtags(translated_md)
    
    # 2. Convert markdown to HTML
    # We enable tables, extra, and codehilite extensions for rich formatting
    html_body = markdown.markdown(styled_md, extensions=['extra', 'codehilite', 'tables'])
    
    # 3. Add global styling elements inside standard HTML template
    html_wrapper = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #1e293b;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }}
  h1, h2, h3, h4 {{
    color: #0f172a;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 600;
  }}
  h1 {{ border-bottom: 1px solid #e2e8f0; padding-bottom: 0.3em; }}
  a {{ color: #2563eb; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{
    background-color: #f1f5f9;
    padding: 2px 4px;
    border-radius: 4px;
    font-family: Consolas, Monaco, monospace;
    font-size: 0.9em;
  }}
  pre {{
    background-color: #f8fafc;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    border: 1px solid #e2e8f0;
  }}
  pre code {{ background-color: transparent; padding: 0; }}
  table {{
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
  }}
  th, td {{
    border: 1px solid #e2e8f0;
    padding: 10px;
    text-align: left;
  }}
  th {{ background-color: #f8fafc; font-weight: 600; }}
  hr {{ border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0; }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    if dry_run:
        print("  [DRY RUN] Would update Google Doc with HTML content.")
        return True

    try:
        # 4. Perform in-place update using Drive API media upload
        media = MediaInMemoryUpload(
            html_wrapper.encode("utf-8"),
            mimetype="text/html"
        )
        
        # Use files().update to replace media content of the Google Doc
        drive_service.files().update(
            fileId=doc_id,
            media_body=media
        ).execute()
        
        print(f"  ✓ Successfully updated {len(html_wrapper):,} bytes of HTML payload.")
        return True
    except Exception as e:
        print(f"  ✗ Failed to update document: {e}")
        return False


def main():
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    
    if not PAYLOAD_FILE.exists():
        print(f"ERROR: Payloads file not found: {PAYLOAD_FILE}")
        print("Please run sync_brain_to_drive.py first to compile payloads.")
        sys.exit(1)
        
    creds = load_credentials()
    if not creds:
        sys.exit(1)
        
    # Build Google Drive service
    try:
        drive_service = build("drive", "v3", credentials=creds)
    except Exception as e:
        print(f"ERROR: Failed to build Drive service: {e}")
        sys.exit(1)
        
    # Read payloads
    try:
        with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
            payloads = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to read payloads file: {e}")
        sys.exit(1)
        
    # Build title_to_id mapping for wiki-links translation
    title_to_id = {}
    for doc_id, doc_info in payloads.items():
        title_to_id[doc_info["name"]] = doc_id
        
    sync_state = load_sync_state()
    
    print(f"\nStarting Google Docs Cloud Sync — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if dry_run:
        print("--- RUNNING IN DRY-RUN MODE ---")
    print()
    
    success_count = 0
    skipped_count = 0
    updated_ids = []
    
    for doc_id, doc_info in payloads.items():
        name = doc_info["name"]
        content = doc_info["content"]
        
        current_hash = calculate_content_hash(content)
        previous_hash = sync_state.get(doc_id)
        
        if not force and previous_hash == current_hash:
            print(f"Skipping (Unchanged): {name} (ID: {doc_id})")
            skipped_count += 1
            continue
            
        if sync_document(drive_service, doc_id, name, content, title_to_id, dry_run=dry_run):
            success_count += 1
            updated_ids.append(doc_id)
            if not dry_run:
                sync_state[doc_id] = current_hash
        
    if not dry_run:
        save_sync_state(sync_state)
        
    print(f"\nCloud Sync finished.")
    print(f"  Updated: {success_count}/{len(payloads)}")
    print(f"  Skipped (No changes): {skipped_count}/{len(payloads)}")


if __name__ == "__main__":
    main()
