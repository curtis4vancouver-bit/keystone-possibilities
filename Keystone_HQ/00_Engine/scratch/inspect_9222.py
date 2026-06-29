import urllib.request
import urllib.error

try:
    urllib.request.urlopen('http://127.0.0.1:9222/')
except urllib.error.HTTPError as e:
    print("Code:", e.code)
    print("Headers:\n", e.headers)
    print("Body:\n", e.read().decode(errors='ignore'))
except Exception as e:
    print("Other error:", e)
