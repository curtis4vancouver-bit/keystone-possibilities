import os
import sys
import json
import urllib.request
import urllib.parse

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)
os.chdir(ROOT_DIR)

def api_get_json(url: str) -> dict:
    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"  HTTP ERROR {e.code}: {e.reason} - {err_body}")
        return {}
    except Exception as e:
        print(f"  ERROR: {str(e)}")
        return {}

def api_delete(url: str) -> dict:
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"  DELETE HTTP ERROR {e.code}: {e.reason} - {err_body}")
        return {}
    except Exception as e:
        print(f"  DELETE ERROR: {str(e)}")
        return {}

def main():
    tokens_file = "social_tokens.json"
    if not os.path.exists(tokens_file):
        print("Error: social_tokens.json not found.")
        return
        
    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
        
    for brand in ["possibilities", "recomposition"]:
        print(f"\n==========================================")
        print(f"BRAND: {brand.upper()}")
        print(f"==========================================")
        meta = tokens.get(brand, {}).get("meta", {})
        user_token = meta.get("user_access_token")
        if not user_token:
            print("No Meta user_access_token found.")
            continue
            
        print(f"User Access Token: {user_token[:30]}...")
        
        # 1. Fetch accounts
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_token}"
        pages_data = api_get_json(pages_url)
        pages = pages_data.get("data", [])
        print(f"Found {len(pages)} Facebook Pages:")
        
        for idx, page in enumerate(pages, 1):
            page_name = page.get("name")
            page_id = page.get("id")
            page_token = page.get("access_token")
            print(f"\n  Page {idx}: '{page_name}' (ID: {page_id})")
            
            # Fetch IG linked account
            ig_url = f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={page_token}"
            ig_data = api_get_json(ig_url)
            ig_account = ig_data.get("instagram_business_account", {})
            ig_id = ig_account.get("id")
            print(f"  Instagram Business Account ID: {ig_id}")
            
            # 2. Query Page Videos (Facebook)
            print("  Fetching recent Facebook videos...")
            videos_url = f"https://graph.facebook.com/v20.0/{page_id}/videos?fields=id,description,title,created_time&access_token={page_token}"
            videos_data = api_get_json(videos_url)
            videos = videos_data.get("data", [])
            print(f"  Found {len(videos)} recent videos:")
            for v in videos:
                print(f"    - FB Video ID: {v.get('id')} | Description: '{v.get('description', '')[:60]}...' | Created: {v.get('created_time')}")
                
            # 3. Query IG Media (Instagram)
            if ig_id:
                print("  Fetching recent Instagram media...")
                media_url = f"https://graph.facebook.com/v20.0/{ig_id}/media?fields=id,caption,media_type,timestamp&access_token={page_token}"
                media_data = api_get_json(media_url)
                media = media_data.get("data", [])
                print(f"  Found {len(media)} recent media items:")
                for m in media:
                    print(f"    - IG Media ID: {m.get('id')} | Type: {m.get('media_type')} | Caption: '{m.get('caption', '')[:60]}...' | Created: {m.get('timestamp')}")

if __name__ == "__main__":
    main()
