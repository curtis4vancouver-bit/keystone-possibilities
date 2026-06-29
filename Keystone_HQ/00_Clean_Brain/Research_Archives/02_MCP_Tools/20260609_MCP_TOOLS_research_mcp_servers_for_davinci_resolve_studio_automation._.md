# Deep Research: Research MCP servers for DaVinci Resolve Studio automation. Is there an official or community MCP server that wraps the Resolve scripting API? If not, what would it take to build one? How does the Resolve Python/Lua API work for timeline manipulation, color grading, render queue management? Complete API reference.
**Domain:** Mcp Tools
**Researched:** 2026-06-09 23:12
**Source:** Google Deep Research via Chrome Automation

---

Advanced Automation in DaVinci Resolve Studio: Model Context Protocol (MCP) Integration and Exhaustive Scripting API Reference

The post-production landscape is undergoing a structural paradigm shift, transitioning from purely manual graphical user interface (GUI) interactions toward programmatic automation and artificial intelligence (AI) orchestration. At the core of this transition for DaVinci Resolve Studio is the official Scripting API, a robust framework accessible via Python and Lua. Historically, this API was utilized exclusively for localized workflow scripts, such as batch rendering automation, automated media ingest, or synchronization tasks. However, the introduction of the Model Context Protocol (MCP) has fundamentally altered the operational boundaries of DaVinci Resolve. By establishing a standardized client-server [[ARCHITECTURE|architecture]], MCP enables Large Language Models (LLMs) and autonomous AI coding [[AGENTS|agents]] (such as [[CLAUDE|Claude]] Desktop or Cursor) to interface directly and safely with the non-linear editor (NLE), interpreting high-level natural language intents and executing complex sequences of API calls.

This research report provides an exhaustive analysis of the DaVinci Resolve MCP server ecosystem, investigating both official support and community-driven initiatives. Furthermore, it details the architectural requirements for engineering a bespoke MCP server from the ground up. Finally, it provides a complete and exhaustive reference manual for the underlying DaVinci Resolve Python/Lua Scripting API, encompassing project lifecycle management, timeline manipulation, color grading automation, and render queue orchestration.

The Model Context Protocol (MCP) Ecosystem for DaVinci Resolve

The Model Context Protocol standardizes how AI models interface with local data sources and software applications. Within the context of DaVinci Resolve Studio, an MCP server acts as an indispensable translation layer. Blackmagic Design, the developer of DaVinci Resolve, does not currently maintain or distribute an official, first-party MCP server. Consequently, the development and maintenance of these integration layers have been entirely spearheaded by the open-source developer community and enterprise automation firms.

Prominent Community Implementations

The definitive and most feature-complete implementation currently available is the samuelgursky/davinci-resolve-mcp repository. This implementation provides 100% coverage of the official DaVinci Resolve Scripting API, effectively mapping 336 out of 336 documented API methods for LLM consumption. The project supports both macOS and Windows, utilizes a WebSocket-based API for real-time communication where applicable, and ships with a local browser control panel for inspecting the NLE's [[STATE|state]].   

Other forks and variants exist within the community to address specific deployment requirements. The Tooflex/davinci-resolve-mcp repository offers a streamlined alternative that exposes core functionalities like timeline manipulation, media ingest, and Fusion composition access. Similarly, apvlv/davinci-resolve-mcp emphasizes project management and advanced scripting execution via its execute_python and execute_lua tools. For enterprise environments, specialized distributions such as Positronikal/davinci-mcp-professional package the server as a pre-configured Claude Desktop Extension, enabling immediate, zero-configuration deployment on macOS and Windows. Finally, DigitalWorkflowCompany/resolve-mcp targets DaVinci Resolve version 20 compatibility, exposing 76 compound tools and 20 resources specifically optimized for automated dailies creation and composite workflows. Ultimately, all these solutions operate by wrapping the identical underlying Blackmagic Design Python Scripting API.   

Architectural Philosophy: Safety and Execution Modes

The leading MCP servers share common architectural philosophies optimized for AI safety, token efficiency, and boundary isolation. The primary server implementation operates as a local stdio process initiated directly by the MCP client. This design deliberately avoids exposing local network listeners or WebSockets for its primary control loop, ensuring that the AI assistant only manipulates the DaVinci Resolve instance running on the authorized host machine.   

A critical safety feature embedded within these MCP servers is the strict immutability of source media. The server treats camera originals and source assets as completely read-only. When executing [[davinci-resolve-mcp/.claude/skills/media-analysis|media analysis]]—such as transcribing audio or running visual frame analysis—the server strictly reads the source files and writes analytical metadata or generated reports exclusively to isolated sidecar directories, scratch disks, or project-specific analysis folders. The server enforces rigid operational rules prohibiting the automatic transcoding, proxy generation, or destructive modification of original media unless an explicitly guarded user prompt forces a derivative workflow.   

Exposing hundreds of discrete API methods directly to a Large Language Model introduces severe context window degradation. If an AI agent must parse and formulate the exact sequence of several individual API calls merely to import a clip and append it to a timeline, the token consumption for tool definitions and sequential reasoning loops becomes computationally expensive and highly prone to hallucination. To mitigate this, robust MCP servers provide specialized execution modes.   

The standard operational paradigm is the Compound Mode. This mode reduces the 336 raw API methods into a streamlined surface of approximately 32 context-efficient tools comprising over 136 guarded workflow actions. These compound tools group related Resolve operations behind comprehensive action parameters. For example, a single manage_timeline tool might encapsulate the underlying API methods CreateEmptyTimeline, AppendToTimeline, GetItemListInTrack, and SetCurrentTimeline. By receiving higher-level instructions, the Python server executes the granular sequence internally, returning a consolidated [[STATE|state]] to the LLM.   

Conversely, Granular Mode is designed for power users and highly specialized agentic workflows. It exposes up to 341 individual tools, mapping one MCP tool directly to one individual DaVinci Resolve API method. This requires the LLM to possess deep intrinsic knowledge of the Resolve object hierarchy but allows for deterministic, low-level manipulation of the software [[STATE|state]] without the assumptions built into compound helpers.   

Architecting an MCP Server: Building from Scratch

For organizations opting to build a proprietary MCP server wrapping the DaVinci Resolve Scripting API, several complex engineering challenges must be addressed. The development process requires deep integration with Blackmagic Design's shared libraries, rigorous Python environment management, and strategic abstraction of the API surface.

Environmental Dependency Mapping and Inter-Process Communication

The DaVinci Resolve Scripting API is accessible exclusively in the paid DaVinci Resolve Studio version; the free edition does not expose external scripting capabilities. To facilitate external server communication, the host application must be configured to accept local network or local machine scripts via the application preferences (Preferences > [[general|General]] > External scripting using > Local).   

Unlike internal scripts executed directly from the DaVinci Resolve console, which automatically inherit the application's runtime environment, an external MCP server must manually load and link to Blackmagic's proprietary fusionscript dynamic library. This requires strict configuration of system environment variables across target operating systems to ensure the Python interpreter can locate the API modules.   

Operating System	Variable	Required Path Designation
macOS	RESOLVE_SCRIPT_API	

/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/ 


macOS	RESOLVE_SCRIPT_LIB	

/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so 


macOS	PYTHONPATH	

$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/ 


Windows	RESOLVE_SCRIPT_API	

%PROGRAMDATA%\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\ 


Windows	RESOLVE_SCRIPT_LIB	

C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll 


Windows	PYTHONPATH	

%PYTHONPATH%;%RESOLVE_SCRIPT_API%\Modules\ 


Linux	RESOLVE_SCRIPT_API	

/opt/resolve/Developer/Scripting/ 


Linux	RESOLVE_SCRIPT_LIB	

/opt/resolve/libs/Fusion/fusionscript.so 


Linux	PYTHONPATH	

$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules/ 

  
The Python 3.12 Deprecation Roadblock

A critical architectural constraint when building a modern MCP server is the current DaVinci Resolve API's dependency on the deprecated Python imp module. The official DaVinciResolveScript.py module utilizes the function imp.load_dynamic("fusionscript", lib_path) to interface with the compiled C++ application core.   

Because the imp module was marked for deprecation in Python 3.4 and completely removed in Python 3.12, developers attempting to automate DaVinci Resolve with cutting-edge Python environments encounter immediate, silent execution failures or ModuleNotFoundError exceptions. While experimental workarounds attempt to substitute imp.load_dynamic with importlib.machinery.ExtensionFileLoader or direct ctypes.CDLL hooks, Blackmagic Design's proprietary scrambling of function names within the dynamic link library complicates alternative loading mechanisms. Consequently, utilizing Python 3.10 or 3.11 remains the required, lowest-risk environment for deploying production-grade MCP servers until Blackmagic Design officially modernizes the internal loader scripts.   

Connection Resiliency and Timeout Protection

When an external Python process communicates with DaVinci Resolve, it utilizes Inter-Process Communication (IPC). If the DaVinci Resolve application is occupied with a heavily threaded task, API calls from the MCP server can hang indefinitely if the IPC is unresponsive. An enterprise-grade MCP server must implement threading to add timeouts to the connection initialization and subsequent API calls. Wrapping the dvr_script.scriptapp("Resolve") execution in a daemonized thread with a strict timeout (e.g., 5 to 10 seconds) prevents the MCP server from locking the AI assistant's context generation if the NLE becomes unresponsive. Furthermore, developers building cross-network tools can initialize the API via local IP addresses dynamically fetched from system interfaces, bypassing localized loopback restrictions.   

DaVinci Resolve Scripting API: Foundational Architecture

The DaVinci Resolve Scripting API is rigidly object-oriented. It represents the internal data structures and [[STATE|state]] of the application through a hierarchical traversal tree. Every automation script must initiate by acquiring the global Resolve object and systematically traversing downward through managers, projects, storage interfaces, timelines, and discrete items.

The Global Resolve Object

The Resolve object is the root entry point for all API interactions. Once imported and instantiated, it provides access to the primary subsystems of the application. As a native object, it can be inspected for further properties using dir() or help() in Python, or table iteration using getmetatable in Lua.   

Resolve Object Methods	Return Type	Architectural Function
Fusion()	Fusion	

Yields the Fusion object, acting as the starting point for all Fusion-specific compositing scripts.


GetMediaStorage()	MediaStorage	

Returns the storage object utilized to query mounted volumes and act on host filesystem media locations.


GetProjectManager()	ProjectManager	

Returns the manager object responsible for handling currently open databases and project lifecycles.


OpenPage(pageName)	Bool	

Forces the GUI to switch to the indicated page ("media", "cut", "edit", "fusion", "color", "fairlight", "deliver").


GetCurrentPage()	String	

Returns the string identifier of the page currently displayed in the main application window.


GetProductName()	String	

Returns the product name (e.g., "DaVinci Resolve Studio").


GetVersion() / GetVersionString()	[int] / String	

Returns the active application version.


Quit()	None	

Programmatically terminates the DaVinci Resolve application.

  
Project Manager Operations

The ProjectManager object is the gateway to database interaction. It governs the creation, deletion, loading, and archiving of projects, as well as the active database connection.

ProjectManager Methods	Return Type	Architectural Function
ArchiveProject(projectName, filePath, isArchiveSrcMedia, isArchiveRenderCache, isArchiveProxyMedia)	Bool	

Archives the specified project to the provided file path. Accepts boolean flags to conditionally include source media, render caches, and proxies.


CreateProject(projectName)	Project	

Initializes and returns a new project if the provided string name is unique within the database.


DeleteProject(projectName)	Bool	

Deletes the designated project from the active database if it is not currently loaded.


LoadProject(projectName)	Project	

Loads the specified project into the active workspace and returns its object.


GetCurrentProject()	Project	

Returns the currently active project object.


SaveProject()	Bool	

Triggers a database save operation for the active project.


GetCurrentDatabase()	{dbInfo}	

Returns a dictionary corresponding to the current database connection containing keys like DbType, DbName, and optionally IpAddress.


GetDatabaseList()	[{dbInfo}]	

Returns a list of dictionaries detailing all databases currently added to the Resolve instance.


SetCurrentDatabase({dbInfo})	Bool	

Switches the connection to the specified database and forcibly closes any open project.

  
Active Project Management

Once a Project object is acquired, it acts as the centralized hub for retrieving the critical components of the post-production workflow: the media pool, the timelines, the gallery, and the render configurations.

Project Methods	Return Type	Architectural Function
GetMediaPool()	MediaPool	

Returns the core MediaPool object, required for ingesting assets and organizing bins.


GetTimelineCount()	int	

Returns the total integer count of timelines currently present in the project.


GetTimelineByIndex(idx)	Timeline	

Returns the timeline at the specified 1-based [[wiki/index|index]] (where 1 <= idx <= project.GetTimelineCount()).


GetCurrentTimeline()	Timeline	

Returns the timeline object currently loaded and active in the GUI viewer.


SetCurrentTimeline(timeline)	Bool	

Sets the provided timeline object as the active timeline for the project.


GetGallery()	Gallery	

Returns the Gallery object, utilized for managing grading stills and PowerGrades.


GetName()	String	

Returns the assigned user-defined name of the project.


SetName(projectName)	Bool	

Renames the project, provided the target name string is unique within the database.


GetPresetList() / SetPreset(name)	[presets] / Bool	

Queries and applies global configuration presets defined in the project settings.

  
Media Storage and Media Pool Operations

Automating the edit process fundamentally requires traversing the boundary between the host operating system's filesystem and DaVinci Resolve's internal asset management structure. This is accomplished via the MediaStorage and MediaPool objects.

Media Storage and Filesystem Interaction

Before a timeline can be constructed, raw media must be ingested from the file system into the active database. The MediaStorage object provides the methods necessary to map directories, discover files, and inject them into the project.

MediaStorage Methods	Return Type	Architectural Function
GetMountedVolumeList()	[paths...]	

Returns an array of absolute folder paths corresponding to storage volumes recognized and mounted by the host operating system.


GetSubFolderList(folderPath)	[paths...]	

Returns an array of nested directory paths located within a specific absolute folder path.


GetFileList(folderPath)	[paths...]	

Returns the media files present within a directory. Notably, sequential image formats (e.g., DPX, EXR sequences) may be logically consolidated into single entries by the API.


RevealInStorage(path)	Bool	

Forces the GUI to expand and highlight the given file or folder path within Resolve's Media Storage panel.


AddItemListToMediaPool([paths])	[MediaPoolItem]	

Ingests the specified array of media file paths into the currently active Media Pool folder, translating OS files into actionable MediaPoolItem objects.


AddClipMattesToMediaPool(item, [paths], stereoEye)	Bool	

Attaches external matte files directly to a specific MediaPoolItem. The optional stereoEye argument specifies whether to attach the matte to the "left" or "right" eye for stereoscopic workflows.


AddTimelineMattesToMediaPool([paths])	[MediaPoolItem]	

Adds specified media files specifically designated as timeline mattes directly into the current media pool folder.

  
Media Pool and Bin Organization

Once media is ingested, it is managed by the MediaPool object. The Media Pool acts as the hierarchical container for bins (referred to programmatically as Folder objects) and timelines. It serves as the primary factory for generating sequences.

MediaPool Methods	Return Type	Architectural Function
GetRootFolder()	Folder	

Returns the [[master|master]] root folder of the Media Pool, the starting point for bin traversal.


AddSubFolder(folder, name)	Folder	

Creates a new bin under the specified Folder object with the assigned string name.


RefreshFolders()	Bool	

Forces an update of the folder structure, a critical method when operating in multi-user collaboration mode where external changes must be synchronized.


GetCurrentFolder() / SetCurrentFolder(folder)	Folder / Bool	

Queries or explicitly sets the active bin within the GUI. Subsequent ingest operations target this active folder.


ImportMedia([paths])	[MediaPoolItem]	

An alternative to AddItemListToMediaPool, this method imports absolute paths directly into the Media Pool, handling sequences automatically.

  

To parse the organization of the Media Pool, a script must interact with the instantiated Folder objects. A Folder provides methods to retrieve its contents and structure: GetClipList() returns an array of MediaPoolItem objects representing the video and audio clips. GetSubFolderList() returns an array of nested Folder objects. Additional administrative functions include GetName() for retrieving the bin's string identifier, GetIsFolderStale() to check synchronization status in collaboration mode, and GetUniqueId() to retrieve the internal UUID of the bin.   

Timeline Manipulation and Conforming Assembly

The construction and manipulation of timelines form the core of programmatic editing workflows. The MediaPool object exposes a suite of methods specifically designed to generate and conform sequences using various paradigms, ranging from bulk assembly to metadata-driven interchange conforming.

Timeline Initialization and Clip Appending

Timelines can be instantiated either as blank slates or pre-populated with arrays of clips.

Timeline Creation & Appending Methods	Description
CreateEmptyTimeline(name)	

Instantiates a blank timeline with the given string identifier and sets it as the active sequence.


CreateTimelineFromClips(name, [clips])	

Creates a new timeline and sequentially appends a provided array of MediaPoolItem objects, ideal for string-outs.


AppendToTimeline([clips])	

Appends an array of MediaPoolItem objects to the currently active timeline, returning an array of resulting TimelineItem objects representing the newly placed instances.


ImportTimelineFromFile(filePath, {options})	

Conforms a timeline entirely from standard interchange formats. Supported files include AAF, EDL, XML, FCPXML, DRT, and ADL. The options dictionary allows scripts to define parameters such as "importSourceClips", "timelineName", and "sourceClipsPath" for missing media reconnection.


ImportIntoTimeline(filePath, {options})	

Imports items from an AAF file into the existing active timeline. The options dictionary configures parameters like "linkToSourceCameraFiles" and "useSizingInfo".


CreateCompoundClip([timelineItems])	

Groups an array of existing TimelineItem objects into a single nested compound clip, accepting an optional dictionary to set the "startTimecode" and "name".


CreateFusionClip([timelineItems])	

Groups timeline items into a dedicated Fusion clip for advanced node-based compositing.

  

A highly significant advancement in the scripting API, introduced natively in DaVinci Resolve 19.0.2, is the inclusion of sub-frame precision. Prior to this update, API timeline assembly was restricted to rigid integer frame boundaries, severely limiting the automation of high-frequency audio conforming or sub-frame syncing. The updated API permits AppendToTimeline([{clipInfo}]) where the clipInfo dictionary now accepts floating-point values for recordFrame indices. Furthermore, developers can now utilize precise getter methods such as GetSourceEndTime(), GetSourceStartTime(), and GetDuration(subframe_precision) which return float values rather than traditional integer arrays, enabling perfect programmatic sync.   

Timeline Track and Item Interrogation

Once a Timeline object is instantiated, it exposes methods to probe its internal structure. A script can invoke GetTrackCount("video" | "audio" | "subtitle") to ascertain the total number of tracks of a specific type, and subsequently use GetItemListInTrack("video", trackIndex) to return an array of all TimelineItem objects residing on that specific track. Tracks can be programmatically added using AddTrack("video" | "audio" | "subtitle").   

When clips reside on a track, they exist as TimelineItem objects. The API exposes GetProperty(propertyKey) and SetProperty(propertyKey, propertyValue) for rigorous spatial, temporal, and composite manipulation.   

These properties are critical for automated reframing, intelligent object tracking pipelines, or generating dynamic picture-in-picture deliverables. The supported keys include:

Pan: Accepts floating-point values ranging from -4.0 to 4.0 relative to the width.   

Tilt: Accepts floating-point values ranging from -4.0 to 4.0 relative to the height.   

ZoomX and ZoomY: Accepts floating-point values spanning from 0.0 to 100.0.   

ZoomGang: Accepts a boolean value to lock or unlock X and Y scaling.   

RotationAngle: Accepts floating-point degree values.   

Exporting Timelines and Interchange Data

Beyond rendering rasterized video files, the API supports the automated extraction of timeline data structures for cross-platform conforming and archival. The Timeline:Export(fileName, exportType, exportSubtype) method enables scripts to serialize metadata payloads to the disk.   

The exportType parameter relies on constants explicitly defined within the global resolve object. Supported constants include resolve.EXPORT_AAF, EXPORT_DRT, EXPORT_EDL, EXPORT_FCP_7_XML, EXPORT_TEXT_CSV, EXPORT_TEXT_TAB, and comprehensive OpenTimelineIO support via EXPORT_OTIO. Furthermore, specific Dolby Vision XML profiles are supported (EXPORT_DOLBY_VISION_VER_2_9, 4_0, and 5_1) alongside varying iterations of Apple's FCPXML format (versions 1.8 through 1.10).   

When exporting AAF or EDL variants, the exportSubtype parameter becomes mandatory to define the handling of source media. Valid subtypes include EXPORT_AAF_NEW, EXPORT_AAF_EXISTING, EXPORT_CDL, EXPORT_SDL, and EXPORT_MISSING_CLIPS. A critical note for automation developers: older FCPXML versions (1.3 through 1.7) were completely deprecated as of DaVinci Resolve 18.1. Modern automation scripts must explicitly default to EXPORT_FCPXML_1_8 or higher to prevent silent execution failures.   

Metadata Management and Item Properties

Metadata management forms the backbone of advanced post-production pipelines. The API provides extensive capabilities to read and mutate both descriptive and functional metadata on both TimelineItem and MediaPoolItem objects.

Metadata Management Methods	Functionality Description
GetMetadata(metadataType)	

Returns specific string metadata associated with the provided key. If invoked without an argument, it returns a comprehensive dictionary of all metadata parameters currently populated for the clip.


SetMetadata(metadataType, value)	

Writes string data to defined metadata fields (e.g., "Scene", "Take", "Camera", "VFX Notes"). Returns a boolean indicating success.


GetMediaId()	

Returns the internal unique UUID string of the MediaPoolItem, crucial for external database tracking.


GetClipProperty() / SetClipProperty()	

Queries or modifies functional properties distinct from standard metadata, such as clip color, Super Scale configuration, or Alpha mode.


AddMarker(frameId, color, name, note, duration, customData)	

Imprints a spatial marker at a specific frame [[wiki/index|index]]. The customData payload string is exceptionally valuable, frequently utilized by MCP servers to store JSON-encoded states or review notes from external LLMs.


GetMarkers()	

Returns a dictionary structured as (frameId -> {information}) containing all markers present on the item.


AddFlag(color) / GetFlagList()	

Flags are similar to markers but apply to the entire clip rather than a specific frame. These methods allow applying, querying, and clearing color-coded flags.

  

Historically, establishing arbitrary custom metadata schemas within DaVinci Resolve was challenging without relying on hijacking marker notes or standard fields like "VFX Notes". However, the 19.0.2 API update introduced GetThirdPartyMetadata(metadataType) and SetThirdPartyMetadata(), enabling studios to inject proprietary database IDs or complex JSON structures directly into the clip file wrapper without polluting standard editorial metadata fields.   

Color Grading and Node Graph Automation

Automating the Color Page requires the script to transition from the contextual TimelineItem down into the underlying Graph object. The node graph constitutes the core mathematical engine of Resolve's image processing pipeline. The API empowers scripts to programmatically enforce color space transformations, conform grades from digital imaging technicians (DITs), and execute complex Dolby Vision analysis algorithms.

To manipulate the color [[STATE|state]], a script must first query the TimelineItem for its specific node graph.

GetNodeGraph() or GetNodeGraph(layerIndex) returns the Graph object associated with the clip. An optional layer [[wiki/index|index]] allows targeting specific nested grading passes.   

GetNumNodes() returns the integer count of distinct serial, parallel, or layer correction nodes currently applied within that graph.   

With the Graph object exposed, automation pipelines can manipulate the image data directly. A critical architectural note for developers: starting from DaVinci Resolve version 16.2, the nodeIndex parameter accepted by node modification methods transitioned from 0-based to 1-based indexing (i.e., 1≤nodeIndex≤totalNodes). Failure to account for this indexing shift within iterative loops will result in IndexError exceptions during automation.   

Node Graph Method	Purpose and Execution Constraints
SetLUT(nodeIndex, lutPath)	

Applies a 1D or 3D LUT cube file to the specified node [[wiki/index|index]]. Requires a validated absolute filesystem path.


GetLUT(nodeIndex)	

Returns the absolute string path of the LUT currently applied to the target node.


SetCDL(nodeIndex, cdlMap)	

Applies a Color Decision List (CDL) conform. The cdlMap is a dictionary requiring standard Slope, Offset, Power (SOP), and Saturation parameters.


ApplyGradeFromDRX(drxPath, mode)	

Completely overwrites the existing node tree with a saved DaVinci Resolve Grade (.drx) file. The mode integer determines keyframe alignment logic: 0 (No keyframes), 1 (Source Timecode alignment), or 2 (Start frame alignment).


SetNodeCacheMode(nodeIndex, mode)	

Programmatically toggles the node cache behavior for complex effects. Modes are -1 (Auto), 0 (Disabled), and 1 (Enabled).


AnalyzeDolbyVision([items], analysisType)	

Triggers the proprietary Dolby Vision engine to analyze exposure metadata across the provided array of clips. Returns a boolean indicating successful initiation.

  

Through the synergistic application of these methods, MCP servers can enable LLMs to ingest a networked folder of .drx files, parse timelines, and autonomously apply specific grades to corresponding clips based on string matching against GetClipProperty("File Name"), effectively bypassing the GUI entirely for automated dailies processing.

Render Queue Management and Automated Delivery

The Deliver page orchestration is arguably the most extensively utilized aspect of the Resolve Scripting API. For enterprise environments managing high volumes of varied deliverables—such as differing resolutions, codecs, frame rates, and aspect ratios tailored for disparate social media platforms—the API facilitates the programmatic generation of render payloads, comprehensive queue management, and execution polling without any human intervention.

Payload Configuration: The SetRenderSettings Dictionary

Before a job can be instantiated and appended to the render queue, the underlying project's render settings must be explicitly mutated. This is achieved via the Project:SetRenderSettings({settings}) method, which accepts a highly specific dictionary of keys dictating the codec architecture, spatial resolution, format wrapper, and temporal range.   

The exact schema of the settings dictionary is strictly enforced. Incorrect combinations—such as requesting an H.264 codec within an incompatible .mxf wrapper—will fail silently upon queueing, leading to empty output states.

The comprehensive list of supported Render Settings keys includes:

Targeting and Naming [[DIRECTIVES|Directives]]:

TargetDir (string): The absolute path defining the output directory.   

CustomName (string): The explicitly defined output file base name.   

UniqueFilenameStyle (int): Determines conflict resolution in the filesystem (0 applies a Prefix, 1 applies a Suffix).   

Temporal Boundaries:

SelectAllFrames (Bool): If set to True, the entire length of the timeline is rendered, overriding in/out points.   

MarkIn / MarkOut (int): Frame indices for rendering partial temporal segments. Completely ignored if SelectAllFrames is active.   

Format and Spatial Configuration:

FormatWidth / FormatHeight (int): Explicit raster pixel dimensions overriding timeline defaults.   

FrameRate (float): Output temporal resolution defined as a float (e.g., 23.976, 24.0).   

PixelAspectRatio (string): Utilizes constants such as 16_9, 4_3, square, or cinemascope.   

ExportVideo / ExportAudio (Bool): Discrete toggles for activating multiplexed streams.   

Codec Specifics:

VideoQuality (int or string): Sets compression fidelity. Accepts 0 (Automatic), integer bounds [1 -> MAX] for explicit bit rates, or string presets (Least, Low, Medium, High, Best).   

AudioCodec (string): Specifies the audio format (e.g., aac, lpcm).   

AudioSampleRate / AudioBitDepth (int): Dictates audio fidelity bounds.   

EncodingProfile (string): An advanced parameter for H.264/H.265 defining profiles (e.g., Main10).   

MultiPassEncode (Bool): Toggles multi-pass analysis for H.264 processing.   

Color Space and Alpha Channel Handlers:

ColorSpaceTag / GammaTag (string): Overrides export color management flagging (e.g., Same as Project, ACEScct, AstroDesign).   

ExportAlpha (Bool): Forces an RGBA output stream if the selected format and codec support transparency.   

AlphaMode (int): Defines transparency mathematics (0 for Premultiplied, 1 for Straight).   

NetworkOptimization (Bool): Triggers 'Fast Start' atom rearrangement, supported only by QuickTime and MP4 formats.   

Job Lifecycle and Execution Polling

Once SetRenderSettings() commits the configuration payload, the job lifecycle must be actively managed via the queue arrays. This process requires a sequential, programmatic [[STATE|state]] machine to successfully output files.

First, the script invokes AddRenderJob(). This method reads the currently active render settings, captures a definitive snapshot, and pushes the job into the queue. Crucially, it returns a unique jobId string necessary for tracking. A script can survey existing queued jobs using GetRenderJobList(), which returns an array of job dictionaries. Invalid or undesired jobs can be purged individually via DeleteRenderJob(jobId) or en masse using the global DeleteAllRenderJobs() function.   

Rendering is formally initiated via StartRendering(). This method is highly versatile; it can accept arrays of specific jobId strings, integer arrays based on queue position, or trigger the entire queue if called without parameters. Furthermore, an optional isInteractiveMode boolean parameter can be passed. When set to True, it forces the DaVinci Resolve GUI to natively render error feedback dialogs—a feature generally disabled during headless automation to prevent scripts from hanging on user-prompt blockers.   

The architectural challenge of automated rendering is that DaVinci Resolve API render calls execute asynchronously. Therefore, automation scripts must employ a continuous polling loop to monitor execution [[STATE|state]].

To automate delivery robustly, scripts must first apply the dictionary payload to SetRenderSettings, push the snapshot to the queue via AddRenderJob, and trigger the engine. Then, the script enters a while loop, continuously evaluating the [[STATE|state]] of IsRenderingInProgress().   

Render Polling Sequence	Execution Logic
Phase 1: Dispatch	Execute StartRendering().
Phase 2: Delay & Poll	

Initiate a while loop checking IsRenderingInProgress(). Implement a programmatic time.sleep() within the loop to prevent thread locking and reduce API chatter.


Phase 3: [[STATE|State]] Evaluation	Once IsRenderingInProgress() returns False, the loop exits.
Phase 4: Output Validation	

The script must invoke GetRenderJobStatus(jobId) to parse the returned dictionary, isolating keys to determine if the job reached 100% completion or returned a "Cancelled" or failed [[STATE|state]].

  

If this polling loop is not implemented, the Python script will immediately terminate upon calling StartRendering(), potentially severing the IPC connection before the DaVinci Resolve engine can finalize the complex file wrappers.

Conclusion

The convergence of the Model Context Protocol (MCP) and the robust DaVinci Resolve Scripting API represents a monumental advancement in programmatic post-production workflows. By providing a secure, stdio-isolated architectural bridge, community-driven MCP servers—exemplified by the comprehensive samuelgursky/davinci-resolve-mcp project—empower sophisticated Large Language Models to bypass complex, manual GUI interactions and execute granular Python [[DIRECTIVES|directives]] natively.

Developing these automation solutions, however, requires an acute understanding of the underlying API's object-oriented hierarchy. AI [[AGENTS|agents]] and human developers alike must be programmed to respect the sequential necessity of acquiring the global Resolve object, systematically traversing down through the MediaPool to ingest assets, constructing precise Timeline assemblies, manipulating discrete Graph nodes, and formatting exact parameter dictionaries for the SetRenderSettings orchestrator.

Furthermore, environmental complexities—specifically the reliance of the Blackmagic Design fusionscript dynamic linker on the deprecated Python 3.12 imp module—necessitate careful, version-controlled runtime deployment, heavily favoring Python 3.10 or 3.11 to ensure operational stability. As the Scripting API continues to iteratively evolve, expanding its capabilities to encompass sub-frame positional precision and third-party metadata injection, the capacity for autonomous AI systems to execute full-scale, unsupervised conforming, grading, and rendering pipelines will only deepen, ultimately positioning conversational LLM orchestration as a fundamental pillar of modern technical post-production.

---
*Auto-ingested into Keystone Brain Vector DB*


---
📁 **See also:** [[Research_Archives/02_MCP_Tools/INDEX|← Directory Index]]

**Related:** [[20260613_VIDEO_PROD_davinci_resolve_studio_scripting_api_complete_reference_for_]] · [[8_1_DaVinci_Resolve_Workflow]] · [[davinci_resolve_api_mastery]]
