import json
import os
import subprocess
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def decode_and_process(page_id, domain, topic_name):
    json_path = os.path.join(PROJECT_ROOT, "scratch", f"temp_report_{page_id}.json")
    txt_path = os.path.join(PROJECT_ROOT, "scratch", f"temp_report_{page_id}.txt")
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return False
        
    print(f"Decoding {json_path}...")
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            content = json.load(f)
        except Exception as e:
            print(f"Failed to parse JSON: {e}. Reading raw content.")
            f.seek(0)
            content = f.read()
            
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Decoded to {txt_path} ({len(content)} chars)")
    
    # Run process_completed_topic.py
    process_script = os.path.join(PROJECT_ROOT, "scratch", "process_completed_topic.py")
    print(f"Running completion processor for topic: '{topic_name}'")
    
    result = subprocess.run(
        [sys.executable, process_script, domain, topic_name, txt_path],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    
    return result.returncode == 0

def main():
    topic_9 = (
        "YouTube music channel growth strategy for independent artists in 2026: "
        "How do independent musicians grow their YouTube channels and drive Spotify/Apple Music streams? "
        "Cover Content ID, YouTube Music integration, lyrics videos, visualizer videos, "
        "behind-the-scenes content, playlist placement strategies, and whether YouTube Shorts "
        "work for music discovery. Include automation approaches for publishing music content across platforms."
    )
    
    topic_10 = (
        "YouTube competitor analysis methodology for niche channels in 2026: "
        "How to systematically analyze competing channels in construction PM, wellness/peptide, and music niches? "
        "Cover tools for competitor research (VidIQ, TubeBuddy, Social Blade alternatives), "
        "metrics to track, content gap analysis, keyword opportunity identification, "
        "and how to reverse-engineer successful competitors' strategies. "
        "Include automation approaches using the YouTube Data API."
    )
    
    success_9 = decode_and_process(9, "YOUTUBE_GROWTH", topic_9)
    success_10 = decode_and_process(10, "YOUTUBE_GROWTH", topic_10)
    
    if success_9 and success_10:
        print("Both pages processed successfully!")
    else:
        print("Some errors occurred during processing.")
        sys.exit(1)

if __name__ == "__main__":
    main()
