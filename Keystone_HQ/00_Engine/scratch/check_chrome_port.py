import socket
import urllib.request
import json

try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json") as response:
        pages = json.loads(response.read().decode("utf-8"))
        print("Success! Chrome remote debugging port is open.")
        for p in pages:
            print(f"Page ID: {p.get('id')} | URL: {p.get('url')}")
except Exception as e:
    print(f"Could not connect to Chrome on port 9222: {e}")
