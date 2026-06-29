import json
import urllib.parse
import urllib.request
import time
import sys

def main():
    tokens_file = "social_tokens.json"
    try:
        with open(tokens_file, "r", encoding="utf-8") as f:
            tokens = json.load(f)
            
        tiktok = tokens["recomposition"]["tiktok"]
        client_key = tiktok["client_key"]
        client_secret = tiktok["client_secret"]
        refresh_token = tiktok["refresh_token"]
        
        print("Refreshing TikTok access token...")
        
        url = "https://open.tiktokapis.com/v2/oauth/token/"
        payload = {
            "client_key": client_key,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        
        data = urllib.parse.urlencode(payload).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'KeystoneApp/2.0'
            }
        )
        
        with urllib.request.urlopen(req) as res:
            resp = json.loads(res.read().decode('utf-8'))
            
        if "access_token" in resp:
            tiktok["access_token"] = resp["access_token"]
            tiktok["refresh_token"] = resp.get("refresh_token", refresh_token)
            tiktok["expires_in"] = resp.get("expires_in", 86400)
            tiktok["refresh_expires_in"] = resp.get("refresh_expires_in", 31536000)
            tiktok["acquired_at"] = int(time.time())
            
            tokens["recomposition"]["tiktok"] = tiktok
            
            with open(tokens_file, "w", encoding="utf-8") as f:
                json.dump(tokens, f, indent=4)
                
            print("SUCCESS: TikTok token refreshed successfully!")
            print(f"New Access Token: {resp['access_token'][:15]}...")
        else:
            print(f"Failed to refresh TikTok token: {resp}")
            
    except Exception as e:
        sys.stdout.write(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
