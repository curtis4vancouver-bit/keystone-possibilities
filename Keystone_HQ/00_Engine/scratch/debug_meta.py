"""Debug Meta token — get the actual error message from Graph API"""
import json, urllib.request, urllib.error

with open("social_tokens.json") as f:
    social = json.load(f)

for brand in ["possibilities", "recomposition"]:
    token = social.get(brand, {}).get("meta", {}).get("user_access_token", "")
    app_id = social.get(brand, {}).get("meta", {}).get("app_id", "")
    app_secret = social.get(brand, {}).get("meta", {}).get("app_secret", "")
    print(f"\n=== {brand.upper()} META TOKEN ===")
    print(f"  Token (first 30): {token[:30]}...")
    print(f"  App ID: {app_id}")
    
    # Try debug_token with app access token
    app_token = f"{app_id}|{app_secret}"
    url = f"https://graph.facebook.com/v20.0/debug_token?input_token={token}&access_token={app_token}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "KeystoneDebug/1.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print(f"  Debug Result: {json.dumps(data, indent=2)}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  Debug Error ({e.code}): {body}")
    
    # Try /me directly
    me_url = f"https://graph.facebook.com/v20.0/me?access_token={token}"
    try:
        req2 = urllib.request.Request(me_url, headers={"User-Agent": "KeystoneDebug/1.0"})
        with urllib.request.urlopen(req2) as resp2:
            me = json.loads(resp2.read().decode())
            print(f"  /me Result: {json.dumps(me, indent=2)}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  /me Error ({e.code}): {body}")
