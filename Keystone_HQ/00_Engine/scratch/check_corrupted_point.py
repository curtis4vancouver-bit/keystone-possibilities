import urllib.request
import json

def check_point():
    point_id = "2032c14f-09e9-4605-94d1-f13722679559"
    url = f"http://localhost:6333/collections/keystone_unified/points/{point_id}"
    
    # Try fetching with payload
    print(f"Querying REST API for point {point_id}...")
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            print("Success:")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Failed to fetch point: {e}")
        
    # Let's see if we can delete it
    # Deleting the point might fix the corruption!
    # Let's check if we can delete it using POST /collections/keystone_unified/points/delete
    # Wait, let's first check if we can fetch it.

if __name__ == "__main__":
    check_point()
