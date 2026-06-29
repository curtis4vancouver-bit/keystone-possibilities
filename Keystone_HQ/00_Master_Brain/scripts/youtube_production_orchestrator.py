# youtube_production_orchestrator.py
"""
Keystone Content Pipeline Orchestrator
=======================================
An end-to-end automated orchestrator for processing, staging, renaming, assembling,
verifying, and uploading video productions across Wayne Stevenson's dual-brand empire.

Provides a CLI dashboard to guide Wayne step-by-step through the production pipeline.
"""

import os
import sys
import re
import json
import time
import shutil
import string
from pathlib import Path

# Configure stdout to use UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Brand/Channel Mapping Constants
BRAND_ROUTING = {
    "possibilities": {
        "name": "Keystone Possibilities",
        "channel_arg": "possibilities",
        "channel_id": "UCu8gdU_R8XE2RvcttGa3drg",
        "token_file": "youtube_token_possibilities.json",
        "category_id": "22",  # People & Blogs / Education
        "keywords": ["construction", "multiplex", "bill 44", "excavation", "squamish", "zoning", "contractor", "pm consulting"],
        "disclaimer": ""
    },
    "recomposition": {
        "name": "Keystone Recomposition",
        "channel_arg": "recomposition",
        "channel_id": "UCMn1f9DTF_iybKmv5WlTm9Q",
        "token_file": "youtube_token_oac.json",
        "category_id": "10",  # Music
        "keywords": ["ambient", "music", "dj", "beat", "lofi", "relaxing", "mix", "soundscape"],
        "disclaimer": ""
    },
    "protocols": {
        "name": "Protocols",
        "channel_arg": "protocols",
        "channel_id": "UCxURlqMNhAtxUTpdXmlOYaw",
        "token_file": "youtube_token_protocols.json",
        "category_id": "27",  # Education / Science & Tech
        "keywords": ["peptide", "longevity", "bpc-157", "semaglutide", "health", "dose", "protocol", "anhedonia", "tirzepatide", "sarcopenia"],
        "disclaimer": (
            "\n\nDisclaimer: This video is for research and educational purposes only. "
            "Peptides and health compounds mentioned are not approved by the FDA for human administration, "
            "are banned by WADA, and are classified as unauthorized drugs by Health Canada. "
            "Consult a licensed physician before starting any wellness protocol."
        )
    }
}

# Noise words to ignore during fuzzy search
NOISE_WORDS = {
    "says", "keep", "exact", "clothes", "the", "avatar", "not", "change", "them", "standing",
    "against", "pure", "black", "background", "medium", "shot", "from", "waist", "camera",
    "pulls", "back", "slowly", "teaching", "mode", "subtitles", "close", "face", "holds",
    "steady", "serious", "expression", "nod", "with", "slight", "smile", "concerned",
    "talking", "talking to camera", "photorealistic", "cinematic", "lighting", "studio"
}

def clean_words(text):
    if not text:
        return set()
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = [w.strip() for w in text.split()]
    return {w for w in words if len(w) >= 3 and w not in NOISE_WORDS}

def calculate_similarity(prompt1, prompt2):
    w1 = clean_words(prompt1)
    w2 = clean_words(prompt2)
    if not w1 or not w2:
        return 0.0
    return len(w1.intersection(w2)) / max(len(w1), len(w2))

class YoutubeProductionOrchestrator:
    def __init__(self):
        self.downloads_dir = Path(r"C:\Users\Curtis\Downloads")
        self.desktop_dir = Path(r"C:\Users\Curtis\Desktop")
        self.scripts_approved_dir = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\09_YouTube_Operations\Scripts_Approved")
        self.content_production_dir = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Content_Production")
        
        self.script_file = None
        self.brand_key = None
        self.slug = None
        self.target_dir = None
        self.is_short = False
        self.clips = []
        self.brolls = []
        self.title = ""
        self.description = ""
        self.tags = []

    def log(self, message, level="INFO"):
        prefix = {
            "INFO": "\033[94m[i]\033[0m",
            "SUCCESS": "\033[92m[+]\033[0m",
            "WARNING": "\033[93m[!]\033[0m",
            "ERROR": "\033[91m[-]\033[0m",
            "HEADER": "\033[95m[*]\033[0m"
        }.get(level, "[i]")
        print(f"{prefix} {message}")

    def prompt_menu(self):
        print("\n" + "="*60)
        print("          KEYSTONE YOUTUBE PRODUCTION ORCHESTRATOR")
        print("="*60)
        
        # 1. Locate Script File
        script_files = []
        for d in [self.scripts_approved_dir, self.content_production_dir]:
            if d.exists():
                script_files.extend(list(d.glob("*.md")))
        
        if not script_files:
            self.log("No approved scripts found in standard directories.", "WARNING")
            path_input = input("Enter the absolute path to your markdown script file: ").strip()
            self.script_file = Path(path_input.strip('\"\''))
        else:
            print("\nAvailable Script Files:")
            for idx, f in enumerate(script_files):
                print(f"  [{idx + 1}] {f.name} ({f.parent.name})")
            
            choice = input(f"\nSelect a script file [1-{len(script_files)}] (or type custom path): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(script_files):
                self.script_file = script_files[int(choice) - 1]
            else:
                self.script_file = Path(choice.strip('\"\''))
        
        if not self.script_file.exists():
            self.log(f"Script file {self.script_file} does not exist. Exiting.", "ERROR")
            sys.exit(1)
            
        self.log(f"Selected Script: {self.script_file.name}", "SUCCESS")
        
        # 2. Select Brand/Channel
        print("\nSelect Channel/Brand:")
        print("  [1] Keystone Possibilities (Construction)")
        print("  [2] Keystone Recomposition (Music)")
        print("  [3] Protocols (Peptide/Health Science)")
        brand_choice = input("Select brand [1-3]: ").strip()
        if brand_choice == "1":
            self.brand_key = "possibilities"
        elif brand_choice == "2":
            self.brand_key = "recomposition"
        else:
            self.brand_key = "protocols"
            
        self.log(f"Selected Brand Routing: {BRAND_ROUTING[self.brand_key]['name']}", "SUCCESS")

        # 3. Detect Video Format
        format_choice = input("\nIs this a Vertical Short (9:16)? [y/N]: ").strip().lower()
        self.is_short = format_choice in ["y", "yes"]
        self.log(f"Format: {'Short (9:16)' if self.is_short else 'Long-Form (16:9)'}", "SUCCESS")

        # 4. Generate Folder Slug
        default_slug = self.script_file.stem.upper().replace(" ", "_").replace("-", "_")
        prefix = "SHORT_" if self.is_short else "LONG_"
        if not default_slug.startswith(prefix):
            default_slug = f"{prefix}{default_slug}"
            
        self.slug = input(f"\nEnter Desktop folder name [{default_slug}]: ").strip()
        if not self.slug:
            self.slug = default_slug
            
        self.target_dir = self.desktop_dir / self.slug
        self.log(f"Staging Location: {self.target_dir}", "SUCCESS")

    def parse_script(self):
        self.log("Parsing script markdown...", "INFO")
        with open(self.script_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Try to parse title/metadata from frontmatter or top lines
        title_match = re.search(r"Title:\s*(.*)", content, re.IGNORECASE)
        if title_match:
            self.title = title_match.group(1).strip()
        else:
            # Fallback: find first # heading
            h1_match = re.search(r"^#\s+(.*)", content, re.M)
            if h1_match:
                self.title = h1_match.group(1).strip()
            else:
                self.title = self.slug.replace("_", " ")

        # Parse Clip blocks (A1, A2...)
        # Matches: ### 📋 CLIP (A\d+) — (WAYNE|VICTORIA|ANA) followed by script and video prompt
        clip_blocks = re.findall(
            r"### 📋 CLIP (A\d+) — (WAYNE|VICTORIA|ANA|Victoria|Wayne|Ana).*?\nTHIS IS THE SCRIPT:\r?\n(.*?)\r?\n\r?\nTHIS IS THE VIDEO PROMPT:\r?\n(.*?)(?=\r?\n\r?\n---|\r?\n---|\Z)",
            content,
            re.DOTALL
        )
        
        self.clips = []
        for clip_id, speaker, script, prompt in clip_blocks:
            # Extract speaker's dialogue
            dialogue_clean = re.sub(r'^(Wayne|Victoria|Ana) says:\s*', '', script, flags=re.IGNORECASE).strip()
            self.clips.append({
                "id": clip_id.strip(),
                "speaker": speaker.strip().capitalize(),
                "dialogue": dialogue_clean,
                "prompt": prompt.strip(),
                "type": "video"
            })

        # Parse B-roll blocks (B1, B2...)
        # Matches: #### 🖼️ B(\d+): prompt content
        broll_blocks = re.findall(
            r"#### 🖼️ B(\d+): .*?\n(.*?)(?=\n\n####|\n\n---|\Z)",
            content,
            re.DOTALL
        )
        self.brolls = []
        for broll_id, prompt in broll_blocks:
            self.brolls.append({
                "id": f"B{broll_id.strip()}",
                "prompt": prompt.strip(),
                "type": "image"
            })

        # Look for explicit Tags list in script
        tags_match = re.search(r"Tags:\s*(.*)", content, re.IGNORECASE)
        if tags_match:
            self.tags = [t.strip() for t in tags_match.group(1).split(",") if t.strip()]
        else:
            self.tags = [self.brand_key, "keystone"]

        self.log(f"Parsed {len(self.clips)} video clips and {len(self.brolls)} B-rolls.", "SUCCESS")
        if self.title:
            self.log(f"Extracted Title: {self.title}", "INFO")

    def stage_folders(self):
        self.log("Staging workspace directories on Desktop...", "INFO")
        videos_path = self.target_dir / "Videos"
        images_path = self.target_dir / "Images"
        thumb_path = self.target_dir / "Thumbnails"
        final_path = self.target_dir / "FINAL"
        
        for d in [videos_path, images_path, thumb_path, final_path]:
            d.mkdir(parents=True, exist_ok=True)
            
        # Verify if old files exist
        old_files = list(self.target_dir.rglob("*.*"))
        if old_files:
            self.log(f"Staging folder is not empty ({len(old_files)} files exist).", "WARNING")
            confirm = input("Would you like to clear this directory before starting? [y/N]: ").strip().lower()
            if confirm in ["y", "yes"]:
                for d in [videos_path, images_path, thumb_path, final_path]:
                    shutil.rmtree(d)
                    d.mkdir(parents=True, exist_ok=True)
                self.log("Cleared folders successfully.", "SUCCESS")

    def rename_and_move_downloads(self):
        """
        Phase 2B Smart Renamer: Scans downloads folder, sorts files by modified time,
        and matches them against the expected script clips/B-rolls using fuzzy prompt match.
        """
        self.log("Scanning downloads folder for new video and image assets...", "INFO")
        
        # 1. Collect candidate files from C:\Users\Curtis\Downloads
        candidate_files = []
        for file_path in self.downloads_dir.glob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() in [".crdownload", ".tmp", ".download"]:
                continue
            if file_path.suffix.lower() not in [".mp4", ".jpeg", ".jpg", ".png"]:
                continue
                
            # Filter files modified in the last 2 hours to avoid grabbing completely unrelated historical files
            age_hours = (time.time() - file_path.stat().st_mtime) / 3600.0
            if age_hours > 2.0:
                continue
                
            candidate_files.append(file_path)
            
        # Sort candidates by mtime (oldest first) to preserve generation sequence
        candidate_files.sort(key=lambda x: x.stat().st_mtime)
        
        self.log(f"Found {len(candidate_files)} recent download files to process.", "INFO")
        
        # Prepare list of pending items from script
        pending_videos = [c for c in self.clips]
        pending_images = [b for b in self.brolls]
        
        matched_ops = []
        
        # Process videos
        video_files = [f for f in candidate_files if f.suffix.lower() == ".mp4"]
        self.log(f"Processing {len(video_files)} downloaded MP4 files...", "INFO")
        
        # Sequence-based matching fallback if fuzzy naming fails
        for idx, file_path in enumerate(video_files):
            # Clean up the filename stem (strip windows suffix ' (1)' and timestamps like '_202606212219')
            stem = re.sub(r'\s*\(\d+\)$', '', file_path.stem)
            stem = re.sub(r'_\d{12}$', '', stem)
            
            # Fuzzy match prompt against all pending videos
            best_item = None
            best_score = -1.0
            
            for item in pending_videos:
                score = calculate_similarity(stem, item["prompt"])
                if score > best_score:
                    best_score = score
                    best_item = item
            
            # If we have a decent match, or fallback to chronological sequence
            if best_item and best_score > 0.15:
                matched_item = best_item
                pending_videos.remove(matched_item)
                self.log(f"Matched {file_path.name} -> {matched_item['id']} (Fuzzy score: {best_score:.2f})", "SUCCESS")
            elif idx < len(self.clips):
                # Fallback to pure sequential order
                matched_item = self.clips[idx]
                if matched_item in pending_videos:
                    pending_videos.remove(matched_item)
                self.log(f"Matched {file_path.name} -> {matched_item['id']} (Chronological sequence fallback)", "WARNING")
            else:
                self.log(f"Could not correlate video {file_path.name} to script clips.", "WARNING")
                continue
                
            dest_path = self.target_dir / "Videos" / f"{matched_item['id']}.mp4"
            matched_ops.append((file_path, dest_path))

        # Process B-rolls (Images)
        image_files = [f for f in candidate_files if f.suffix.lower() in [".jpeg", ".jpg", ".png"]]
        self.log(f"Processing {len(image_files)} downloaded image files...", "INFO")
        
        for idx, file_path in enumerate(image_files):
            stem = re.sub(r'\s*\(\d+\)$', '', file_path.stem)
            stem = re.sub(r'_\d{12}$', '', stem)
            
            best_item = None
            best_score = -1.0
            
            for item in pending_images:
                score = calculate_similarity(stem, item["prompt"])
                if score > best_score:
                    best_score = score
                    best_item = item
                    
            if best_item and best_score > 0.15:
                matched_item = best_item
                pending_images.remove(matched_item)
                self.log(f"Matched B-roll {file_path.name} -> {matched_item['id']} (Fuzzy score: {best_score:.2f})", "SUCCESS")
            elif idx < len(self.brolls):
                matched_item = self.brolls[idx]
                if matched_item in pending_images:
                    pending_images.remove(matched_item)
                self.log(f"Matched B-roll {file_path.name} -> {matched_item['id']} (Chronological sequence fallback)", "WARNING")
            else:
                self.log(f"Could not correlate image {file_path.name} to B-rolls.", "WARNING")
                continue
                
            dest_path = self.target_dir / "Images" / f"{matched_item['id']}.jpeg"
            matched_ops.append((file_path, dest_path))

        # Verify matched assets count
        if not matched_ops:
            self.log("No matching downloads found. Verify you have downloaded your assets from Google Flow.", "WARNING")
            return
            
        print("\nStaged Matches Table:")
        print("-" * 65)
        for src, dest in matched_ops:
            print(f"  {src.name:<30} -> {dest.parent.name}/{dest.name}")
        print("-" * 65)
        
        confirm = input("\nExecute rename and copy? [Y/n]: ").strip().lower()
        if confirm not in ["n", "no"]:
            for src, dest in matched_ops:
                try:
                    shutil.copy2(src, dest)
                except Exception as e:
                    self.log(f"Error copying {src.name}: {e}", "ERROR")
            self.log("Rename and organize operations executed successfully.", "SUCCESS")
            
            # Validate files count in destination folders
            v_count = len(list((self.target_dir / "Videos").glob("*.mp4")))
            i_count = len(list((self.target_dir / "Images").glob("*.jpeg")))
            self.log(f"Staged Assets Status: Videos count = {v_count}/{len(self.clips)}, Images count = {i_count}/{len(self.brolls)}", "SUCCESS")

    def generate_davinci_script(self):
        """Generates a customized timeline assembly python script inside the project folder."""
        self.log("Generating DaVinci Resolve Timeline Assembly script...", "INFO")
        
        script_content = f"""# assemble_timeline.py
import os
import sys
import re

def init_resolve():
    os.environ["RESOLVE_SCRIPT_API"] = r"C:\\ProgramData\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting"
    os.environ["RESOLVE_SCRIPT_LIB"] = r"C:\\Program Files\\Blackmagic Design\\DaVinci Resolve\\fusionscript.dll"
    
    modules_path = os.path.join(os.environ["RESOLVE_SCRIPT_API"], "Modules")
    if modules_path not in sys.path:
        sys.path.append(modules_path)

    import DaVinciResolveScript as dvr
    resolve = dvr.scriptapp("Resolve")
    if not resolve:
        raise RuntimeError("Resolve scripting interface offline. Is Resolve open?")
    return resolve

def get_numeric_prefix(filename):
    match = re.search(r'(\\d+)', filename)
    return int(match.group(1)) if match else 9999

def assemble_project():
    project_name = "{self.slug}"
    timeline_name = "{self.slug}_Timeline"
    desktop_dir = r"{self.target_dir}"
    
    video_dir = os.path.join(desktop_dir, "Videos")
    broll_dir = os.path.join(desktop_dir, "Images")
    thumb_dir = os.path.join(desktop_dir, "Thumbnails")
    
    print("Initializing DaVinci Resolve...")
    try:
        resolve = init_resolve()
    except RuntimeError as e:
        print(f"Error: {{e}}")
        return
        
    pm = resolve.GetProjectManager()
    
    print(f"Creating project: {{project_name}}")
    project = pm.CreateProject(project_name)
    if not project:
        print(f"Project '{{project_name}}' already exists. Loading...")
        project = pm.LoadProject(project_name)
        
    if not project:
        print("Error: Could not load or create project.")
        return
        
    media_pool = project.GetMediaPool()
    media_storage = resolve.GetMediaStorage()
    
    # Collect files
    video_files = sorted(
        [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith('.mp4')],
        key=lambda x: get_numeric_prefix(os.path.basename(x))
    )
    broll_files = sorted(
        [os.path.join(broll_dir, f) for f in os.listdir(broll_dir) if f.endswith(('.png', '.jpg', '.jpeg'))],
        key=lambda x: get_numeric_prefix(os.path.basename(x))
    )
    
    # Import files to Media Pool
    print("Importing media to pool...")
    imported_videos = media_storage.AddItemListToMediaPool(video_files)
    imported_brolls = media_storage.AddItemListToMediaPool(broll_files)
    
    def get_items_list(imported):
        if isinstance(imported, dict):
            return list(imported.values())
        return imported or []
        
    videos_items = sorted(get_items_list(imported_videos), key=lambda x: get_numeric_prefix(x.GetName()))
    brolls_items = sorted(get_items_list(imported_brolls), key=lambda x: get_numeric_prefix(x.GetName()))
    
    # Create empty timeline
    for i in range(1, project.GetTimelineCount() + 1):
        t = project.GetTimelineByIndex(i)
        if t.GetName() == timeline_name:
            media_pool.DeleteTimelines([t])
            break
            
    print("Creating empty timeline...")
    timeline = media_pool.CreateEmptyTimeline(timeline_name)
    project.SetCurrentTimeline(timeline)
    
    # Set settings
    project.SetSetting("timelineFrameRate", "24.000")
    if {str(self.is_short)}:
        project.SetSetting("timelineResolutionWidth", "1080")
        project.SetSetting("timelineResolutionHeight", "1920")
    else:
        project.SetSetting("timelineResolutionWidth", "1920")
        project.SetSetting("timelineResolutionHeight", "1080")
        
    # Ensure Track V2 exists for B-roll overlays
    if timeline.GetTrackCount("video") < 2:
        timeline.AddTrack("video")
        
    # Append videos to track V1
    print("Appending videos to V1/A1...")
    media_pool.AppendToTimeline(videos_items)
    
    # Centering B-rolls on transitions
    timeline_video_items = timeline.GetItemListInTrack("video", 1)
    
    FPS = 24
    DURATION_SEC = 2.0
    TOTAL_FRAMES = int(FPS * DURATION_SEC)
    HALF_FRAMES = TOTAL_FRAMES // 2
    
    broll_insertions = []
    print("Positioning B-rolls on V2...")
    for idx, broll in enumerate(brolls_items):
        if idx < len(timeline_video_items) - 1:
            transition_frame = timeline_video_items[idx].GetEnd()
            record_frame = transition_frame - HALF_FRAMES
            
            broll_info = {{
                "mediaPoolItem": broll,
                "startFrame": 0,
                "endFrame": TOTAL_FRAMES - 1,
                "recordFrame": record_frame,
                "trackIndex": 2,
                "mediaType": 1
            }}
            broll_insertions.append(broll_info)
            print(f"Placed B-roll {{idx+1}} at transition frame {{transition_frame}}")
            
    if broll_insertions:
        media_pool.AppendToTimeline(broll_insertions)
        
    pm.SaveProject()
    print("SUCCESS: DaVinci Resolve timeline assembly complete!")

if __name__ == "__main__":
    assemble_project()
"""

        dest_script = self.target_dir / "assemble_timeline.py"
        with open(dest_script, "w", encoding="utf-8") as f:
            f.write(script_content)
        self.log(f"Saved custom assembly script to {dest_script}", "SUCCESS")
        self.log("To assemble, open DaVinci Resolve, then run: python assemble_timeline.py", "INFO")

    def run_quality_gate(self):
        """Pre-upload quality gate check."""
        self.log("Executing pre-upload quality gate verification...", "INFO")
        
        # 1. Title verification
        title_len = len(self.title)
        title_ok = title_len <= 100
        self.log(f"Video Title Check: '{self.title}' ({title_len} chars) - {'PASSED' if title_ok else 'FAILED (Too long)'}", "SUCCESS" if title_ok else "ERROR")
        
        # 2. Keyword Correlation check
        content_text = f"{self.title} {self.description} " + " ".join(self.tags)
        correlation_passed = True
        matched_brand = None
        
        for k, info in BRAND_ROUTING.items():
            matches = [w for w in info["keywords"] if w in content_text.lower()]
            if matches:
                matched_brand = k
                self.log(f"Keyword Matches for brand '{k}': {matches}", "INFO")
                
        if matched_brand and matched_brand != self.brand_key:
            self.log(f"Mismatch: Content maps to brand '{matched_brand}', but routing is configured for brand '{self.brand_key}'!", "ERROR")
            correlation_passed = False
        else:
            self.log("Keyword routing correlation check: PASSED.", "SUCCESS")

        # 3. Append disclaimer if required
        disclaimer = BRAND_ROUTING[self.brand_key]["disclaimer"]
        final_description = self.description
        if disclaimer and disclaimer not in final_description:
            final_description += disclaimer
            self.log("Appended legal disclaimer to description.", "SUCCESS")

        # 4. Altered / Synthetic Content Label check
        # Must be enabled since we are using Google Flow synthetic voice/avatars
        ai_label = "Enabled (alteredOrSyntheticContent = true)"
        self.log(f"AI Altered Content Label: {ai_label}", "SUCCESS")

        # Create output quality gate log
        log_content = f"""### PRE-UPLOAD QUALITY GATE LOG
- **Target Platform**: YouTube
- **Target Channel/Profile**: {BRAND_ROUTING[self.brand_key]['name']}
- **OAuth Token File**: {BRAND_ROUTING[self.brand_key]['token_file']}
- **Aspect Ratio**: {'9:16' if self.is_short else '16:9'}
- **AI Synthetic Content Label**: Enabled
- **Keyword Correlation Check**: {'PASSED' if correlation_passed else 'FAILED'}
- **Disclaimer Appended**: {'Yes' if disclaimer else 'No / N/A'}
- **Publish Status**: Queued as Unlisted
"""
        print("\n" + "="*50)
        print(log_content)
        print("="*50)
        
        # Write log file locally
        gate_log_file = self.target_dir / "pre_upload_quality_gate.json"
        metadata = {
            "title": self.title,
            "description": final_description,
            "tags": self.tags,
            "channel": self.brand_key,
            "category_id": BRAND_ROUTING[self.brand_key]["category_id"],
            "privacy_status": "unlisted",
            "token_file": BRAND_ROUTING[self.brand_key]["token_file"],
            "is_short": self.is_short,
            "alteredOrSyntheticContent": True
        }
        with open(gate_log_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
            
        self.log(f"Saved quality gate metadata log to {gate_log_file}", "SUCCESS")
        return metadata

    def upload_finished_video(self, metadata):
        """Checks for final video and triggers upload via JSON file or CLI instruction."""
        final_dir = self.target_dir / "FINAL"
        final_videos = list(final_dir.glob("*.mp4"))
        
        if not final_videos:
            self.log(f"No final video found in {final_dir}. Put your rendered video there to upload.", "WARNING")
            return
            
        video_file = final_videos[0]
        self.log(f"Found finished video: {video_file.name}", "SUCCESS")
        
        confirm = input(f"Do you want to upload {video_file.name} to YouTube ({BRAND_ROUTING[self.brand_key]['name']})? [y/N]: ").strip().lower()
        if confirm in ["y", "yes"]:
            # Write a special queue file so that the agent can pick it up and invoke the tool
            queue_file = Path(r"C:\Users\Curtis\.gemini\antigravity\brain\322df745-1c6f-47c0-96d2-c4ee82d0bc19\scratch\upload_queue.json")
            queue_data = {
                "file_path": str(video_file),
                "title": metadata["title"],
                "description": metadata["description"],
                "tags": metadata["tags"],
                "channel": metadata["channel"],
                "category_id": metadata["category_id"],
                "privacy_status": metadata["privacy_status"]
            }
            with open(queue_file, "w", encoding="utf-8") as f:
                json.dump(queue_data, f, indent=2)
                
            self.log(f"Video queued for upload. Agent will execute upload from queue_file.", "SUCCESS")

    def run(self):
        self.prompt_menu()
        self.parse_script()
        self.stage_folders()
        
        while True:
            print("\nOptions:")
            print("  [1] Scan downloads and rename/move assets (Phase 2B)")
            print("  [2] Generate DaVinci assembly script")
            print("  [3] Run Pre-Upload Quality Gate check & Queue upload")
            print("  [4] Exit")
            opt = input("Select an option [1-4]: ").strip()
            
            if opt == "1":
                self.rename_and_move_downloads()
            elif opt == "2":
                self.generate_davinci_script()
            elif opt == "3":
                metadata = self.run_quality_gate()
                self.upload_finished_video(metadata)
            elif opt == "4":
                self.log("Exiting. Good luck with your video production!", "SUCCESS")
                break

if __name__ == "__main__":
    orchestrator = YoutubeProductionOrchestrator()
    orchestrator.run()
