import sys
import os

def setup_resolve_path():
    if os.name == "nt": # Windows
        sys.path.append(r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules")
    elif os.name == "posix": # macOS / Linux
        sys.path.append(r"/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

setup_resolve_path()

try:
    import DaVinciResolveScript as dvr
except ImportError:
    print("Unable to locate DaVinciResolveScript API. Verify DaVinci Developer modules are installed.")
    sys.exit(1)

def build_episodic_video(video_path: str, audio_path: str, music_path: str, output_name: str):
    resolve = dvr.scriptapp("Resolve")
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    media_pool = project.GetMediaPool()
    
    # 1. Setup media storage and import assets
    media_storage = resolve.GetMediaStorage()
    imported_clips = media_storage.AddItemsToMediaPool([video_path, audio_path, music_path])
    
    if len(imported_clips) < 3:
        print("Error: Could not import all assets into Media Pool.")
        return False
        
    video_item = imported_clips[0]
    audio_item = imported_clips[1]
    music_item = imported_clips[2]
    
    # 2. Create a clean empty timeline
    timeline = media_pool.CreateEmptyTimeline(output_name)
    project.SetCurrentTimeline(timeline)
    
    # 3. Structure clip info arrays to place items on specific tracks
    # Track 1 (V1): High-Performance Architectural Video (Google Flow)
    # Track 2 (A1): ElevenLabs Voice Clone (Speech)
    # Track 3 (A2): Keystone Melodic House Track (124 BPM Background)
    
    # Get audio length to bound the timeline
    audio_duration = float(audio_item.GetClipProperty("Duration")) # Returns length in frames or seconds
    
    video_clip_info = {
        "mediaPoolItem": video_item,
        "startFrame": 0,
        "endFrame": int(audio_duration * 24), # Assuming 24fps timeline
        "mediaType": 1, # Video only
        "trackIndex": 1
    }
    
    audio_clip_info = {
        "mediaPoolItem": audio_item,
        "startFrame": 0,
        "endFrame": int(audio_duration * 24),
        "mediaType": 2, # Audio only
        "trackIndex": 1
    }
    
    music_clip_info = {
        "mediaPoolItem": music_item,
        "startFrame": 0,
        "endFrame": int(audio_duration * 24),
        "mediaType": 2, # Audio only
        "trackIndex": 2
    }
    
    # Append the structured table of tables to the timeline
    media_pool.AppendToTimeline([video_clip_info])
    media_pool.AppendToTimeline([audio_clip_info])
    media_pool.AppendToTimeline([music_clip_info])
    
    # 4. Save and configure render settings
    project_manager.SaveProject()
    print(f"Timeline '{output_name}' successfully built and synced.")
    return True

if __name__ == "__main__":
    # Command-line arguments: video_file, voiceover_file, background_music, output_timeline_name
    if len(sys.argv) >= 5:
        build_episodic_video(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("Usage: python video_builder.py <video_file> <voiceover_file> <background_music> <output_timeline_name>")
