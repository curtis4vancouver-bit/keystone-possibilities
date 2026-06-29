import urllib.request
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_post(url, payload):
    print(f"Testing POST to: {url}")
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/json'
            }
        )
        with urllib.request.urlopen(req, context=ctx) as r:
            body = r.read().decode('utf-8')
            print(f"Status: {r.status}")
            print(f"Headers: {dict(r.headers)}")
            print(f"Response: {body}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Body: {e.read().decode('utf-8')[:250]}")
    except Exception as e:
        print(f"Error testing POST {url}: {e}")
    print("-" * 50)

# Test POST with empty payload to verify endpoint existence (should return invalid JSON / missing slug error)
test_post(
    "https://keystonepossibilities.ca/?update_post_sovereign=1", 
    {}
)
