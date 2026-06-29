import os
import sys
import json
import logging

ROOT_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)
os.chdir(ROOT_DIR)

from youtube_api_manager import YouTubeAPIManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

video_path = r"C:\Users\Curtis\Desktop\short .mov"

title = "Mounjaro Muscle Loss: The 4-Pillar Protocol"

description = """⚠️ Medical Disclaimer: I am not a doctor. This video is a personal case study and should not be taken as medical advice. Always consult your physician before making any changes to your health protocol.

🤖 Note: Wayne runs an AI Digital Twin avatar (generated via HeyGen) as the primary on-camera host for all Recomposition video content.

You are losing weight on Mounjaro but destroying your structural foundation. In the clinical trials up to 40% of weight lost was lean muscle, not fat. I lost 48 pounds on Mounjaro, but my strength was tanking, so I built a 4-pillar protocol to stop the muscle wasting immediately. 

🔗 Connect & Learn More:
📘 The Protocol & Website: https://keystonerecomposition.com
▶️ The Protocol (YouTube): https://www.youtube.com/@keystonerecomposition
🎵 My Music Channel: https://www.youtube.com/@waynestevenson-y6o

#Mounjaro #MuscleLoss #GLP1 #WeightLossJourney #Recomposition #FatLoss #FitnessOver40 #Peptides"""

tags = [
    "Mounjaro muscle loss",
    "GLP-1 muscle wasting",
    "prevent muscle loss on Mounjaro",
    "Ozempic muscle loss",
    "GLP-1 side effects",
    "sarcopenia",
    "weight loss journey",
    "fitness over 40",
    "peptides",
    "Wayne Stevenson",
    "Keystone Recomposition"
]

token_file = "youtube_token.json"

manager = YouTubeAPIManager(token_file=token_file)
if manager.youtube:
    logger.info("Uploading video as PRIVATE draft to The Protocol channel...")
    response = manager.upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="27",
        privacy_status="private"
    )
    if response:
        logger.info(f"SUCCESS! Video ID: {response.get('id')}")
    else:
        logger.error("Upload failed.")
else:
    logger.error("Auth failed.")
