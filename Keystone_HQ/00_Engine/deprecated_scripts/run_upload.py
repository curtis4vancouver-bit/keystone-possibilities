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
    video_path = r"C:\Users\Curtis\Desktop\short 21.mov"
    if not os.path.exists(video_path):
        logger.error(f"Error: Video file not found at {video_path}")
        sys.exit(1)

    title = "The Silent GLP-1 Muscle Leak! 🚨"
    
    description = """If you are using GLP-1 agonists, your rapid weight loss might be a dangerous trap. Up to forty percent of every pound you lose is not fat—it is active, functional skeletal muscle tissue. This silent muscle leak destroys your baseline metabolic rate, leaving you weaker and setting you up for rapid weight rebound. Sarcopenic obesity is a silent epidemic for men over forty using these highly potent metabolic peptide agonists.

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

    # Try standard token first
    token_file = "youtube_token.json"
    if not os.path.exists(token_file) and os.path.exists("youtube_token_oac.json"):
        token_file = "youtube_token_oac.json"
        
    logger.info(f"Using YouTube token file: {token_file}")
    
    try:
        manager = YouTubeAPIManager(token_file=token_file)
        if not manager.youtube:
            logger.error("Authentication failed. Make sure tokens are valid.")
            sys.exit(1)
            
        logger.info("Uploading video as PRIVATE draft for review...")
        response = manager.upload_video(
            file_path=video_path,
            title=title,
            description=description,
            tags=tags,
            category_id="27",  # Education
            privacy_status="private"
        )
        
        if response:
            logger.info("🎉 SUCCESS! Video uploaded successfully!")
            print(json.dumps(response, indent=2))
        else:
            logger.error("❌ Upload failed.")
    except Exception as e:
        logger.error(f"❌ Execution failed: {str(e)}")

if __name__ == "__main__":
    main()
