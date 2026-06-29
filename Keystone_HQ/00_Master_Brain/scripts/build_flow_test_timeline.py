import os
import sys
import re
from pathlib import Path

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
    """Extracts numeric prefix to properly sort 'A1.mp4', 'B1.jpeg' etc."""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 9999

def assemble_project():
    desktop_root = Path(r"C:\Users\Curtis\Desktop")
    
    # Locate the latest project folder matching FLOW_* on Desktop
    flow_dirs = sorted(
        [d for d in desktop_root.glob("FLOW_*") if d.is_dir()],
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    if not flow_dirs:
        print("Error: No folder matching 'FLOW_*' found on Desktop.")
        # Fallback to FLOW_RUN_TEST if it exists
        test_dir = desktop_root / "FLOW_RUN_TEST"
        if test_dir.exists():
            flow_dir = test_dir
        else:
            return
    else:
        flow_dir = flow_dirs[0]
        
    project_name = flow_dir.name
    timeline_name = f"{project_name}_Timeline"
    
    video_dir = flow_dir / "Videos"
    broll_dir = flow_dir / "Images"
    thumb_dir = flow_dir / "Thumbnails"
    
    print(f"[+] Found project folder: {flow_dir}")
    print("Initializing DaVinci Resolve...")
    try:
        resolve = init_resolve()
    except RuntimeError as e:
        print(f"Error: {e}")
        return
        
    pm = resolve.GetProjectManager()
    
    print(f"Creating new project: {project_name}")
    project = pm.CreateProject(project_name)
    if not project:
        print(f"Project '{project_name}' already exists. Loading it...")
        project = pm.LoadProject(project_name)
        
    if not project:
        print("Error: Could not load or create project.")
        return
        
    media_pool = project.GetMediaPool()
    
    # Collect files
    video_files = []
    if video_dir.exists():
        video_files = sorted(
            [str(video_dir / f) for f in os.listdir(video_dir) if f.endswith(('.mp4', '.mov'))],
            key=lambda x: get_numeric_prefix(os.path.basename(x))
        )
        
    broll_files = []
    if broll_dir.exists():
        broll_files = sorted(
            [str(broll_dir / f) for f in os.listdir(broll_dir) if f.endswith(('.png', '.jpg', '.jpeg'))],
            key=lambda x: get_numeric_prefix(os.path.basename(x))
        )
        
    thumb_files = []
    if thumb_dir.exists():
        thumb_files = [str(thumb_dir / f) for f in os.listdir(thumb_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Found {len(video_files)} videos, {len(broll_files)} B-rolls, and {len(thumb_files)} thumbnails.")
    if not video_files:
        print("Error: No video files found to assemble.")
        return
        
    media_storage = resolve.GetMediaStorage()
    
    # Import files to Media Pool
    print("Importing media to pool...")
    imported_videos = media_storage.AddItemListToMediaPool(video_files)
    imported_brolls = media_storage.AddItemListToMediaPool(broll_files) if broll_files else []
    imported_thumbs = media_storage.AddItemListToMediaPool(thumb_files) if thumb_files else []
    
    # Convert list/dict responses to sorted lists of media items
    def get_items_list(imported):
        if isinstance(imported, dict):
            return list(imported.values())
        return imported or []
        
    videos_items = sorted(get_items_list(imported_videos), key=lambda x: get_numeric_prefix(x.GetName()))
    brolls_items = sorted(get_items_list(imported_brolls), key=lambda x: get_numeric_prefix(x.GetName()))
    
    print(f"Media Pool imported: {len(videos_items)} videos and {len(brolls_items)} B-rolls.")
    
    # Delete existing timeline if present to start fresh
    for i in range(1, project.GetTimelineCount() + 1):
        t = project.GetTimelineByIndex(i)
        if t.GetName() == timeline_name:
            media_pool.DeleteTimelines([t])
            break
            
    print("Creating empty timeline...")
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    project.SetCurrentTimeline(timeline)
    project.SetSetting("timelineFrameRate", "24.000")
    
    # Ensure Track V2 exists for B-roll
    if timeline.GetTrackCount("video") < 2:
        timeline.AddTrack("video")
        
    # Append videos to track V1
    print("Appending videos to V1/A1...")
    media_pool.AppendToTimeline(videos_items)
    
    # Centering B-rolls on transitions
    timeline_video_items = timeline.GetItemListInTrack("video", 1)
    
    FPS = 24
    DURATION_SEC = 2.0  # 2 seconds total duration (centered on transition)
    TOTAL_FRAMES = int(FPS * DURATION_SEC) # 48 frames
    HALF_FRAMES = TOTAL_FRAMES // 2        # 24 frames
    
    broll_insertions = []
    print("Positioning B-rolls on V2...")
    for idx, broll in enumerate(brolls_items):
        if idx < len(timeline_video_items) - 1:
            # Center over the transition boundary between Clip A(idx+1) and A(idx+2)
            transition_frame = timeline_video_items[idx].GetEnd()
            record_frame = transition_frame - HALF_FRAMES
            
            broll_info = {
                "mediaPoolItem": broll,
                "startFrame": 0,
                "endFrame": TOTAL_FRAMES - 1,
                "recordFrame": record_frame,
                "trackIndex": 2,
                "mediaType": 1
            }
            broll_insertions.append(broll_info)
            print(f"Placed Broll {idx+1} at transition frame {transition_frame} (inserting at {record_frame})")
            
    if broll_insertions:
        media_pool.AppendToTimeline(broll_insertions)
        
    pm.SaveProject()
    print(f"SUCCESS: {project_name} timeline assembly complete!")

if __name__ == "__main__":
    assemble_project()
