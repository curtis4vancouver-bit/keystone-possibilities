import os
import sys

# Setup imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MASTER_BRAIN_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, MASTER_BRAIN_DIR)
os.chdir(MASTER_BRAIN_DIR)

from youtube_api_manager import YouTubeAPIManager

def upload_short():
    video_path = r"C:\Users\Curtis\Desktop\short 20.mov"
    thumbnail_path = r"C:\Users\Curtis\Desktop\thumb.jpeg"
    
    # We are uploading to Protocols channel, so we need youtube_token.json
    token_file = os.path.join(MASTER_BRAIN_DIR, "youtube_token.json")
    
    manager = YouTubeAPIManager(token_file=token_file)
    if not manager.youtube:
        print("Failed to authenticate YouTube API manager.")
        sys.exit(1)
        
    title = "Why Your Belly Fat Won't Budge (The Fix)"
    
    description = """Are you hitting the gym but still carrying a stubborn gut? Visceral fat doesn't behave like normal subcutaneous fat—it acts like an endocrine organ that poisons your metabolism. In this short, we break down why you need to repair your biological infrastructure and how growth hormone secretagogues like CJC-1295 and Tesamorelin act as the heavy machinery to demolish visceral fat. Tap the related video link on screen for the full 15-minute protocol breakdown!

---
🏗️ Building Something? Custom homes, multiplexes, and commercial developments
in the Sea-to-Sky Corridor: https://keystonepossibilities.ca

🧬 Explore the full wellness research library: https://keystoneprotocols.ca

🎵 Training Soundscapes — Lock in your deep-focus workout with the official
Keystone Recomposition Deep House Mix: https://www.youtube.com/watch?v=LNlAiAu5YOo

---
🔗 CONNECT:
• TikTok: https://www.tiktok.com/@keystonerecomposition
• Instagram: https://www.instagram.com/keystonerecomposition
• Facebook: https://www.facebook.com/166025896601563
• Spotify: https://open.spotify.com/artist/52v3Qe6Jo0hg764driOl5Y
• LinkedIn: https://www.linkedin.com/in/stevenson4vancouver

#VisceralFat #BodyRecomposition #PeptideProtocols
---
⚖️ MEDICAL DISCLAIMER:
The information in this video is for scientific study, educational analysis,
and general research purposes only. It does not constitute medical advice,
diagnosis, or treatment. Consult your physician before starting any new protocol.

🤖 SYNTHETIC MEDIA / AI DIGITAL TWIN DISCLOSURE:
The host is a photorealistic digital representation of Wayne Stevenson,
synthesized using advanced visual networks. All personal health metrics,
real B-roll footage, and audio journals are authentic."""

    tags = [
        "CJC-1295", 
        "Tesamorelin", 
        "Visceral Fat", 
        "Belly Fat Loss", 
        "Peptides for fat loss", 
        "Body Recomposition", 
        "GLP-1 alternatives", 
        "Men over 40 fitness", 
        "Sarcopenia", 
        "Biohacking"
    ]
    
    # Upload video
    response = manager.upload_video(
        file_path=video_path,
        title=title,
        description=description,
        tags=tags,
        category_id="27", # Education
        privacy_status="private" # Upload as private first so user can link the related long-form video in YouTube Studio and check it
    )
    
    if response:
        video_id = response.get('id')
        print(f"Uploaded successfully. Video ID: {video_id}")
        
        # Upload the extracted thumbnail
        thumb_response = manager.set_thumbnail(video_id, thumbnail_path)
        if thumb_response:
            print("Thumbnail set successfully.")
        else:
            print("Failed to set thumbnail.")
            
if __name__ == "__main__":
    upload_short()
