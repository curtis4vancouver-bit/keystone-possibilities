import os
import json
import urllib.request
import urllib.parse

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
tokens_file = os.path.join(ROOT_DIR, "social_tokens.json")

def api_get_json(url: str) -> dict:
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def main():
    if not os.path.exists(tokens_file):
        print(f"Error: {tokens_file} not found.")
        return

    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)

    for brand in ["possibilities", "recomposition"]:
        print(f"\n=====================================")
        print(f"BRAND: {brand.upper()}")
        print(f"=====================================")
        meta = tokens.get(brand, {}).get("meta", {})
        token = meta.get("user_access_token")
        if not token:
            print("No Meta token found.")
            continue
            
        debug_url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={token}"
        data = api_get_json(debug_url)
        print("TOKEN DEBUG:")
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
