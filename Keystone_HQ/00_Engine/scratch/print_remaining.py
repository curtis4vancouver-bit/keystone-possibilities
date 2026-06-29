import json

queue_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\learning_queue.json"
with open(queue_path, "r", encoding="utf-8") as f:
    queue_data = json.load(f)

print("--- LEARNING QUEUE STATUS ---")
total_topics = 0
total_completed = 0
pending_by_domain = {}

for domain_info in queue_data["queue"]:
    domain = domain_info["domain"]
    topics = domain_info["topics"]
    completed = domain_info.get("completed", [])
    
    total_topics += len(topics)
    total_completed += len(completed)
    
    pending = [t for t in topics if t not in completed]
    pending_by_domain[domain] = pending
    
    print(f"Domain: {domain} | Total: {len(topics)} | Completed: {len(completed)} | Remaining: {len(pending)}")

print(f"\nOverall: {total_completed}/{total_topics} completed. {total_topics - total_completed} remaining.")

print("\n--- DETAILED PENDING TOPICS BY DOMAIN ---")
for domain, pending in pending_by_domain.items():
    if pending:
        print(f"\n[{domain}] - {len(pending)} pending:")
        for i, t in enumerate(pending, 1):
            print(f"  {i}. {t[:120]}...")
