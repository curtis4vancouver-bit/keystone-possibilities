import sys
import os
import argparse

sys.path.insert(0, r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
from youtube_api_manager import YouTubeAPIManager
from googleapiclient.http import MediaFileUpload

def update_metadata(video_id):
    print(f"Updating metadata for video: {video_id}")
    mgr = YouTubeAPIManager(token_file=r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\youtube_token.json")
    
    # 1. Update Description and Tags
    try:
        videos_list_response = mgr.youtube.videos().list(id=video_id, part="snippet").execute()
        if not videos_list_response.get("items"):
            print("Video not found.")
            return
            
        snippet = videos_list_response["items"][0]["snippet"]
        
        # Rewrite the AI Disclosure in the description
        old_desc = snippet["description"]
        
        # Split out the old AI disclosure
        parts = old_desc.split("dY - AI CONTENT DISCLOSURE & DIGITAL TWIN DISCLAIMER:")
        
        new_disclosure = """dY - AI CONTENT DISCLOSURE & DIGITAL TWIN DISCLAIMER:
This is my digital twin, and I'll be updating my digital twin every week so it stays like me, and it's of me, Wayne Stevenson. While I'm out doing other million-dollar jobs, I will have every once in a while a site that I build on or the retreats that I build in the future filmed while I'm building them, as well as the trip to Mexico.

s-,? MEDICAL & EDUCATIONAL DISCLAIMER:
The information provided in this video is for scientific study, educational analysis, and general research purposes only. It does not constitute medical advice, diagnosis, or treatment. Peptide compounds (such as CJC-1295 with DAC, Tesamorelin, and Ipamorelin) are high-potency research chemicals that must only be utilized under the direct supervision of a licensed, qualified medical professional. Always consult your physician before beginning any new training, supplementation, or peptide protocols.
"""
        
        new_desc = parts[0] + new_disclosure
        snippet["description"] = new_desc
        
        # Max out the tags (up to 500 chars)
        extra_tags = [
            "CJC-1295 DAC", "Tesamorelin", "Visceral fat loss", "GH bleed", "Peptide therapy", 
            "Men over 40 fat loss", "Wayne Stevenson", "Keystone Recomposition", "Squamish wellness", 
            "FDA compounding ban", "Builder Blueprint", "Body Recomposition", "Muscle growth peptides",
            "Fat loss peptides", "Anti-aging men", "Growth hormone optimization", "Ipamorelin stack"
        ]
        
        # Ensure we don't exceed 500 characters
        final_tags = []
        char_count = 0
        for tag in extra_tags:
            if char_count + len(tag) + 2 <= 500: # +2 for comma and space
                final_tags.append(tag)
                char_count += len(tag) + 2
                
        snippet["tags"] = final_tags
        
        update_request = mgr.youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": snippet
            }
        )
        update_request.execute()
        print("Metadata updated successfully.")
        
    except Exception as e:
        print(f"Failed to update metadata: {e}")
        
    # 2. Add to Playlist
    playlist_id = "PL22ZXw2RiZLS1qw6Q1_Xh5FMbeI0nKd3t"
    try:
        request = mgr.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()
        print("Added to 'The Builder Blueprint Protocol' playlist.")
    except Exception as e:
        print(f"Failed to add to playlist: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video_id", help="The ID of the uploaded video")
    args = parser.parse_args()
    update_metadata(args.video_id)
