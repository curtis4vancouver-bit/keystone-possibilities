import os
import sys

# Setup environment
os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"

modules_path = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)

if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

import DaVinciResolveScript as dvr
resolve = dvr.scriptapp("Resolve")
pm = resolve.GetProjectManager()
project = pm.GetCurrentProject()
timeline = project.GetCurrentTimeline()

print(f"Timeline Name: {timeline.GetName()}")
print(f"FPS: {timeline.GetSetting('timelineFrameRate')}")

v1_items = timeline.GetItemListInTrack("video", 1)
v2_items = timeline.GetItemListInTrack("video", 2)

print(f"Track V1 (Video Clips) Count: {len(v1_items)}")
print(f"Track V2 (B-roll Images) Count: {len(v2_items)}")

# Print timing for the first few transitions
print("\n--- Timing Verification (First 5 clips) ---")
for idx in range(min(5, len(v2_items))):
    v1_clip = v1_items[idx]
    v2_clip = v2_items[idx]
    
    v1_end = v1_clip.GetEnd()
    v2_start = v2_clip.GetStart()
    v2_end = v2_clip.GetEnd()
    
    # Calculate offset
    offset = v1_end - v2_start
    duration = v2_end - v2_start
    
    print(f"B-roll {idx+1}:")
    print(f"  Video {idx+1} ends at frame: {v1_end} (approx {v1_end/24.0:.2f}s)")
    print(f"  B-roll starts at frame: {v2_start} (approx {v2_start/24.0:.2f}s)")
    print(f"  B-roll ends at frame: {v2_end} (approx {v2_end/24.0:.2f}s)")
    print(f"  Overlap before transition: {offset} frames ({offset/24.0:.2f}s)")
    print(f"  Total B-roll duration: {duration} frames ({duration/24.0:.2f}s)")
