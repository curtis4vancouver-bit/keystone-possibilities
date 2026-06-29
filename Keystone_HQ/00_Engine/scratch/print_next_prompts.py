import sys
import os

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def main():
    daemon = OvernightResearchDaemon()
    batch = daemon.get_next_batch(3)
    for i, x in enumerate(batch, 1):
        print(f"=== TOPIC {i} ===")
        print(f"Domain: {x['domain']}")
        print(f"Topic: {x['topic']}")
        print(f"Prompt:\n{x['prompt']}")
        print("=" * 40)

if __name__ == "__main__":
    main()
