import sys
sys.path.insert(0, r'C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\Qdrant_Brain')
from episodic_memory import search_episodes

results = search_episodes('optimization')
print(f'Found {len(results)} episodes:')
for r in results:
    ts = r.get('timestamp', '?')
    at = r.get('action_type', '?')
    sm = r.get('summary', '?')[:120]
    print(f'  [{ts}] {at} - {sm}')
