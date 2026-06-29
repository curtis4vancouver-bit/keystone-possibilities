"""
MASTER VERIFY + OAC MUSIC FIX + MISPLACED VIDEO CLEANUP
1. Verify all 12 Protocols/Possibilities updates went through
2. Update all 21 OAC music videos (pure music tags, NO links, NO GLP)
3. Set misplaced Wolverine Stack on Possibilities to Private
"""
import sys, io, os, json, time
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

# Force unbuffered output so we can see real-time progress in logs
import builtins
def print(*args, **kwargs):
    kwargs['flush'] = True
    builtins.print(*args, **kwargs)

from youtube_api_manager import YouTubeAPIManager
manager = YouTubeAPIManager(token_file="youtube_token.json")
yt = manager.youtube

# ============================================================
# PART 1: VERIFY PROTOCOLS + POSSIBILITIES UPDATES
# ============================================================
print("=" * 70)
print("  PART 1: VERIFYING ALL 12 UPDATES")
print("=" * 70)

PROTOCOLS_IDS = ["DW-VXf2GXk0", "c--naKpO5_M", "3giPCEFfVTY", "NLTSFHhT9cc",
                  "zFUwRvTI7EU", "pBB4W2kOgQM", "PwQqt6U0kdo", "d9wBAZgZx7E", "ynSo4eOaIeU"]
POSSIBILITIES_IDS = ["IhgwE96Jcs4", "WgnbFGenZC8", "WGlZeW3Lz9M"]

verified = 0
failed_verify = 0

for vid_id in PROTOCOLS_IDS + POSSIBILITIES_IDS:
    try:
        r = yt.videos().list(part="snippet", id=vid_id).execute()
        if r["items"]:
            s = r["items"][0]["snippet"]
            desc = s.get("description", "")
            tags = s.get("tags", [])
            has_ecosystem = "KEYSTONE ECOSYSTEM" in desc
            has_website = "keystonepossibilities.ca" in desc
            has_tags = len(tags) >= 10
            
            status = "✅" if (has_ecosystem and has_website and has_tags) else "⚠️"
            if status == "✅":
                verified += 1
            else:
                failed_verify += 1
            
            print(f"  {status} {s['title'][:50]}")
            print(f"     Links: {'✅' if has_ecosystem else '❌'} Ecosystem | {'✅' if has_website else '❌'} Website | Tags: {len(tags)}")
    except Exception as e:
        print(f"  ❌ {vid_id}: {e}")
        failed_verify += 1
    time.sleep(0.3)

print(f"\n  Verified: {verified}/12 | Issues: {failed_verify}/12")

# ============================================================
# PART 2: SET MISPLACED VIDEO TO PRIVATE
# ============================================================
print("\n" + "=" * 70)
print("  PART 2: FIXING MISPLACED WOLVERINE STACK ON POSSIBILITIES")
print("=" * 70)

try:
    r = yt.videos().list(part="snippet,status", id="CScmP8MYaWE").execute()
    if r["items"]:
        current_privacy = r["items"][0]["status"]["privacyStatus"]
        print(f"  Current privacy: {current_privacy}")
        
        if current_privacy != "private":
            yt.videos().update(
                part="status",
                body={
                    "id": "CScmP8MYaWE",
                    "status": {"privacyStatus": "private"}
                }
            ).execute()
            print(f"  ✅ Set to PRIVATE — health video removed from construction channel")
        else:
            print(f"  ✅ Already private")
except Exception as e:
    print(f"  ❌ Error: {e}")

# ============================================================
# PART 3: FIX ALL OAC MUSIC VIDEOS
# ============================================================
print("\n" + "=" * 70)
print("  PART 3: UPDATING OAC MUSIC VIDEOS (pure music, NO links, NO GLP)")
print("=" * 70)

# Music-only tags — optimized for YouTube Music discovery
MUSIC_TAGS = [
    "deep house", "melodic techno", "deep house mix 2026", "workout music",
    "focus music", "gym music", "training music", "chill house",
    "electronic music", "ambient music", "deep house workout",
    "motivation music", "study music", "running music"
]

# Genre-specific tag additions based on video content
GENRE_MAP = {
    "rooftop": ["rooftop mix", "summer mix", "chill vibes"],
    "healing": ["healing frequencies", "solfeggio", "432hz", "meditation music"],
    "winter": ["winter arc", "dark motivation", "winter training"],
    "workout": ["workout motivation", "gym motivation", "fitness music"],
    "ocean": ["ocean sounds", "nature sounds", "sleep sounds", "recovery"],
    "cello": ["cello music", "acoustic", "ambient cello"],
    "storm": ["motivation", "discipline music", "mens motivation"],
}

# Get all 21 OAC music videos
OAC_CHANNEL_ID = "UCMn1f9DTF_iybKmv5WlTm9Q"
uploads = "UU" + OAC_CHANNEL_ID[2:]

manager_oac = YouTubeAPIManager(token_file="youtube_token_oac.json")
yt_oac = manager_oac.youtube

try:
    all_oac = []
    next_page = None
    while True:
        r = yt_oac.playlistItems().list(
            part="snippet,status",
            playlistId=uploads,
            maxResults=50,
            pageToken=next_page
        ).execute()
        for item in r.get("items", []):
            vid = item["snippet"]
            privacy = item.get("status", {}).get("privacyStatus", "?")
            if privacy == "public":
                all_oac.append({
                    "id": vid["resourceId"]["videoId"],
                    "title": vid["title"],
                    "privacy": privacy
                })
        next_page = r.get("nextPageToken")
        if not next_page:
            break
    
    print(f"  Found {len(all_oac)} public OAC music videos")
    
    oac_updated = 0
    oac_failed = 0
    
    for video in all_oac:
        vid_id = video["id"]
        title = video["title"]
        
        try:
            # Get full details
            detail = yt_oac.videos().list(part="snippet,status", id=vid_id).execute()
            if not detail["items"]:
                continue
            
            snippet = detail["items"][0]["snippet"]
            old_desc = snippet.get("description", "")
            
            # Determine genre for extra tags
            title_lower = title.lower()
            extra = []
            for keyword, extra_tags in GENRE_MAP.items():
                if keyword in title_lower:
                    extra.extend(extra_tags)
            
            # Build clean music-only description
            # Extract the core musical description (first paragraph of existing desc, 
            # stripped of any links or health references)
            first_line = old_desc.split('\n')[0] if old_desc else title
            
            # Clean any health/GLP references from the existing description
            clean_lines = []
            for line in old_desc.split('\n'):
                line_lower = line.lower()
                # Skip lines with health/GLP/link content
                if any(word in line_lower for word in [
                    'glp', 'peptide', 'mounjaro', 'bpc', 'tb-500', 'wolverine',
                    'tirzepatide', 'protocol', 'recomposition', 'metabolism',
                    'keystonepossibilities.ca', 'youtube.com/@', 'http',
                    'keystone ecosystem', 'disclaimer', 'medical', 
                    'subscribe', 'weight loss', 'body fat'
                ]):
                    continue
                clean_lines.append(line)
            
            # Build the new clean description
            cleaned_body = '\n'.join(clean_lines).strip()
            if not cleaned_body or len(cleaned_body) < 20:
                cleaned_body = title
            
            new_desc = f"""{cleaned_body}

🎵 Produced by KeyStone Recomposition
Genre: Deep House / Melodic Electronic

Perfect for: Workouts, Focus, Study, Running, Meditation

#DeepHouse #WorkoutMusic #FocusMusic #ElectronicMusic"""

            # Build tags
            video_tags = MUSIC_TAGS.copy() + extra
            # Trim to safe limit
            seen = set()
            safe_tags = []
            total_chars = 0
            for t in video_tags:
                tl = t.lower()
                if tl not in seen and total_chars + len(t) + 1 < 450:
                    seen.add(tl)
                    safe_tags.append(t)
                    total_chars += len(t) + 1
            
            # Update
            yt_oac.videos().update(
                part="snippet",
                body={
                    "id": vid_id,
                    "snippet": {
                        "title": snippet["title"],
                        "description": new_desc,
                        "tags": safe_tags,
                        "categoryId": "10"  # Music category
                    }
                }
            ).execute()
            
            oac_updated += 1
            print(f"  ✅ {title[:55]}")
            print(f"     Tags: {len(safe_tags)} | Cat: Music | No links ✓")
            
        except Exception as e:
            oac_failed += 1
            err_str = str(e)
            if "403" in err_str or "forbidden" in err_str.lower():
                print(f"  🔒 {title[:55]} — No write access (Brand Account)")
            else:
                print(f"  ❌ {title[:55]} — {err_str[:80]}")
        
        time.sleep(1)  # Rate limit
    
    print(f"\n  OAC Results: {oac_updated} updated, {oac_failed} failed")

except Exception as e:
    print(f"  ❌ Error listing OAC videos: {e}")

# ============================================================
# FINAL SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("  FINAL SUMMARY")
print("=" * 70)
print(f"  Protocols + Possibilities verified: {verified}/12")
print(f"  Misplaced video: Set to Private")
print(f"  OAC music videos: {oac_updated} updated")
print("=" * 70)
