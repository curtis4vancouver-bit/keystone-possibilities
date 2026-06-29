import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:65047/json") as response:
        pages = json.loads(response.read().decode("utf-8"))
        print("Success! Connected to Antigravity DevTools.")
        for p in pages:
            print(f"Page ID: {p.get('id')} | URL: {p.get('url')} | Type: {p.get('type')}")
except Exception as e:
    print(f"Failed to connect: {e}")
