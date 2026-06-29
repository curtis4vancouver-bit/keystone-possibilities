import os
import json

brain_dir = r"C:\Users\Curtis\.gemini\antigravity\brain"

def main():
    matching_brains = []
    for item in os.listdir(brain_dir):
        item_path = os.path.join(brain_dir, item)
        if os.path.isdir(item_path):
            transcript_path = os.path.join(item_path, ".system_generated", "logs", "transcript.jsonl")
            if os.path.exists(transcript_path):
                try:
                    with open(transcript_path, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            if "gemini.google.com" in line:
                                matching_brains.append(item)
                                break
                except:
                    pass
    
    print("Brains containing gemini.google.com:")
    for brain in matching_brains:
        print(brain)

if __name__ == "__main__":
    main()
