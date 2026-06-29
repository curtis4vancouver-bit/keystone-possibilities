import os
import json

digest_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Master_Docs\CONSOLIDATED_BRAIN_HISTORY_DIGEST.md"
if os.path.exists(digest_path):
    with open(digest_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    sections = content.split("## 📁 Conversation ID: ")
    header = sections[0]
    
    chunks = []
    for sec in sections[1:]:
        lines = sec.split("\n")
        conv_id = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        
        chunks.append({
            "conv_id": conv_id,
            "source": f"chat_archive/brain_{conv_id[:8]}",
            "content": f"# Chat Archive for Brain {conv_id[:8]}\nOriginal Conversation ID: {conv_id}\n\n" + body
        })
    
    print(json.dumps(chunks, indent=2))
else:
    print("Digest file not found.")
