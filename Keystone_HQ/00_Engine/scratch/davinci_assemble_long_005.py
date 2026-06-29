import sys
import os
import re
import time

# Add DaVinci Resolve Scripting API path
sys.path.append(r'C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules')
import DaVinciResolveScript as dvr_script

def get_numeric_prefix(filename):
    """Extract leading number prefix (e.g. '8_video.mp4' or '8_image.jpeg' -> 8)"""
    match = re.match(r'^(\d+)_', filename)
    return int(match.group(1)) if match else -1

def main():
    print("Connecting to DaVinci Resolve...")
    resolve = dvr_script.scriptapp('Resolve')
    if not resolve:
        print("Error: Could not connect to DaVinci Resolve. Is it open?")
        sys.exit(1)
        
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        print("Error: No active project found in DaVinci Resolve. Please open a project first.")
        sys.exit(1)
        
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    # 1. Define source directories
    video_dir = r"C:\Users\Curtis\Desktop\it\video"
    broll_dir = r"C:\Users\Curtis\Desktop\it\b roll"
    
    # 2. Collect files to import
    files_to_import = []
    
    if os.path.exists(video_dir):
        for f in os.listdir(video_dir):
            if f.lower().endswith(('.mp4', '.mov')):
                files_to_import.append(os.path.join(video_dir, f))
    else:
        print(f"Error: Video directory {video_dir} does not exist.")
        sys.exit(1)
        
    if os.path.exists(broll_dir):
        for f in os.listdir(broll_dir):
            if f.lower().endswith(('.jpeg', '.jpg', '.png')):
                files_to_import.append(os.path.join(broll_dir, f))
    else:
        print(f"Error: B-roll directory {broll_dir} does not exist.")
        sys.exit(1)
        
    print(f"Found {len(files_to_import)} files to import.")
    
    # 3. Create or set the Media Pool Bin Folder to keep things clean
    bin_name = "LONG_005_Media"
    bin_folder = None
    for f in root_folder.GetSubFolderList():
        if f.GetName() == bin_name:
            bin_folder = f
            break
    if not bin_folder:
        bin_folder = media_pool.AddSubFolder(root_folder, bin_name)
    media_pool.SetCurrentFolder(bin_folder)
    
    # 4. Import media
    print("Importing media into DaVinci Resolve...")
    imported_items = media_pool.ImportMedia(files_to_import)
    if not imported_items:
        print("Warning: ImportMedia returned empty, checking if items already exist in bin...")
    
    # Retrieve all clips from the current folder to build our dictionary
    clips = bin_folder.GetClipList()
    print(f"Total clips in bin '{bin_name}': {len(clips)}")
    
    # Map clips by prefix and type
    video_clips = {}
    broll_clips = {}
    
    for clip in clips:
        name = clip.GetName()
        prefix = get_numeric_prefix(name)
        if prefix == -1:
            continue
            
        clip_type = clip.GetClipProperty("Clip Type")
        
        # Fallback to extension check if Clip Type is empty/unknown
        if not clip_type:
            if name.lower().endswith(('.mp4', '.mov')):
                clip_type = "Video"
            elif name.lower().endswith(('.jpeg', '.jpg', '.png')):
                clip_type = "Image"
                
        if clip_type == "Video":
            video_clips[prefix] = clip
        elif clip_type == "Image":
            broll_clips[prefix] = clip
            
    print(f"Mapped {len(video_clips)} video clips and {len(broll_clips)} B-roll pictures.")
    
    if not video_clips:
        print("Error: No video clips were mapped. Cannot build timeline.")
        sys.exit(1)
        
    # 5. Get sorted video clips
    sorted_video_prefixes = sorted(video_clips.keys())
    sorted_video_items = [video_clips[p] for p in sorted_video_prefixes]
    
    print("Videos to place (in order):")
    for p in sorted_video_prefixes:
        print(f"  Clip {p}: {video_clips[p].GetName()}")
        
    # Get FPS for timeline calculations
    FPS = float(project.GetSetting('timelineFrameRate'))
    if not FPS or FPS <= 0:
        FPS = 24.0 # Default fallback
    print(f"Timeline FPS: {FPS}")
    
    # 6. Create Timeline
    timeline_name = "LONG_005_Assembly"
    
    # Name the timeline with a unique suffix to avoid conflicts
    timeline_name = f"LONG_005_Assembly_{int(time.time())}"
            
    print(f"Creating timeline '{timeline_name}'...")
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    if not timeline:
        print("Error: Could not create timeline.")
        sys.exit(1)
        
    project.SetCurrentTimeline(timeline)
    
    # Create Track V2 programmatically for B-rolls (V1 is default)
    timeline.AddTrack("video")
    
    # 7. Append videos sequentially to Track V1/A1
    print("Appending talking head videos back-to-back on Track 1...")
    # Passing raw MediaPoolItems directly preserves the synchronized audio
    appended_videos = media_pool.AppendToTimeline(sorted_video_items)
    if not appended_videos:
        print("Error: Failed to append videos to timeline.")
        sys.exit(1)
    print(f"Appended {len(appended_videos)} videos.")
    
    # Wait for DaVinci Resolve timeline to update
    time.sleep(1)
    
    # Get timeline items on Track 1 to find exact transition boundaries
    timeline_videos = timeline.GetItemListInTrack("video", 1)
    print(f"Found {len(timeline_videos)} video items on Track V1.")
    
    if len(timeline_videos) != len(sorted_video_items):
        print("Warning: Timeline video item count mismatch! Using item boundaries for placement.")
        
    # 8. Build overlay clip info for B-rolls on Track V2
    clip_infos = []
    overlap_frames = int(2.0 * FPS) # 2 seconds = 48 frames at 24fps
    broll_duration_frames = int(4.0 * FPS) # 4 seconds total duration
    
    print("Calculating B-roll placement positions...")
    for idx, timeline_video in enumerate(timeline_videos):
        # The transition index (1-based) corresponds to the end of this video clip
        broll_number = idx + 1
        
        if broll_number not in broll_clips:
            print(f"  Warning: B-roll picture {broll_number} not found in Media Pool. Skipping.")
            continue
            
        broll_item = broll_clips[broll_number]
        
        # For clips 1 to N-1, place B-roll centered on the end of the clip (transition point)
        if idx < len(timeline_videos) - 1:
            transition_frame = timeline_video.GetEnd()
            record_frame = transition_frame - overlap_frames
        else:
            # For the last clip, place it at the very end of the video
            transition_frame = timeline_video.GetEnd()
            record_frame = transition_frame - overlap_frames
            
        print(f"  B-roll {broll_number} ({broll_item.GetName()}): placing at frame {record_frame} (overlaps transition at {transition_frame})")
        
        info = {
            "mediaPoolItem": broll_item,
            "trackIndex": 2, # V2
            "recordFrame": record_frame,
            "startFrame": 0,
            "endFrame": broll_duration_frames - 1,
            "mediaType": 1 # Video/Image type
        }
        clip_infos.append(info)
        
    if clip_infos:
        print(f"Appending {len(clip_infos)} B-rolls to Track 2...")
        appended_brolls = media_pool.AppendToTimeline(clip_infos)
        print(f"Successfully appended {len(appended_brolls) if appended_brolls else 0} B-roll overlays.")
    else:
        print("No B-rolls to append.")
        
    pm.SaveProject()
    print("Assembly script finished successfully!")

if __name__ == "__main__":
    main()
