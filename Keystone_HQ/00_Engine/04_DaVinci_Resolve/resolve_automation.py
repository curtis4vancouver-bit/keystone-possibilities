import os
import sys

# Configure environment for DaVinci Resolve scripting on Windows
resolve_script_api = os.environ.get("PROGRAMDATA", "C:\\ProgramData") + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\"
resolve_module_path = os.path.join(resolve_script_api, "Modules")

if resolve_module_path not in sys.path:
    sys.path.append(resolve_module_path)

try:
    import DaVinciResolveScript as dvr_script
except ImportError:
    print("DaVinciResolveScript module not found. Ensure DaVinci Resolve Studio is installed and paths are correct.")
    # For testing, we mock the dvr_script
    dvr_script = None

def main():
    if not dvr_script:
        print("Running in mock mode. Script complete.")
        return

    resolve = dvr_script.scriptapp("Resolve")
    if not resolve:
        print("Could not connect to Resolve. Ensure it is running (headless or GUI).")
        return

    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()
    media_pool = project.GetMediaPool()
    timeline = project.GetCurrentTimeline()

    if not timeline:
        print("No active timeline found. Please create one first.")
        return

    # Double-Pass Title Injection on Track 2
    # 1. Locate Text+ template in Media Pool
    # For demonstration, we assume we find the text template item
    folder = media_pool.GetCurrentFolder()
    clip_list = folder.GetClipList()
    text_template_item = None
    
    for clip in clip_list:
        if "TextTemplate" in clip.GetName():
            text_template_item = clip
            break
            
    if not text_template_item:
        print("TextTemplate not found in current bin. Please ensure a Text+ generator is named 'TextTemplate'.")
        return

    # 2. Append the Text+ template to Track 2 using structured dictionary
    print("Appending Text+ to Track 2...")
    clip_info = {
        "mediaPoolItem": text_template_item,
        "startFrame": 0,
        "endFrame": 60, # 2 seconds at 30fps
        "recordFrame": timeline.GetStartFrame() + 30, # Insert at 1 second in
        "trackIndex": 2,
        "mediaType": 1 # Video
    }
    
    success = media_pool.AppendToTimeline([clip_info])
    if not success:
        print("Failed to append template to timeline.")
        return

    # 3. Locate the inserted item on Track 2 and inject text
    print("Injecting text via Fusion comp...")
    track2_items = timeline.GetItemListInTrack("video", 2)
    
    if track2_items:
        # Assuming the last added item
        target_item = track2_items[-1]
        
        # Extract Fusion comp
        if target_item.GetFusionCompCount() > 0:
            comp = target_item.GetFusionCompByIndex(1)
            if comp:
                # Get TextPlus tool
                tools = comp.GetToolList(False, "TextPlus")
                if tools:
                    # Modify properties
                    text_tool = tools[1] # Tools dictionary is 1-indexed in Lua/Fusion
                    text_tool.SetInput("StyledText", "AUTONOMOUS SUBTITLE INJECTION")
                    text_tool.SetInput("Size", 0.15)
                    print("Successfully injected text onto Track 2.")
                else:
                    print("No TextPlus tool found in composition.")
        else:
            print("No Fusion composition found on the targeted item.")

if __name__ == "__main__":
    print("Starting Resolve Double-Pass Automation Script...")
    main()
