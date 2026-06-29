"""Pull competitor tags, posting times, and metadata from top peptide/GLP-1 videos."""
import yt_dlp
import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COMPETITOR_VIDEOS = [
    "https://www.youtube.com/watch?v=OfcexE9s4yw",  # Thomas DeLauer - Wolverine Stack
    "https://www.youtube.com/watch?v=rOGRiEtMKqw",  # Surgeon Explains BPC-157/TB-500
    "https://www.youtube.com/watch?v=HIrI8STJPJo",  # Talking With Docs - BPC-157
    "https://www.youtube.com/watch?v=FY-pLnzv5YE",  # Matt Kaeberlein + DeLauer full ep
]

all_tags = {}
all_data = []

for url in COMPETITOR_VIDEOS:
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            data = {
                "title": info.get("title"),
                "channel": info.get("uploader"),
                "views": info.get("view_count"),
                "likes": info.get("like_count"),
                "upload_date": info.get("upload_date"),
                "duration": info.get("duration"),
                "tags": info.get("tags", []),
                "description_first_300": info.get("description", "")[:300],
            }
            all_data.append(data)
            
            # Aggregate tags
            for tag in info.get("tags", []):
                tag_lower = tag.lower()
                all_tags[tag_lower] = all_tags.get(tag_lower, 0) + 1
            
            print(f"--- {data['channel']}: {data['title'][:60]} ---")
            print(f"  Views: {data['views']:,} | Likes: {data['likes']:,}")
            print(f"  Upload: {data['upload_date']} | Duration: {data['duration']}s")
            print(f"  Tags ({len(data['tags'])}): {', '.join(data['tags'][:15])}")
            print()
    except Exception as e:
        print(f"ERROR on {url}: {e}")
        print()

# Show aggregated top tags
print("\n=== AGGREGATED COMPETITOR TAGS (sorted by frequency) ===")
sorted_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)
for tag, count in sorted_tags[:30]:
    print(f"  [{count}x] {tag}")

# Save full report
with open("competitor_intel.json", "w", encoding="utf-8") as f:
    json.dump({
        "videos": all_data,
        "aggregated_tags": dict(sorted_tags),
    }, f, indent=2, ensure_ascii=False)

print("\nSaved to competitor_intel.json")
