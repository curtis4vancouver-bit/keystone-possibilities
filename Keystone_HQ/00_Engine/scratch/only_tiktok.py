import os
import sys

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)
os.chdir(ROOT_DIR)

from social_publisher import SocialPublisher

def main():
    publisher = SocialPublisher()
    video_path = r"C:\Users\Curtis\Desktop\short .mov"
    tiktok_title = "The Silent GLP-1 Muscle Leak! #GLP1 #Sarcopenia #MuscleLoss #OzempicWeightLoss #PeptideProtocols #MenOver40 #LongevityBuilder #SquamishWellness #KeystoneProtocols #Biohacking"
    
    print("🚀 Publishing local desktop video to TikTok...")
    tiktok_res = publisher.publish_to_tiktok(
        brand="recomposition",
        title=tiktok_title,
        video_url=video_path,
        dry_run=False,
        cover_timestamp_ms=39000
    )
    print(f"TikTok Result: {tiktok_res}")

if __name__ == "__main__":
    main()
