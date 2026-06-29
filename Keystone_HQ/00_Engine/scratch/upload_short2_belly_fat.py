import os
import sys
import json
import logging
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from youtube_api_manager import YouTubeAPIManager

# Reconfigure output to utf-8
sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_or_create_playlist(manager, playlist_title):
    try:
        logger.info(f"Checking for existing playlist named '{playlist_title}'...")
        playlists_response = manager.youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50
        ).execute()

        for item in playlists_response.get("items", []):
            if item["snippet"]["title"].strip().lower() == playlist_title.strip().lower():
                playlist_id = item["id"]
                logger.info(f"Found existing playlist: '{playlist_title}' with ID: {playlist_id}")
                return playlist_id

        logger.info(f"Playlist '{playlist_title}' not found. Creating a new one...")
        body = {
            "snippet": {
                "title": playlist_title,
                "description": "Short, tactical high-performance wellness and longevity blueprints from Keystone Protocols.",
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "public"
            }
        }
        create_response = manager.youtube.playlists().insert(
            part="snippet,status",
            body=body
        ).execute()
        
        playlist_id = create_response["id"]
        logger.info(f"✅ Successfully created playlist '{playlist_title}' with ID: {playlist_id}")
        return playlist_id
    except Exception as e:
        logger.error(f"Error getting/creating playlist: {str(e)}")
        return None

def add_video_to_playlist(manager, video_id, playlist_id):
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    
    max_retries = 5
    retry_delay = 15
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Attempting to add video {video_id} to playlist {playlist_id} (Attempt {attempt}/{max_retries})...")
            response = manager.youtube.playlistItems().insert(
                part="snippet",
                body=body
            ).execute()
            logger.info(f"✅ Successfully added video to playlist! Item ID: {response.get('id')}")
            return response
        except Exception as e:
            logger.warning(f"Failed to add video to playlist: {str(e)}")
            if attempt < max_retries:
                logger.info(f"Waiting {retry_delay} seconds for YouTube to index the video before retrying...")
                time.sleep(retry_delay)
            else:
                logger.error("❌ Max retries reached. Failed to add video to playlist programmatically.")
                return None

def main():
    video_path = r"C:\Users\Curtis\Desktop\short 2.mov"
    if not os.path.exists(video_path):
        logger.error(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    title = "Demolish Stubborn Belly Fat (The Clinical Way) 🏗️🔥"
    
    description = """Stop wasting hours on the treadmill and killing your joints. Cardio only burns the surface. If you want to demolish stubborn visceral gut fat, you have to bring in the demolition crew. 🏗️🔥

Watch the full breakdown on how to restructure your core on my YouTube channel now! (Link in bio/comments) 👇

#KeystoneRecomposition #BellyFatDemolition #Over40Fitness #VisceralFat #PeptideTherapy #MensHealth #CJC1295 #Tesamorelin #Biohacking #FatLossTips #HighEndFitness #TestosteroneOptimization

---

🔗 RELATED DEEP-DIVE MASTERCLASS:
Watch the full masterclass video: "Is GLP-1 Costing You 40% of Your Muscle?": https://www.youtube.com/watch?v=wvJ9sYIbigM

---

🔗 KEYSTONE OFFICIAL RESOURCES & BLUEPRINTS:
* High-Performance Wellness Blueprint: https://keystonerecomposition.com
* Real Estate & Project Management: https://keystonepossibilities.com (BC Builder License #52603)
* Spotify Official Artist Profile: https://open.spotify.com/artist/WayneStevenson

🎵 SOUNDTRACK:
Listen to Wayne Stevenson's "Keystone Recomposition" ambient and deep house tracks on Spotify, Apple Music, and Amazon. Fully written, produced, and syndicated via TooLost Music.

---

🚨 CLINICAL & MEDICAL DISCLAIMER:
This clinical analysis is strictly for scientific study, educational, and research purposes. It is not medical advice. Always consult a licensed medical professional before starting protocols, peptide cycles, or exercise plans.

🤖 SYNTHETIC MEDIA & AI DIGITAL TWIN DISCLOSURE:
Please note: A high-fidelity AI digital twin avatar has been used to present this scientific research. I am out in the field managing construction projects in the Sea-to-Sky corridor, so our digital media pipeline compiles these video blueprints to ensure you receive high-quality daily research without interruption."""

    tags = [
        "Keystone Recomposition",
        "Belly Fat Demolition",
        "Over 40 Fitness",
        "Visceral Fat",
        "Peptide Therapy",
        "Men's Health",
        "CJC-1295",
        "Tesamorelin",
        "Biohacking",
        "Fat Loss Tips",
        "High-End Fitness",
        "Testosterone Optimization"
    ]

    token_file = "youtube_token.json"
    logger.info(f"Initializing upload pipeline using token: {token_file}")
    
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            logger.error("Failed to authenticate.")
            sys.exit(1)
            
        channels_response = manager.youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()
        channel_title = channels_response["items"][0]["snippet"]["title"]
        logger.info(f"Target YouTube Channel: {channel_title}")
        
        if "protocols" not in channel_title.lower():
            logger.error(f"CRITICAL WARNING: Target channel '{channel_title}' does not seem to be Keystone Protocols! Aborting.")
            sys.exit(1)

        playlist_id = get_or_create_playlist(manager, "Keystone Protocols Shorts")

        logger.info("Uploading video as PRIVATE draft for review...")
        response = manager.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags,
            category_id="27",
            privacy_status="private"
        )
        
        if response and response.get("id"):
            video_id = response["id"]
            logger.info(f"🎉 SUCCESS! Video uploaded. ID: {video_id}")
            logger.info(f"YouTube Studio Link: https://studio.youtube.com/video/{video_id}/edit")
            logger.info(f"Public YouTube Watch Link: https://youtu.be/{video_id}")
            
            if playlist_id:
                logger.info("Waiting 10 seconds for initial indexing before attempting playlist insertion...")
                time.sleep(10)
                add_video_to_playlist(manager, video_id, playlist_id)
            else:
                logger.warning("Skipping playlist insertion because playlist ID was not available.")
                
            print("\n==================================================")
            print("🚀 PIPELINE COMPLETION REPORT:")
            print(f"Uploaded Video ID: {video_id}")
            print(f"Target Channel: {channel_title}")
            print(f"Added to Playlist ID: {playlist_id}")
            print(f"Direct Studio Edit Link: https://studio.youtube.com/video/{video_id}/edit")
            print("==================================================")
        else:
            logger.error("❌ Video upload failed.")
            
    except Exception as e:
        logger.error(f"❌ Execution failed: {str(e)}")

if __name__ == "__main__":
    main()
