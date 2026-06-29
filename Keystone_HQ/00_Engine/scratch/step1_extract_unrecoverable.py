#!/usr/bin/env python3
"""
Step 1: Extract the 16 unrecoverable sources from Qdrant BEFORE wiping.
Uses query_points with source filter (not scroll) to bypass Gridstore corruption.
Saves each source as a .md file in Research_Archives/Recovered_From_Qdrant/
"""

import os
import sys
import json
from pathlib import Path
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORKSPACE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
OUTPUT_DIR = WORKSPACE / "Research_Archives" / "Recovered_From_Qdrant"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COLLECTION = "keystone_unified"
VECTOR_NAME = "fast-bge-small-en-v1.5"

# The 16 sources that only exist inside Qdrant
UNRECOVERABLE_SOURCES = [
    "deep_research/20260609_AGENT_ARCH_mandatory_skill_loading",
    "7.3_character_consistency",
    "7.2_prompt_engineering",
    "flow_avatar_characters_v1",
    "9.4_instagram_reels_requirements",
    "Keystone_Agent_Training_Vault.gdoc",
    "deep_research/ai_music_video_production_2026",
    "7.1_flow_reference",
    "2.3_review_strategy",
    "PHONETIC_BREAKDOWN_RULES_V1",
    "google-flow-veo-masterclass-2026-06-09-part1",
    "MUSIC_PROVEN_FLOW_PROMPTS_2026-06-09",
    "Strategic_Brand_Scaling_Blueprint.gdoc",
    "directory_listings_walkthrough_2026-06-07",
    "google-flow-veo-masterclass-2026-06-09-part2",
    "MUSIC_001_session_2026-06-09",
]


def extract_source(client, embed_model, source_id):
    """Extract all chunks for a given source_id using filtered vector search.
    We search with a generic query but filter strictly by source, then paginate
    by excluding already-seen point IDs."""
    
    # Use a generic embedding query (just to satisfy the API)
    # The source filter does the real work
    generic_query = "keystone brand content production"
    query_vec = list(embed_model.embed([generic_query]))[0].tolist()
    
    all_chunks = {}  # chunk_index -> document text
    seen_ids = set()
    max_iterations = 20  # Safety limit
    
    for iteration in range(max_iterations):
        try:
            # Build filter: must match source, must not be already-seen IDs
            must_conditions = [
                models.FieldCondition(
                    key="source",
                    match=models.MatchValue(value=source_id)
                )
            ]
            
            # We can't easily exclude by ID in Qdrant filter, so we'll use
            # a large limit and deduplicate in Python
            results = client.query_points(
                collection_name=COLLECTION,
                query=query_vec,
                using=VECTOR_NAME,
                query_filter=models.Filter(must=must_conditions),
                limit=100,  # Get all at once
                with_payload=True,
            )
            
            new_found = 0
            for point in results.points:
                pid = str(point.id)
                if pid not in seen_ids:
                    seen_ids.add(pid)
                    payload = point.payload or {}
                    chunk_idx = payload.get("chunk_index", len(all_chunks))
                    doc_text = payload.get("document", "")
                    if doc_text:
                        all_chunks[chunk_idx] = doc_text
                        new_found += 1
            
            if new_found == 0:
                break  # No new chunks found
                
        except Exception as e:
            print(f"    Error querying for {source_id}: {e}")
            break
    
    return all_chunks


def main():
    print("=" * 60)
    print("STEP 1: EXTRACTING UNRECOVERABLE SOURCES FROM QDRANT")
    print("=" * 60)
    
    client = QdrantClient(url="http://localhost:6333")
    embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    
    total_extracted = 0
    total_chunks = 0
    manifest = []
    
    for source_id in UNRECOVERABLE_SOURCES:
        print(f"\n  Extracting: {source_id}...")
        chunks = extract_source(client, embed_model, source_id)
        
        if not chunks:
            print(f"    WARNING: No chunks recovered for {source_id}")
            continue
        
        # Reassemble document in chunk order
        sorted_chunks = sorted(chunks.items(), key=lambda x: x[0])
        full_document = "\n\n".join([text for _, text in sorted_chunks])
        
        # Generate safe filename
        safe_name = source_id.replace("/", "_").replace("\\", "_").replace(" ", "_")
        if not safe_name.endswith(".md"):
            safe_name += ".md"
        
        # Add recovery header
        header = f"# Recovered from Qdrant Vector Database\n"
        header += f"# Original source_id: {source_id}\n"
        header += f"# Chunks recovered: {len(chunks)}\n"
        header += f"# Recovery date: 2026-06-14\n\n---\n\n"
        
        output_path = OUTPUT_DIR / safe_name
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header + full_document)
        
        print(f"    Saved {len(chunks)} chunks -> {output_path.name}")
        total_extracted += 1
        total_chunks += len(chunks)
        manifest.append({
            "source_id": source_id,
            "chunks": len(chunks),
            "filename": safe_name,
            "chars": len(full_document),
        })
    
    # Save manifest
    manifest_path = OUTPUT_DIR / "_recovery_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"EXTRACTION COMPLETE")
    print(f"  Sources recovered: {total_extracted} / {len(UNRECOVERABLE_SOURCES)}")
    print(f"  Total chunks saved: {total_chunks}")
    print(f"  Output directory: {OUTPUT_DIR}")
    print(f"  Manifest: {manifest_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
