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
    """Finds or creates a playlist with the given title."""
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

        # If not found, create it
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
    """Adds a video to a playlist with retries to handle YouTube index propagation delay."""
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
    retry_delay = 15 # seconds
    
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
    video_path = r"C:\Users\Curtis\Desktop\short 21.mov"
    if not os.path.exists(video_path):
        logger.error(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    title = "The Silent GLP-1 Muscle Leak! 🚨"
    
    description = """If you are using GLP-1 agonists, your rapid weight loss might be a dangerous trap. Up to forty percent of every pound you lose is not fat—it is active, functional skeletal muscle tissue. This silent muscle leak destroys your baseline metabolic rate, leaving you weaker and setting you up for rapid weight rebound. Sarcopenic obesity is a silent epidemic for men over forty using these highly potent metabolic peptide agonists.

To protect your load-bearing structures, you must engineer a highly customized, hyper-targeted amino acid and protein protocol, aiming for a protein floor of at least 200 grams daily, spread across four major titrations, combined with high-tension resistance loads to force active cellular hypertrophy and signal muscle preservation.

#GLP1 #Sarcopenia #MuscleLoss #OzempicWeightLoss #PeptideProtocols #MenOver40 #LongevityBuilder #SquamishWellness #KeystoneProtocols #Biohacking

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
        "GLP-1 muscle loss",
        "sarcopenia prevention",
        "prevent muscle loss on Ozempic",
        "tirzepatide muscle wasting",
        "sarcopenic obesity",
        "muscle growth over 40",
        "peptide therapy muscle",
        "BPC-157 muscle repair",
        "protein titration",
        "Squamish wellness retreat",
        "Keystone Protocols",
        "Wayne Stevenson"
    ]

    token_file = "youtube_token.json"
    logger.info(f"Initializing upload pipeline using token: {token_file}")
    
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            logger.error("Failed to authenticate.")
            sys.exit(1)
            
        # Verify it's Keystone Protocols channel
        channels_response = manager.youtube.channels().list(
            part="snippet",
            mine=True
        ).execute()
        channel_title = channels_response["items"][0]["snippet"]["title"]
        logger.info(f"Target YouTube Channel: {channel_title}")
        
        if "protocols" not in channel_title.lower():
            logger.error(f"CRITICAL WARNING: Target channel '{channel_title}' does not seem to be Keystone Protocols! Aborting.")
            sys.exit(1)

        # 1. Get or create the "Keystone Protocols Shorts" playlist
        playlist_id = get_or_create_playlist(manager, "Keystone Protocols Shorts")

        # 2. Upload the video
        logger.info("Uploading video as PRIVATE draft for review...")
        response = manager.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags,
            category_id="27",  # Education
            privacy_status="private"
        )
        
        if response and response.get("id"):
            video_id = response["id"]
            logger.info(f"🎉 SUCCESS! Video uploaded. ID: {video_id}")
            logger.info(f"YouTube Studio Link: https://studio.youtube.com/video/{video_id}/edit")
            logger.info(f"Public YouTube Watch Link: https://youtu.be/{video_id}")
            
            # 3. Add to playlist with retry logic to allow indexing
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
