import sys
import os

sys.path.insert(0, r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
from youtube_api_manager import YouTubeAPIManager

def add_tags():
    video_id = "ohMgTNrlz0Y"
    mgr = YouTubeAPIManager(token_file=r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\youtube_token.json")
    
    videos_list_response = mgr.youtube.videos().list(id=video_id, part="snippet").execute()
    snippet = videos_list_response["items"][0]["snippet"]
    
    current_tags = snippet.get("tags", [])
    
    extra_tags = [
        "Longevity", "TRT", "Biohacking", "Antiaging", "HGH",
        "Fat Loss", "Building Muscle", "Men's Health", "Testosterone",
        "Bodybuilding", "Fitness", "Workout", "Diet", "Nutrition"
    ]
    
    for t in extra_tags:
        if t not in current_tags:
            current_tags.append(t)
            
    # Truncate to 500 chars limit (comma-separated string length)
    final_tags = []
    char_count = 0
    for tag in current_tags:
        # YouTube counts length including commas
        tag_len = len(tag) + (1 if final_tags else 0)
        if char_count + tag_len <= 500:
            final_tags.append(tag)
            char_count += tag_len
        else:
            break
            
    snippet["tags"] = final_tags
    
    update_request = mgr.youtube.videos().update(
        part="snippet",
        body={
            "id": video_id,
            "snippet": snippet
        }
    )
    update_request.execute()
    print(f"Tags updated successfully! Total tags: {len(final_tags)}, Total characters: {char_count}")

add_tags()
