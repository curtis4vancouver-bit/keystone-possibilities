# Deep Research: DaVinci Resolve Studio scripting API complete reference for 2026: What are ALL the available Python/Lua scripting functions for automating DaVinci Resolve 19/20? Cover the Resolve, ProjectManager, Project, MediaPool, MediaPoolItem, Timeline, TimelineItem, and Gallery objects. Include specific code examples for: creating timelines from media, setting track properties, adding markers, managing render jobs, importing/exporting projects, and automating the Color page. Focus on headless automation without GUI interaction.
**Domain:** Video Prod
**Researched:** 2026-06-13 01:38
**Source:** Google Deep Research via Chrome Automation

---

DaVinci Resolve Studio 2026 Scripting API: Comprehensive Headless Automation Framework for Enterprise Video Pipelines

The automation of post-production pipelines has evolved from simple batch-rendering scripts into the orchestration of fully autonomous media generation ecosystems. For an artificial intelligence agent system—such as Keystone Sovereign—tasked with managing a diverse portfolio of construction business timelapses, multi-channel YouTube syndication, and expansive health content networks, the need for programmatic, zero-touch post-production is absolute. DaVinci Resolve Studio, spanning versions 19, 20, and the 21.0 beta, provides a formidable Python 3 and Lua scripting Application Programming Interface (API) capable of executing end-to-end media ingestion, temporal assembly, precise node-based color grading, and rendering without any graphical user interface (GUI) interaction.   

This technical dossier provides an exhaustive reference and architectural guide to the DaVinci Resolve Scripting API as of May 2026. The analysis maps the complete object hierarchy—encompassing the Resolve root, ProjectManager, Project, MediaPool, Timeline, and Color Page structures—required to construct a resilient, headless automation framework.

1. The Headless Execution Environment and Connection Architecture

Deploying DaVinci Resolve within a continuous integration/continuous deployment (CI/CD) or an autonomous agent server environment requires strict management of environment variables, subprocess lifecycle execution, and inter-process communication (IPC) timeouts. DaVinci Resolve Studio (the paid tier) is explicitly required for this architecture; the free tier restricts external API execution and limits critical rendering features.   

1.1 Programmatic Environment Configuration

Before the DaVinciResolveScript module can be successfully imported by a Python interpreter operating outside of the Resolve console, the Python environment must be dynamically pointed to the API bridge and dynamic linking libraries. While these dependencies can be configured statically at the operating system level, programmatic injection ensures that the autonomous agent can be containerized and deployed across diverse computing nodes (Linux, Windows, or macOS) with zero manual setup.   

The autonomous agent process utilizes the DaVinciResolveScript module to connect to the Resolve Daemon via fusionscript libraries, utilizing LAN IP discovery on macOS if the localhost binding fails. The schematic flow moves from the external agent process, through environment variables to the DaVinciResolveScript module, across the IPC bridge (fusionscript.so or fusionscript.dll), and finally into the DaVinci Resolve subprocess running with the -nogui flag.   

1.2 Subprocess Instantiation and Headless Invocation

For zero-touch environments, DaVinci Resolve must be launched as a background daemon. Passing the -nogui command-line argument disables the graphical user interface entirely, freeing up system resources while maintaining full functionality of the underlying Python API. Launching Resolve as a subprocess of the main AI agent ensures that the master controller maintains process lifecycle dominance, allowing it to forcefully terminate the daemon in the event of a catastrophic memory leak.   

Python
import os
import sys
import subprocess
import threading
import time

def configure_resolve_environment():
    """Injects Resolve API paths into the Python environment dynamically."""
    if sys.platform == "darwin":
        api_path = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/"
        lib_path = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    elif sys.platform == "win32":
        api_path = os.path.join(os.environ.get("PROGRAMDATA", ""), 
                                "Blackmagic Design", "DaVinci Resolve", "Support", "Developer", "Scripting")
        lib_path = os.path.join(os.environ.get("PROGRAMFILES", ""), 
                                "Blackmagic Design", "DaVinci Resolve", "fusionscript.dll")
    else:
        api_path = "/opt/resolve/Developer/Scripting/"
        lib_path = "/opt/resolve/libs/Fusion/fusionscript.so"

    os.environ.setdefault("RESOLVE_SCRIPT_API", api_path)
    os.environ.setdefault("RESOLVE_SCRIPT_LIB", lib_path)
    
    modules_path = os.path.join(api_path, "Modules")
    if modules_path not in sys.path:
        sys.path.insert(0, modules_path)

def launch_headless_resolve():
    """Spawns DaVinci Resolve in headless mode as a daemon subprocess."""
    resolve_executable = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
    if sys.platform == "darwin":
        resolve_executable = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/MacOS/Resolve"
    elif sys.platform.startswith("linux"):
        resolve_executable = "/opt/resolve/bin/resolve"
        
    args = [resolve_executable, "-nogui"]
    return subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

1.3 IPC Timeout Wrapping and Connection Bootstrapping

Because Resolve's external scripting API relies heavily on inter-process communication via fusionscript.dll or fusionscript.so, remote procedural calls can hang indefinitely if the internal C++ application thread locks or encounters an unhandled exception. For autonomous [[AGENTS|agents]] managing mission-critical content delivery (such as daily YouTube uploads), all connections must be wrapped in strict timeout threads to ensure the system can recover from an application freeze.   

Furthermore, macOS environments possess a known behavior where Resolve occasionally binds the API listener to the active Local Area Network (LAN) IP instead of the localhost loopback address (127.0.0.1). If the initial scriptapp("Resolve") call returns None, a sophisticated pinghost fallback mechanism must interrogate the network interfaces.   

Python
configure_resolve_environment()
import DaVinciResolveScript as dvr_script

def call_with_timeout(func, timeout=10.0):
    """Executes a Resolve API call with a strict timeout to prevent thread locks."""
    result = [None]
    error = [None]

    def wrapper():
        try:
            result = func()
        except Exception as e:
            error = e

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    thread.join(timeout=timeout)
    
    if thread.is_alive():
        raise TimeoutError("DaVinci Resolve IPC call timed out.")
    if error:
        raise error
    return result

def connect_to_resolve():
    """Connects to the Resolve application object, handling LAN IP bindings."""
    resolve = call_with_timeout(lambda: dvr_script.scriptapp("Resolve"), timeout=5.0)
    if resolve:
        return resolve

    if sys.platform == "darwin":
        hosts = dvr_script.pinghosts('')
        if hosts:
            for _, info in hosts.items():
                if info.get('IP'):
                    resolve = dvr_script.scriptapp("Resolve", info['IP'])
                    if resolve: return resolve
                    
        import subprocess
        result = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('inet ') and '127.0.0.1' not in line and '169.254.' not in line:
                ip = line.split()
                resolve = dvr_script.scriptapp("Resolve", ip)
                if resolve: return resolve
    return None

resolve_app = connect_to_resolve()

2. Core Object Hierarchy: Resolve, MediaStorage, and ProjectManager

The DaVinci Resolve API follows a strictly hierarchical document object model (DOM). Operations cascade from the global application object down into specific, instantiated data representations.   

2.1 The Global Resolve Object

The Resolve object serves as the root application interface, instantiated directly from the scripting bridge. It operates as a factory for acquiring the major subsystem managers.   

API Method	Return Type	Architectural Function
Fusion()	Fusion	

Returns the base Fusion object. This serves as the starting point for invoking internal Fusion scripts, managing node-based compositing, and injecting Text+ macros into timelines.


GetMediaStorage()	MediaStorage	

Returns the media storage interface, required for filesystem querying and initial media ingestion from disk.


GetProjectManager()	ProjectManager	

Returns the global project manager, enabling database connection routing and project lifecycle control.


OpenPage(pageName)	Bool	

Switches internal user interface pages (e.g., "media", "edit", "color", "deliver"). While running headlessly, invoking this is absolutely critical for forcing the application's internal [[STATE|state]] machine to update, particularly prior to rendering.


GetCurrentPage()	string	

Returns the currently active internal page.

  
2.2 The MediaStorage Object

The MediaStorage object forms the necessary bridge between the operating system's raw filesystem and Resolve's internal database indexing mechanisms. Before media can be manipulated on a timeline, it must pass through this layer.   

API Method	Return Type	Architectural Function
GetMountedVolumeList()	[string...]	

Returns a Python list containing absolute paths for all filesystem volumes currently mounted and visible to Resolve.


GetSubFolderList(folderPath)	[string...]	

Returns absolute paths of all subdirectories within a given target path.


GetFileList(folderPath)	[string...]	

Enumerates media files within a specified path. Crucially, this method evaluates image sequences (e.g., DPX, EXR, or TIFF sets from a construction timelapse) as logically consolidated single entities, rather than thousands of individual frames.


AddItemsToMediaPool(items)	[MediaPoolItem]	

Pushes raw filesystem items directly into the current Media Pool bin.

  

For a system tasked with processing high-resolution construction timelapses, GetFileList() serves as the primary mechanism for detecting new image sequences pushed to a network-attached storage (NAS) array. The autonomous agent can routinely poll the NAS, identify newly consolidated EXR sequences, and seamlessly push them into a project bin.

2.3 The ProjectManager Object

High-volume video production necessitates logical segregation of assets. Project automation allows the system to silo distinct business channels—for instance, keeping Daily Health Vlogs separate from long-term Real Estate Time-lapses—into separate databases and projects.   

API Method	Return Type	Architectural Function
GetCurrentDatabase()	{dict}	

Returns a dictionary containing 'DbType', 'DbName', and 'IpAddress'.


GetDatabaseList()	[{dict}...]	

Enumerates all configured PostgreSQL or disk-based databases.


SetCurrentDatabase(dbInfo)	Bool	

Routes the application to a different database backend and forcefully closes any open projects.


CreateProject(name)	Project	

Initializes a new project, assuming the string name is unique.


LoadProject(name)	Project	

Loads a dormant project from the database into active memory.


GetCurrentProject()	Project	

Retrieves the instantiated Project object.


SaveProject()	Bool	

Commits all transient timeline and color changes to the database.


CloseProject(project)	Bool	

Flushes a project from memory without committing unsaved changes.


DeleteProject(name)	Bool	

Purges a project entirely. The target project must not be currently loaded.


ImportProject(path)	Bool	

Unpacks and ingests a .drp (DaVinci Resolve Project) file from disk.


ExportProject(name, path, stills)	Bool	

Writes a project out to a portable .drp package.


ArchiveProject(name, path,...)	Bool	

Generates a .dra (DaVinci Resolve Archive) folder. This copies all source media, proxies, and render caches into a self-contained unit, essential for cold storage.

  
Architecture Example: Automated Project Templating and Cold Storage

In a highly scalable pipeline, creating projects from scratch is inefficient. An autonomous agent will typically import a meticulously pre-configured template project (containing custom smart bins, pre-built node graphs, and standardized render presets), execute its manipulations, and then export a standalone archive.

Python
def process_and_archive_project(project_manager, template_drp_path, output_dra_path):
    """Imports a standardized template, manipulates it, and executes a cold archive."""
    project_name = "Health_Content_Batch_042"
    
    success = project_manager.ImportProject(template_drp_path, project_name)
    if not success:
        raise RuntimeError(f"Failed to import DRP template from {template_drp_path}.")
        
    project = project_manager.LoadProject(project_name)
    
    #... Advanced timeline assembly and grading logic executes here...
    
    project_manager.SaveProject()
    project_manager.CloseProject(project)
    
    # Generate a DaVinci Resolve Archive (DRA) for cold storage
    archive_success = project_manager.ArchiveProject(
        project_name, 
        output_dra_path,
        isArchiveSrcMedia=True,
        isArchiveRenderCache=False,
        isArchiveProxyMedia=False
    )
    
    if archive_success:
        # Purge the database to maintain performance and prevent bloating
        project_manager.DeleteProject(project_name) 

3. The Project Object: Global Settings and Render Orchestration

The Project object serves as the central nervous system for a given batch of media. It governs overarching configurations, High Dynamic Range (HDR) workflows, timeline frame rates, canvas resolutions, and acts as the interface for the rendering queue.   

3.1 Project Lifecycle Methods
API Method	Return Type	Architectural Function
GetName()	string	

Retrieves the literal string name of the project.


SetName(name)	Bool	

Renames the project within the database.


GetMediaPool()	MediaPool	

Returns the MediaPool object associated with this project.


GetTimelineCount()	int	

Returns the absolute number of timelines generated within the project.


GetTimelineByIndex(idx)	Timeline	

Returns a specific timeline based on a 1-based index.


GetCurrentTimeline()	Timeline	

Retrieves the sequence currently loaded into the viewer.


SetCurrentTimeline(tl)	Bool	

Forces the internal viewer to mount the specified timeline.


GetSetting(settingName)	string	

Retrieves the value of a specific project setting. Passing an empty string returns a massive dictionary of all configured key-value pairs.


SetSetting(settingName, val)	Bool	

Injects a string value into a global project parameter.

  
3.2 Programmatic HDR and Color Management Configuration

Managing color science programmatically is notoriously rigid. Setting parameters out of sequence will result in the API silently failing. For a modern YouTube pipeline pushing high-fidelity footage, DaVinci Color Management must be explicitly engaged before granular input and output color spaces can be defined.   

When configuring an environment for HDR (High Dynamic Range), specific string literals must be passed to the SetSetting method. Common settings include timelineFrameRate (e.g., "24", "29.97 DF"), timelineResolutionWidth (e.g., "3840"), and colorScienceMode ("davinciYRGB", "davinciYRGBColorManagedv2", or "ACEScct").   

Python
import time

def configure_project_hdr(project):
    """Strictly sequences the configuration of Rec.2020 ST2084 HDR delivery."""
    # Step 1: Engage DaVinci Color Management (This MUST precede spatial definitions)
    project.SetSetting("colorScienceMode", "davinciYRGBColorManagedv2")
    project.SetSetting("isAutoColorManage", "0")
    project.SetSetting("separateColorSpaceAndGamma", "1")
    
    # Step 1.5: IPC Thread Buffer
    time.sleep(0.25) 
    
    # Step 2: Define Spatial and Chromatic Parameters
    hdr_configuration = {
        "timelineFrameRate": "24",
        "timelineResolutionWidth": "3840",
        "timelineResolutionHeight": "2160",
        "superScale": "0", # Auto scaling
        "colorSpaceInput": "Rec.2020",
        "colorSpaceInputGamma": "ST2084",
        "colorSpaceTimeline": "Rec.2020",
        "colorSpaceTimelineGamma": "Rec.2100 ST2084",
        "colorSpaceOutput": "Rec.2020",
        "colorSpaceOutputGamma": "Rec.2100 ST2084",
        "timelineWorkingLuminanceMode": "HDR 4000",
        "hdrMasteringLuminanceMax": "4000",
        "hdrMasteringOn": "1"
    }
    
    for key, val in hdr_configuration.items():
        success = project.SetSetting(key, val)
        if not success:
            print(f"Warning: Failed to set parameter {key} to {val}")

3.3 Headless Render Queue Orchestration

Output generation in a headless environment requires programmatic job addition, formatting selection, and continuous asynchronous polling to determine completion status.   

API Method	Return Type	Architectural Function
GetRenderFormats()	{dict}	

Returns a mapping of format descriptions to actual file extensions (e.g., {"QuickTime": "mov"}).


GetRenderCodecs(fmt)	{dict}	

Returns a mapping of codecs explicitly available for the given format.


SetCurrentRenderFormatAndCodec(f, c)	Bool	

Assigns the output container and specific codec (e.g., "mov", "ProRes422HQ").


SetRenderSettings({dict})	Bool	

Defines robust export configurations, heavily relying on keys like TargetDir, CustomName, SelectAllFrames, ExportVideo, and ExportAudio.


AddRenderJob()	string	

Pushes the active timeline to the render queue and returns a unique Job ID string.


StartRendering([jobIds])	Bool	

Commences rendering operations for the specified array of Job IDs.


IsRenderingInProgress()	Bool	

Acts as a global boolean polling flag.


GetRenderJobStatus(jobId)	{dict}	

Returns a highly detailed status dictionary, including the critical CompletionPercentage and JobStatus flags.


DeleteRenderJobByIndex(idx)	Bool	

Cleans up the queue post-execution.

  
Architecture Example: Dispatching Render Jobs

A notorious edge case in the Resolve Scripting API occurs during headless rendering. The API frequently fails to commit render settings or add a job to the queue if the internal graphical [[STATE|state]] machine does not believe it is on the "Deliver" page. Even when running with -nogui, a forced page switch via resolve.OpenPage("deliver") followed by a thread sleep is a mandatory architectural safeguard.   

Python
def dispatch_and_monitor_render(resolve, project, timeline, output_path):
    """Adds a timeline to the render queue and blocks the thread until completion."""
    project.SetCurrentTimeline(timeline)
    
    # [[STATE|State]] Machine Synchronization (Mandatory)
    resolve.OpenPage("deliver")
    time.sleep(1.0)
    
    project.SetCurrentRenderFormatAndCodec("mov", "ProRes422HQ")
    
    # Resolve 19.1 introduced options to replace files dynamically
    render_settings = {
        "SelectAllFrames": True,
        "TargetDir": os.path.dirname(output_path),
        "CustomName": os.path.basename(output_path).split('.'),
        "ExportVideo": True,
        "ExportAudio": True,
    }
    project.SetRenderSettings(render_settings)
    
    job_id = project.AddRenderJob()
    if not job_id:
        raise RuntimeError("Failed to inject render job into the queue.")
        
    project.StartRendering([job_id])
    
    # Asynchronous polling loop
    while project.IsRenderingInProgress():
        status_dict = project.GetRenderJobStatus(job_id)
        percentage = status_dict.get('CompletionPercentage', 0)
        # In an autonomous system, broadcast this metric to a message queue (e.g., RabbitMQ)
        print(f"Render Task {job_id} Progression: {percentage}%")
        time.sleep(2.5)
        
    final_status = project.GetRenderJobStatus(job_id)
    if final_status!= "Complete":
        raise Exception(f"Critical Rendering Error. Final [[STATE|State]]: {final_status}")
        
    # Flush the queue to prevent database bloating
    project.DeleteRenderJobByIndex(1)

4. MediaPool and MediaPoolItem Asset Management

The MediaPool orchestrates the logical bins and source clips within a project. In automated video production, validating media integrity and injecting search-friendly metadata are foundational data engineering steps before any algorithmic assembly occurs.

4.1 MediaPool Object Reference
API Method	Return Type	Architectural Function
GetRootFolder()	Folder	

Returns the master root bin of the project.


AddSubFolder(folder, name)	Folder	

Generates a new bin nested beneath a specified parent folder.


GetCurrentFolder()	Folder	

Retrieves the active bin.


SetCurrentFolder(folder)	Bool	

Redirects the active context to a specific bin.


ImportMedia([filePaths])	[MediaPoolItem]	

Ingests an array of absolute file paths directly into the current folder.


CreateEmptyTimeline(name)	Timeline	

Instantiates a completely blank timeline object.


CreateTimelineFromClips(n, [clips])	Timeline	

Rapidly generates a timeline pre-populated with an array of source media.


AppendToTimeline([{clipInfo}])	``	

A deeply powerful function that appends items by passing dictionaries containing exact frame dictates, trackIndex, and mediaType.


ImportTimelineFromFile(path)	Timeline	

Parses interchange formats (XML, AAF, OpenTimelineIO) to reconstruct a sequence engineered by third-party systems.


DeleteClips([clips])	Bool	

Destroys specified clips from the media pool database.

  
4.2 MediaPoolItem Object Reference

Every distinct file or image sequence in the bin is instantiated as a MediaPoolItem. These objects carry mutable internal properties (like clip colors and frame rates) and metadata that influence downstream behaviors.   

API Method	Return Type	Architectural Function
GetName()	string	

Retrieves the clip's assigned name.


GetMetadata(type)	string	

Extracts descriptive metadata (e.g., "Shot", "Scene", "Take").


SetMetadata(type, val)	Bool	

Modifies descriptive metadata attributes.


GetClipProperty(prop)	string or {dict}	

Queries physical interpretation properties like "File Path", "Frames", or "Alpha mode".


SetClipProperty(prop, val)	Bool	

Overrides interpretation properties.


GetClipColor() / SetClipColor(col)	string / Bool	

Modifies the UI color swatch of the clip, useful for visually tracking AI processing stages.


LinkProxyMedia(path)	Bool	

Attaches a pre-computed proxy file to the heavy source media item.

  
Architecture Example: Ensuring Media Integrity and Metadata Tagging

When autonomous [[AGENTS|agents]] pull media down from shared cloud buckets, transmission errors can result in truncated or missing files. The agent must programmatically verify that the paths tied to MediaPoolItem objects resolve on the local filesystem before appending them to timelines, thus preventing catastrophic "Media Offline" red frames from making it to a YouTube upload. Furthermore, files generated by Node-based compositing software often contain faulty alpha channels that must be stripped programmatically.   

Python
def validate_media_and_strip_alpha(media_pool_items):
    """
    Checks for offline source media, strips faulty alpha channels, 
    and injects AI-processing [[STATE|state]] metadata.
    """
    from pathlib import Path
    validated_clips =
    
    for clip in media_pool_items:
        properties = clip.GetClipProperty()
        file_path = properties.get("File Path", "")
        
        if file_path and Path(file_path).exists():
            # Force Alpha Mode to "None" to prevent compositing blending errors
            clip.SetClipProperty("Alpha mode", "None")
            
            # Inject metadata to signal to other microservices that this clip is verified
            clip.SetMetadata("Comments", "Keystone_Agent_Validated")
            
            # Change the clip color in the GUI for human debugging
            clip.SetClipColor("Green")
            validated_clips.append(clip)
        else:
            print(f"CRITICAL: Media Offline detected for source path {file_path}")
            clip.SetClipColor("Red")
            
    return validated_clips


5. Timeline and TimelineItem Architectural Assembly

The absolute core of automated video construction lies in the algorithmic manipulation of Timeline and TimelineItem objects. The API permits highly complex assemblies utilizing layered tracks, dynamic adjustments, and programmatically inserted Fusion compositions.

5.1 Timeline Object Reference

The Timeline object handles global track arrays, overarching duration metrics, marker indexing, and data interchange output.   

API Method	Return Type	Architectural Function
GetName()	string	

Retrieves the string name of the timeline.


SetName(name)	Bool	

DaVinci Resolve 19.1 implemented robust support for dynamically setting timeline and media pool clip names via API without encountering locking errors.


GetStartFrame() / GetEndFrame()	int	

Returns temporal boundaries measured in frames based on the timeline's fundamental framerate.


GetTrackCount(trackType)	int	

Evaluates the total count for a specific string identifier: "audio", "video", or "subtitle".


AddTrack(trackType, {audioFmt})	Bool	

Instantiates a new horizontal track. The audio format dictionary allows the definition of complex routing (e.g., AddTrack("audio", {"audioType": "5.1"})).


DeleteTrack(trackType, index)	Bool	

Purges an entire track and all contained items based on a 1-based index.


GetTrackName(type, idx)	string	

Queries the user-facing name of the track.


SetTrackName(type, idx, name)	Bool	

Dynamically renames the track, essential for visual organization.


GetIsTrackEnabled(type, idx)	Bool	

Queries visibility/playback [[STATE|state]].


SetTrackEnable(type, idx, Bool)	Bool	

Mutes audio or blinds video execution on the designated track.


SetTrackLock(type, idx, Bool)	Bool	

Activating the lock prevents subsequent API algorithms from accidentally rippling or overwriting data on master tracks.


GetItemListInTrack(type, idx)	``	

Returns an ordered array of instantiated items populating the track.


DuplicateTimeline(name)	Timeline	

Generates a clone of the sequence. Highly effective for A/B testing rendering versions.


CreateCompoundClip([items])	TimelineItem	

Collapses multiple items into a single manageable entity.


Export(path, type, subtype)	Bool	

Exfiltrates the sequence data into interchange formats.

  
Evolution of Export Types (v18.1 through v21)

Generating non-rendered interchange formats allows AI [[AGENTS|agents]] to hand off temporal data to external audio mixing or visual effects systems. As of DaVinci Resolve 18.1, legacy FCPXML versions (1.3 through 1.7) were entirely deprecated. Modern [[AGENTS|agents]] must strictly utilize contemporary constants:   

resolve.EXPORT_AAF (Advanced Authoring Format)

resolve.EXPORT_FCPXML_1_10 (or versions 1_8, 1_9)

resolve.EXPORT_OTIO (OpenTimelineIO, greatly expanded in Resolve 19)    

resolve.EXPORT_DRT (DaVinci Resolve Timeline archive)

resolve.EXPORT_TEXT_CSV (For data analysis of edit lengths)    

5.2 TimelineItem Object Reference

While a MediaPoolItem points to a file on a disk, a TimelineItem represents a highly specific, temporal instance of that file resting on a timeline track. Multiple TimelineItem objects can reference a single MediaPoolItem.

API Method	Return Type	Architectural Function
GetMediaPoolItem()	MediaPoolItem	

Resolves the pointer backward to the source media.


GetDuration()	int	

Evaluates the frame length of the clip instance.


GetStart(), GetEnd()	int	

Frame boundary markers relative to the global timeline.


GetLeftOffset(), GetRightOffset()	int	

Evaluates the temporal offset trimmed from the source media head and tail.


SetProperty(key, val)	Bool	

Modifies instance-level Inspector parameters (e.g., Pan, Tilt, Zoom, Opacity).


GetNodeGraph()	Graph	

Major Addition in v21.0 Beta: Allows the scripting agent to pull the Color Page node tree directly from the timeline context, avoiding clumsy navigation paradigms.


GetColorGroup()	ColorGroup	

Retrieves the associated color pipeline group object for the specific instance.

  
5.3 Architecture Example: Programmatic Timeline Assembly

The following subroutine demonstrates how the Keystone Sovereign agent constructs a layered YouTube video format. It initializes isolated video and audio tracks, assigns rigid nomenclature, locks master voiceover tracks, and executes precision placement of media using dictionary payloads.   

Python
def construct_multitrack_timeline(media_pool, video_broll, voiceover_clip, music_clip):
    """Algorithmic assembly of a multitrack sequence."""
    # Instantiation generates V1 and A1 by default
    timeline = media_pool.CreateEmptyTimeline("AI_Auto_Generated_Sovereign_Vlog")
    
    # 1. Establish Track Architecture (1-based integer indexing)
    timeline.SetTrackName("video", 1, "A-Roll_Primary")
    timeline.SetTrackName("audio", 1, "VoiceOver_Master")
    
    # 2. Add supplementary tracks for B-Roll and music
    timeline.AddTrack("video") # Generates V2
    timeline.AddTrack("audio", {"audioType": "stereo"}) # Generates A2
    timeline.SetTrackName("video", 2, "B-Roll_Cutaways")
    timeline.SetTrackName("audio", 2, "Background_Music")
    
    # 3. Precision Append execution
    # Injecting video assets into V1
    for clip in video_broll:
        media_pool.AppendToTimeline()
        
    # Injecting audio assets
    media_pool.AppendToTimeline()
    
    media_pool.AppendToTimeline()
    
    # 4. [[STATE|State]] Protection
    # Lock the background music track to prevent rippling during downstream API manipulations
    timeline.SetTrackLock("audio", 2, True)
    
    return timeline

6. Temporal Metadata and Marker Automation

For an autonomous agent spanning independent microservices, standard relational databases often fall out of sync with highly malleable non-linear editing (NLE) timelines. To solve this, markers serve as the primary embedded database storage mechanism. DaVinci Resolve exposes hidden customData strings within markers specifically designed for API developer integration, allowing systems to encode JSON states directly into the timeline track.   

6.1 Marker Management Methods

These functions are callable on both Timeline (for global markers) and TimelineItem (for clip-bound markers) objects.

API Method	Return Type	Architectural Function
AddMarker(frame, col, name, note, dur, customData)	Bool	

Injects a temporal marker. The customData string remains entirely hidden from the GUI.


GetMarkers()	{dict}	

Returns a massive dictionary of all markers bound to the entity, keyed by frame number.


GetMarkerByCustomData(data)	{dict}	

Locates markers via strict, exact string matching of the hidden payload.


UpdateMarkerCustomData(frame, data)	Bool	

Modifies the hidden payloads of existing markers.


GetMarkerCustomData(frame)	string	

Retrieves the payload string based on temporal location.


DeleteMarkersByColor(col)	Bool	

Purges distinct sets of markers globally.

  
6.2 Architecture Example: Using CustomData for JSON [[STATE|State]] Management

By converting complex dictionaries into stringified JSON and injecting them into the customData parameter, an agent can pass multi-layered rendering instructions—such as instructions for generating animated lower-third titles or localized audio translations—directly inside the timeline. A downstream process can later extract this payload and execute the work.   

Python
import json

def encode_actionable_marker(timeline_item, start_frame, duration, action_dict):
    """
    Injects a duration marker containing JSON-encoded execution logic 
    for downstream microservice processing.
    """
    payload_string = json.dumps(action_dict)
    
    success = timeline_item.AddMarker(
        frameId=start_frame,
        color="Blue",
        name="Agent_Action_Node",
        note="Requires External Subprocess Execution",
        duration=duration,
        customData=payload_string
    )
    return success

def execute_embedded_marker_actions(timeline_item):
    """Retrieves and executes hidden payload instructions."""
    all_markers = timeline_item.GetMarkers()
    
    for frame, marker_info in all_markers.items():
        if marker_info['color'] == 'Blue':
            payload_string = timeline_item.GetMarkerCustomData(frame)
            if payload_string:
                action_logic = json.loads(payload_string)
                
                # Logic Routing Example:
                if action_logic.get('action_type') == 'generate_fusion_lower_third':
                    primary_text = action_logic.get('text_string')
                    # Invoke Fusion API to dynamically build the title overlay
                    print(f"Building lower third at frame {frame} with text: {primary_text}")

7. Programmatic Color Page and Gallery Operations

Historically, the Color Page was the most opaque subsystem to the scripting API, relying largely on GUI manipulation. However, subsequent major updates—accelerating heavily in DaVinci Resolve 19 and culminating in the 21.0 beta—have finally exposed deep Node Graph manipulation capabilities and comprehensive Gallery automation to external scripting environments.   

7.1 Gallery, Albums, and Still Capture

The Gallery represents the database of stored color grades (Stills and PowerGrades). [[AGENTS|Agents]] can automate the application of consistent "lookbooks" across massive channels by importing .drx (DaVinci Resolve Exchange) files into the gallery.   

Object Context	API Method	Return Type	Architectural Function
Project	GetGallery()	Gallery	

Extracts the root gallery object.


Gallery	GetGalleryStillAlbums()	``	

Returns a list of structural albums.


Gallery	GetCurrentStillAlbum()	GalleryStillAlbum	

Returns the active target album.


GalleryStillAlbum	ImportStills([paths])	Bool	

Programmatically ingests .drx grades or reference image files from disk.


GalleryStillAlbum	GetStills()	``	

Retrieves an array of stored object references.


GalleryStillAlbum	ExportStills([stills], dir, prefix, fmt)	Bool	

Exfiltrates grades. Supported formats: dpx, tif, jpg, drx.


Timeline	GrabStill() / GrabAllStills(src)	GalleryStill	

Captures the active viewer or forces the system to grab a still from every clip in the timeline (using the first frame or middle frame).

  
7.2 The Graph Object (Node Tree Manipulation)

Retrieving the node graph for a specific clip enables the AI agent to inject Lookup Tables (LUTs), Color Decision Lists (CDLs), or entire composite node structures computationally. Critical Architectural Constraint: Node indexing within SetLUT and GetLUT functions is strictly 1-based, enforcing the rule 1 <= nodeIndex <= GetNumNodes(). This represents a deviation from standard Python 0-based indexing and frequently triggers IndexError faults in poorly constructed scripts.   

API Method	Return Type	Architectural Function
GetNumNodes()	int	

Calculates the total quantity of active nodes in the tree.


SetLUT(nodeIndex, lutPath)	Bool	

Applies a specific LUT to a node. The lutPath can be an absolute OS path or a relative path tracking from the internal master LUT directory.


GetLUT(nodeIndex)	string	

Queries the current LUT path occupying the node.


SetNodeEnabled(idx, bool)	Bool	

Programmatically bypasses or activates a node in the tree.


GetNodeLabel(idx)	string	

Retrieves the text label assigned to the node.


GetToolsInNode(idx)	[string...]	

DaVinci 19 introduced support to enumerate the exact color tools utilized inside a specific node.


ApplyGradeFromDRX(path, mode)	Bool	

Replaces or appends an entire node tree architecture imported from disk. Modes: 0 (No keyframes applied), 1 (Source Timecode aligned execution), 2 (Start Frame aligned execution).

  
7.3 Architecture Example: Automated Primary Grading Pipeline

For sprawling health and construction YouTube channels, an autonomous agent must normalize heavily compressed log footage and apply a creative look completely autonomously. The Resolve 21.0 beta introduced the incredibly potent ability to pull GetNodeGraph() directly from the TimelineItem, dramatically simplifying the API calls required to color a timeline.   

Python
def apply_autonomous_look_pipeline(timeline):
    """
    Iterates through video track 1, applying a base DRX node tree for normalization, 
    and a specific creative LUT to Node 2.
    """
    track_items = timeline.GetItemListInTrack("video", 1)
    if not track_items: return
    
    for item in track_items:
        # Resolve 21.0 API Enhancement: Access the node graph directly
        graph = item.GetNodeGraph()
        
        # 1. Apply a full base node structure from a pre-built DRX
        # Mode 0 implies dropping temporal keyframes during application
        drx_success = graph.ApplyGradeFromDRX("/network/storage/looks/Base_Log_Normalization.drx", 0)
        
        # API Bug Context (v19/v21 Beta): On macOS and Linux systems, the Graph object 
        # occasionally loses its memory reference after a DRX application.
        # Re-fetching the object is a mandatory safety mechanism.
        graph = item.GetNodeGraph() 
        
        # 2. Inject specific creative LUT into Node 2
        # Node indexing is strictly 1-based.
        num_nodes = graph.GetNumNodes()
        if num_nodes >= 2:
            lut_path = "Film Looks/Rec709 Kodak 2383 D60.cube"
            lut_applied = graph.SetLUT(2, lut_path)
            
            if lut_applied:
                # Ensure the node is active and not bypassed
                graph.SetNodeEnabled(2, True)
            
            # Update the UI color to visually flag graded clips for human auditing
            item.SetClipColor("Orange")

8. Emerging Automation Horizons: Fusion Integration and Advanced AI Features

Beyond pure structural assembly, modern iterations of DaVinci Resolve (v19 and v20) have rapidly expanded API coverage to interface directly with Blackmagic's proprietary internal AI tools and the node-based Fusion composition engine.

The Fusion page operates on its own dedicated internal scripting architecture (historically built heavily on Lua), but the Resolve Python API provides crucial entry points to bridge timelines with Fusion graphs. Scripts can leverage functions like InsertFusionTitleIntoTimeline(titleName) or InsertFusionCompositionIntoTimeline() to procedurally drop animated graphics over video tracks. With Resolve 19's enhancements to OpenTimelineIO and MultiText tools , an autonomous agent can ingest a .csv file containing subtitle data, generate a dedicated Text+ track, and utilize the Fusion scripting object (resolve.Fusion()) to dynamically alter the typography, kerning, and color of individual words to match YouTube pacing standards.   

Furthermore, API documentation reveals growing support for triggering complex Neural Engine processes computationally. The ability to invoke Dolby Vision analysis , trigger IntelliSearch indexing, and manipulate clip usage statistics across timelines  signifies that DaVinci Resolve is rapidly transforming from a human-driven desktop application into an enterprise-grade backend rendering engine.   

9. Conclusion

The DaVinci Resolve Studio scripting API provides an exceptionally deep, DOM-based architecture capable of sustaining fully headless, autonomous video production pipelines. For an artificial intelligence system like Keystone Sovereign, manipulating the ProjectManager, MediaPool, Timeline, and Graph objects bypasses the latency, cost, and inconsistency associated with human editorial workflows.

By bootstrapping the environment variables programmatically, launching the -nogui background daemon, wrapping all IPC calls in rigorous thread timeouts, and strictly sequencing HDR color science configurations prior to invoking the Project render queue, a centralized Python agent can operate continuously. The system can autonomously ingest raw 6K construction footage, slice it according to audio waveforms, construct a multilayered timeline with locked voiceover tracks, apply .drx node trees for perfect mathematical color calibration, and output finalized UHD packages—executing entirely untouched by human hands.

---
*Auto-ingested into Keystone Brain Vector DB*


---
📁 **See also:** ← Directory Index

**Related:** [[20260522_davinci_resolve_color_grading_automation_and_lut_application_via_scripting]] · [[20260613_VIDEO_PROD_automating_davinci_resolve_fusion_compositions_via_scripting]] · [[20260522_davinci_resolve_fusion_scripting_for_text_overlays_and_lower_thirds_automati]]

**Related:** [[20260522_davinci_resolve_api_reference]]
