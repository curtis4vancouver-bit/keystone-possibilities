import os
import sys
import re

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
    """Extracts numeric prefix to properly sort 'A1.mp4', 'B1.mp4' etc."""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 9999

def assemble_project():
    print("Initializing DaVinci Resolve...")
    resolve = init_resolve()
    pm = resolve.GetProjectManager()
    
    # We load or create a project named LONG_001
    print("Loading or creating project: LONG_001")
    project = pm.GetCurrentProject()
    if not project:
        project = pm.CreateProject("LONG_001")
    else:
        # Check if project name matches
        if project.GetName() != "LONG_001":
            project = pm.CreateProject("LONG_001")
            
    if not project:
        print("Project might already exist. Loading it...")
        project = pm.LoadProject("LONG_001")
        
    media_pool = project.GetMediaPool()
    root_folder = media_pool.GetRootFolder()
    
    # Create a unique bin for this build
    bin_name = "LONG_001_Media"
    bin_folder = None
    for f in root_folder.GetSubFolderList():
        if f.GetName() == bin_name:
            bin_folder = f
            break
    if not bin_folder:
        bin_folder = media_pool.AddSubFolder(root_folder, bin_name)
    media_pool.SetCurrentFolder(bin_folder)
    
    # Paths
    video_dir = r"C:\Users\Curtis\Desktop\LONG_FORM_PRODUCTION\Videos"
    broll_dir = r"C:\Users\Curtis\Desktop\LONG_FORM_PRODUCTION\Images"
    
    media_storage = resolve.GetMediaStorage()
    
    print("Importing media...")
    # Import Videos (A1..A26)
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_items = media_storage.AddItemsToMediaPool(video_files)
    if not video_items:
        # Fallback to current folder clip list if already imported
        video_items = [c for c in bin_folder.GetClipList() if c.GetName().startswith("A")]
    
    # Import B-rolls (B1..B25)
    broll_files = [os.path.join(broll_dir, f) for f in os.listdir(broll_dir) if f.endswith('.mp4')]
    broll_items = media_storage.AddItemsToMediaPool(broll_files)
    if not broll_items:
        broll_items = [c for c in bin_folder.GetClipList() if c.GetName().startswith("B")]
        
    # Convert dict value list if needed (AddItemsToMediaPool returns dict)
    if isinstance(video_items, dict):
        video_items = list(video_items.values())
    if isinstance(broll_items, dict):
        broll_items = list(broll_items.values())
        
    # Sort
    video_items.sort(key=lambda x: get_numeric_prefix(x.GetName()))
    broll_items.sort(key=lambda x: get_numeric_prefix(x.GetName()))
    
    print(f"Loaded {len(video_items)} A-clips and {len(broll_items)} B-rolls.")
    
    # Delete existing timeline if it exists
    TIMELINE_NAME = "LONG_001_Timeline"
    for i in range(1, project.GetTimelineCount() + 1):
        t = project.GetTimelineByIndex(i)
        if t.GetName() == TIMELINE_NAME:
            media_pool.DeleteTimelines([t])
            break
            
    print("Creating Timeline...")
    timeline = media_pool.CreateEmptyTimeline(TIMELINE_NAME)
    project.SetCurrentTimeline(timeline)
    project.SetSetting("timelineFrameRate", "24.000")
    
    # Ensure V2 track exists for b-roll
    if timeline.GetTrackCount("video") < 2:
        timeline.AddTrack("video") 
        
    # 1. Append videos to V1 (raw list retains audio)
    print("Appending videos to V1/A1...")
    media_pool.AppendToTimeline(video_items)
    
    # 2. Append B-rolls to V2 (centered on cuts)
    print("Calculating transitions and appending B-rolls to V2...")
    timeline_video_items = timeline.GetItemListInTrack("video", 1)
    
    FPS = 24
    DURATION_SEC = 3 # Trimming each video B-roll to 3 seconds centered on cut
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
            "mediaType": 1 # Video type (ignores audio track)
        }
        broll_insertions.append(broll_info)
        
    media_pool.AppendToTimeline(broll_insertions)
    
    pm.SaveProject()
    print("Timeline Assembly Complete!")

if __name__ == "__main__":
    assemble_project()
