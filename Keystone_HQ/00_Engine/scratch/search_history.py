import os
import json

transcript_path = r"C:\Users\Curtis\.gemini\antigravity\brain\69f4ab04-3dc1-4dfb-9eff-fd3ab39fafcf\.system_generated\logs\transcript.jsonl"

if not os.path.exists(transcript_path):
    print("Transcript path does not exist!")
    # Let's list the parent directory to see what it is
    parent = os.path.dirname(transcript_path)
    if os.path.exists(parent):
        print(f"Parent directory {parent} exists. Files in it:")
        print(os.listdir(parent))
    else:
        print(f"Parent directory {parent} does not exist!")
    exit()

print("Transcript found! Searching...")

terms = ["functions.php", "update_page_sovereign", "deploy", "wp-admin", "theme-editor"]

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        try:
            step = json.loads(line)
            content = str(step)
            for term in terms:
                if term in content:
                    print(f"Line {line_idx} contains '{term}':")
                    # print type and first 300 chars of content
                    print(f"  Type: {step.get('type')}, Status: {step.get('status')}")
                    print(f"  Tool calls: {step.get('tool_calls')}")
                    snippet = content[:500]
                    print(f"  Snippet: {snippet}...\n")
                    break
        except Exception as e:
            print(f"Error parsing line {line_idx}: {e}")
