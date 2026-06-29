import requests
import time

# Check all collections
r = requests.get("http://localhost:6333/collections")
data = r.json()
print("=== QDRANT BRAIN HEALTH CHECK ===")
print(f"Status: {data['status']}")
print(f"Response time: {data['time']*1000:.4f} ms")
print(f"\nNamespaces found: {len(data['result']['collections'])}")
for c in data['result']['collections']:
    name = c['name']
    # Get point count for each collection
    cr = requests.get(f"http://localhost:6333/collections/{name}")
    cd = cr.json()
    count = cd['result']['points_count']
    print(f"  - {name}: {count} vectors")

# Speed test: run a search and measure latency
print("\n=== SPEED TEST ===")
start = time.perf_counter_ns()
search_payload = {
    "vector": [0.0] * 384,  # dummy vector for latency test
    "limit": 5
}
sr = requests.post("http://localhost:6333/collections/general/points/search", json=search_payload)
end = time.perf_counter_ns()
latency_us = (end - start) / 1000
latency_ms = latency_us / 1000
print(f"Search latency (round-trip including HTTP): {latency_ms:.2f} ms ({latency_us:.0f} microseconds)")
print(f"Qdrant internal time: {sr.json().get('time', 'N/A')}")
