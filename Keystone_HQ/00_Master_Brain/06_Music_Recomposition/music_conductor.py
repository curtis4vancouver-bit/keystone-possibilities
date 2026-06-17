#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Keystone Recomposition — Music & Lyrics Conductor CLI
Automates track curation, story-driven lyric generation, and queue management.
"""

import os
import sys
import json
import shutil
import re
import random
from datetime import datetime

# Force UTF-8 encoding
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Root and Workspace Paths
ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
MUSIC_DIR = os.path.join(ROOT_DIR, "06_Music_Recomposition")
QUEUE_FILE = os.path.join(MUSIC_DIR, "MUSIC_PRODUCTION_QUEUE.md")

# Physical Desktop Paths
DESKTOP_DIR = r"C:\Users\Curtis\Desktop"
NEW_SONGS_DIR = os.path.join(DESKTOP_DIR, "New Songs")
SOUNDS_DIR = os.path.join(DESKTOP_DIR, "sounds")
REJECTED_DIR = os.path.join(SOUNDS_DIR, "rejected")
READY_FOR_TOOLOST_DIR = os.path.join(DESKTOP_DIR, "ready for toolost")
MUSICMATCH_DIR = os.path.join(DESKTOP_DIR, "musicmacth")
COMPLETED_ALBUMS_DIR = os.path.join(DESKTOP_DIR, "compeleted albums")

# Ensure all physical directories exist
for folder in [NEW_SONGS_DIR, SOUNDS_DIR, REJECTED_DIR, READY_FOR_TOOLOST_DIR, MUSICMATCH_DIR, COMPLETED_ALBUMS_DIR]:
    os.makedirs(folder, exist_ok=True)

# Try to initialize Vertex AI client
genai_client = None
try:
    key_path = os.path.join(ROOT_DIR, "scratch", "gcs_key.json")
    if os.path.exists(key_path):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
        from google import genai
        genai_client = genai.Client(vertexai=True, project="semiotic-ion-458504-e9", location="us-central1")
        print("[Conductor] Vertex AI Client initialized successfully using gcs_key.json.")
    else:
        print("[Conductor] Warning: scratch/gcs_key.json not found. Lyrics generation will use mock fallback.")
except Exception as e:
    print(f"[Conductor] Error initializing GenAI client: {e}. Lyrics generation will use mock fallback.")


def generate_lyrics(track_title, album_name):
    """Generates story-driven, desaturated Deep House lyrics using Vertex AI."""
    if not genai_client:
        return get_mock_lyrics(track_title, album_name)

    # Determine specific theme based on album name
    album_lower = album_name.lower()
    language = "English"
    theme_prompt = ""

    if "legado" in album_lower:
        language = "Spanish"
        theme_prompt = "Spanish-language deep house. Poetic Spanish lyrics about legacy, building foundations, iron, dawn, and building something permanent. (Target Latin American markets)."
    elif "domani" in album_lower or "l'architettura" in album_lower:
        language = "Italian"
        theme_prompt = "Italian-language deep house. Mediterranean construction/architectural poetry."
    elif "cadence" in album_lower or "recovery" in album_lower:
        theme_prompt = "Downtempo chill house. Focus on recovery, rest days, meditation, ice bath, cold plunge, breathing, tension release, and cellular rebuild."
    elif "ascent" in album_lower:
        theme_prompt = "Epic progressive deep house. Peak performance, summit metaphors, ultimate transformation, physical drive, breaking records, and base camp to peak journey."
    elif "flow state" in album_lower:
        theme_prompt = "Flow-state and productivity deep house. Focus, neural pathways, building rhythm, discipline, repetition, and steady momentum."
    else:
        # Default / deep house 3 / general Recomposition
        theme_prompt = "Motivational deep house. Ingest themes of heavy civil construction/transformation, concrete foundations in the Sea-to-Sky mist, hypertrophy, sarcopenia defense, 200g protein floor, tracking biomarkers, and morning momentum."

    prompt = f"""You are the Music Brand Lyricist for Wayne Stevenson's Keystone Recomposition brand.
Your goal is to write lyrics for a Melodic Deep House track titled "{track_title}" from the album "{album_name}".

Language: {language}
Theme Details: {theme_prompt}

Guidelines:
- Moody, desaturated, minimalist, organic architectural aesthetic.
- Avoid generic EDM pop clichés (no "dance all night", "party in the club", etc.).
- Structure the lyrics with clear markers like [Verse], [Drop], [Chorus], [Outro] as plain text.
- Keep vocal lines short and repetitive, suitable for vocal chops or sparse spoken-word hooks over a steady 124 BPM deep house beat.
- Incorporate concrete/brutalist construction elements and biohacking/recomposition themes.
- Provide ONLY the lyrics sheet without conversational text.
"""

    try:
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[Conductor] Vertex AI API Error: {e}. Falling back to mock lyrics.")
        return get_mock_lyrics(track_title, album_name)


def get_mock_lyrics(track_title, album_name):
    """Fallback mock lyrics generator when Vertex AI is offline."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""[Style: Deep House, Melodic, 124 BPM]
[Album: {album_name}]
[Track: {track_title}]
[Generated: {timestamp} (Fallback Mode)]

[Verse 1]
Concrete foundations in the Sea-to-Sky mist,
Cellular rebuilding, a protocol checklist.
Raw infrastructure, the heavy load we bear,
Recomping the body, breathing cold mountain air.

[Chorus]
We build the foundation, we scale through the stone,
An elite physical engine, carving out our own.
Hold the line, feel the weight,
Discipline frequency, we build our fate.

[Outro]
Steady momentum, rise from the clay.
Keystone recomposition... today.
"""


def scan_desktop_new_songs():
    """Scans Desktop New Songs folder and returns a list of albums and their audio files."""
    valid_extensions = ('.wav', '.mp3', '.m4a', '.flac')
    albums = {}
    
    if not os.path.exists(NEW_SONGS_DIR):
        return {}
        
    for root, dirs, filenames in os.walk(NEW_SONGS_DIR):
        for f in sorted(filenames):
            if f.lower().endswith(valid_extensions):
                # Relative path from NEW_SONGS_DIR
                rel_path = os.path.relpath(os.path.join(root, f), NEW_SONGS_DIR)
                album_name = os.path.dirname(rel_path)
                if not album_name:
                    album_name = "(root)"
                albums.setdefault(album_name, []).append(rel_path)
    return albums


def clean_track_title(filename):
    """Cleans a track filename to a pretty title."""
    # Remove extension
    base, _ = os.path.splitext(os.path.basename(filename))
    # Remove prefix like "Track 01_" or "Track 1 -"
    clean = re.sub(r'^Track\s*\d+[\s_-]*', '', base, flags=re.IGNORECASE)
    # Replace underscores and dashes with spaces
    clean = clean.replace('_', ' ').replace('-', ' ')
    # Clean double spaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    # Title-case
    return clean.title()


def update_queue_file(album_id, track_number, clean_title, status):
    """Updates the status of a track under a specific album in MUSIC_PRODUCTION_QUEUE.md."""
    if not os.path.exists(QUEUE_FILE):
        print(f"[Conductor] Error: Queue file not found at {QUEUE_FILE}")
        return False
        
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    updated = False
    new_lines = []
    in_target_album = False
    
    # Header format: "### 1. deep house 3 (13 tracks)"
    album_header_pattern = re.compile(rf'^###\s*{album_id}\.\s*(.*)')
    # Track row format: "| 1 | Track 01_ SQUAMISH MIST | Awaiting curation |"
    track_row_pattern = re.compile(rf'^\|\s*{track_number}\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|')
    
    for line in lines:
        album_match = album_header_pattern.match(line)
        if album_match:
            in_target_album = True
        elif line.startswith('###') and in_target_album:
            in_target_album = False
            
        if in_target_album:
            track_match = track_row_pattern.match(line)
            if track_match:
                old_track_text = track_match.group(1).strip()
                
                # Keep prefix formatting (e.g. "Track 01_ ")
                prefix_match = re.match(r'^(Track\s*\d+[\s_-]*)(.*)', old_track_text)
                prefix = f"Track {track_number:02d}_ "
                if prefix_match:
                    prefix = prefix_match.group(1)
                
                new_track_text = f"{prefix}{clean_title.upper()}"
                line = f"| {track_number} | {new_track_text} | {status} |\n"
                updated = True
                in_target_album = False  # Done updating this track
                
        new_lines.append(line)
        
    if updated:
        with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False


def run_conductor():
    """Main Conductor CLI execution loop."""
    print("=" * 60)
    print("      🎵 KEYSTONE RECOMPOSITION — MUSIC & LYRICS CONDUCTOR 🎵")
    print("=" * 60)
    
    # Step 1: Scan Desktop
    albums = scan_desktop_new_songs()
    if not albums:
        print(f"[Conductor] No albums or audio tracks found in: {NEW_SONGS_DIR}")
        print("Please place Suno generated albums in subdirectories there.")
        sys.exit(0)
        
    # Map index to album names (excluding root if empty or handle it)
    album_keys = sorted([k for k in albums.keys() if k != "(root)"])
    if "(root)" in albums:
        album_keys.append("(root)")
        
    print(f"\nDiscovered {len(album_keys)} album folder(s) in 'New Songs':")
    for idx, name in enumerate(album_keys, 1):
        print(f"  {idx}. {name} ({len(albums[name])} track(s))")
        
    try:
        choice = input("\nSelect album number to curate (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            sys.exit(0)
        album_idx = int(choice) - 1
        if album_idx < 0 or album_idx >= len(album_keys):
            print("Invalid selection.")
            sys.exit(1)
    except ValueError:
        print("Invalid selection.")
        sys.exit(1)
        
    selected_album = album_keys[album_idx]
    tracks = albums[selected_album]
    
    # Try to map selected album to its ID in MUSIC_PRODUCTION_QUEUE.md
    album_id = 1
    if "flow state" in selected_album.lower():
        album_id = 2
    elif "legado" in selected_album.lower():
        album_id = 3
    elif "cadence" in selected_album.lower():
        album_id = 4
    elif "ascent" in selected_album.lower():
        album_id = 5
        
    print(f"\nStarting Curation for Album: {selected_album} (Mapped Queue ID: {album_id})")
    print("-" * 60)
    
    for idx, track_rel_path in enumerate(tracks, 1):
        src_track_path = os.path.join(NEW_SONGS_DIR, track_rel_path)
        filename = os.path.basename(track_rel_path)
        default_clean_title = clean_track_title(filename)
        
        print(f"\n[{idx}/{len(tracks)}] Processing file: {filename}")
        print(f"Suggested Title: {default_clean_title}")
        
        # Action prompt
        action = ""
        while action not in ['k', 'r', 's', 'q']:
            action = input("Action: [k] Keep, [r] Reject, [s] Skip, [q] Quit: ").strip().lower()
            
        if action == 'q':
            print("\nExiting Conductor loop.")
            break
        elif action == 's':
            print("Skipped.")
            continue
        elif action == 'r':
            # Move to rejected folder
            dest_dir = os.path.join(REJECTED_DIR, selected_album)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)
            shutil.move(src_track_path, dest_path)
            print(f"Rejected. Moved to {dest_path}")
            
            # Sync Queue status
            update_queue_file(album_id, idx, default_clean_title, "Rejected")
            continue
            
        # Action is KEEP ('k')
        custom_title = input(f"Enter clean track title [default: {default_clean_title}]: ").strip()
        final_title = custom_title if custom_title else default_clean_title
        
        # 1. Generate ISRC code
        unique_id = abs(hash(filename + str(random.random()))) % 100000
        isrc_code = f"CA-KST-26-{unique_id:05d}"
        print(f"Generated ISRC: {isrc_code}")
        
        # 2. Call Lyric Generator
        print("Generating desaturated lyrics from Vertex AI...")
        lyrics = generate_lyrics(final_title, selected_album)
        print("\n--- Lyrics Preview ---")
        print("\n".join(lyrics.split("\n")[:10]) + "\n...")
        print("----------------------")
        
        # 3. Create TooLost Package JSON
        meta_package = {
            "title": final_title,
            "artist": "Keystone Recomposition",
            "isrc": isrc_code,
            "genre": "Dance/Electronic",
            "subgenre": "Deep House",
            "tempo_bpm": 124,
            "distribution_platforms": ["Spotify", "Apple Music", "Amazon Music", "Beatport"],
            "release_date": datetime.now().strftime("%Y-%m-%d"),
            "audio_file": f"{selected_album}/{final_title}.wav",
            "artwork_status": "Default Keystone Logo Linked"
        }
        
        # 4. Save files to final targets
        # TooLost Metadata goes in 'ready for toolost'
        dest_meta_dir = os.path.join(READY_FOR_TOOLOST_DIR, selected_album)
        os.makedirs(dest_meta_dir, exist_ok=True)
        dest_meta_file = os.path.join(dest_meta_dir, f"TooLost_Package_{isrc_code}.json")
        with open(dest_meta_file, "w", encoding="utf-8") as f:
            json.dump(meta_package, f, indent=2)
            
        # Move audio file to 'sounds' directory
        dest_audio_dir = os.path.join(SOUNDS_DIR, selected_album)
        os.makedirs(dest_audio_dir, exist_ok=True)
        dest_audio_file = os.path.join(dest_audio_dir, f"{final_title}.wav")
        shutil.move(src_track_path, dest_audio_file)
        
        # Save Musixmatch lyrics sheet to 'musicmacth'
        dest_lyrics_dir = os.path.join(MUSICMATCH_DIR, selected_album)
        os.makedirs(dest_lyrics_dir, exist_ok=True)
        dest_lyrics_file = os.path.join(dest_lyrics_dir, f"Musixmatch_Lyrics_{isrc_code}.txt")
        with open(dest_lyrics_file, "w", encoding="utf-8") as f:
            f.write(lyrics)
            
        # 5. Move copies of metadata and audio to musicmatch to finish the full sync
        dest_mm_meta = os.path.join(dest_lyrics_dir, f"TooLost_Package_{isrc_code}.json")
        dest_mm_audio = os.path.join(dest_lyrics_dir, f"{final_title}.wav")
        shutil.copy2(dest_meta_file, dest_mm_meta)
        shutil.copy2(dest_audio_file, dest_mm_audio)
        
        # 6. Update Queue file
        success = update_queue_file(album_id, idx, final_title, "Packaged")
        if success:
            print(f"Successfully curated and packaged track {idx}. Updated MUSIC_PRODUCTION_QUEUE.md")
        else:
            print(f"Warning: Failed to update queue file for track {idx}")
            
    print("\nCuration session complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_conductor()
