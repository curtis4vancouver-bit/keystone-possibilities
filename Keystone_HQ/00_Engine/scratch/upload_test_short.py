import sys
import os

# Set paths
SCRIPT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.insert(0, SCRIPT_DIR)

from youtube_api_manager import YouTubeAPIManager

video_path = r"c:\Users\Curtis\Desktop\Keystone Content Engine\02_Shorts\Short_1_Staging\short.mov"

title = "Squamish Permit Delays: Why Your Custom Build Is Stuck 😬"

description = (
    "Building a custom home in Squamish? The permits aren't the only thing delayed—new growth charges "
    "and structural shifts are squeezing Vancouver custom builds. Here is how high-end project management "
    "keeps your build moving when municipal backlogs freeze the site.\n\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "🏗️ KEYSTONE POSSIBILITIES — Luxury Construction & Project Management\n"
    "🔬 Health & Protocols → https://www.youtube.com/@KeystoneProtocols\n"
    "🎵 Focus Music for Builders → https://www.youtube.com/@KeyStoneRecomposition\n"
    "🌐 Website → https://www.keystonepossibilities.ca\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    "#squamish #construction #vancouverbuilder #customhome #projectmanagement #keystonepossibilities #shorts"
)

tags = [
    "luxury construction Vancouver", "custom home builder", "project management Vancouver",
    "BC builder", "luxury renovation", "North Shore construction", "West Vancouver homes",
    "construction project manager", "Keystone Possibilities", "luxury home builder BC",
    "Vancouver renovation contractor", "custom build Vancouver", "Squamish permits",
    "Squamish growth charges", "Squamish development"
]

print("=== Starting YouTube Upload ===")
manager = YouTubeAPIManager(token_file=os.path.join(SCRIPT_DIR, "youtube_token.json"))

if not manager.youtube:
    print("Error: Could not initialize YouTube API Manager.")
    sys.exit(1)

# Upload as PUBLIC
response = manager.upload_video(
    file_path=video_path,
    title=title,
    description=description,
    tags=tags,
    category_id="22",  # People & Blogs
    privacy_status="public"
)

if response:
    print("SUCCESS")
    print(f"Video ID: {response.get('id')}")
else:
    print("FAILED")
