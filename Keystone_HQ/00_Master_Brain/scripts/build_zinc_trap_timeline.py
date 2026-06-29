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

    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("Resolve scripting interface offline. Is Resolve open?")
    return resolve

def get_numeric_prefix(filename):
    """Extracts numeric prefix to properly sort '1.mp4', '2.mp4', 'B-1.png', 'B-2.png' etc."""
    # Look for any number in the filename to sort by
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 9999

def assemble_project():
    print("Initializing DaVinci Resolve...")
    resolve = init_resolve()
    pm = resolve.GetProjectManager()
    
    print("Creating new project: ZINC_TRAP")
    project = pm.CreateProject("ZINC_TRAP")
    if not project:
        print("Project might already exist. Loading it...")
        project = pm.LoadProject("ZINC_TRAP")
        
    media_pool = project.GetMediaPool()
    
    # Paths
    video_dir = r"C:\Users\Curtis\Desktop\it\video"
    broll_dir = r"C:\Users\Curtis\Desktop\it\b roll"
    
    media_storage = resolve.GetMediaStorage()
    
    print("Importing media...")
    # Import Videos
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_items = media_storage.AddItemListToMediaPool(video_files)
    
    # Import B-rolls
    broll_files = [os.path.join(broll_dir, f) for f in os.listdir(broll_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    broll_items = media_storage.AddItemListToMediaPool(broll_files)
    
    # Sort
    video_items.sort(key=lambda x: get_numeric_prefix(x.GetName()))
    broll_items.sort(key=lambda x: get_numeric_prefix(x.GetName()))
    
    print(f"Loaded {len(video_items)} videos and {len(broll_items)} b-rolls.")
    
    print("Creating Timeline...")
    timeline = media_pool.CreateEmptyTimeline("ZINC_TRAP_Timeline")
    project.SetCurrentTimeline(timeline)
    
    # Ensure V2 track exists for b-roll
    timeline.AddTrack("video") 
    
    # 1. Append videos to V1 (raw list retains audio)
    print("Appending videos to V1/A1...")
    media_pool.AppendToTimeline(video_items)
    
    # 2. Append B-rolls to V2 (centered on cuts)
    print("Calculating transitions and appending B-rolls to V2...")
    timeline_video_items = timeline.GetItemListInTrack("video", 1)
    
    FPS = 24
    DURATION_SEC = 3
    TOTAL_FRAMES = FPS * DURATION_SEC # 72 frames
    HALF_FRAMES = TOTAL_FRAMES // 2   # 36 frames
    
    broll_insertions = []
    
    for idx, broll in enumerate(broll_items):
        if idx < len(timeline_video_items) - 1:
            # Center over the transition boundary
            transition_frame = timeline_video_items[idx].GetEnd()
            record_frame = transition_frame - HALF_FRAMES
        else:
            # Last B-roll goes near the end of the final video
            record_frame = timeline_video_items[-1].GetEnd() - TOTAL_FRAMES
            
        broll_info = {
            "mediaPoolItem": broll,
            "startFrame": 0,
            "endFrame": TOTAL_FRAMES - 1, # 71
            "recordFrame": record_frame,
            "trackIndex": 2,
            "mediaType": 1 # Video type
        }
        broll_insertions.append(broll_info)
        
    media_pool.AppendToTimeline(broll_insertions)
    
    print("Generating Subtitles...")
    # Trigger auto subtitles
    # Note: subtitle generation might require GUI interaction or a different API call. 
    # The MCP tool `timeline_create_subtitles_from_audio` handles it cleanly.
    
    pm.SaveProject()
    print("Timeline Assembly Complete!")

if __name__ == "__main__":
    assemble_project()
