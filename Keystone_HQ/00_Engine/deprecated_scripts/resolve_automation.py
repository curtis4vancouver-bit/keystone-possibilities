#!/usr/bin/env python3
"""
KEYSTONE HQ - DAVINCI RESOLVE AUTOMATION ENGINE & CO-PILOT
Bootstraps connection to DaVinci Resolve Studio and exposes timeline analytics,
YouTube chapter generation, and biophilic text overlay injection.
"""

import os
import sys

def init_resolve_paths():
    """Configures environment variables required to script DaVinci Resolve on Windows."""
    print("🔧 Bootstrapping DaVinci Resolve Scripting Environment...")
    
    # 1. Add standard scripting folders to system path
    program_data = os.environ.get("PROGRAMDATA", "C:\\ProgramData")
    resolve_script_api = os.path.join(program_data, "Blackmagic Design", "DaVinci Resolve", "Support", "Developer", "Scripting")
    
    # Standard Python API location
    sys.path.append(os.path.join(resolve_script_api, "Modules"))
    
    # Environment variables DaVinci expects
    os.environ["RESOLVE_SCRIPT_API"] = resolve_script_api
    os.environ["RESOLVE_SCRIPT_LIB"] = "C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
    
    print(f"✅ Set RESOLVE_SCRIPT_API: {resolve_script_api}")
    print(f"✅ Set RESOLVE_SCRIPT_LIB: {os.environ['RESOLVE_SCRIPT_LIB']}")

def get_resolve():
    """Establishes connection to the running instance of DaVinci Resolve."""
    try:
        import DaVinciResolveScript as dvr
        resolve = dvr.scriptapp("Resolve")
        if not resolve:
            print("❌ Error: Resolve is running but could not establish scripting link.")
            print("💡 Tip: Ensure 'External Scripting Using Local' is enabled in Resolve -> Preferences -> System -> General.")
            return None
        return resolve
    except ImportError:
        print("❌ Error: DaVinciResolveScript Python module could not be imported.")
        print("💡 Tip: Ensure Resolve is installed in default path and environment paths are configured.")
        return None
    except Exception as e:
        print(f"❌ Connection error: {str(e)}")
        return None

def analyze_active_timeline():
    """Inspects the open project and generates detailed timeline diagnostics."""
    resolve = get_resolve()
    if not resolve:
        return
        
    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    
    if not project:
        print("📁 Status: No active project loaded. Open a project in Resolve to begin.")
        return
        
    print(f"\n📂 Active Project: {project.GetName()}")
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("🎞️ Status: No timeline loaded in the active project.")
        return
        
    print(f"🎞️ Active Timeline: {timeline.GetName()}")
    print(f"⏱️ Start Timecode: {timeline.GetStartFrame()}")
    
    # Fetch markers
    markers = timeline.GetMarkers()
    if markers:
        print(f"\n📍 Timeline Markers Found ({len(markers)}):")
        for frame, marker in sorted(markers.items()):
            print(f"  - Frame {frame}: {marker.get('name', 'No Name')} [{marker.get('color', 'Blue')}] - {marker.get('note', '')}")
            
        # Generate YouTube Chapters
        print("\n📺 GENERATED YOUTUBE CHAPTERS (Ready to Copy):")
        print("-" * 50)
        # Convert frames to standard HH:MM:SS format (assuming 24fps default)
        for frame, marker in sorted(markers.items()):
            fps = 24  # Standard cinematic framerate
            total_seconds = int(frame / fps)
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            
            timecode_str = f"{minutes:02d}:{seconds:02d}"
            if hours > 0:
                timecode_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
            print(f"{timecode_str} - {marker.get('name', 'Chapter')}")
        print("-" * 50)
    else:
        print("\n📍 Status: No markers found on this timeline. Add markers in Resolve to auto-generate chapters.")

def main():
    init_resolve_paths()
    resolve = get_resolve()
    
    if resolve:
        print("🚀 Successfully connected to DaVinci Resolve!")
        analyze_active_timeline()
    else:
        print("\n⚠️ Connection pending. Run this script once DaVinci Resolve is fully launched and your project is open.")

if __name__ == "__main__":
    main()
