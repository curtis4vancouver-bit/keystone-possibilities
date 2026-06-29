import os
import sys
import json
import logging

# Ensure CWD is the script's directory for relative imports and token file lookup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    # FOOLPROOF VIDEO FILE RESOLUTION
    desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    possible_names = ["whislter.mov", "whistler.mov", "Whistler.mov", "whislter.mp4", "whistler.mp4"]
    video_path = None
    
    for name in possible_names:
        path = os.path.join(desktop_dir, name)
        if os.path.exists(path):
            video_path = path
            break
            
    if not video_path:
        # Fallback to direct absolute paths
        absolute_paths = [
            r"C:\Users\Curtis\Desktop\whislter.mov",
            r"C:\Users\Curtis\Desktop\whistler.mov",
            r"C:\Users\Curtis\Desktop\Whistler.mov"
        ]
        for path in absolute_paths:
            if os.path.exists(path):
                video_path = path
                break

    if not video_path:
        logger.error("Error: Could not locate the Whistler Short video file on the Desktop.")
        sys.exit(1)

    logger.info(f"✅ Found video file to upload at: {video_path}")

    # METADATA & SEO HARDENING
    title = "The Whistler Permit Trap: Why Custom Builds Stall for 13 Months"
    
    description = """If you're planning a custom build in Whistler or West Vancouver, the structure isn't your biggest financial risk. \n\nThe dirt is.\n\nBetween aggressive riparian environmental regulations and steep bedrock topography, site prep alone can blow your budget by $200,000 before you pour a single footing. \n\nMost contractors bid the house and downplay the dirt. But hitting a protected watercourse can stall your project for 13 months. That's 13 months of massive carrying costs with zero site progress.\n\nYou don't just need a builder. You need a project manager who engineers out the municipal and environmental risks long before a shovel hits the ground. \n\nWayne Stevenson | BC Licensed Builder #52603 | Principal, Keystone Possibilities\n\n📋 FREE CONSULTATION — Planning a custom home, multiplex, or commercial build in the Sea-to-Sky Corridor?\n→ https://keystonepossibilities.ca\n\n🔗 CONNECT:\n• LinkedIn: https://www.linkedin.com/in/stevenson4vancouver\n• Instagram: https://www.instagram.com/keystonepossibilities\n• High-Performance Wellness Blueprint: https://keystonerecomposition.com\n\n🎵 SOUNDTRACK & MUSIC:\nListen to Wayne Stevenson's "Keystone Recomposition" ambient and deep house tracks on Spotify, Apple Music, and Amazon. Fully written, produced, and syndicated via TooLost Music.\n→ Spotify Official Artist Profile: https://open.spotify.com/artist/WayneStevenson\n→ YouTube Music: https://www.youtube.com/@keystonerecomposition\n\n🤖 SYNTHETIC MEDIA / AI DIGITAL TWIN DISCLOSURE:\nThe host is a photorealistic digital representation of Wayne Stevenson, synthesized using advanced visual networks. All construction data and professional commentary are authentic.\n\n#WhistlerBuilder #WestVancouver #ProjectManagement #CustomHomeBuild #BCBuilder #SeaToSky #RiparianZone #ConstructionCosts #KeystonePossibilities #Builder2026"""

    tags = [
        "Whistler custom home builder",
        "West Vancouver construction",
        "riparian zone permits BC",
        "steep slope engineering Vancouver",
        "construction project management",
        "luxury home builder Sea to Sky",
        "Squamish building permits",
        "BC construction delays",
        "custom home cost control",
        "independent project manager",
        "Whistler builder",
        "site prep costs BC",
        "construction risk mitigation",
        "Keystone Possibilities",
        "value engineering construction"
    ]

    token_file = "youtube_token_possibilities.json"
    if not os.path.exists(token_file):
        logger.error(f"Error: Possibilities token file not found at {token_file}")
        sys.exit(1)
        
    logger.info(f"Using YouTube token file: {token_file} (Keystone Possibilities)")
    
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            logger.error("Authentication failed. Make sure tokens are valid.")
            sys.exit(1)
            
        logger.info("Uploading video as PRIVATE draft to Keystone Possibilities...")
        response = manager.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags,
            category_id="22",  # People & Blogs
            privacy_status="private"
        )
        
        if response:
            logger.info("🎉 SUCCESS! Video uploaded successfully to Keystone Possibilities!")
            video_id = response.get('id')
            print(json.dumps(response, indent=2))
            
            # Custom Thumbnail Upload
            thumbnail_path = r"C:\Users\Curtis\.gemini\antigravity\brain\251191b3-5526-4abe-90aa-156efa41d317\poss003_thumbnail_1780030802379.png"
            if os.path.exists(thumbnail_path):
                logger.info("Found custom thumbnail image. Uploading...")
                manager.set_thumbnail(video_id, thumbnail_path)
            else:
                logger.warning(f"Custom thumbnail not found at: {thumbnail_path}. Skipping thumbnail upload.")
        else:
            logger.error("❌ Upload failed.")
    except Exception as e:
        logger.error(f"❌ Execution failed: {str(e)}")

if __name__ == "__main__":
    main()
