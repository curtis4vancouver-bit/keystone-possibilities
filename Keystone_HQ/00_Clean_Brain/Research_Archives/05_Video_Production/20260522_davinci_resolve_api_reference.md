# DaVinci Resolve 19 - Python Scripting API Complete Reference

**Research Date:** May 22, 2026
**Domain:** davinci_resolve
**Status:** Comprehensive reference - verified against community docs and official [[README|README]]
**Requires:** DaVinci Resolve Studio (paid) - free version does NOT expose the scripting API

---

## Table of Contents

1. [Environment Setup](#environment-setup)
2. [API Object Hierarchy](#api-object-hierarchy)
3. [Resolve Object](#resolve-object)
4. [ProjectManager Object](#projectmanager-object)
5. [Project Object](#project-object)
6. [MediaStorage Object](#mediastorage-object)
7. [MediaPool Object](#mediapool-object)
8. [MediaPoolItem Object](#mediapoolitem-object)
9. [Folder Object](#folder-object)
10. [Timeline Object](#timeline-object)
11. [TimelineItem Object](#timelineitem-object)
12. [Gallery and GalleryStill Objects](#gallery-objects)
13. [Fusion Composition Scripting](#fusion-composition-scripting)
14. [Color Grading and LUT Automation](#color-grading-and-lut-automation)
15. [Render Queue Management](#render-queue-management)
16. [Markers and Metadata](#markers-and-metadata)
17. [Audio Track Management](#audio-track-management)
18. [Project Settings Reference](#project-settings-reference)
19. [YouTube Production Automation Example](#youtube-production-automation-example)
20. [Sources and Community Resources](#sources)

---

## 1. Environment Setup <a name="environment-setup"></a>

### Prerequisites

- **DaVinci Resolve Studio** (paid version required for API access)
- **Python 3.7+** (3.10+ recommended for Resolve 19)
- **External scripting enabled:** Preferences > System > [[general|General]] > "External scripting using" set to "Local"

### Environment Variables (Windows)

```powershell
# Set these in System Environment Variables or your script launcher
$env:RESOLVE_SCRIPT_API = "C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting"
$env:RESOLVE_SCRIPT_LIB = "C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
$env:PYTHONPATH = "$env:RESOLVE_SCRIPT_API\Modules;$env:PYTHONPATH"
```

### Environment Variables (macOS)

```bash
export RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules:$PYTHONPATH"
```

### Environment Variables (Linux)

```bash
export RESOLVE_SCRIPT_API="/opt/resolve/Developer/Scripting"
export RESOLVE_SCRIPT_LIB="/opt/resolve/libs/Fusion/fusionscript.so"
export PYTHONPATH="$RESOLVE_SCRIPT_API/Modules:$PYTHONPATH"
```

### Connection Boilerplate

```python
import DaVinciResolveScript as dvr_script

resolve = dvr_script.scriptapp("Resolve")
project_manager = resolve.GetProjectManager()
project = project_manager.GetCurrentProject()
media_pool = project.GetMediaPool()
timeline = project.GetCurrentTimeline()
```

### Script Locations (for Workspace > Scripts menu)

| OS | Path |
|---|---|
| Windows | `%AppData%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp\` |
| macOS | `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Comp/` |
| Linux | `~/.local/share/DaVinciResolve/Fusion/Scripts/Comp/` |

When scripts are placed in these folders, they appear in the **Workspace > Scripts** menu inside Resolve. Scripts run from within Resolve automatically get `resolve`, `fusion`, and `bmd` global objects.

---

## 2. API Object Hierarchy <a name="api-object-hierarchy"></a>

```
Resolve
  |-- GetMediaStorage() --> MediaStorage
  |-- GetProjectManager() --> ProjectManager
  |     |-- GetCurrentProject() --> Project
  |           |-- GetMediaPool() --> MediaPool
  |           |     |-- GetRootFolder() --> Folder
  |           |     |     |-- GetSubFolderList() --> [Folder, ...]
  |           |     |     |-- GetClipList() --> [MediaPoolItem, ...]
  |           |     |-- CreateEmptyTimeline(name) --> Timeline
  |           |     |-- AppendToTimeline(clips) --> [TimelineItem, ...]
  |           |-- GetCurrentTimeline() --> Timeline
  |           |     |-- GetItemListInTrack(type, idx) --> [TimelineItem, ...]
  |           |-- GetGallery() --> Gallery
  |                 |-- GetCurrentStillAlbum() --> GalleryStillAlbum
  |                       |-- GetStills() --> [GalleryStill, ...]
  |-- Fusion() --> Fusion
  |-- OpenPage(pageName)
```

---

## 3. Resolve Object <a name="resolve-object"></a>

The top-level entry point to the entire API.

| Method | Returns | Description |
|---|---|---|
| `GetMediaStorage()` | MediaStorage | Access to media storage browser |
| `GetProjectManager()` | ProjectManager | Main project management object |
| `OpenPage(pageName)` | Bool | Switch page: "media", "cut", "edit", "fusion", "color", "fairlight", "deliver" |
| `GetCurrentPage()` | String | Returns name of current page |
| `GetProductName()` | String | e.g., "DaVinci Resolve Studio" |
| `GetVersion()` | [list] | Returns version info as list |
| `GetVersionString()` | String | e.g., "19.0.2" |
| `Fusion()` | Fusion | Returns the Fusion object for Fusion scripting |
| `LoadLayoutPreset(presetName)` | Bool | Loads a saved UI layout |
| `UpdateLayoutPreset(presetName)` | Bool | Updates a layout preset with current layout |
| `ExportLayoutPreset(presetName, path)` | Bool | Exports layout preset to file |
| `ImportLayoutPreset(path, presetName)` | Bool | Imports layout from file |
| `Quit()` | None | Quits DaVinci Resolve |

---

## 4. ProjectManager Object <a name="projectmanager-object"></a>

| Method | Returns | Description |
|---|---|---|
| `CreateProject(projectName)` | Project | Creates and opens a new project |
| `DeleteProject(projectName)` | Bool | Deletes specified project |
| `LoadProject(projectName)` | Project | Loads an existing project |
| `GetCurrentProject()` | Project | Returns active project |
| `SaveProject()` | Bool | Saves current project |
| `CloseProject(project)` | Bool | Closes specified project |
| `CreateFolder(folderName)` | Bool | Creates a project folder in project manager |
| `DeleteFolder(folderName)` | Bool | Deletes a project folder |
| `GetProjectListInCurrentFolder()` | [String] | Lists projects in current folder |
| `GetFolderListInCurrentFolder()` | [String] | Lists folders in current folder |
| `GotoRootFolder()` | Bool | Navigates to root project folder |
| `GotoParentFolder()` | Bool | Navigates up one level |
| `OpenFolder(folderName)` | Bool | Opens a project manager folder |
| `ImportProject(filePath, projectName)` | Bool | Imports a .drp project file |
| `ExportProject(projectName, filePath, withStills)` | Bool | Exports project to .drp file |
| `RestoreProject(filePath, projectName)` | Bool | Restores from .drp backup |

---

## 5. Project Object <a name="project-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetMediaPool()` | MediaPool | Returns the MediaPool |
| `GetTimelineCount()` | Int | Number of timelines |
| `GetTimelineByIndex(idx)` | Timeline | 1-based [[wiki/index|index]] |
| `GetCurrentTimeline()` | Timeline | Active timeline |
| `SetCurrentTimeline(timeline)` | Bool | Switch active timeline |
| `GetGallery()` | Gallery | Access gallery stills |
| `GetName()` | String | Project name |
| `SetName(name)` | Bool | Rename project |
| `GetPresetList()` | [String] | Available render presets |
| `SetPreset(presetName)` | Bool | Apply render preset |
| `GetSetting(settingName)` | String | Get project setting (pass "" for dict of all) |
| `SetSetting(settingName, value)` | Bool | Set project setting |
| `GetRenderFormats()` | {String: String} | Dict of available render formats |
| `GetRenderCodecs(formatName)` | {String: String} | Codecs for a given format |
| `GetCurrentRenderFormatAndCodec()` | {format, codec} | Current render format/codec |
| `SetCurrentRenderFormatAndCodec(format, codec)` | Bool | Set render format and codec |
| `SetRenderSettings(settings)` | Bool | Set render parameters dict |
| `GetRenderJobList()` | [{jobInfo}] | All render jobs |
| `GetRenderPresetList()` | [String] | All render presets |
| `AddRenderJob()` | String | Adds job to queue, returns jobId |
| `DeleteRenderJob(jobId)` | Bool | Remove job from queue |
| `DeleteAllRenderJobs()` | Bool | Clear render queue |
| `StartRendering(jobId)` | Bool | Start render (specific or all) |
| `StartRendering(isInteractiveMode)` | Bool | Start with optional UI mode |
| `StopRendering()` | None | Stop active renders |
| `IsRenderingInProgress()` | Bool | Check render status |
| `GetRenderJobStatus(jobId)` | {status} | Returns job completion/error info |
| `LoadRenderPreset(presetName)` | Bool | Load a render preset |
| `SaveAsNewRenderPreset(presetName)` | Bool | Save current settings as preset |
| `InsertAudioToCurrentTrackAtPlayhead(mediaPath, startOffset, duration)` | Bool | Insert audio clip |

---

## 6. MediaStorage Object <a name="mediastorage-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetMountedVolumeList()` | [String] | List of mounted drives/volumes |
| `GetSubFolderList(folderPath)` | [String] | Subfolders at path |
| `GetFileList(folderPath)` | [String] | Files at path |
| `RevealInStorage(filePath)` | Bool | Highlights file in media storage panel |
| `AddItemListToMediaPool(items)` | [MediaPoolItem] | Import items from storage to pool |
| `AddItemListToMediaPool(items, startFrame, endFrame)` | [MediaPoolItem] | Import with in/out points |
| `AddClipMattesToMediaPool(item, paths, stereoEye)` | Bool | Add matte files to clip |

---

## 7. MediaPool Object <a name="mediapool-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetRootFolder()` | Folder | Root media pool folder |
| `AddSubFolder(folder, name)` | Folder | Create subfolder |
| `RefreshFolders()` | Bool | Refresh folder display |
| `CreateEmptyTimeline(name)` | Timeline | New empty timeline |
| `CreateTimelineFromClips(name, clips)` | Timeline | Timeline pre-populated with clips |
| `AppendToTimeline(clips)` | [TimelineItem] | Append clips to current timeline |
| `AppendToTimeline(clipInfos)` | [TimelineItem] | Append with detailed placement |
| `ImportMedia(filePaths)` | [MediaPoolItem] | Import files to current folder |
| `ImportMedia(clipInfos)` | [MediaPoolItem] | Import with metadata |
| `ExportMetadata(fileName, clips)` | Bool | Export clip metadata to CSV |
| `GetCurrentFolder()` | Folder | Currently selected folder |
| `SetCurrentFolder(folder)` | Bool | Set target folder |
| `DeleteClips(clips)` | Bool | Remove clips from pool |
| `DeleteFolders(folders)` | Bool | Remove folders |
| `MoveClips(clips, targetFolder)` | Bool | Move clips between folders |
| `MoveFolders(folders, targetFolder)` | Bool | Move folders |
| `GetClipMatteList(item)` | [paths] | Get matte files for a clip |
| `GetTimelineMatteList(timeline)` | [paths] | Get mattes used in timeline |
| `DeleteTimelines(timelines)` | Bool | Delete timelines |
| `GetUniqueId()` | String | Unique identifier for media pool |
| `ImportTimelineFromFile(filePath, options)` | Timeline | Import EDL/XML/AAF/FCPXML |

### AppendToTimeline clipInfo Dictionary Keys

```python
clip_info = {
    "mediaPoolItem": media_pool_item,  # Required: the MediaPoolItem object
    "startFrame": 0,                    # Source start frame
    "endFrame": 100,                    # Source end frame
    "mediaType": 1,                     # 1 = video only, 2 = audio only
    "trackIndex": 1,                    # Target track (1-based)
    "recordFrame": 0                    # Timeline position (record frame)
}
```

---

## 8. MediaPoolItem Object <a name="mediapoolitem-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetName()` | String | Clip name |
| `GetMetadata(key)` | String/Dict | Get metadata (empty key = all metadata dict) |
| `SetMetadata(key, value)` | Bool | Set metadata field |
| `SetMetadata({key: value, ...})` | Bool | Set multiple metadata fields |
| `GetMediaId()` | String | Unique media identifier |
| `AddMarker(frameId, color, name, note, duration, customData)` | Bool | Add clip marker |
| `GetMarkers()` | {frameId: {info}} | Get all markers |
| `DeleteMarkersByColor(color)` | Bool | Delete markers by color |
| `DeleteMarkerAtFrame(frameNum)` | Bool | Delete specific marker |
| `DeleteMarkerByCustomData(customData)` | Bool | Delete by custom data field |
| `AddFlag(color)` | Bool | Add flag to clip |
| `GetFlagList()` | [String] | Get all flags |
| `ClearFlags(color)` | Bool | Clear flags ("" for all) |
| `GetClipColor()` | String | Get clip color label |
| `SetClipColor(color)` | Bool | Set clip color label |
| `GetClipProperty(propertyName)` | String/Dict | Get property (empty = all props) |
| `SetClipProperty(propertyName, value)` | Bool | Set clip property |
| `LinkProxyMedia(proxyPath)` | Bool | Link proxy media file |
| `UnlinkProxyMedia()` | Bool | Unlink proxy |
| `ReplaceClip(filePath)` | Bool | Replace media file |
| `GetUniqueId()` | String | Unique identifier |

---

## 9. Folder Object <a name="folder-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetClipList()` | [MediaPoolItem] | All clips in folder |
| `GetName()` | String | Folder name |
| `GetSubFolderList()` | [Folder] | Child folders |
| `GetUniqueId()` | String | Unique identifier |

---

## 10. Timeline Object <a name="timeline-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetName()` | String | Timeline name |
| `SetName(name)` | Bool | Rename timeline |
| `GetStartFrame()` | Int | Start frame of timeline |
| `GetEndFrame()` | Int | End frame of timeline |
| `GetTrackCount(trackType)` | Int | Count tracks: "audio", "video", "subtitle" |
| `GetItemListInTrack(trackType, [[wiki/index|index]])` | [TimelineItem] | Get clips in track (1-based) |
| `AddMarker(frameId, color, name, note, duration, customData)` | Bool | Add timeline marker |
| `GetMarkers()` | {frameId: {info}} | Get all markers |
| `DeleteMarkersByColor(color)` | Bool | Delete markers by color |
| `DeleteMarkerAtFrame(frameNum)` | Bool | Delete specific marker |
| `DeleteMarkerByCustomData(customData)` | Bool | Delete by custom data |
| `GetSetting(settingName)` | String/Dict | Get timeline setting (empty = all) |
| `SetSetting(settingName, value)` | Bool | Set timeline setting |
| `InsertGeneratorIntoTimeline(generatorName)` | TimelineItem | Insert generator (e.g., "Solid Color") |
| `InsertFusionGeneratorIntoTimeline(generatorName)` | TimelineItem | Insert Fusion generator |
| `InsertTitleIntoTimeline(titleName)` | TimelineItem | Insert title template |
| `InsertFusionTitleIntoTimeline(titleName)` | TimelineItem | Insert Fusion title template |
| `GrabStill()` | GalleryStill | Capture still from current frame |
| `GrabAllStills(stillFrameSource)` | [GalleryStill] | Grab all stills |
| `SetCurrentTimecode(timecode)` | Bool | Set playhead position |
| `GetCurrentTimecode()` | String | Get playhead timecode |
| `GetCurrentVideoItem()` | TimelineItem | Item under playhead |
| `GetTrackName(trackType, trackIndex)` | String | Get track name |
| `SetTrackName(trackType, trackIndex, name)` | Bool | Set track name |
| `DuplicateTimeline(name)` | Timeline | Duplicate timeline |
| `CreateCompoundClip(timelineItems, clipInfo)` | TimelineItem | Create compound clip |
| `CreateFusionClip(timelineItems)` | TimelineItem | Create Fusion clip from items |
| `Export(filePath, exportType, exportSubtype)` | Bool | Export EDL/XML/AAF etc. |
| `GetUniqueId()` | String | Unique identifier |
| `AddTrack(trackType, trackOptions)` | Bool | Add video/audio/subtitle track |
| `DeleteTrack(trackType, trackIndex)` | Bool | Delete a track |
| `SetTrackEnable(trackType, trackIndex, enabled)` | Bool | Enable/disable track |
| `GetIsTrackEnabled(trackType, trackIndex)` | Bool | Check track [[STATE|state]] |
| `SetTrackLock(trackType, trackIndex, locked)` | Bool | Lock/unlock track |
| `GetIsTrackLocked(trackType, trackIndex)` | Bool | Check lock [[STATE|state]] |
| `ApplyGradeFromDRX(path, grade, items)` | Bool | Apply color grade from .drx file |

---

## 11. TimelineItem Object <a name="timelineitem-object"></a>

| Method | Returns | Description |
|---|---|---|
| `GetName()` | String | Item/clip name |
| `GetDuration()` | Int | Duration in frames |
| `GetEnd()` | Int | End frame on timeline |
| `GetStart()` | Int | Start frame on timeline |
| `GetLeftOffset()` | Int | Left trim offset |
| `GetRightOffset()` | Int | Right trim offset |
| `SetProperty(propertyName, value)` | Bool | Set item property |
| `GetProperty(propertyName)` | String/Dict | Get item property |
| `GetMediaPoolItem()` | MediaPoolItem | Source pool item |
| `GetFusionCompCount()` | Int | Number of Fusion compositions |
| `GetFusionCompByIndex(idx)` | FusionComp | Get Fusion comp (1-based) |
| `GetFusionCompNameList()` | [String] | List comp names |
| `SetClipColor(color)` | Bool | Set clip color label |
| `GetClipColor()` | String | Get clip color |
| `ClearClipColor()` | Bool | Clear color label |
| `AddFlag(color)` | Bool | Add flag |
| `GetFlagList()` | [String] | Get flags |
| `ClearFlags(color)` | Bool | Clear flags |
| `AddMarker(frameId, color, name, note, duration, customData)` | Bool | Add marker |
| `GetMarkers()` | {frameId: {info}} | Get markers |
| `DeleteMarkersByColor(color)` | Bool | Delete by color |
| `DeleteMarkerAtFrame(frameNum)` | Bool | Delete at frame |
| `DeleteMarkerByCustomData(data)` | Bool | Delete by custom data |
| `AddFusionComp()` | FusionComp | Create new Fusion comp |
| `ImportFusionComp(path)` | FusionComp | Import .comp file |
| `ExportFusionComp(path, compIndex)` | Bool | Export .comp file |
| `DeleteFusionCompByName(compName)` | Bool | Delete Fusion comp |
| `LoadFusionCompByName(compName)` | FusionComp | Load comp by name |
| `RenameFusionCompByName(oldName, newName)` | Bool | Rename comp |
| `GetNodeGraph(version)` | Graph | Color node graph |
| `GetColorGroup()` | ColorGroup | Color group assignment |
| `SetLUT(nodeIndex, lutPath)` | Bool | Apply LUT to node (1-based [[wiki/index|index]]) |
| `GetLUT(nodeIndex)` | String | Get LUT path from node |
| `SetCDL(CDL_map)` | Bool | Apply CDL values |
| `GetCDL()` | {CDL_map} | Get CDL values |
| `AddTake(mediaPoolItem, startFrame, endFrame)` | Bool | Add take to multicam |
| `GetSelectedTakeIndex()` | Int | Current selected take |
| `GetTakesCount()` | Int | Number of takes |
| `GetTakeByIndex(idx)` | {takeInfo} | Get take details |
| `DeleteTakeByIndex(idx)` | Bool | Delete take |
| `SelectTakeByIndex(idx)` | Bool | Switch to take |
| `FinalizeTake()` | Bool | Finalize multicam take |
| `CopyGrades(tgtTimelineItems)` | Bool | Copy grades to other items |
| `UpdateSidecar()` | Bool | Update sidecar file |

---

## 12. Gallery and GalleryStill Objects <a name="gallery-objects"></a>

### Gallery

| Method | Returns | Description |
|---|---|---|
| `GetGalleryStillAlbums()` | [GalleryStillAlbum] | List all albums |
| `GetCurrentStillAlbum()` | GalleryStillAlbum | Active album |
| `SetCurrentStillAlbum(album)` | Bool | Switch album |

### GalleryStillAlbum

| Method | Returns | Description |
|---|---|---|
| `GetStills()` | [GalleryStill] | Get all stills |
| `GetLabel(idx)` | String | Get label for still |
| `SetLabel(idx, label)` | Bool | Set label |
| `ExportStills(stills, folderPath, filePrefix, format)` | Bool | Export stills |
| `DeleteStills(stills)` | Bool | Delete stills |

---

## 13. Fusion Composition Scripting <a name="fusion-composition-scripting"></a>

Fusion compositions live inside TimelineItems. You access them to create text overlays, effects, and motion graphics.

### Creating a Text Overlay

```python
# Get the current timeline item
timeline = project.GetCurrentTimeline()
items = timeline.GetItemListInTrack("video", 1)

# Create a Fusion clip from existing items
fusion_clip = timeline.CreateFusionClip(items)

# OR create a new Fusion comp on a timeline item
comp = items[0].AddFusionComp()

# Access the Fusion composition
comp = items[0].GetFusionCompByIndex(1)

# Add a Text+ node
text_node = comp.AddTool("TextPlus")
text_node.SetInput("StyledText", "YOUR TITLE HERE")
text_node.SetInput("Font", "Open Sans")
text_node.SetInput("Size", 0.08)
text_node.SetInput("Center", {1: 0.5, 2: 0.9})  # x, y position

# Connect to MediaOut if needed
media_out = comp.FindTool("MediaOut1")
if media_out:
    media_out.SetInput("Input", text_node.Output)
```

### Common Fusion Tools

| Tool Name | Usage |
|---|---|
| `TextPlus` | Rich text with formatting |
| `Background` | Solid/gradient background |
| `Merge` | Composite two images |
| `Transform` | Position, scale, rotate |
| `Blur` | Gaussian blur |
| `ColorCorrector` | Color adjustment |
| `Rectangle` | Rectangular mask/shape |
| `Polygon` | Freeform mask |

---

## 14. Color Grading and LUT Automation <a name="color-grading-and-lut-automation"></a>

### Apply LUT to All Clips

```python
timeline = project.GetCurrentTimeline()
lut_path = "C:/LUTs/FilmLook.cube"

# Iterate all video clips on track 1
items = timeline.GetItemListInTrack("video", 1)
for item in items:
    item.SetLUT(1, lut_path)  # nodeIndex is 1-based
```

### Apply Grade from .drx File

```python
# Export/import complete grades with node trees
items = timeline.GetItemListInTrack("video", 1)
timeline.ApplyGradeFromDRX("/path/to/grade.drx", 0, items)
```

### CDL (Color Decision List) Operations

```python
item = timeline.GetCurrentVideoItem()

# Get current CDL values
cdl = item.GetCDL()
# Returns: {"NodeIndex": "1", "Slope": "1 1 1", "Offset": "0 0 0",
#           "Power": "1 1 1", "Saturation": "1"}

# Set CDL values
item.SetCDL({
    "NodeIndex": "1",
    "Slope": "1.1 1.0 0.9",
    "Offset": "0.01 0.0 -0.01",
    "Power": "1.0 1.0 1.0",
    "Saturation": "1.2"
})
```

---

## 15. Render Queue Management <a name="render-queue-management"></a>

### SetRenderSettings Keys

| Key | Type | Description |
|---|---|---|
| `TargetDir` | String | Output directory path |
| `CustomName` | String | Output filename |
| `FormatWidth` | Int | Output width in pixels |
| `FormatHeight` | Int | Output height in pixels |
| `FrameRate` | Float | Output frame rate |
| `PixelAspectRatio` | String | Pixel aspect ratio |
| `ExportVideo` | Bool | Enable video export |
| `ExportAudio` | Bool | Enable audio export |
| `ExportAlpha` | Bool | Include alpha channel |
| `SelectAllFrames` | Bool | True = entire timeline |
| `MarkIn` | Int | Start frame (if not all frames) |
| `MarkOut` | Int | End frame (if not all frames) |
| `VideoQuality` | Int/String | Quality setting |
| `AudioCodec` | String | Audio codec name |
| `AudioBitDepth` | Int | Audio bit depth |
| `AudioSampleRate` | Int | Audio sample rate |
| `ColorSpaceTag` | String | Output color space |
| `GammaTag` | String | Output gamma |
| `EncodingProfile` | String | Encoding profile |
| `MultiPassEncode` | Bool | Multi-pass encoding |
| `NetworkOptimization` | Bool | Network optimization |
| `UniqueFilenameStyle` | Int | 0=Prefix, 1=Suffix |

### Complete Render Workflow

```python
project = resolve.GetProjectManager().GetCurrentProject()

# Step 1: Load a render preset (optional)
project.LoadRenderPreset("YouTube 1080p")

# Step 2: Override specific settings
project.SetRenderSettings({
    "TargetDir": "C:/Renders/Output",
    "CustomName": "MyVideo_Final",
    "FormatWidth": 1920,
    "FormatHeight": 1080,
    "ExportVideo": True,
    "ExportAudio": True,
    "SelectAllFrames": True
})

# Step 3: Set format and codec
project.SetCurrentRenderFormatAndCodec("mp4", "H264")

# Step 4: Add to render queue
job_id = project.AddRenderJob()

# Step 5: Start rendering
if job_id:
    project.StartRendering(job_id)

# Step 6: Monitor progress
import time
while project.IsRenderingInProgress():
    status = project.GetRenderJobStatus(job_id)
    print(f"Progress: {status.get('CompletionPercentage', 0)}%")
    time.sleep(2)

print("Render complete!")
```

---

## 16. Markers and Metadata <a name="markers-and-metadata"></a>

### Working with Markers

Markers are available on Timeline, TimelineItem, and MediaPoolItem objects. All share the same interface.

```python
# Add a marker at frame 100
timeline.AddMarker(100, "Blue", "Chapter 1", "Introduction section", 1, "ch01")

# Add marker with custom data (for programmatic access)
timeline.AddMarker(500, "Green", "Sponsor", "Sponsor segment", 150, "sponsor_read")

# Get all markers - returns dict keyed by frame number
markers = timeline.GetMarkers()
# {100: {"color": "Blue", "duration": 1, "note": "Introduction section",
#         "name": "Chapter 1", "customData": "ch01"}, ...}

# Delete markers
timeline.DeleteMarkersByColor("Blue")  # Delete all blue markers
timeline.DeleteMarkerAtFrame(100)       # Delete marker at specific frame
timeline.DeleteMarkerByCustomData("ch01")  # Delete by custom data
```

### Working with Metadata

```python
clip = media_pool.GetRootFolder().GetClipList()[0]

# Get all metadata
all_meta = clip.GetMetadata("")
# Returns dict with keys like: "Description", "Comments", "Keywords",
#   "People", "Scene", "Shot", "Take", "Good Take", ...

# Set specific metadata
clip.SetMetadata("Description", "B-roll construction site footage")
clip.SetMetadata("Keywords", "construction, exterior, drone")

# Set multiple at once
clip.SetMetadata({
    "Scene": "001",
    "Shot": "A",
    "Good Take": "true"
})

# Get clip properties (different from metadata)
props = clip.GetClipProperty("")
# Returns: "File Path", "Duration", "FPS", "Resolution", "Codec", etc.
```

---

## 17. Audio Track Management <a name="audio-track-management"></a>

```python
timeline = project.GetCurrentTimeline()

# Get audio track count
audio_track_count = timeline.GetTrackCount("audio")

# Get items on specific audio track
for track_idx in range(1, audio_track_count + 1):
    audio_items = timeline.GetItemListInTrack("audio", track_idx)
    track_name = timeline.GetTrackName("audio", track_idx)
    print(f"Track {track_idx} ({track_name}): {len(audio_items)} clips")

# Rename audio tracks
timeline.SetTrackName("audio", 1, "Dialogue")
timeline.SetTrackName("audio", 2, "Music")
timeline.SetTrackName("audio", 3, "SFX")

# Add a new audio track
timeline.AddTrack("audio")

# Lock/unlock tracks
timeline.SetTrackLock("audio", 3, True)  # Lock SFX track
is_locked = timeline.GetIsTrackLocked("audio", 3)

# Enable/disable tracks
timeline.SetTrackEnable("audio", 2, False)  # Mute music track

# Insert audio at playhead
project.InsertAudioToCurrentTrackAtPlayhead(
    "C:/Audio/background_music.mp3",
    startOffset=0,
    duration=3000  # frames
)
```

---

## 18. Project Settings Reference <a name="project-settings-reference"></a>

### Discovering All Settings

```python
# Get ALL project settings as a dictionary
all_settings = project.GetSetting("")
for key, value in sorted(all_settings.items()):
    print(f"{key}: {value}")

# Same for timeline
all_timeline_settings = timeline.GetSetting("")
```

### Common Project Setting Keys

| Key | Example Value | Description |
|---|---|---|
| `timelineResolutionWidth` | "1920" | Project resolution width |
| `timelineResolutionHeight` | "1080" | Project resolution height |
| `timelineFrameRate` | "24.000" | Frame rate |
| `timelinePlaybackFrameRate` | "24" | Playback frame rate |
| `videoCaptureNumChannels` | "2" | Video channels |
| `audioCaptureNumChannels` | "2" | Audio channels |
| `colorScienceMode` | "dapiColorManagedv2" | Color science mode |
| `colorSpaceInput` | "Rec.709 (Scene)" | Input color space |
| `colorSpaceTimeline` | "Rec.709 (Scene)" | Timeline color space |
| `colorSpaceOutput` | "Rec.709 Gamma 2.4" | Output color space |
| `superScale` | "0" | Super scale setting |
| `useCATransform` | "0" | Chromatic adaptation |

### Setting Project Resolution and Frame Rate

```python
# Set to 4K 30fps
project.SetSetting("timelineResolutionWidth", "3840")
project.SetSetting("timelineResolutionHeight", "2160")
project.SetSetting("timelineFrameRate", "30.000")

# Set to 1080p 24fps (cinematic)
project.SetSetting("timelineResolutionWidth", "1920")
project.SetSetting("timelineResolutionHeight", "1080")
project.SetSetting("timelineFrameRate", "24.000")
```

---

## 19. YouTube Production Automation Example <a name="youtube-production-automation-example"></a>

A complete real-world script for automating a YouTube video production pipeline:

```python
"""
YouTube Video Production Automation for DaVinci Resolve 19
Automates: project setup, media import, timeline creation, render
"""
import DaVinciResolveScript as dvr_script
import os
import time

# ---- Configuration ----
VIDEO_TITLE = "How to Build a Website"
FOOTAGE_DIR = "D:/Footage/ep42"
MUSIC_DIR = "D:/Audio/background"
LUT_PATH = "C:/LUTs/YouTube_Look.cube"
OUTPUT_DIR = "D:/Renders/YouTube"
RESOLUTION = ("1920", "1080")
FRAME_RATE = "24.000"

# ---- Connect to Resolve ----
resolve = dvr_script.scriptapp("Resolve")
pm = resolve.GetProjectManager()
project = pm.CreateProject(VIDEO_TITLE)

if not project:
    project = pm.GetCurrentProject()

# ---- Configure Project Settings ----
project.SetSetting("timelineResolutionWidth", RESOLUTION[0])
project.SetSetting("timelineResolutionHeight", RESOLUTION[1])
project.SetSetting("timelineFrameRate", FRAME_RATE)

media_pool = project.GetMediaPool()
root = media_pool.GetRootFolder()

# ---- Create Folder Structure ----
footage_folder = media_pool.AddSubFolder(root, "Footage")
music_folder = media_pool.AddSubFolder(root, "Music")
graphics_folder = media_pool.AddSubFolder(root, "Graphics")

# ---- Import Media ----
media_pool.SetCurrentFolder(footage_folder)
video_files = [
    os.path.join(FOOTAGE_DIR, f)
    for f in os.listdir(FOOTAGE_DIR)
    if f.endswith(('.mp4', '.mov', '.mxf'))
]
imported_clips = media_pool.ImportMedia(video_files)

media_pool.SetCurrentFolder(music_folder)
music_files = [
    os.path.join(MUSIC_DIR, f)
    for f in os.listdir(MUSIC_DIR)
    if f.endswith(('.mp3', '.wav', '.aac'))
]
media_pool.ImportMedia(music_files)

# ---- Create Timeline ----
media_pool.SetCurrentFolder(footage_folder)
timeline = media_pool.CreateTimelineFromClips(VIDEO_TITLE, imported_clips)
project.SetCurrentTimeline(timeline)

# ---- Apply LUT to All Clips ----
video_items = timeline.GetItemListInTrack("video", 1)
for item in video_items:
    item.SetLUT(1, LUT_PATH)

# ---- Add Chapter Markers ----
timeline.AddMarker(0, "Blue", "Intro", "Opening hook", 1, "")
timeline.AddMarker(720, "Green", "Main Content", "Tutorial begins", 1, "")

# ---- Name Audio Tracks ----
if timeline.GetTrackCount("audio") >= 2:
    timeline.SetTrackName("audio", 1, "Voiceover")
    timeline.SetTrackName("audio", 2, "Background Music")

# ---- Set Up Render ----
project.LoadRenderPreset("H.264 Master")
project.SetRenderSettings({
    "TargetDir": OUTPUT_DIR,
    "CustomName": VIDEO_TITLE.replace(" ", "_"),
    "FormatWidth": int(RESOLUTION[0]),
    "FormatHeight": int(RESOLUTION[1]),
    "ExportVideo": True,
    "ExportAudio": True,
    "SelectAllFrames": True
})
project.SetCurrentRenderFormatAndCodec("mp4", "H264")

# ---- Queue and Render ----
job_id = project.AddRenderJob()
if job_id:
    project.StartRendering(job_id)
    while project.IsRenderingInProgress():
        status = project.GetRenderJobStatus(job_id)
        pct = status.get("CompletionPercentage", 0)
        print(f"Rendering: {pct}%")
        time.sleep(5)
    print("RENDER COMPLETE")
    print(f"Output: {OUTPUT_DIR}/{VIDEO_TITLE.replace(' ', '_')}.mp4")
else:
    print("ERROR: Failed to add render job")
```

---

## 20. Sources and Community Resources <a name="sources"></a>

### Official Documentation

- **In-app:** Help > Documentation > Developer > Scripting > `README.txt`
- **Blackmagic Design Forum:** https://forum.blackmagicdesign.com/

### Community API Documentation (Recommended)

| Resource | URL |
|---|---|
| Deric's API Docs (searchable) | https://deric.github.io/DaVinciResolve-API-Docs/ |
| X-Raym Cloud Docs | https://extremraym.com/cloud/resolve-scripting-doc/ |
| ResolveDevDoc (ReadTheDocs) | https://resolvedevdoc.readthedocs.io/en/latest/ |
| GitHub: Official README mirror | https://github.com/deric/DaVinciResolve-API-Docs |

### Python Type Stubs and Dev Tools

| Tool | URL |
|---|---|
| fusionscript-stubs (IDE autocomplete) | https://github.com/czukowski/fusionscript-stubs |
| DaVinci Resolve Toolkit (VS Code) | Search "DaVinci Resolve" in VS Code Extensions |

### Tutorial Creators

- **AlexTheCreative** (alexthecreative.com) - scripting tutorials and cheat sheets
- **dev.to DaVinci Resolve** - community automation articles

### Key [[Limitations|Limitations]]

1. **Studio only** - The free version of DaVinci Resolve does NOT expose the scripting API
2. **No custom metadata keys** - You cannot create user-defined metadata fields; workaround is storing JSON in existing fields like "Comments" or "VFX Notes"
3. **No direct UI track selection** - The API cannot programmatically "click" or "select" tracks in the GUI
4. **Fusion API is separate** - The legacy Fusion Scripting Guide covers node manipulation; the Resolve README covers project/timeline operations
5. **Version sensitivity** - Methods can be added/changed in point releases (e.g., 19.0.2); always check your local README.txt
6. **Frame rate strings** - The API returns frame rates as strings; fractional rates like 29.97 may need parsing

---

*Report generated for Keystone Sovereign system. Research conducted May 22, 2026.*
*This document covers DaVinci Resolve 19.x Python scripting API based on official documentation references and community-maintained sources.*


---
📁 **See also:** [[Research_Archives/05_Video_Production/INDEX|← Directory Index]]

**Related:** [[20260613_VIDEO_PROD_davinci_resolve_studio_scripting_api_complete_reference_for_]] · [[8_1_DaVinci_Resolve_Workflow]] · [[davinci_resolve_api_mastery]]
