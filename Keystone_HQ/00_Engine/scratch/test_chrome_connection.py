import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:58072/json") as response:
        pages = json.loads(response.read().decode())
    print("SUCCESS: Connected to Chrome debug port on 58072!")
    print(f"Total pages open: {len(pages)}")
    for p in pages[:10]:
        print(f"- {p.get('title')} ({p.get('id')}) -> {p.get('url')}")
except Exception as e:
    print(f"FAILED to connect: {e}")
