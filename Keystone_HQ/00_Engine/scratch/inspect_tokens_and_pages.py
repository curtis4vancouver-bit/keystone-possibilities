import os
import sys
import json
import urllib.request

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
        user_access_token = meta.get("user_access_token")
        
        if not user_access_token:
            print("  No Meta user_access_token found.")
            continue
            
        print(f"  User Access Token: {user_access_token[:30]}...")
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}"
        pages_data = api_get_json(pages_url)
        pages = []
        if isinstance(pages_data, dict) and "data" in pages_data:
            pages = pages_data.get("data", [])
        
        # If no pages returned, try direct query fallback for known target IDs
        if not pages:
            target_ids = ["898671469990393", "166025896601563"]
            for tid in target_ids:
                direct_url = f"https://graph.facebook.com/v20.0/{tid}?fields=name,access_token&access_token={user_access_token}"
                direct_data = api_get_json(direct_url)
                if "access_token" in direct_data:
                    pages.append({
                        "id": tid,
                        "name": direct_data.get("name"),
                        "access_token": direct_data["access_token"]
                    })
                    
        print(f"  Found {len(pages)} Facebook Page(s):")
        
        for idx, page in enumerate(pages, 1):
            page_name = page.get("name")
            page_id = page.get("id")
            page_token = page.get("access_token")
            print(f"    Page {idx}: '{page_name}' (ID: {page_id})")
            
            # Check connected IG account
            ig_url = f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={page_token}"
            ig_data = api_get_json(ig_url)
            ig_account = ig_data.get("instagram_business_account", {})
            ig_id = ig_account.get("id")
            print(f"      Instagram Business Account ID: {ig_id}")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
