import os
import sys

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, ROOT_DIR)
os.chdir(ROOT_DIR)

from social_publisher import SocialPublisher

def main():
    publisher = SocialPublisher()
    video_path = r"C:\Users\Curtis\Desktop\short .mov"

    # Description structured exactly to your guidelines:
    # 1. Primary hook/SEO description at the very top
    # 2. Medical disclaimer in the middle
    # 3. AI twin disclaimer below it
    # 4. Hashtags
    # 5. Connect / Protocols links at the very bottom
    description = """You are losing weight on Mounjaro but destroying your structural foundation. In the clinical trials up to 40% of weight lost was lean muscle, not fat. I lost 48 pounds on Mounjaro, but my strength was tanking, so I built a 4-pillar protocol to stop the muscle wasting immediately.

⚠️ Medical Disclaimer: I am not a doctor. This video is a personal case study and should not be taken as medical advice. Always consult your physician before making any changes to your health protocol.

🤖 Note: Wayne runs an AI Digital Twin avatar (generated via HeyGen) as the primary on-camera host for all Recomposition video content.

#Mounjaro #MuscleLoss #GLP1 #WeightLossJourney #Recomposition #FatLoss #FitnessOver40 #Peptides

🔗 Connect & Learn More:
📘 The Protocol & Website: https://keystonerecomposition.com
▶️ The Protocol (YouTube): https://www.youtube.com/@keystonerecomposition
🎵 My Music Channel: https://www.youtube.com/@waynestevenson-y6o"""

    # TikTok caption (title hook + hashtags)
    tiktok_title = "The Silent GLP-1 Muscle Leak! #GLP1 #Sarcopenia #MuscleLoss #OzempicWeightLoss #PeptideProtocols #MenOver40 #LongevityBuilder #SquamishWellness #KeystoneProtocols #Biohacking"

    print("🚀 STARTING MULTI-PLATFORM DISTRIBUTION Sprint (Recomposition Brand)...")

    # 1. Facebook Page (Upload Video with Description)
    print("\n--- [1/3] Publishing to Facebook Page (Recomposition) ---")
    fb_res = publisher.publish_to_meta_facebook(brand="recomposition", text=description, media_url=video_path, dry_run=False)
    print(f"Facebook Result: {fb_res}")

    # 2. Instagram Reels (Upload Video Container, Poll until finished, then Publish)
    print("\n--- [2/3] Publishing to Instagram Reels (Recomposition) ---")
    ig_res = publisher.publish_to_meta_instagram(brand="recomposition", caption=description, image_url=video_path, dry_run=False)
    print(f"Instagram Result: {ig_res}")

    # 3. TikTok Business (Upload Video with Custom Cover Image Offset in the last 2 seconds)
    print("\n--- [3/3] Publishing to TikTok (Recomposition) ---")
    # Video duration is 40.08s, so 39000 ms (39s) is perfectly inside the final 2-second thumbnail window
    tiktok_res = publisher.publish_to_tiktok(brand="recomposition", title=tiktok_title, video_url=video_path, dry_run=False, cover_timestamp_ms=39000)
    print(f"TikTok Result: {tiktok_res}")

    print("\n🏁 DISTRIBUTION SPRINT COMPLETE!")

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    main()
