import os
import sys
import json
import logging

# Ensure CWD is correct
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    video_path = r"C:\Users\Curtis\Desktop\short 2.mov"
    if not os.path.exists(video_path):
        logger.error(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    title = "The GLP-1 Muscle Trap (Don't Ignore Your Frame) 🚨 #Shorts"
    
    description = """If you're on a GLP-1 and ignoring your muscle mass, you are literally building a house on a crumbling foundation. The weight drops, but so does your structural integrity. You're burning through lean tissue, your metabolism slows way down, and your survival switch flips. 

We have to fix the frame. Check out the full 8-minute masterclass on the exact Builder's Recomposition Protocol to stop the loss on our channel.

#GLP1 #Sarcopenia #MuscleLoss #OzempicWeightLoss #KeystoneProtocols

---
🔗 KEYSTONE OFFICIAL RESOURCES:
* TikTok: https://www.tiktok.com/@keystonerecomposition
* Spotify Official Artist Profile: https://open.spotify.com/artist/WayneStevenson
* High-Performance Wellness Blueprint: https://keystonerecomposition.com
* Real Estate & Project Management: https://keystonepossibilities.com

🚨 CLINICAL DISCLAIMER:
Strictly for scientific study, educational, and research purposes. Not medical advice.

🤖 SYNTHETIC MEDIA DISCLOSURE:
A high-fidelity AI digital twin avatar has been used to present this scientific research."""

    tags = [
        "GLP-1 muscle loss",
        "sarcopenia prevention",
        "prevent muscle loss on Ozempic",
        "tirzepatide muscle wasting",
        "muscle growth over 40",
        "peptide therapy muscle",
        "Keystone Protocols",
        "Wayne Stevenson"
    ]

    token_file = "youtube_token.json"
        
    logger.info(f"Using YouTube token file: {token_file} (Keystone Protocols)")
    
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            logger.error("Authentication failed. Make sure tokens are valid.")
            sys.exit(1)
            
        logger.info("Uploading video as PRIVATE draft for review (Not for Kids is hardcoded in API Manager)...")
        response = manager.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags,
            category_id="27",  # Education
            privacy_status="private"
        )
        
        if response:
            logger.info("🎉 SUCCESS! Video uploaded successfully to Keystone Protocols!")
            video_id = response.get('id')
            print(json.dumps(response, indent=2))
            
            # Set custom thumbnail
            thumbnail_path = r"C:\Users\Curtis\Desktop\short_2_thumbnail.jpg"
            manager.set_thumbnail(video_id, thumbnail_path)
            
        else:
            logger.error("❌ Upload failed.")
    except Exception as e:
        logger.error(f"❌ Execution failed: {str(e)}")

if __name__ == "__main__":
    main()
