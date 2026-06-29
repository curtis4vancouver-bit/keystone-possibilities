import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PARENT_DIR)
os.chdir(PARENT_DIR)

from video_hosting_bridge import list_hosted_media

print("Testing GCS bucket access...")
media = list_hosted_media()
print(f"GCS bucket accessible. Found {len(media)} existing files in social_media/.")
for m in media[:5]:
    print(f"  {m['name']} ({m['size_mb']}MB)")

print("\nGCS Bridge: READY")
