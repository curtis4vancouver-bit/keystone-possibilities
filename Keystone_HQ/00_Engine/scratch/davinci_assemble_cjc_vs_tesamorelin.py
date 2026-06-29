import os
import sys
import re
import time

def init_resolve():
    """Bootstraps connection to running DaVinci Resolve Studio on Windows."""
    os.environ["RESOLVE_SCRIPT_API"] = r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
    os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
    
    modules_path = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
    if modules_path not in sys.path:
        sys.path.append(modules_path)

    try:
        import DaVinciResolveScript as dvr
    except ImportError:
        print("Error: Could not import DaVinciResolveScript. Check API path.")
        return None

    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        print("Error: Resolve scripting interface offline. Is Resolve open?")
        return None
    return resolve

def get_numeric_prefix(filename):
    """Sorts files numerically by their leading number prefix (e.g. '8_video.mp4' -> 8)."""
    match = re.match(r'^(\d+)', filename)
    return int(match.group(1)) if match else 9999

def assemble_project_timeline(video_dir, broll_dir, timeline_name="CJC_vs_Tesamorelin"):
    resolve = init_resolve()
    if not resolve:
        return

    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    print(f"Connected to DaVinci Resolve Project: {project.GetName()}")
    
    # 1. Ingest Assets into dedicated Bin Folder
    bin_folder = None
    for f in root_folder.GetSubFolderList():
        if f.GetName() == "Video_Assembly_Media":
            bin_folder = f
            break
    if not bin_folder:
        bin_folder = media_pool.AddSubFolder(root_folder, "Video_Assembly_Media")
    media_pool.SetCurrentFolder(bin_folder)
    
    # Gather media paths
    print(f"Loading video clips from: {video_dir}")
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_files.sort(key=lambda x: get_numeric_prefix(os.path.basename(x)))
    
    print(f"Loading B-roll images from: {broll_dir}")
    broll_files = [os.path.join(broll_dir, f) for f in os.listdir(broll_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    broll_files.sort(key=lambda x: get_numeric_prefix(os.path.basename(x)))

    print(f"Found {len(video_files)} video clips and {len(broll_files)} B-roll images.")
    
    if len(broll_files) > len(video_files) - 1:
        print(f"Notice: You provided {len(broll_files)} B-roll images, but there are only {len(video_files)} video clips.")
        print(f"Only the first {len(video_files) - 1} images will be used for transitions.")
        broll_files = broll_files[:len(video_files) - 1]

    # Import to media pool
    print("Importing clips to media pool...")
    imported_videos = media_pool.ImportMedia(video_files)
    imported_brolls = media_pool.ImportMedia(broll_files)
    
    # Wait for import
    time.sleep(2)
    
    # Sort imported items by name
    imported_videos.sort(key=lambda item: get_numeric_prefix(item.GetName()))
    imported_brolls.sort(key=lambda item: get_numeric_prefix(item.GetName()))

    # 3. Create Timeline & Track V2
    print(f"Creating timeline '{timeline_name}'...")
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    if not timeline:
        print("Failed to create timeline. Make sure media pool has frame rate set correctly.")
        return

    project.SetCurrentTimeline(timeline)
    timeline.SetSetting("timelineFrameRate", "24.0") # Set target frame rate
    
    # Create Track V2 programmatically for B-rolls
    print("Adding Video Track 2...")
    timeline.AddTrack("video") 
    
    # 4. Append Videos back-to-back on Track 1 (V1/A1 with Audio intact)
    print("Appending talking-head video clips to Track 1 (V1/A1)...")
    media_pool.AppendToTimeline(imported_videos)
    
    # Wait for timeline to update
    time.sleep(2)
    
    # 5. Place B-roll images on Track 2 (V2) centered at video transitions
    print("Overlaying B-roll transition images on Track 2 (V2)...")
    video_items = timeline.GetItemListInTrack("video", 1)
    
    overlap_frames = 24 # 1 second before the transition at 24fps
    broll_duration = 48 # 2 seconds total duration
    
    for idx, broll_item in enumerate(imported_brolls):
        if idx >= len(video_items) - 1:
            break # No more transitions
            
        transition_frame = video_items[idx].GetEnd()
        record_frame = transition_frame - overlap_frames
            
        broll_info = {
            "mediaPoolItem": broll_item,
            "startFrame": 0,
            "endFrame": broll_duration - 1,
            "recordFrame": record_frame,
            "trackIndex": 2,
            "mediaType": 1
        }
        
        # Append the specific image clip information
        media_pool.AppendToTimeline([broll_info])
        
    pm.SaveProject()
    print("Timeline assembly complete!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Assemble Keystone Video")
    parser.add_argument("--videos", required=True, help="Path to videos directory")
    parser.add_argument("--brolls", required=True, help="Path to B-roll directory")
    args = parser.parse_args()
    
    assemble_project_timeline(args.videos, args.brolls)
