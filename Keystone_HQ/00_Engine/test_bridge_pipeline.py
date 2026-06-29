"""
Keystone Vector Brain Integration Pipeline Test
================================================
Verifies the end-to-end integration loop between Python automation and the
local/remote Supabase/Google Cloud Vector Brain database.
"""

import sys
from pathlib import Path

# Add root directory to python path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from gemini_auto_runner import query_vector_brain, ingest_file_to_brain
except ImportError as e:
    print(f"Error importing gemini_auto_runner: {e}")
    sys.exit(1)


def run_test():
    print("=" * 60)
    print("STARTING END-TO-END PIPELINE DIAGNOSTIC")
    print("=" * 60)

    # 1. Verify Pre-Prompt Context Querying
    test_query = "What is the vault key for Squamish Peak?"
    print(f"\n[STEP 1] Testing vector search query: '{test_query}'...")
    
    brain_output = query_vector_brain(test_query, limit=1)
    
    if brain_output:
        print("\n>>> Success! Retrieved brain context:")
        print("-" * 50)
        print(brain_output.strip())
        print("-" * 50)
    else:
        print("\n>>> ERROR: Could not retrieve context from the Vector Brain.")
        sys.exit(1)

    # 2. Verify Pre-Prompt Injection formatting
    print("\n[STEP 2] Formatting simulated prompt injection...")
    prompt = "Write an on-site PM report describing how we used the vault key."
    
    if "VECTOR BRAIN PRIOR CONTEXT" in brain_output:
        injected_prompt = (
            f"{brain_output}\n\n"
            f"[INSTRUCTION]:\n"
            f"Using the relevant prior context above, please complete this deep research task:\n"
            f"{prompt}"
        )
        print("\n>>> Simulated Injected Prompt:")
        print("-" * 50)
        print(injected_prompt.strip()[:350] + "...\n[TRUNCATED FOR DISPLAY]")
        print("-" * 50)
    else:
        print("\n>>> ERROR: No prior context tags found in database search output.")
        sys.exit(1)

    # 3. Verify Post-Response Ingestion Round-Trip
    print("\n[STEP 3] Testing auto-ingestion pipeline round-trip...")
    test_file_path = SCRIPT_DIR / "scratch" / "test_pipeline_output.md"
    test_file_path.parent.mkdir(exist_ok=True)

    test_content = (
        "# Brand Awareness Campaign Sync\n"
        "Date: May 2026\n"
        "Campaign Code: BRAND-AWARENESS-2026-ACTIVE\n"
        "Mission: Standardize the luxury brand voice of Keystone construction and health protocols.\n"
    )

    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print(f"Created simulated research output at: {test_file_path}")

    # Trigger auto-ingestion
    source_name = "test_pipeline_round_trip_ingest"
    ingest_file_to_brain(test_file_path, source_name)

    # 4. Query the newly ingested data to confirm ingestion works
    verify_query = "What is the Campaign Code for brand awareness?"
    print(f"\n[STEP 4] Querying Vector Brain for newly ingested data: '{verify_query}'...")
    
    verify_output = query_vector_brain(verify_query, limit=1)
    
    if verify_output and "BRAND-AWARENESS-2026-ACTIVE" in verify_output:
        print("\n>>> Success! Round-trip fully verified!")
        print("-" * 50)
        print(verify_output.strip())
        print("-" * 50)
    else:
        print("\n>>> ERROR: Could not retrieve newly ingested data from Vector Brain.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("INTEGRATION PIPELINE PASSES 100% OF TESTS!")
    print("=" * 60)


if __name__ == "__main__":
    run_test()
