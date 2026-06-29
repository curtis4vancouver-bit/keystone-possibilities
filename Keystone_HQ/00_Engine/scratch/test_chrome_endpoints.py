import urllib.request
import json

endpoints = ["/json", "/json/list", "/json/version", "/json/protocol"]
for ep in endpoints:
    try:
        url = f"http://127.0.0.1:58072{ep}"
        req = urllib.request.Request(url)
        # Chrome DevTools sometimes requires Host header or allows localhost
        # req.add_header('Host', 'localhost:58072')
        with urllib.request.urlopen(req) as response:
            data = response.read().decode()
            print(f"SUCCESS {ep}: Response length {len(data)}")
            print(data[:300])
    except Exception as e:
        print(f"FAILED {ep}: {e}")
