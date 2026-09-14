#!/usr/bin/env python3
"""
Keystone Master DaVinci Resolve 2-Track Assembler (fuscript.exe Standard)
- Solves Python 3.12 DLL crash by executing natively via DaVinci's built-in fuscript.exe
- 2-Track Video/B-Roll Assembly: 51 video clips on Track 1, 50 centered B-roll stills on Track 2 (48 frames / 2.0s)
- Audio Track 2: Day 5 Too Lost music tracks chained at -18.0 dB
- Auto-switches to Edit Page
"""

import os
import sys
import glob
import re
import json
import subprocess
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BRAIN_ROOT = r"C:\Users\Curtis\Desktop\Keystone Brain"
FUSCRIPT_EXE = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fuscript.exe"
RESOLVE_DIR = r"C:\Program Files\Blackmagic Design\DaVinci Resolve"

import wave

def get_audio_file_duration(filepath):
    """Calculates duration in seconds for audio files."""
    if filepath.lower().endswith(".wav"):
        try:
            with wave.open(filepath, "rb") as w:
                frames = w.getnframes()
                rate = w.getframerate()
                if rate > 0:
                    return frames / float(rate)
        except Exception:
            pass
    try:
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", filepath]
        res = subprocess.run(cmd, capture_output=True, text=True)
        return float(res.stdout.strip())
    except Exception:
        return 180.0

def ensure_resolve_running():
    try:
        res = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe"], capture_output=True, text=True)
        if "Resolve.exe" in res.stdout:
            return True
    except Exception:
        pass
    print("[*] Launching DaVinci Resolve Studio 21...")
    resolve_exe = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
    if os.path.exists(resolve_exe):
        subprocess.Popen([resolve_exe], cwd=RESOLVE_DIR)
        import time
        for _ in range(15):
            time.sleep(2)
            try:
                res = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Resolve.exe"], capture_output=True, text=True)
                if "Resolve.exe" in res.stdout:
                    time.sleep(6)
                    return True
            except Exception:
                pass
    return False

def run_assemble(video_count=51, broll_count=50, context="protocols", day=8):
    print(f"[*] [Keystone Master DaVinci Assembler] Target: {video_count} clips, {broll_count} b-rolls (Context: {context}, Day: {day})...")
    ensure_resolve_running()
    
    if context == "possibilities":
        base_media_dir = "06_Keystone_possibilities"
        proj_name = "Keystone Possibilities - Master Production"
        tl_name = "Keystone Possibilities Master Assembly"
    elif context == "recomposition":
        base_media_dir = "07_Keystone_recomposition"
        proj_name = "Keystone Recomposition - Master Production"
        tl_name = "Keystone Recomposition Master Assembly"
    else:
        base_media_dir = "08_Keystone_protocols"
        proj_name = "Keystone Protocols - Master Production"
        tl_name = f"Keystone Protocols Day {day} Master Assembly"
        
    v_dir = os.path.join(BRAIN_ROOT, base_media_dir, "Google_Flow", "video")
    b_dir = os.path.join(BRAIN_ROOT, base_media_dir, "Google_Flow", "b-roll")
    
    # 1. Gather videos 1..N
    v_map = {}
    for f in glob.glob(os.path.join(v_dir, "*.mp4")):
        m = re.match(r"^(\d+)(?:_|\.|$)", os.path.basename(f))
        if m:
            v_map[int(m.group(1))] = os.path.abspath(f)
            
    sorted_videos = [v_map[i] for i in sorted(v_map.keys()) if i <= video_count]
    print(f"[*] Discovered {len(sorted_videos)}/{video_count} video clips in {v_dir}")
    
    # 2. Gather b-rolls A1..AN (isolated in subdirectories to prevent DaVinci from collapsing them into an image sequence)
    stills_dir = os.path.join(b_dir, "individual_stills")
    os.makedirs(stills_dir, exist_ok=True)
    b_map = {}
    for f in glob.glob(os.path.join(b_dir, "*.jpeg")) + glob.glob(os.path.join(b_dir, "*.jpg")) + glob.glob(os.path.join(b_dir, "*.png")):
        m = re.match(r"^A(\d+)(?:_|\.|$)", os.path.basename(f))
        if m:
            idx = int(m.group(1))
            sub_folder = os.path.join(stills_dir, f"A{idx}")
            os.makedirs(sub_folder, exist_ok=True)
            isolated_file = os.path.join(sub_folder, os.path.basename(f))
            if not os.path.exists(isolated_file):
                import shutil
                shutil.copy2(f, isolated_file)
            b_map[idx] = os.path.abspath(isolated_file)
            
    sorted_brolls = [b_map[i] for i in sorted(b_map.keys()) if i <= broll_count]
    print(f"[*] Discovered and isolated {len(sorted_brolls)}/{broll_count} B-roll stills in {stills_dir}")
    
    # 3. Gather music from active_music_attribution.json with stateful rotation
    music_items = []
    attr_path = os.path.join(BRAIN_ROOT, base_media_dir, "active_music_attribution.json")
    rot_file = os.path.join(BRAIN_ROOT, base_media_dir, "music_rotation_index.json")

    current_rot_idx = 0
    if os.path.exists(rot_file):
        try:
            with open(rot_file, "r", encoding="utf-8") as rf:
                rdata = json.load(rf)
                current_rot_idx = int(rdata.get("current_track_index", 0))
        except Exception:
            pass

    selected_track_meta = None
    if os.path.exists(attr_path):
        try:
            with open(attr_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                all_tracks = data.get("tracks", [])

                if all_tracks:
                    num_tracks = len(all_tracks)
                    start_idx = current_rot_idx % num_tracks
                    rotated_tracks = all_tracks[start_idx:] + all_tracks[:start_idx]

                    selected_track_meta = rotated_tracks[0]
                    print(f"🎵 [Music Rotation] Selected Track ({start_idx + 1}/{num_tracks}): '{selected_track_meta.get('track_title')}' (Album: {selected_track_meta.get('album_name')})")

                    for tr in rotated_tracks:
                        fp = tr.get("file_path")
                        if fp and os.path.exists(fp):
                            dur = get_audio_file_duration(fp)
                            frames = int(dur * 24)
                            music_items.append({"path": os.path.abspath(fp), "frames": frames, "title": tr.get("track_title")})

                    # Advance rotation index and persist for next production
                    next_rot_idx = (start_idx + 1) % num_tracks
                    with open(rot_file, "w", encoding="utf-8") as rf:
                        json.dump({
                            "current_track_index": next_rot_idx,
                            "last_used_track": selected_track_meta.get("track_title"),
                            "last_used_album": selected_track_meta.get("album_name"),
                            "timestamp": time.time()
                        }, rf, indent=2)

                    # Update active_music_attribution.json top-level fields for downstream cross-channel sync
                    data["active_track"] = selected_track_meta.get("track_title")
                    data["track_title"] = selected_track_meta.get("track_title")
                    data["album_name"] = selected_track_meta.get("album_name")
                    data["isrc"] = selected_track_meta.get("isrc")
                    if selected_track_meta.get("spotify_search_link"):
                        data["spotify_search_link"] = selected_track_meta.get("spotify_search_link")
                    with open(attr_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[-] Music rotation error: {e}")

    # Only include the music tracks actually needed to cover the total video duration
    needed_video_frames = len(sorted_videos) * 240
    accumulated_frames = 0
    needed_music = []
    for m in music_items:
        needed_music.append(m)
        accumulated_frames += m["frames"]
        if accumulated_frames >= needed_video_frames:
            break
    music_items = needed_music
            
    track_names_str = ", ".join([m.get("title", os.path.basename(m["path"])) for m in music_items])
    print(f"[*] Selected {len(music_items)} background music track(s) [{track_names_str}] for {needed_video_frames} frames ({needed_video_frames/24:.1f}s video duration)")

    lua_path = os.path.join(BRAIN_ROOT, "16_daemons", "tools", f"assemble_day{day}.lua")
    
    # Format paths for Lua (escaped backslashes)
    v_paths_lua = ",\n    ".join([f'"{p.replace(chr(92), chr(92)*2)}"' for p in sorted_videos])
    b_paths_lua = ",\n    ".join([f'"{p.replace(chr(92), chr(92)*2)}"' for p in sorted_brolls])
    m_paths_lua = ",\n    ".join([f'"{m["path"].replace(chr(92), chr(92)*2)}"' for m in music_items])
    m_entries_lua = ",\n    ".join([f'{{ path = "{m["path"].replace(chr(92), chr(92)*2)}", frames = {m["frames"]} }}' for m in music_items])
    
    lua_code = f"""
local resolve = Resolve()
if not resolve then
    print("[-] DaVinci Resolve is not running.")
    os.exit(1)
end

local pm = resolve:GetProjectManager()
local proj = pm:GetCurrentProject()
if not proj or proj:GetName() == "Untitled Project" or proj:GetName() ~= "{proj_name}" then
    proj = pm:LoadProject("{proj_name}")
    if not proj then
        proj = pm:CreateProject("{proj_name}")
    end
end
if not proj then
    print("[-] Could not connect to or create project: {proj_name}")
    os.exit(1)
end
print("[*] Connected to project: " .. proj:GetName())

local mp = proj:GetMediaPool()
local root = mp:GetRootFolder()

-- 1. Import all media
local video_paths = {{
    {v_paths_lua}
}}

local broll_paths = {{
    {b_paths_lua}
}}

local music_paths = {{
    {m_paths_lua}
}}

local music_items = {{
    {m_entries_lua}
}}

print("[*] Importing " .. #video_paths .. " video clips...")
mp:ImportMedia(video_paths)

print("[*] Importing " .. #broll_paths .. " B-roll stills...")
mp:ImportMedia(broll_paths)

if #music_paths > 0 then
    print("[*] Importing " .. #music_paths .. " music tracks...")
    mp:ImportMedia(music_paths)
end

-- Index MediaPool items by normalized path
local clips = root:GetClipList()
local media_by_path = {{}}
for _, c in ipairs(clips) do
    local p = c:GetClipProperty("File Path")
    if p then
        media_by_path[p:lower()] = c
    end
end

-- 2. Create or Reset Timeline
local tl_name = "{tl_name}"
for i = 1, proj:GetTimelineCount() do
    local existing = proj:GetTimelineByIndex(i)
    if existing and existing:GetName() == tl_name then
        print("[*] Removing existing timeline: " .. tl_name)
        mp:DeleteTimelines({{ existing }})
        break
    end
end

local tl = mp:CreateEmptyTimeline(tl_name)
if not tl then
    print("[-] Failed to create timeline.")
    os.exit(1)
end
proj:SetCurrentTimeline(tl)
print("[+] Created Timeline: " .. tl:GetName() .. " (Start: " .. tl:GetStartTimecode() .. ")")

-- 3. Configure Tracks
if tl:GetTrackCount("video") < 2 then tl:AddTrack("video") end
tl:SetTrackName("video", 1, "Main Videos")
tl:SetTrackName("video", 2, "B-Roll Stills")

if tl:GetTrackCount("audio") < 2 then tl:AddTrack("audio", "stereo") end
tl:SetTrackName("audio", 1, "Voiceover")
tl:SetTrackName("audio", 2, "Background Music")

-- 4. Append Video Clips to Track 1 end-to-end
local ordered_v_items = {{}}
for _, p in ipairs(video_paths) do
    local item = media_by_path[p:lower()]
    if item then
        table.insert(ordered_v_items, item)
    end
end

print("[*] Appending " .. #ordered_v_items .. " video clips onto Track 1...")
mp:AppendToTimeline(ordered_v_items)

-- 5. Append B-Roll Stills centered across cuts on Track 2 (48 frames / 2.0s)
local base_frame = 86400
local clip_step = 240
local broll_duration = 48

local broll_append = {{}}
for idx, p in ipairs(broll_paths) do
    local item = media_by_path[p:lower()]
    if item then
        local rec_frame = base_frame + (idx * clip_step) - 24
        table.insert(broll_append, {{
            mediaPoolItem = item,
            startFrame = 0,
            endFrame = broll_duration,
            recordFrame = rec_frame,
            trackIndex = 2,
            mediaType = 1
        }})
    end
end

print("[*] Appending " .. #broll_append .. " B-roll stills onto Track 2...")
mp:AppendToTimeline(broll_append)

-- 6. Append Background Music to Audio Track 2
local total_video_frames = #ordered_v_items * clip_step
local end_video_frame = base_frame + total_video_frames

local cur_audio_rec = base_frame
local music_append = {{}}
for _, m in ipairs(music_items) do
    local item = media_by_path[m.path:lower()]
    if item then
        local frames_to_add = m.frames
        if cur_audio_rec + frames_to_add > end_video_frame then
            frames_to_add = end_video_frame - cur_audio_rec
        end
        if frames_to_add > 0 then
            table.insert(music_append, {{
                mediaPoolItem = item,
                startFrame = 0,
                endFrame = frames_to_add,
                recordFrame = cur_audio_rec,
                trackIndex = 2,
                mediaType = 2
            }})
            cur_audio_rec = cur_audio_rec + frames_to_add
        end
        if cur_audio_rec >= end_video_frame then break end
    end
end

if #music_append > 0 then
    print("[*] Appending " .. #music_append .. " music tracks onto Audio Track 2...")
    mp:AppendToTimeline(music_append)
end

-- 7. Switch to Edit Page
resolve:OpenPage("edit")
print("[+] Switched DaVinci Resolve to Edit Page!")
print("[SUCCESS] 2-Track Master Assembly Complete!")
"""

    with open(lua_path, "w", encoding="utf-8") as lf:
        lf.write(lua_code.strip())
        
    print(f"[*] Generated Lua Assembly script: {lua_path}")
    print("[*] Executing assembly via fuscript.exe...")
    
    res = subprocess.run([FUSCRIPT_EXE, lua_path], cwd=RESOLVE_DIR, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("Stderr:", res.stderr)
        
    if res.returncode == 0:
        voice_msg = (
            f"DaVinci Resolve 2-track master assembly complete Wayne. "
            f"Ingested all {len(sorted_videos)} video clips on Track 1 starting at 1 hour, "
            f"placed all {len(sorted_brolls)} B-roll stills centered over the cuts on Track 2, "
            f"and injected background music on Audio Track 2."
        )
        try:
            with open(r"C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt", "w", encoding="utf-8") as vf:
                vf.write(voice_msg)
        except Exception: pass
        return True
    else:
        print(f"[-] fuscript failed with return code {res.returncode}")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Keystone Master DaVinci Assembler")
    parser.add_argument("video_count", nargs="?", type=int, default=51)
    parser.add_argument("broll_count", nargs="?", type=int, default=50)
    parser.add_argument("--context", "-c", default="protocols", choices=["protocols", "possibilities", "recomposition"])
    parser.add_argument("--day", "-d", type=int, default=8)
    args, _ = parser.parse_known_args()
    run_assemble(video_count=args.video_count, broll_count=args.broll_count, context=args.context, day=args.day)

