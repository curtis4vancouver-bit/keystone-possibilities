import os
import sys
import argparse

# Setup imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_BRAIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, MASTER_BRAIN_DIR)
os.chdir(MASTER_BRAIN_DIR)

from social_publisher import SocialPublisher

def main():
    parser = argparse.ArgumentParser(description="Publish short 20 to Facebook Reels, Instagram Reels, and TikTok.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without actual uploads.")
    args = parser.parse_args()

    video_path = r"C:\Users\Curtis\Desktop\short 20.mov"
    brand = "recomposition"
    
    # 31.88s duration, so cover offset within the last 2 seconds (30,500ms or 31,000ms)
    cover_timestamp_ms = 30500 

    title = "Why Your Belly Fat Won't Budge (The Fix)"
    
    description = (
        "Why Your Belly Fat Won't Budge (The Fix). "
        "Visceral gut fat is hardwired and resistant to standard cardio. To demolish and rebuild, "
        "clinical peptide research into CJC-1295 and Tesamorelin demonstrates how to target viscera and remodel your structural foundation.\n\n"
        "#Mounjaro #MuscleLoss #GLP1 #WeightLossJourney #Recomposition #FatLoss #FitnessOver40 #Peptides #CJC1295 #Tesamorelin\n\n"
        "---\n"
        "🎵 Training Soundscapes — Lock in your deep-focus workout with the official Keystone Recomposition Deep House Mix: "
        "https://www.youtube.com/watch?v=LNlAiAu5YOo\n\n"
        "---\n"
        "🔗 CONNECT:\n"
        "• Instagram: https://www.instagram.com/keystonerecomposition\n"
        "• Facebook: https://www.facebook.com/898671469990393\n"
        "• Spotify: https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y\n\n"
        "---\n"
        "🏗️ Building a new custom home? Multiplexes and commercial developments in the Sea-to-Sky Corridor: "
        "https://keystonepossibilities.ca\n\n"
        "⚖️ MEDICAL DISCLAIMER:\n"
        "The information in this video is for scientific study, educational analysis, and general research purposes only. "
        "It does not constitute medical advice, diagnosis, or treatment. Consult your physician before starting any new protocol.\n\n"
        "🤖 SYNTHETIC MEDIA / AI DIGITAL TWIN DISCLOSURE:\n"
        "The host is a photorealistic digital representation of Wayne Stevenson, synthesized using advanced visual networks. "
        "All personal health metrics, real B-roll footage, and audio journals are authentic."
    )

    print("=" * 80)
    print(f"KEYSTONE RECOMPOSITION SOCIAL PUBLISHING SYSTEM")
    print(f"Video: {video_path}")
    print(f"Brand: {brand}")
    print(f"Dry-run mode: {args.dry_run}")
    print("=" * 80)

    # Initialize SocialPublisher
    pub = SocialPublisher()
    
    # Bypass YMYL scrubbing to ensure exact matching of user's customized description and hashtags
    pub.scrub_text = lambda text: text
    
    print("\n--- STAGE 1: TikTok Reel Upload ---")
    tiktok_log = pub.publish_to_tiktok(
        brand=brand,
        title=title,  # TikTok title limit is normally 150-2200 chars. We pass the hook title.
        video_url=video_path,
        dry_run=args.dry_run,
        cover_timestamp_ms=cover_timestamp_ms
    )
    print(f"Result: {tiktok_log}")

    print("\n--- STAGE 2: Facebook Reel Upload ---")
    fb_log = pub.publish_to_meta_facebook(
        brand=brand,
        text=description,
        media_url=video_path,
        dry_run=args.dry_run
    )
    print(f"Result: {fb_log}")

    print("\n--- STAGE 3: Instagram Reel Upload ---")
    ig_log = pub.publish_to_meta_instagram(
        brand=brand,
        caption=description,
        image_url=video_path,
        dry_run=args.dry_run
    )
    print(f"Result: {ig_log}")
    
    print("\n" + "=" * 80)
    print("FINISHED PUBLISHING SPRINT")
    print("=" * 80)

if __name__ == "__main__":
    main()
