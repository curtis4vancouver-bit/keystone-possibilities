"""Full platform health check: YouTube + Facebook + Instagram + TikTok + LinkedIn"""
import sys, os, json, time
sys.path.insert(0, r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
os.chdir(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("   KEYSTONE EMPIRE — FULL PLATFORM HEALTH CHECK")
print("=" * 70)

# === 1. YouTube (all 3 channels) ===
print("\n--- YOUTUBE API (3 Channels) ---")
from youtube_api_manager import YouTubeAPIManager

yt_tokens = {
    "Possibilities": ("youtube_token_possibilities.json", "UCu8gdU_R8XE2RvcttGa3drg"),
    "Protocols":     ("youtube_token.json",               "UCxURlqMNhAtxUTpdXmlOYaw"),
    "Recomposition": ("youtube_token_oac.json",           "UCMn1f9DTF_iybKmv5WlTm9Q"),
}

yt_results = {}
for name, (token_file, expected_id) in yt_tokens.items():
    try:
        mgr = YouTubeAPIManager(token_file=token_file)
        res = mgr.youtube.channels().list(part="snippet,statistics", mine=True).execute()
        if res.get("items"):
            ch = res["items"][0]
            match = ch["id"] == expected_id
            yt_results[name] = "PASS" if match else "WRONG CHANNEL"
            print(f"  {name:15s} | {ch['snippet']['title']:30s} | {ch['id']} | {'PASS' if match else 'FAIL - WRONG ID'}")
        else:
            yt_results[name] = "EMPTY"
            print(f"  {name:15s} | mine=True returned empty")
    except Exception as e:
        yt_results[name] = f"ERROR: {e}"
        print(f"  {name:15s} | ERROR: {e}")

# === 2. Meta (Facebook + Instagram) ===
print("\n--- META (Facebook Pages + Instagram Business) ---")
with open("social_tokens.json") as f:
    social = json.load(f)

meta_results = {}
for brand in ["possibilities", "recomposition"]:
    token = social.get(brand, {}).get("meta", {}).get("user_access_token")
    if not token:
        meta_results[brand] = "NO TOKEN"
        print(f"  {brand:15s} | NO META TOKEN")
        continue

    # Check token validity
    import urllib.request
    try:
        url = f"https://graph.facebook.com/v20.0/me?fields=id,name&access_token={token}"
        req = urllib.request.Request(url, headers={"User-Agent": "KeystoneHealthCheck/1.0"})
        with urllib.request.urlopen(req) as resp:
            me = json.loads(resp.read().decode())
        print(f"  {brand:15s} | Facebook User: {me.get('name')} (ID: {me.get('id')})")
        
        # Check pages
        pages_url = f"https://graph.facebook.com/v20.0/me/accounts?access_token={token}"
        req2 = urllib.request.Request(pages_url, headers={"User-Agent": "KeystoneHealthCheck/1.0"})
        with urllib.request.urlopen(req2) as resp2:
            pages = json.loads(resp2.read().decode()).get("data", [])
        
        for page in pages:
            print(f"  {' ':15s} | Page: {page.get('name')} (ID: {page.get('id')})")
            # Check Instagram Business Account link
            ig_url = f"https://graph.facebook.com/v20.0/{page['id']}?fields=instagram_business_account&access_token={page.get('access_token', token)}"
            req3 = urllib.request.Request(ig_url, headers={"User-Agent": "KeystoneHealthCheck/1.0"})
            try:
                with urllib.request.urlopen(req3) as resp3:
                    ig_data = json.loads(resp3.read().decode())
                    ig_id = ig_data.get("instagram_business_account", {}).get("id")
                    if ig_id:
                        print(f"  {' ':15s} |   -> Instagram Business: {ig_id}")
                    else:
                        print(f"  {' ':15s} |   -> No Instagram Business linked")
            except Exception as e:
                print(f"  {' ':15s} |   -> Instagram check error: {e}")
        
        meta_results[brand] = "PASS"
    except Exception as e:
        meta_results[brand] = f"ERROR: {e}"
        print(f"  {brand:15s} | ERROR: {e}")

# === 3. TikTok ===
print("\n--- TIKTOK ---")
tiktok = social.get("recomposition", {}).get("tiktok", {})
if tiktok.get("access_token"):
    acquired = tiktok.get("acquired_at", 0)
    age_h = (time.time() - acquired) / 3600
    expires_h = (tiktok.get("expires_in", 86400) / 3600) - age_h
    refresh_expires_d = (tiktok.get("refresh_expires_in", 0) / 86400) - (age_h / 24)
    print(f"  Recomposition   | Token Age: {age_h:.1f}h | Access Expires: {expires_h:.1f}h | Refresh Valid: {refresh_expires_d:.0f} days")
    if tiktok.get("refresh_token"):
        print(f"  {' ':15s} | Refresh Token: PRESENT (auto-renew OK)")
    else:
        print(f"  {' ':15s} | Refresh Token: MISSING (manual re-auth needed!)")
else:
    print(f"  Recomposition   | NO TIKTOK TOKEN")

# === 4. LinkedIn ===
print("\n--- LINKEDIN ---")
for brand in ["possibilities", "recomposition"]:
    li = social.get(brand, {}).get("linkedin", {})
    if li.get("access_token"):
        acquired = li.get("acquired_at", 0)
        age_h = (time.time() - acquired) / 3600
        expires_h = (li.get("expires_in", 5184000) / 3600) - age_h
        print(f"  {brand:15s} | Expires in: {expires_h:.0f}h ({expires_h/24:.0f} days)")
    else:
        print(f"  {brand:15s} | NO LINKEDIN TOKEN")

# === SUMMARY ===
print("\n" + "=" * 70)
print("   SUMMARY")
print("=" * 70)
all_pass = True
for name, result in yt_results.items():
    status = "PASS" if result == "PASS" else "FAIL"
    if status == "FAIL": all_pass = False
    print(f"  YouTube {name:15s}: {status}")
for brand, result in meta_results.items():
    status = "PASS" if result == "PASS" else "FAIL"
    if status == "FAIL": all_pass = False
    print(f"  Meta {brand:18s}: {status}")
print(f"  TikTok:                {'PASS' if tiktok.get('refresh_token') else 'FAIL'}")
print(f"\n  OVERALL: {'ALL SYSTEMS GO' if all_pass else 'ISSUES DETECTED'}")
print("=" * 70)
