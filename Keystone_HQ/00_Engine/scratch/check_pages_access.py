import os
import sys
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
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {e.reason}", "body": err_body}
    except Exception as e:
        return {"error": str(e)}

def main():
    if not os.path.exists(tokens_file):
        print(f"Error: {tokens_file} not found.")
        return

    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)

    meta = tokens.get("recomposition", {}).get("meta", {})
    user_access_token = meta.get("user_access_token")
    
    if not user_access_token:
        print("No Meta user_access_token found under 'recomposition'.")
        return

    print("=================================================================")
    print("Checking specific Facebook Page and Instagram IDs access...")
    print("=================================================================")
    
    test_ids = ["61583823506176", "898671469990393", "166025896601563"]
    for tid in test_ids:
        print(f"\nChecking ID: {tid}")
        url = f"https://graph.facebook.com/v20.0/{tid}?fields=name,id,category,username,instagram_business_account&access_token={user_access_token}"
        data = api_get_json(url)
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
