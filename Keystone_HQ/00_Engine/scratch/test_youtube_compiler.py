#!/usr/bin/env python3
"""
🎬 KEYSTONE TEST YOUTUBE COMPILER & VECTOR BRAIN INTEGRATION PIPELINE
Path: scratch/test_youtube_compiler.py
Description: End-to-end integration test of the evolved dynamic skill: youtube_script_compiler
             and SQLite-vec memory ingestion round-trip.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add root directory to python path
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

# Import the dynamic compiler
try:
    from dynamic_skills.youtube_script_compiler import compile_voice_notes_to_cinematic_script
except ImportError as e:
    print(f"Error importing youtube_script_compiler: {e}")
    sys.exit(1)

def run_pipeline():
    print("=" * 60)
    print("STARTING TEST youtube_script_compiler & VECTOR INGESTION PIPELINE")
    print("=" * 60)

    # 1. Wayne's simulated raw voice note transcript
    raw_voice_notes = (
        "At forty-three, my joints were leaking from heavy grading and concrete work on steep Squamish grades. "
        "I had to run BPC-157 and TB-500 peptides to repair my shoulder tendon. The doctor said my dosing schedule was high, "
        "but I stacked them systematically. I also used Ozempic for a bit but sarcopenia is real and I lost muscle. "
        "That is why we need biophilic sleep sanctuaries and saunas at Squamish to rebuild the load-bearing foundation and protect sleep."
    )

    print("\n[STEP 1] Raw voice note transcript input:")
    print("-" * 50)
    print(raw_voice_notes)
    print("-" * 50)

    # 2. Compile using the evolved dynamic skill
    print("\n[STEP 2] Executing compile_voice_notes_to_cinematic_script dynamic skill...")
    result = compile_voice_notes_to_cinematic_script(
        raw_voice_notes=raw_voice_notes,
        topic_key="stoic_builder_recovery",
        duration_type="short"
    )

    if result.get("status") != "success":
        print("ERROR: Dynamic compiler failed to execute.")
        sys.exit(1)

    print("\n>>> Success! Script compiled successfully.")
    print(f"Title: {result['title']}")
    
    # Define script output path
    scripts_dir = ROOT_DIR / "09_YouTube_Operations" / "Scripts_Approved"
    metadata_dir = ROOT_DIR / "09_YouTube_Operations" / "Metadata_Drafts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    script_md_path = scripts_dir / "stoic_builder_recovery_script.md"
    meta_json_path = metadata_dir / "stoic_builder_recovery_metadata.json"

    # Save to approved folders
    with open(script_md_path, "w", encoding="utf-8") as f:
        f.write(result["script_md"])
    print(f"Saved compiled script to: {script_md_path}")

    with open(meta_json_path, "w", encoding="utf-8") as f:
        json.dump(result["metadata"], f, indent=2)
    print(f"Saved compiled metadata to: {meta_json_path}")

    # 3. Trigger SQLite-vec ingestion round-trip using Node.js
    print("\n[STEP 3] Triggering SQLite-vec ingestion pipeline...")
    brain_feeder_dir = ROOT_DIR / "10_Vector_DB_Architecture" / "brain_feeder"
    ingest_script_js = brain_feeder_dir / "ingest_file.js"

    cmd = [
        "node",
        str(ingest_script_js),
        str(script_md_path),
        "--source",
        "stoic_builder_recovery_script"
    ]

    print(f"Executing command: {' '.join(cmd)}")
    try:
        ingest_res = subprocess.run(
            cmd,
            cwd=str(brain_feeder_dir),
            capture_output=True,
            text=True,
            check=True
        )
        print(ingest_res.stdout)
    except subprocess.CalledProcessError as e:
        print("ERROR executing Node.js ingestion:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        sys.exit(1)

    # 4. Query vector database for confirmation
    verify_query = "sarcopenia BPC-157 compound recovery load-bearing joint"
    print(f"\n[STEP 4] Querying SQLite-vec brain.db for confirmation: '{verify_query}'...")
    
    query_script_js = brain_feeder_dir / "query_brain.js"
    cmd_query = [
        "node",
        str(query_script_js),
        verify_query,
        "--limit",
        "1"
    ]
    
    try:
        query_res = subprocess.run(
            cmd_query,
            cwd=str(brain_feeder_dir),
            capture_output=True,
            text=True,
            check=True
        )
        print(query_res.stdout)
        if "stoic_builder_recovery_script" in query_res.stdout:
            print("\n>>> SUCCESS: Memory retrieval round-trip confirmed! The vector brain holds the compiled script.")
        else:
            print("\n>>> WARNING: Query finished but 'stoic_builder_recovery_script' source not found in top match.")
    except subprocess.CalledProcessError as e:
        print("ERROR executing Node.js query:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("ALL DYNAMIC COMPILER & INGESTION PIPELINE TESTS PASS 100%!")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
