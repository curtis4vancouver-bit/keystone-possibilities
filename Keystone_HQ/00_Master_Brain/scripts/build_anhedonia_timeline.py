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
    """Extracts numeric prefix to properly sort 'A1.mp4', 'A10.mp4', 'B1.jpeg', 'B10.jpeg' etc."""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else 9999

def assemble_project():
    print("[+] Initializing DaVinci Resolve...")
    try:
        resolve = init_resolve()
    except RuntimeError as e:
        print(f"[-] Error: {e}")
        print("[-] Please ensure DaVinci Resolve Studio is open with a project loaded.")
        sys.exit(1)
        
    pm = resolve.GetProjectManager()
    
    project_name = "LONG_033_GLP1_ANHEDONIA"
    print(f"[+] Creating or loading project: {project_name}")
    project = pm.CreateProject(project_name)
    if not project:
        print("[*] Project already exists. Loading it...")
        project = pm.LoadProject(project_name)
        
    if not project:
        print("[-] Failed to load project.")
        sys.exit(1)
        
    media_pool = project.GetMediaPool()
    
    # Paths
    video_dir = r"C:\Users\Curtis\Desktop\LONG_033_GLP1_ANHEDONIA\Videos"
    broll_dir = r"C:\Users\Curtis\Desktop\LONG_033_GLP1_ANHEDONIA\Images"
    
    media_storage = resolve.GetMediaStorage()
    
    print("[+] Importing media items...")
    # Import Videos (A1.mp4 - A50.mp4)
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')]
    video_files.sort(key=lambda x: get_numeric_prefix(os.path.basename(x)))
    video_items = media_storage.AddItemListToMediaPool(video_files)
    
    # Import B-rolls (B1.jpeg - B50.jpeg)
    broll_files = [os.path.join(broll_dir, f) for f in os.listdir(broll_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    broll_files.sort(key=lambda x: get_numeric_prefix(os.path.basename(x)))
    broll_items = media_storage.AddItemListToMediaPool(broll_files)
    
    # Re-sort imported items to be absolutely sure
    video_items.sort(key=lambda x: get_numeric_prefix(x.GetName()))
    broll_items.sort(key=lambda x: get_numeric_prefix(x.GetName()))
    
    print(f"[+] Loaded {len(video_items)} video clips and {len(broll_items)} B-roll images.")
    
    timeline_name = "Protocol_033_GLP1_Anhedonia"
    print(f"[+] Creating Timeline: {timeline_name}")
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    project.SetCurrentTimeline(timeline)
    
    # Ensure V2 track exists for B-roll overlays
    timeline.AddTrack("video") 
    
    # 1. Append videos to V1 (raw list retains audio track linkage)
    print("[+] Appending video clips to Track V1/A1...")
    media_pool.AppendToTimeline(video_items)
    
    # 2. Append B-rolls to V2 (centered on cuts)
    print("[+] Calculating boundaries and placing B-rolls on Track V2...")
    timeline_video_items = timeline.GetItemListInTrack("video", 1)
    
    FPS = 24
    DURATION_SEC = 2.0
    TOTAL_FRAMES = int(FPS * DURATION_SEC) # 48 frames
    HALF_FRAMES = TOTAL_FRAMES // 2        # 24 frames
    
    broll_insertions = []
    
    for idx, broll in enumerate(broll_items):
        # We have 50 B-rolls and 50 Videos.
        # B1-B49 are placed centered on the transitions between A1/A2, A2/A3, ..., A49/A50.
        # B50 is placed at the end of A50 as a 2-second outro slide.
        if idx < len(timeline_video_items) - 1:
            transition_frame = timeline_video_items[idx].GetEnd()
            record_frame = transition_frame - HALF_FRAMES
        else:
            # Outro slide B50 goes at the end of the final video clip
            record_frame = timeline_video_items[-1].GetEnd() - TOTAL_FRAMES
            
        broll_info = {
            "mediaPoolItem": broll,
            "startFrame": 0,
            "endFrame": TOTAL_FRAMES - 1,
            "recordFrame": record_frame,
            "trackIndex": 2,
            "mediaType": 1 # Video type
        }
        broll_insertions.append(broll_info)
        
    media_pool.AppendToTimeline(broll_insertions)
    
    pm.SaveProject()
    print("[+] DaVinci Resolve Timeline Assembly Complete!")

if __name__ == "__main__":
    assemble_project()
