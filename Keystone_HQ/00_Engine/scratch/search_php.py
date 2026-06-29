with open("scratch/remote_functions.php", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Search for functions or filters related to rankmath, sitemap, video, or schema
import re
pattern = re.compile(r"rank_math|sitemap|video|schema|wp_head", re.IGNORECASE)

matches = []
for idx, line in enumerate(lines):
    if pattern.search(line):
        matches.append((idx + 1, line.strip()))

print(f"Found {len(matches)} matching lines:")
for num, content in matches[:100]:
    print(f"Line {num}: {content[:120]}")
if len(matches) > 100:
    print(f"... and {len(matches) - 100} more matches.")
