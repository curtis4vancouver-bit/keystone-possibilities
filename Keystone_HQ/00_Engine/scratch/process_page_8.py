import json
import os
import subprocess
import sys

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def main():
    json_path = os.path.join(PROJECT_ROOT, "scratch", "temp_report_8.json")
    txt_path = os.path.join(PROJECT_ROOT, "scratch", "temp_report_8.txt")
    
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
        
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
    domain = "YOUTUBE_GROWTH"
    topic = (
        "YouTube AI-generated content disclosure requirements and policies in mid-2026: "
        "What are the CURRENT rules for disclosing AI-generated content on YouTube? "
        "Cover which types of AI content require disclosure (AI avatars, AI voiceover, AI images, AI scripts), "
        "where disclosures must appear, penalties for non-compliance, and best practices for channels "
        "that heavily use AI in their production pipeline. Include specific wording templates that satisfy YouTube's requirements."
    )
    
    print(f"Running completion processor for topic: '{topic}'")
    result = subprocess.run(
        [sys.executable, process_script, domain, topic, txt_path],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)
    
    if result.returncode == 0:
        print("Page 8 processed successfully!")
    else:
        print("Page 8 processing failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
