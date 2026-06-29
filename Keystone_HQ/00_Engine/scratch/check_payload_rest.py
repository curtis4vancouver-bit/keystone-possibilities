import urllib.request
import json

def check_point_payload():
    point_id = "2032c14f-09e9-4605-94d1-f13722679559"
    url = f"http://localhost:6333/collections/keystone_unified/points/{point_id}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            result = data.get("result") or {}
            print(f"Point ID: {result.get('id')}")
            print(f"Has Vector: {result.get('vector') is not None}")
            print(f"Payload keys: {list(result.get('payload', {}).keys())}")
            print("Payload content:")
            print(json.dumps(result.get("payload", {}), indent=2))
    except Exception as e:
        print(f"Failed to fetch point: {e}")

if __name__ == "__main__":
    check_point_payload()
