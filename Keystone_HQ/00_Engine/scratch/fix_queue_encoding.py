import json
import os

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
QUEUE_FILE = os.path.join(PROJECT_ROOT, "learning_queue.json")

def normalize(s):
    # Replace common dash variants and spaces
    return "".join(c for c in s if c.isalnum()).lower()

with open(QUEUE_FILE, "r", encoding="utf-8") as f:
    queue = json.load(f)

fixed_count = 0
for domain in queue.get("queue", []):
    completed = domain.get("completed", [])
    topics = domain.get("topics", [])
    
    new_completed = []
    for c_topic in completed:
        c_norm = normalize(c_topic)
        matched = False
        for t_topic in topics:
            if normalize(t_topic) == c_norm:
                new_completed.append(t_topic)
                matched = True
                if c_topic != t_topic:
                    print(f"Fixed mismatch in {domain['domain']}:\n  Old: {c_topic}\n  New: {t_topic}")
                    fixed_count += 1
                break
        if not matched:
            new_completed.append(c_topic)
            
    domain["completed"] = new_completed

if fixed_count > 0:
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    print(f"Saved {fixed_count} fixed completed topics.")
else:
    print("No mismatches found.")
