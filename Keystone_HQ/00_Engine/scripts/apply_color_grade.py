#!/usr/bin/env python3
"""
Keystone DaVinci Resolve DRX Grade Application
Applies a DRX node tree template to timeline clips.

Usage:
  # Apply to all video clips in Track 1
  python scripts/apply_color_grade.py --drx "04_DaVinci_Resolve/Grades/braw_cinematic_base.drx" --track 1

  # Apply to all video clips in the active timeline
  python scripts/apply_color_grade.py --drx "04_DaVinci_Resolve/Grades/braw_cinematic_base.drx" --all
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import argparse
from typing import List

def setup_resolve_path():
    if os.name == "nt": # Windows
        sys.path.append(r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules")
    elif os.name == "posix": # macOS / Linux
        sys.path.append(r"/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")

setup_resolve_path()

try:
    import DaVinciResolveScript as dvr
except ImportError:
    print("❌ Unable to locate DaVinciResolveScript API. Verify DaVinci Developer modules are installed.")
    sys.exit(1)


def get_all_video_clips(timeline) -> List:
    clips = []
    video_track_count = timeline.GetTrackCount("video")
    for track_index in range(1, video_track_count + 1):
        items = timeline.GetItemListInTrack("video", track_index)
        if items:
            clips.extend(items)
    return clips


def get_clips_by_track(timeline, track_index: int) -> List:
    items = timeline.GetItemListInTrack("video", track_index)
    return items if items else []


def get_clips_by_color(timeline, color_name: str) -> List:
    clips = []
    video_track_count = timeline.GetTrackCount("video")
    for track_index in range(1, video_track_count + 1):
        items = timeline.GetItemListInTrack("video", track_index)
        if items:
            for item in items:
                if item.GetClipColor().lower() == color_name.lower():
                    clips.append(item)
    return clips


def apply_drx_to_clips(clips: List, drx_path: str) -> int:
    if not os.path.isfile(drx_path):
        print(f"❌ DRX file not found: {drx_path}")
        return 0

    success_count = 0
    for clip in clips:
        graph = clip.GetNodeGraph()
        if not graph:
            print(f"  ❌ No node graph available for clip: {clip.GetName()}")
            continue

        # gradeMode = 0: "No keyframes", 1: "Source Timecode aligned", 2: "Start Frames aligned"
        if graph.ApplyGradeFromDRX(drx_path, 0):
            success_count += 1
            print(f"  ✅ DRX applied: {clip.GetName()}")
        else:
            print(f"  ❌ DRX application failed: {clip.GetName()}")

    return success_count


def main():
    parser = argparse.ArgumentParser(description="Apply DRX grading templates to DaVinci Resolve timeline clips")
    
    # Target selection
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument('--all', action='store_true', help='Apply to all video clips in active timeline')
    target_group.add_argument('--track', type=int, help='Apply to specific video track (1-based)')
    target_group.add_argument('--color', type=str, help='Apply to clips with specific color (e.g. Orange)')

    # Grading parameters
    parser.add_argument('--drx', type=str, required=True, help='Path to the DRX template file')

    args = parser.parse_args()

    # Convert relative DRX path to absolute path
    drx_path = os.path.abspath(args.drx)
    if not os.path.exists(drx_path):
        print(f"❌ DRX path does not exist: {drx_path}")
        sys.exit(1)

    print("=" * 60)
    print("🎨 Keystone DaVinci Resolve DRX Grade Application")
    print("=" * 60)

    # Connect to DaVinci Resolve
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        print("❌ Could not connect to DaVinci Resolve. Ensure DaVinci Resolve Studio is running.")
        sys.exit(1)

    pm = resolve.GetProjectManager()
    project = pm.GetCurrentProject()
    if not project:
        print("❌ No project is currently open in DaVinci Resolve.")
        sys.exit(1)

    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("❌ No active timeline is open.")
        sys.exit(1)

    print(f"Connected to Project: {project.GetName()}")
    print(f"Active Timeline:     {timeline.GetName()}")
    print(f"Loading DRX File:    {drx_path}")
    print()

    # Get target clips
    if args.all:
        clips = get_all_video_clips(timeline)
        print(f"Targeting: All video clips ({len(clips)} found)")
    elif args.track:
        clips = get_clips_by_track(timeline, args.track)
        print(f"Targeting: Video Track {args.track} ({len(clips)} clips found)")
    elif args.color:
        clips = get_clips_by_color(timeline, args.color)
        print(f"Targeting: Clips of color '{args.color}' ({len(clips)} found)")

    if not clips:
        print("❌ No target clips found matching the criteria.")
        sys.exit(0)

    # Refresh LUT list first in case DRX uses a LUT
    project.RefreshLUTList()

    # Apply grading
    print("Applying grading template...")
    success = apply_drx_to_clips(clips, drx_path)
    
    print()
    print("=" * 60)
    print(f"🎉 Grading Complete: {success}/{len(clips)} clips successfully graded.")
    print("=" * 60)


if __name__ == "__main__":
    main()
