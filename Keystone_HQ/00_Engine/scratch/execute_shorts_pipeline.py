import sys
import os
import json
import logging

# Ensure CWD is correct
SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)
os.chdir(SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_or_create_playlist(manager, playlist_title):
    """Checks if playlist exists, if not creates it. Returns playlist ID."""
    try:
        playlists_response = manager.youtube.playlists().list(
            part="snippet,contentDetails",
            mine=True,
            maxResults=50
        ).execute()
        
        for pl in playlists_response.get("items", []):
            if pl["snippet"]["title"].lower() == playlist_title.lower():
                logger.info(f"Found existing playlist: {playlist_title} ({pl['id']})")
                return pl["id"]
                
        # If not found, create it
        logger.info(f"Creating new playlist: {playlist_title}")
        create_resp = manager.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": playlist_title,
                    "description": "Short video insights and daily protocols from the Keystone empire."
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        ).execute()
        
        logger.info(f"Successfully created playlist! ID: {create_resp['id']}")
        return create_resp["id"]
    except Exception as e:
        logger.error(f"Error getting/creating playlist: {e}")
        return None

def add_video_to_playlist(manager, playlist_id, video_id):
    """Inserts a video into a playlist."""
    try:
        # Check if already in playlist to avoid duplicates
        items_resp = manager.youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        ).execute()
        
        for item in items_resp.get("items", []):
            if item["snippet"]["resourceId"]["videoId"] == video_id:
                logger.info(f"Video {video_id} is already in playlist {playlist_id}.")
                return True
                
        # Insert
        logger.info(f"Adding video {video_id} to playlist {playlist_id}...")
        pl_result = manager.youtube.playlistItems().insert(
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
        ).execute()
        logger.info(f"✅ Success! Video added to playlist. Item ID: {pl_result.get('id')}")
        return True
    except Exception as e:
        logger.error(f"Failed to add to playlist: {e}")
        return False

def main():
    video_path = r"C:\Users\Curtis\Desktop\short 21.mov"
    title = "The Silent GLP-1 Muscle Leak! 🚨"
    
    # We will link it to the main video "Is GLP-1 Costing You 40% of Your Muscle?" (wvJ9sYIbigM)
    main_video_id = "wvJ9sYIbigM"
    main_video_url = f"https://youtu.be/{main_video_id}"
    
    description = f"""If you are using GLP-1 agonists, your rapid weight loss might be a dangerous trap. Up to forty percent of every pound you lose is not fat—it is active, functional skeletal muscle tissue. This silent muscle leak destroys your baseline metabolic rate, leaving you weaker and setting you up for rapid weight rebound. Sarcopenic obesity is a silent epidemic for men over forty using these highly potent metabolic peptide agonists.

📺 MAIN MASTERCLASS VIDEO:
Watch our full clinical breakdown on preventing muscle loss: {main_video_url}

To protect your load-bearing structures, you must engineer a highly customized, hyper-targeted amino acid and protein protocol, aiming for a protein floor of at least 200 grams daily, spread across four major titrations, combined with high-tension resistance loads to force active cellular hypertrophy and signal muscle preservation.

#GLP1 #Sarcopenia #MuscleLoss #OzempicWeightLoss #PeptideProtocols #MenOver40 #LongevityBuilder #SquamishWellness #KeystonePossibilities #BiohackingBuilder

---

🔗 KEYSTONE OFFICIAL RESOURCES & BLUEPRINTS:
* Real Estate & Project Management: https://keystonepossibilities.com (BC Builder License #52603)
* High-Performance Wellness Blueprint: https://keystonerecomposition.com
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

    results = {}

    # PART 1: Update the already uploaded video on Keystone Possibilities
    possibilities_video_id = "-abkt0cDDY4"
    logger.info(f"--- Processing Keystone Possibilities (@KeystonePossibilities) ---")
    pos_manager = YouTubeAPIManager(token_file="youtube_token.json")
    if pos_manager.youtube:
        # Update description to include main video link
        logger.info(f"Updating description for {possibilities_video_id} on Possibilities...")
        pos_manager.update_video_metadata(
            video_id=possibilities_video_id,
            description=description
        )
        
        # Get/create "Keystone Protocols Shorts" playlist
        pl_id = get_or_create_playlist(pos_manager, "Keystone Protocols Shorts")
        if pl_id:
            add_video_to_playlist(pos_manager, pl_id, possibilities_video_id)
            results["possibilities"] = {
                "video_id": possibilities_video_id,
                "playlist_id": pl_id
            }
    else:
        logger.error("Failed to authenticate for Keystone Possibilities.")

    # PART 2: Upload to KeyStone Recomposition (OAC) channel as well
    logger.info(f"\n--- Processing KeyStone Recomposition (OAC Channel) ---")
    oac_manager = YouTubeAPIManager(token_file="youtube_token_oac.json")
    if oac_manager.youtube:
        if os.path.exists(video_path):
            logger.info("Uploading short 21 to KeyStone Recomposition...")
            response = oac_manager.upload_video(
                file_path=video_path,
                title=title,
                description=description,
                tags=tags,
                category_id="27",  # Education
                privacy_status="private"
            )
            if response:
                oac_video_id = response.get("id")
                logger.info(f"Successfully uploaded to KeyStone Recomposition! Video ID: {oac_video_id}")
                
                # Get/create "Keystone Protocols Shorts" playlist
                pl_id = get_or_create_playlist(oac_manager, "Keystone Protocols Shorts")
                if pl_id:
                    add_video_to_playlist(oac_manager, pl_id, oac_video_id)
                    results["recomposition"] = {
                        "video_id": oac_video_id,
                        "playlist_id": pl_id
                    }
            else:
                logger.error("Failed to upload to KeyStone Recomposition.")
        else:
            logger.error(f"Video file not found at {video_path} for OAC upload.")
    else:
        logger.error("Failed to authenticate for KeyStone Recomposition.")

    # Output results summary
    print("\n=== PIPELINE RESULTS ===")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
