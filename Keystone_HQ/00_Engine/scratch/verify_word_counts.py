import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

script_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Research_Archives\SCRIPT_001_HEYGEN_OMINI_SEGMENTS.md"

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all dialogue lines
dialogues = re.findall(r'`Wayne says: (.+?)`', content)

total_words = 0
issues = []
for i, d in enumerate(dialogues, 1):
    # Remove ellipses for word counting
    clean = d.replace('...', ' ')
    words = len(clean.split())
    total_words += words
    flag = ""
    if words < 25:
        flag = " ⚠️ LOW"
        issues.append(i)
    elif words > 32:
        flag = " ⚠️ HIGH"
        issues.append(i)
    print(f"CLIP {i:03d}: {words} words{flag}")

print(f"\n--- SUMMARY ---")
print(f"Total clips: {len(dialogues)}")
print(f"Total words: {total_words}")
print(f"Average words/clip: {total_words / len(dialogues):.1f}")
print(f"Estimated duration at 2.5 words/sec: {total_words / 2.5:.0f} seconds ({total_words / 2.5 / 60:.1f} minutes)")
print(f"Estimated duration at 3.0 words/sec: {total_words / 3.0:.0f} seconds ({total_words / 3.0 / 60:.1f} minutes)")
if issues:
    print(f"\nClips with potential issues: {issues}")
else:
    print("\nAll clips within 25-30 word target range!")
