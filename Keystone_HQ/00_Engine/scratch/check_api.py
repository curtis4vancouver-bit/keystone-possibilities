import urllib.request
import json

def get_collection_info():
    try:
        url = "http://localhost:6333/collections/keystone_unified"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            data = json.loads(res_body)
            print("Collection Info:")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error querying Qdrant API: {e}")

if __name__ == "__main__":
    get_collection_info()
