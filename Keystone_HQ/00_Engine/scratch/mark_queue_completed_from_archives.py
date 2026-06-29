import os
import json
import re

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
QUEUE_FILE = os.path.join(PROJECT_ROOT, "learning_queue.json")
RESEARCH_ARCHIVES = os.path.join(PROJECT_ROOT, "Research_Archives")

with open(QUEUE_FILE, "r", encoding="utf-8") as f:
    queue_data = json.load(f)

# Get all file names in Research_Archives (flat files)
files = [f for f in os.listdir(RESEARCH_ARCHIVES) if f.endswith(".md")]

print(f"Loaded {len(files)} files from Research_Archives.")

marked_count = 0
for domain_info in queue_data["queue"]:
    domain = domain_info["domain"]
    topics = domain_info["topics"]
    completed = domain_info.get("completed", [])
    
    for topic in topics:
        if topic in completed:
            continue
            
        # Try to find a matching file
        # We can clean the topic name to make a regex
        # Use first 40 chars of the topic name
        clean_topic = re.sub(r'[^a-zA-Z0-9]', '_', topic.lower())
        short_topic = clean_topic[:30].strip('_')
        
        # Also clean file names
        match_found = False
        for f in files:
            clean_f = re.sub(r'[^a-zA-Z0-9]', '_', f.lower())
            # check if short_topic is in clean_f or check if keyword overlap is high
            # e.g. "getting_youtube_videos_indexed" in "20260613_video_seo_advanced_technical_architecture_for_youtube_video_indexing"
            # Let's check some keywords
            keywords = [w for w in short_topic.split('_') if len(w) > 3]
            if len(keywords) >= 3:
                overlap = [w in clean_f for w in keywords]
                if sum(overlap) >= len(keywords) * 0.7: # 70% of keywords match
                    match_found = True
                    matching_file = f
                    break
        
        # Special manual matches
        if not match_found:
            if "youtube videos indexed" in topic.lower() and any("video_indexing" in fn for fn in files):
                match_found = True
                matching_file = [fn for fn in files if "video_indexing" in fn][0]
            elif "local seo domination" in topic.lower() and any("local_seo" in fn for fn in files):
                match_found = True
                matching_file = [fn for fn in files if "local_seo" in fn][0]

        if match_found:
            completed.append(topic)
            print(f"Marked completed: [{domain}] '{topic[:60]}...' matched with file: {matching_file}")
            marked_count += 1
            
    domain_info["completed"] = completed
    if len(completed) >= len(topics):
        domain_info["status"] = "completed"

if marked_count > 0:
    queue_data["last_updated"] = datetime.datetime.now().isoformat() if 'datetime' in globals() else "2026-06-13T10:30:00"
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, indent=2, ensure_ascii=False)
    print(f"Updated queue! Marked {marked_count} topics as completed.")
else:
    print("No new completions marked.")
