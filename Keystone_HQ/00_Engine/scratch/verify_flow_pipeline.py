# Keystone Sovereign - Comprehensive Verification and Diagnostic Suite
# Runs simulated music tracks and content campaigns through the automated pipeline.

import os
import sys
import json
import shutil

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, "06_Music_Recomposition"))
sys.path.append(os.path.join(ROOT_DIR, "09_YouTube_Operations"))

try:
    import music_mcp
    from youtube_flow_agent import YouTubeFlowAgent
    from sovereign_coordinator import KeystoneSovereign
except ImportError as e:
    print(f"Import Error during setup: {e}")
    sys.exit(1)

# Helper function to print test sections
def print_section(title):
    print("\n" + "="*60)
    print(f" {title.upper()} ")
    print("="*60)

def run_diagnostics():
    print_section("starting diagnostic suite")
    
    # ── Test 1: Desktop Directories Check ────────────────────────────
    print("\n[Step 1] Verifying Desktop Directories...")
    desktop_dir = r"C:\Users\Curtis\Desktop"
    folders = {
        "New Songs": os.path.join(desktop_dir, "New Songs"),
        "sounds": os.path.join(desktop_dir, "sounds"),
        "ready for toolost": os.path.join(desktop_dir, "ready for toolost"),
        "musicmacth": os.path.join(desktop_dir, "musicmacth"),
        "compeleted albums": os.path.join(desktop_dir, "compeleted albums")
    }
    
    for name, path in folders.items():
        if os.path.exists(path):
            print(f"  [OK] Folder '{name}' exists at: {path}")
        else:
            print(f"  [INFO] Folder '{name}' missing. Attempting creation...")
            os.makedirs(path, exist_ok=True)
            print(f"  [OK] Folder '{name}' successfully created.")

    # ── Test 2: Simulated Music pipeline ────────────────────────────
    print_section("testing music recomposition pipeline")
    
    test_track_name = "KSTR-99999_mock_suno_track.wav"
    mock_src_path = os.path.join(folders["New Songs"], test_track_name)
    
    # Create an empty dummy file to simulate Suno WAV download
    with open(mock_src_path, "w") as f:
        f.write("MOCK_AUDIO_BYTES_DAT_SUN_YO")
    print(f"\n[Music 1] Created mock Sun Yo track in 'New Songs': {test_track_name}")
    
    # 1. Scan New Songs
    scan_res_raw = music_mcp.scan_desktop_new_songs()
    scan_res = json.loads(scan_res_raw)
    assert scan_res["status"] == "Success", "scan_desktop_new_songs failed"
    assert test_track_name in scan_res["files"], "Mock track not found in scan"
    print("  [OK] scan_desktop_new_songs() detected track successfully.")

    # 2. Curate Track (Approved -> Move to sounds)
    curate_res_raw = music_mcp.curate_desktop_song(test_track_name, take_song=True)
    curate_res = json.loads(curate_res_raw)
    assert curate_res["status"] == "Success", "curate_desktop_song failed"
    assert not os.path.exists(mock_src_path), "Audio track still in New Songs folder"
    sound_path = os.path.join(folders["sounds"], test_track_name)
    assert os.path.exists(sound_path), "Audio track not in sounds folder"
    print("  [OK] curate_desktop_song() moved track to 'sounds'.")

    # 3. Prepare for TooLost Package
    isrc = "CA-KST-26-99999"
    prep_res_raw = music_mcp.prepare_for_toolost(test_track_name, isrc_code=isrc)
    prep_res = json.loads(prep_res_raw)
    assert prep_res["status"] == "Success", "prepare_for_toolost failed"
    assert not os.path.exists(sound_path), "Audio track still in sounds folder"
    ready_audio = os.path.join(folders["ready for toolost"], test_track_name)
    ready_json = os.path.join(folders["ready for toolost"], f"TooLost_Package_{isrc}.json")
    assert os.path.exists(ready_audio), "Audio track not in ready for toolost folder"
    assert os.path.exists(ready_json), "TooLost JSON manifest missing"
    print("  [OK] prepare_for_toolost() compiled audio and metadata package in 'ready for toolost'.")

    # 4. Sync Musixmatch
    lyrics = "[Verse 1]\nSovereign builder on the Squamish site\nCellular reconstruction under early morning light"
    sync_res_raw = music_mcp.distribute_and_sync_musixmatch(isrc, lyrics)
    sync_res = json.loads(sync_res_raw)
    assert sync_res["status"] == "Success", "distribute_and_sync_musixmatch failed"
    assert not os.path.exists(ready_audio), "Audio track still in ready for toolost folder"
    
    mm_audio = os.path.join(folders["musicmacth"], test_track_name)
    mm_json = os.path.join(folders["musicmacth"], f"TooLost_Package_{isrc}.json")
    mm_lyrics = os.path.join(folders["musicmacth"], f"Musixmatch_Lyrics_{isrc}.txt")
    
    assert os.path.exists(mm_audio), "Audio track not in musicmacth folder"
    assert os.path.exists(mm_json), "TooLost JSON manifest not in musicmacth"
    assert os.path.exists(mm_lyrics), "Musixmatch lyrics text file missing"
    print("  [OK] distribute_and_sync_musixmatch() syndication and sync completed in 'musicmacth'.")

    # 5. Finalize Album
    final_res_raw = music_mcp.finalize_completed_album(test_track_name)
    final_res = json.loads(final_res_raw)
    assert final_res["status"] == "Success", "finalize_completed_album failed"
    assert not os.path.exists(mm_audio), "Audio track still in musicmacth folder"
    
    comp_audio = os.path.join(folders["compeleted albums"], test_track_name)
    comp_json = os.path.join(folders["compeleted albums"], f"TooLost_Package_{isrc}.json")
    comp_lyrics = os.path.join(folders["compeleted albums"], f"Musixmatch_Lyrics_{isrc}.txt")
    
    assert os.path.exists(comp_audio), "Audio track not archived in compeleted albums"
    assert os.path.exists(comp_json), "Metadata JSON not archived in compeleted albums"
    assert os.path.exists(comp_lyrics), "Lyrics file not archived in compeleted albums"
    print("  [OK] finalize_completed_album() archived all package elements into 'compeleted albums'.")

    # ── Test 3: YouTube Flow Scripting & Compliance ────────────────
    print_section("testing youtube & social scripting agent")
    
    agent = YouTubeFlowAgent()
    
    # 1. YMYL compliance scrub
    raw_ymyl_text = "Here is the peptide dosing protocol. We are stacking it to buy from our primary vendor."
    scrubbed = agent.scrub_ymyl(raw_ymyl_text)
    print(f"\n[YMYL Scrub]\n  Original: {raw_ymyl_text}\n  Scrubbed: {scrubbed}")
    assert "dosing" not in scrubbed.lower(), "dosing not scrubbed"
    assert "protocol" not in scrubbed.lower(), "protocol not scrubbed"
    assert "stacking" not in scrubbed.lower(), "stacking not scrubbed"
    assert "vendor" not in scrubbed.lower(), "vendor not scrubbed"
    print("  [OK] YMYL compliance scrubbing works perfectly.")

    # 2. ElevenLabs Phonetics replacements
    raw_phonetics_text = "Testing Tirzepatide, Retatrutide, and BPC-157 voice synthesis."
    phonetic_res = agent.convert_to_phonetics(raw_phonetics_text)
    print(f"\n[Phonetic Converter]\n  Original: {raw_phonetics_text}\n  Phonetic: {phonetic_res}")
    assert "Teer zeppa tide" in phonetic_res, "Tirzepatide phonetic conversion failed"
    assert "Retta true tide" in phonetic_res, "Retatrutide phonetic conversion failed"
    assert "B P C one fifty seven" in phonetic_res, "BPC-157 phonetic conversion failed"
    print("  [OK] ElevenLabs phonetic transcription rules verified.")

    # 3. Google Flow (Veo 3.1 & Imagen 3) Prompt Generation
    prompts = agent.generate_labs_flow_prompts("Wolverine Stack")
    print("\n[Google Flow Prompts]")
    for p in prompts:
        print(f"  Scene: {p['scene']}")
        print(f"    Imagen 3: {p['imagen_prompt']}")
        print(f"    Veo 3.1:  {p['veo_prompt']}")
        assert "--no watermark" in p['imagen_prompt'], "Standard negative string missing from Imagen prompt"
        assert "slow dolly-in" in p['veo_prompt'] or "rack focus" in p['veo_prompt'] or "tracking shot" in p['veo_prompt'], "Veo prompt lacking motion-only guidelines"
    print("  [OK] Imagen 3 and Veo 3.1 static-to-motion guidelines are 100% compliant.")

    # 4. Campaign compiling
    print("\n[Campaign Compilation]")
    compile_msg = agent.compile_campaign("Wolverine Stack")
    print(f"  {compile_msg}")
    topic_slug = "wolverine_stack"
    script_file = os.path.join(ROOT_DIR, "09_YouTube_Operations", "Scripts_Approved", f"{topic_slug}_script.txt")
    meta_file = os.path.join(ROOT_DIR, "09_YouTube_Operations", "Metadata_Drafts", f"{topic_slug}_metadata.json")
    assert os.path.exists(script_file), "Approved script file not generated"
    assert os.path.exists(meta_file), "Metadata JSON file not generated"
    print("  [OK] Social campaign written to disk successfully.")

    # ── Test 4: Sovereign Coordinator & Shared State ───────────────
    print_section("testing sovereign coordinator & shared state")
    
    coordinator = KeystoneSovereign()
    
    # 1. Trigger YouTube campaign through parent
    print("\n[Coordinator Campaign Trigger]")
    coord_campaign_res = coordinator.trigger_youtube_campaign("Wolverine Stack")
    print(f"  Result: {coord_campaign_res}")
    
    # Check jobs list in state
    jobs = coordinator.state["subagent_jobs"]["youtube_flow_agent"]
    assert len(jobs) > 0, "No youtube_flow_agent jobs queued in coordinator"
    latest_job = jobs[-1]
    assert latest_job["status"] == "Completed", "Job did not transition to Completed"
    print("  [OK] Parent coordinator successfully delegated and recorded task execution.")

    # 2. Desktop music monitoring
    print("\n[Coordinator Music Monitor]")
    coordinator.monitor_desktop_music()
    status = coordinator.state["music_pipeline_status"]
    assert "compeleted albums" in status, "compeleted albums missing from pipeline status"
    assert test_track_name in status["compeleted albums"]["files"], "Archived test file not recorded in state"
    print("  [OK] monitor_desktop_music() successfully refreshed folder states in shared json.")

    # ── Cleanup Mock Files ──────────────────────────────────────────
    print_section("cleaning up mock files")
    for file_to_del in [comp_audio, comp_json, comp_lyrics]:
        if os.path.exists(file_to_del):
            os.remove(file_to_del)
            print(f"  Cleaned up archived test file: {os.path.basename(file_to_del)}")
            
    print("\n" + "="*60)
    print(" DIAGNOSTIC SUITE COMPLETED SUCCESSFULLY: ALL CHECKS PASSED ")
    print("="*60 + "\n")

if __name__ == "__main__":
    run_diagnostics()
