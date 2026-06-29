# 🎬 DAVINCI RESOLVE SUBTITLE FIX WORKFLOW (AUTOMATED)

## 📋 OVERVIEW
This workflow documents the automated programmatic approach to fixing broken AI-generated subtitles (e.g., misspellings of drug names like "Mounjaro", "tirzepatide", "retatrutide") and removing isolated speaker names (e.g., "Wayne", "Victoria") from DaVinci Resolve timelines, while preserving the "bouncing karaoke style" timing perfectly.

Because the DaVinci Resolve Python API does not support editing subtitle text directly via `item.SetName()`, the only reliable way is to export the timeline's subtitle track to an `.srt` file, clean it using regex/dictionary replacements, delete the old subtitles, and append the new `.srt` clip at `timeline.GetStartFrame()`.

---

## 🛠️ AUTOMATED PROCESS (2-STEP EXECUTION)

We have automated this into two simple Python scripts located in `scratch/`.

### 1️⃣ STEP 1: Export and Clean Subtitles (`export_manual_srt_short.py`)
This script reads subtitles from track 1, converts their frame-based timings into SRT timecodes (offset by the timeline's start frame to prevent sync drift), and applies cleanups.

Create `scratch/export_manual_srt_short.py`:
```python
import os
import sys
import re

def init_resolve():
    os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    os.environ["PYTHONPATH"] = os.environ["RESOLVE_SCRIPT_API"] + r"\Modules"
    sys.path.append(os.environ["RESOLVE_SCRIPT_API"] + r"\Modules")

try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    init_resolve()
    import DaVinciResolveScript as dvr_script

resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

fps = float(timeline.GetSetting("timelineFrameRate")) if timeline.GetSetting("timelineFrameRate") else 24.0
start_frame = timeline.GetStartFrame()

def frames_to_srt_time(f):
    offset = f - start_frame
    total_seconds = offset / fps
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int(round((total_seconds - int(total_seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

items = timeline.GetItemListInTrack("subtitle", 1)
if not items:
    print("No subtitle items found.")
    sys.exit()

srt_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\captions_fixed_short.srt"

# Clean spelling/wording errors here:
replacements = {
    "tears": "tirz-",
    "eptide and": "epatide and",
    "red a": "reta-",
    "knife. I": "knife.",
    "Break down": "I break down"
}

with open(srt_path, "w", encoding="utf-8") as f:
    srt_index = 1
    for item in items:
        text = item.GetName()
        original_text = text
        
        # Apply word fixes
        for target, replacement in replacements.items():
            if target in text:
                text = text.replace(target, replacement)
        
        # Remove trailing speaker name labels
        text = re.sub(r'\b(Wayne|Victoria)\b[^\w]*$', '', text, flags=re.IGNORECASE).strip()
        
        if not text:
            continue
            
        start_time = frames_to_srt_time(item.GetStart())
        end_time = frames_to_srt_time(item.GetEnd())
        
        f.write(f"{srt_index}\n{start_time} --> {end_time}\n{text}\n\n")
        srt_index += 1

print(f"Wrote cleaned subtitles to {srt_path}")
```

Run step 1:
```bash
python scratch/export_manual_srt_short.py
```

---

### 2️⃣ STEP 2: Clear, Import, and Inject (`import_and_place_subtitles_short.py`)
This script programmatically deletes the corrupted clips, imports the fixed `.srt` directly into the Media Pool, and appends it to track 1 at the precise start frame.

Create `scratch/import_and_place_subtitles_short.py`:
```python
import os
import sys

def init_resolve():
    os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    os.environ["PYTHONPATH"] = os.environ["RESOLVE_SCRIPT_API"] + r"\Modules"
    sys.path.append(os.environ["RESOLVE_SCRIPT_API"] + r"\Modules")

try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    init_resolve()
    import DaVinciResolveScript as dvr_script

resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()
media_pool = project.GetMediaPool()

# 1. Delete original subtitle track items
items = timeline.GetItemListInTrack("subtitle", 1)
if items:
    timeline.DeleteClips(items)
    print(f"Deleted {len(items)} original subtitle clips.")

# 2. Import the new clean SRT clip
srt_path = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scratch\captions_fixed_short.srt"
imported = media_pool.ImportMedia([srt_path])
if not imported:
    print("Error: Failed to import SRT.")
    sys.exit()

srt_clip = imported[0]

# 3. Append to timeline at the exact start frame to prevent timing shift
start_time = timeline.GetStartFrame()
clip_info = {
    "mediaPoolItem": srt_clip,
    "recordFrame": start_time
}
result = media_pool.AppendToTimeline([clip_info])
print(f"Append result: {result}")
```

Run step 2:
```bash
python scratch/import_and_place_subtitles_short.py
```

---

## 💡 KEY REVELATIONS FOR PERFECT EXECUTION
- **Timeline start-frame offset**: Resolve timelines do not start at 0. Subtracting `timeline.GetStartFrame()` (often frame `86400` or 1 hour) before doing SRT timecode calculations ensures captions are perfectly synchronized with the timeline start frame.
- **Direct import & return**: Using `media_pool.ImportMedia([srt_path])` returns the newly imported `MediaPoolItem` object directly, so you don't need to query the entire media pool folders to find it.
- **AppendToTimeline list of dicts**: Providing `AppendToTimeline([{"mediaPoolItem": srt_clip, "recordFrame": start_time}])` puts the clip at the exact frame position instead of appending it to the very end of the timeline.

---
📁 **See also:** ← Directory Index
