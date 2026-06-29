import os
import shutil
import time
from datetime import datetime

# Paths
INBOX_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Omi_Inbox"
TRANSCRIPTS_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Master_Docs\Omi_Transcripts"

def format_and_ingest():
    if not os.path.exists(INBOX_DIR):
        print(f"Inbox not found: {INBOX_DIR}")
        return
        
    for filename in os.listdir(INBOX_DIR):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(INBOX_DIR, filename)
            
            # Read raw content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate YAML Frontmatter
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d %H:%M:%S")
            safe_name = filename.replace('.txt', '').replace('.md', '')
            
            yaml_header = f"""---
id: omi-transcript-{int(time.time())}
title: "Omi Capture: {safe_name}"
type: transcript
summary: "Omi passive capture transcript for {safe_name}"
tags:
  - okf
  - transcript
  - omi-transcript
  - passive-memory
created: '{now.isoformat()}'
updated: '{now.isoformat()}'
---
# Omi Capture: {safe_name}
**Captured Date:** {date_str}

## Transcript Log
{content}

---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
"""
            
            # Create new markdown file in the Transcripts directory
            new_filename = f"{now.strftime('%Y%m%d_%H%M%S')}_{safe_name}.md"
            new_filepath = os.path.join(TRANSCRIPTS_DIR, new_filename)
            
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(yaml_header)
            
            print(f"Ingested: {new_filename}")
            
            # Remove original file from Inbox to prevent duplicate processing
            os.remove(filepath)

if __name__ == "__main__":
    print("Running Omi Passive Brain Ingestor...")
    format_and_ingest()
    print("Ingestion complete.")
