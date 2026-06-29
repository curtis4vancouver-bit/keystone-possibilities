import sys
import os

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

daemon = OvernightResearchDaemon()
batch = daemon.get_next_batch(3)

print("BATCH DETAILS:")
for i, item in enumerate(batch, 1):
    print(f"\n--- TOPIC {i} ---")
    print(f"Domain: {item['domain']}")
    print(f"Topic: {item['topic']}")
    print("Prompt:")
    print(item['prompt'])
