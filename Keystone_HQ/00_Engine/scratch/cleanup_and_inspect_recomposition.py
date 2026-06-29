import os
import sys
import json
import urllib.request
import urllib.parse

# Set stdout to UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)
os.chdir(ROOT_DIR)

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

def main():
    tokens_file = "social_tokens.json"
    if not os.path.exists(tokens_file):
        print("Error: social_tokens.json not found.")
        return
        
    with open(tokens_file, "r", encoding="utf-8") as f:
        tokens = json.load(f)
        
    # ==========================================
    # 1. DELETING MISTAKES ON POSSIBILITIES
    # ==========================================
    print("\n--- [1] CLEANING UP MISTAKES ON POSSIBILITIES (CONSTRUCTION) ---")
    poss_meta = tokens.get("possibilities", {}).get("meta", {})
    poss_user_token = poss_meta.get("user_access_token")
    
    if poss_user_token:
        # Fetch page token for Keystone Possibilities Ltd
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={poss_user_token}"
        pages_data = api_get_json(pages_url)
        pages = pages_data.get("data", [])
        
        poss_page = next((p for p in pages if p.get("id") == "166025896601563"), None)
        if poss_page:
            poss_page_token = poss_page["access_token"]
            
            # Delete FB Video
            fb_video_id = "1610308273387763"
            print(f"Deleting Facebook video {fb_video_id} from construction page...")
            fb_del_url = f"https://graph.facebook.com/v20.0/{fb_video_id}?access_token={poss_page_token}"
            fb_res = api_delete(fb_del_url)
            print(f"Facebook Deletion Result: {fb_res}")
            
            # Delete IG Media
            ig_media_id = "18104836129984362"
            print(f"Deleting Instagram Reel {ig_media_id} from construction Instagram...")
            ig_del_url = f"https://graph.facebook.com/v20.0/{ig_media_id}?access_token={poss_page_token}"
            ig_res = api_delete(ig_del_url)
            print(f"Instagram Deletion Result: {ig_res}")
        else:
            print("Could not find page token for Keystone Possibilities Ltd.")
    else:
        print("No possibilities user token found.")

    # ==========================================
    # 2. INSPECTING RECOMPOSITION META ACCOUNT
    # ==========================================
    print("\n--- [2] INSPECTING RECOMPOSITION META ACCOUNT ---")
    rec_meta = tokens.get("recomposition", {}).get("meta", {})
    rec_user_token = rec_meta.get("user_access_token")
    
    if rec_user_token:
        print(f"Recomposition User Access Token: {rec_user_token[:30]}...")
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={rec_user_token}"
        pages_data = api_get_json(pages_url)
        pages = pages_data.get("data", [])
        print(f"Found {len(pages)} Facebook Pages connected to Recomposition Meta account:")
        
        for idx, page in enumerate(pages, 1):
            page_name = page.get("name")
            page_id = page.get("id")
            page_token = page.get("access_token")
            # Safe print
            safe_name = page_name.encode('ascii', errors='ignore').decode('ascii')
            print(f"  Page {idx}: '{safe_name}' (ID: {page_id})")
            
            # Check IG account
            ig_url = f"https://graph.facebook.com/v20.0/{page_id}?fields=instagram_business_account&access_token={page_token}"
            ig_data = api_get_json(ig_url)
            ig_account = ig_data.get("instagram_business_account", {})
            ig_id = ig_account.get("id")
            print(f"    Instagram Business Account ID: {ig_id}")
    else:
        print("No recomposition user token found.")

if __name__ == "__main__":
    main()
