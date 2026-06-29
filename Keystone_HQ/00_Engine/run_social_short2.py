import os
import sys

# Ensure CWD is correct
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from social_publisher import SocialPublisher

publisher = SocialPublisher()

content = """If you're on a GLP-1 and ignoring your muscle mass, you are literally building a house on a crumbling foundation. The weight drops, but so does your structural integrity. You're burning through lean tissue, your metabolism slows way down, and your survival switch flips. 

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

publisher.enqueue_post(
    brand="recomposition",
    platforms=["facebook", "instagram", "tiktok"],
    content=content,
    title="The GLP-1 Muscle Trap (Don't Ignore Your Frame) 🚨",
    media_url=r"C:\Users\Curtis\Desktop\short 2.mov",
    delay_days=0
)

# Process immediately
publisher.process_due_posts(dry_run=False)
