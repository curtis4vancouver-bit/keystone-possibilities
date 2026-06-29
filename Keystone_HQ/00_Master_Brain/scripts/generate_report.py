import os
import re

script_path = r'C:\Users\Curtis\.gemini\antigravity\brain\38bad2b8-a186-4461-a6cb-22c340307c47\SCRIPT_008_KLOW_GLOW_ZINC_TRAP.md'
broll_dir = r'C:\Users\Curtis\Desktop\it\b roll'
artifact_path = r'C:\Users\Curtis\.gemini\antigravity\brain\38bad2b8-a186-4461-a6cb-22c340307c47\broll_verification.md'

with open(script_path, encoding='utf-8') as f:
    lines = f.readlines()

prompts = []
capture = False
for line in lines:
    if 'B-ROLL IMAGE PROMPTS' in line:
        capture = True
    elif 'THUMBNAIL PROMPTS' in line:
        capture = False
    elif capture and not line.startswith('```') and len(line.strip()) > 10:
        prompts.append(line.strip())

files = [f for f in os.listdir(broll_dir) if f.lower().endswith(('.png', '.jpeg', '.jpg'))]

def sort_key(x):
    match = re.search(r'(\d+)', x)
    return int(match.group(1)) if match else 999

files.sort(key=sort_key)

with open(artifact_path, 'w', encoding='utf-8') as f:
    f.write('---\n')
    f.write('RequestFeedback: false\n')
    f.write('Summary: B-Roll Visual Verification Report\n')
    f.write('UserFacing: true\n')
    f.write('---\n\n')
    f.write('# B-Roll Visual Verification Report\n\n')
    f.write('Scroll through this report to visually verify that every single B-roll image matches its intended prompt from the script.\n\n')
    
    for i, prompt in enumerate(prompts):
        file_name = files[i] if i < len(files) else 'Missing'
        file_path = os.path.join(broll_dir, file_name)
        # Using forward slashes for markdown image paths
        file_path_md = file_path.replace('\\', '/')
        f.write(f'### Prompt {i+1}\n')
        f.write(f'*{prompt}*\n\n')
        f.write(f'**File:** `{file_name}`\n\n')
        if file_name != 'Missing':
            f.write(f'![B-Roll {i+1}](file:///{file_path_md})\n\n')
        f.write('---\n\n')

print("Report generated successfully.")
