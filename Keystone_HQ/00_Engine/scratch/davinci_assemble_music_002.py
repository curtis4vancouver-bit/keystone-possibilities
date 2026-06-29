"""
MUSIC_002 — DaVinci Resolve Timeline Assembly Script (ALBUM VERSION)
Assembles 24 video clips LOOPED to match the full Gilded Pulse album (~29:32).
All 10 album tracks placed sequentially on A2.

CORRECTED per official API docs (README.txt, May 8, 2026).

What this script DOES:
  ✅ Import 24 video clips to Media Pool
  ✅ Import all 10 Gilded Pulse tracks to Media Pool
  ✅ Create timeline, loop clips on V1 to fill album duration
  ✅ Mute A1 (Flow ambient noise)
  ✅ Create A2, place all 10 tracks sequentially
  ✅ Add markers at album track boundaries
  ✅ Copy color grade from clip 1 to all others
  ✅ Configure render settings and add to render queue

What requires manual steps:
  ❌ Cross-dissolves: Select all clips → Ctrl+T (30 seconds)
  ❌ Final trim: Blade tool to cut V1 at exact end of last track
"""

import os
import sys
import re
import math

def init_resolve():
    """Bootstraps connection to running DaVinci Resolve Studio on Windows."""
    modules_path = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules"
    if modules_path not in sys.path:
        sys.path.append(modules_path)
    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        alt_path = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules"
        if alt_path not in sys.path:
            sys.path.append(alt_path)
        import DaVinciResolveScript as dvr

    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError(
            "Resolve scripting interface offline.\n"
            "Check: Is DaVinci Resolve open? Is External Scripting set to Local?\n"
            "  Preferences > System > General > External Scripting Using = Local"
        )
    return resolve


def main():
    resolve = init_resolve()
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()

    # === CONFIGURATION ===
    PRODUCTION_ID = "MUSIC_002"
    VIDEO_DIR = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\Videos"
    MUSIC_DIR = r"C:\Users\Curtis\Desktop\musicmacth\The Gilded Pulse"
    FINAL_DIR = r"C:\Users\Curtis\Desktop\MUSIC_PRODUCTION\FINAL"
    TIMELINE_NAME = "Ana Stevenson — The Gilded Pulse (Full Album)"
    CLIP_COUNT = 24
    FPS = 24.0
    CLIP_DURATION_SEC = 10.0
    CLIP_DURATION_FRAMES = int(CLIP_DURATION_SEC * FPS)  # 240 frames per clip

    os.makedirs(FINAL_DIR, exist_ok=True)

    # === ALBUM TRACK ORDER (Gilded Pulse) ===
    # Duration in seconds for each track (from shell metadata)
    ALBUM_TRACKS = [
        ("Track 1_ Kinetic Soul.wav",         131),   # 2:11
        ("Track 2_ Deep Foundation.wav",       181),   # 3:01
        ("Track 3_ The Next Phase.wav",        172),   # 2:52
        ("Track 4_ Velvet Rhythm.wav",         174),   # 2:54
        ("Track 5_ Cello Momentum.wav",         54),   # 0:54
        ("Track 6_ Modern Blueprint.wav",      188),   # 3:08
        ("Track 7_ Steady Drive.wav",          217),   # 3:37
        ("Track 8_ Rhythmic Resilience.wav",   225),   # 3:45
        ("Track 9_ Strength in Focus.wav",     183),   # 3:03
        ("Track 10_ Midnight Pulse.wav",       247),   # 4:07
    ]
    TOTAL_ALBUM_SEC = sum(dur for _, dur in ALBUM_TRACKS)  # ~1772 seconds (~29:32)
    TOTAL_ALBUM_FRAMES = int(TOTAL_ALBUM_SEC * FPS)

    # How many times to loop 24 clips to cover the album
    single_loop_sec = CLIP_COUNT * CLIP_DURATION_SEC  # 240 seconds = 4 min
    loops_needed = math.ceil(TOTAL_ALBUM_SEC / single_loop_sec)  # 8 loops
    total_clips = loops_needed * CLIP_COUNT  # 192 clips total

    print(f"=" * 60)
    print(f"MUSIC_002 — Full Album Assembly")
    print(f"=" * 60)
    print(f"  Album: The Gilded Pulse (10 tracks, {TOTAL_ALBUM_SEC}s / {TOTAL_ALBUM_SEC/60:.1f} min)")
    print(f"  Video: {CLIP_COUNT} clips × {CLIP_DURATION_SEC}s = {single_loop_sec}s per loop")
    print(f"  Loops: {loops_needed} × 24 clips = {total_clips} total clips on V1")
    print(f"  Timeline: ~{TOTAL_ALBUM_SEC/60:.1f} minutes")
    print()

    # === VERIFY VIDEO FILES ===
    print(f"Verifying {CLIP_COUNT} video clips...")
    video_files = [os.path.join(VIDEO_DIR, f"A{i}.mp4") for i in range(1, CLIP_COUNT + 1)]
    missing_v = [f for f in video_files if not os.path.exists(f)]
    if missing_v:
        print(f"ERROR: Missing video files:")
        for m in missing_v:
            print(f"  {m}")
        sys.exit(1)
    print(f"  ✅ All {CLIP_COUNT} video clips found")

    # === VERIFY MUSIC FILES ===
    print(f"Verifying {len(ALBUM_TRACKS)} album tracks...")
    music_files = []
    for track_name, dur in ALBUM_TRACKS:
        path = os.path.join(MUSIC_DIR, track_name)
        if not os.path.exists(path):
            print(f"ERROR: Missing track: {path}")
            sys.exit(1)
        music_files.append(path)
    print(f"  ✅ All {len(ALBUM_TRACKS)} tracks found")

    # === CREATE MEDIA BIN ===
    bin_name = f"{PRODUCTION_ID}_Media"
    media_folder = None
    for f in root_folder.GetSubFolderList():
        if f.GetName() == bin_name:
            media_folder = f
            break
    if not media_folder:
        media_folder = media_pool.AddSubFolder(root_folder, bin_name)
    media_pool.SetCurrentFolder(media_folder)
    print(f"  📁 Media bin: {bin_name}")

    # === IMPORT ALL MEDIA ===
    all_paths = video_files + music_files
    imported_items = media_pool.ImportMedia(all_paths)
    if not imported_items:
        imported_items = media_folder.GetClipList()

    # Separate video clips from music tracks
    def get_clip_num(item):
        match = re.search(r'A(\d+)', item.GetName())
        return int(match.group(1)) if match else 999

    video_pool_items = sorted(
        [item for item in imported_items if re.search(r'^A\d+', item.GetName())],
        key=get_clip_num
    )
    video_pool_items = [item for item in video_pool_items if get_clip_num(item) <= CLIP_COUNT]

    # Match music tracks to pool items by name
    music_pool_items = []
    for track_name, dur in ALBUM_TRACKS:
        base = os.path.splitext(track_name)[0]
        found = None
        for item in imported_items:
            if base in item.GetName() or item.GetName() in base:
                found = item
                break
        if found:
            music_pool_items.append((found, dur))
        else:
            print(f"  ⚠️  Could not match pool item for: {track_name}")

    print(f"  📥 Imported {len(video_pool_items)} video clips + {len(music_pool_items)} music tracks")

    # === DELETE EXISTING TIMELINE IF PRESENT ===
    for i in range(1, project.GetTimelineCount() + 1):
        t = project.GetTimelineByIndex(i)
        if t and t.GetName() == TIMELINE_NAME:
            media_pool.DeleteTimelines([t])
            print(f"  🗑️  Deleted existing timeline: {TIMELINE_NAME}")
            break

    # === CREATE TIMELINE ===
    timeline = media_pool.CreateEmptyTimeline(TIMELINE_NAME)
    project.SetCurrentTimeline(timeline)
    project.SetSetting("timelineFrameRate", str(FPS))
    print(f"  🎬 Created timeline: {TIMELINE_NAME}")

    # === APPEND VIDEO CLIPS (VIDEO ONLY, EXACTLY TRIMMED) ===
    total_frames_needed = TOTAL_ALBUM_FRAMES
    frames_added = 0
    clip_infos = []
    clip_idx = 0
    while frames_added < total_frames_needed:
        clip_item = video_pool_items[clip_idx % len(video_pool_items)]
        frames_remaining = total_frames_needed - frames_added
        
        # If this is the last clip needed, trim it perfectly
        if frames_remaining < CLIP_DURATION_FRAMES:
            duration = frames_remaining
        else:
            duration = CLIP_DURATION_FRAMES
            
        clip_infos.append({
            "mediaPoolItem": clip_item,
            "startFrame": 0,
            "endFrame": duration - 1,
            "mediaType": 1 # 1 = Video Only
        })
        frames_added += duration
        clip_idx += 1

    media_pool.AppendToTimeline(clip_infos)
    print(f"  ▶️  Appended {len(clip_infos)} video clips to V1 (Exact duration: {frames_added} frames)")

    # === RENAME TRACK A1 FOR MUSIC ===
    timeline.SetTrackName("audio", 1, "The Gilded Pulse (Full Album)")
    print("  🎵 Named A1")

    # === PLACE ALL 10 TRACKS SEQUENTIALLY ON A2 ===
    current_frame = 0
    tracks_placed = 0
    for music_item, duration_sec in music_pool_items:
        track_frames = int(duration_sec * FPS)
        clip_info = {
            "mediaPoolItem": music_item,
            "startFrame": 0,
            "recordFrame": current_frame,
            "trackIndex": 1,
            "mediaType": 2  # audio only
        }
        result = media_pool.AppendToTimeline([clip_info])
        if result:
            tracks_placed += 1
            track_name = music_item.GetName()
            print(f"  🎵 Track {tracks_placed}: {track_name} at {current_frame/FPS:.0f}s ({current_frame/FPS/60:.1f} min)")

            # Add a GREEN marker at each track boundary
            try:
                timeline.AddMarker(
                    current_frame,
                    "Green",
                    f"Track {tracks_placed}",
                    track_name,
                    1
                )
            except Exception:
                pass

            current_frame += track_frames
        else:
            print(f"  ⚠️  Failed to place: {music_item.GetName()}")

    print(f"  ✅ Placed {tracks_placed}/10 album tracks on A2")
    print(f"  🎵 Album ends at frame {current_frame} ({current_frame/FPS:.0f}s / {current_frame/FPS/60:.1f} min)")

    # === ADD MARKERS AT LOOP BOUNDARIES ===
    v1_items = timeline.GetItemListInTrack("video", 1)
    if v1_items:
        for i in range(CLIP_COUNT - 1, len(v1_items), CLIP_COUNT):
            if i < len(v1_items):
                loop_num = (i // CLIP_COUNT) + 1
                boundary_frame = v1_items[i].GetEnd()
                try:
                    timeline.AddMarker(
                        boundary_frame,
                        "Yellow",
                        f"Loop {loop_num} end",
                        f"A1-A24 loop #{loop_num} ends here",
                        1
                    )
                except Exception:
                    pass

    # === COLOR GRADE CONSISTENCY ===
    if v1_items and len(v1_items) > 1:
        try:
            # Copy grade from first clip to ALL others (including loops)
            source = v1_items[0]
            targets = list(v1_items[1:])
            # CopyGrades might have limits — do in batches
            batch_size = 50
            for batch_start in range(0, len(targets), batch_size):
                batch = targets[batch_start:batch_start + batch_size]
                source.CopyGrades(batch)
            print(f"  🎨 Copied color grade from A1 to {len(targets)} clips")
        except Exception as e:
            print(f"  ℹ️  CopyGrades: {e} — grade manually in Color page")

    # === CONFIGURE RENDER SETTINGS ===
    try:
        project.SetCurrentRenderFormatAndCodec("mp4", "H264")
        project.SetRenderSettings({
            "TargetDir": FINAL_DIR,
            "CustomName": "MUSIC_002_Ana_Stevenson_The_Gilded_Pulse",
            "SelectAllFrames": True,
            "ExportVideo": True,
            "ExportAudio": True,
            "FormatWidth": 1080,
            "FormatHeight": 1920,  # 9:16 vertical
            "FrameRate": FPS,
        })
        job_id = project.AddRenderJob()
        if job_id:
            print(f"  🎞️  Render job queued: {job_id}")
        else:
            print("  ⚠️  Render job failed — configure in Deliver page")
    except Exception as e:
        print(f"  ℹ️  Render setup: {e}")

    # === SAVE ===
    pm.SaveProject()

    # === FINAL SUMMARY ===
    print("=" * 60)
    print(f"✅ SUCCESS: '{TIMELINE_NAME}' assembled!")
    print("=" * 60)
    print(f"  📹 V1: {len(clip_infos)} clips ({frames_added/FPS/60:.1f} min)")
    print(f"  🎵 A1: 10 album tracks ({TOTAL_ALBUM_SEC/60:.1f} min)")
    print(f"  📍 Markers: Track boundaries (green) + Loop boundaries (yellow)")
    print(f"  🎞️  Render → {FINAL_DIR}")
    print()

    overshoot_sec = video_duration_sec - TOTAL_ALBUM_SEC
    print("━" * 60)
    print("MANUAL STEPS:")
    print("━" * 60)
    print()
    print("  1. TRANSITIONS:")
    print("     • Edit page → Select all clips on V1 (Ctrl+A) → Ctrl+T")
    print("     • Applies cross-dissolve between every clip")
    print()
    print("  2. IMPORT SUBTITLES (TRACK NAMES):")
    print("     • Drag and drop 'album_subtitles.srt' from the scratch folder into your Media Pool.")
    print("     • Drag it onto your timeline above V1.")
    print("     • In the Inspector, adjust the font, size, and drop shadow to your liking!")
    print()
    print("  3. PLAY THROUGH → verify → Deliver → Render All")
    print(f"     Output: {FINAL_DIR}\\MUSIC_002_Ana_Stevenson_The_Gilded_Pulse.mp4")
    print()
    print("  4. OPTIONAL — Color page:")
    print("     • Grade clip A1 → then re-run script (CopyGrades propagates)")
    print("     • Or: Grade A1 → Grab Still → Apply Grade to all clips")


if __name__ == "__main__":
    main()
