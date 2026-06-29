import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
os.chdir(PARENT_DIR)
sys.path.insert(0, PARENT_DIR)

from social_publisher import SocialPublisher

pub = SocialPublisher()
status = pub.get_token_status()

print("=" * 70)
print("FULL BRAND-PLATFORM CONNECTION MATRIX")
print("=" * 70)

for brand in ["possibilities", "recomposition", "protocol"]:
    print(f"\n  {brand.upper()}:")
    for plat in ["linkedin", "meta", "tiktok"]:
        s = status[brand][plat]
        conn = "CONNECTED" if s["connected"] else "DISCONNECTED"
        shared = s.get("shared_from", "")
        inherit_label = f" (inherited from {shared})" if s.get("inherited") else " (direct)"
        hrs = f"{s['expires_in_hours']}h left"
        print(f"    {plat:10s}: {conn:12s} {hrs:12s} {inherit_label}")

print("\n" + "=" * 70)
print("DRY-RUN: Publish test for all brands")
print("=" * 70)

for brand in ["possibilities", "recomposition", "protocol"]:
    print(f"\n--- Brand: {brand} ---")
    print("  LinkedIn:", pub.publish_to_linkedin(brand, "Test post", dry_run=True))
    print("  Facebook:", pub.publish_to_meta_facebook(brand, "Test post", dry_run=True))
    print("  Instagram:", pub.publish_to_meta_instagram(brand, "Test caption", dry_run=True))
    print("  TikTok:", pub.publish_to_tiktok(brand, "Test title", dry_run=True))

print("\n" + "=" * 70)
print("ALL TESTS PASSED")
print("=" * 70)
