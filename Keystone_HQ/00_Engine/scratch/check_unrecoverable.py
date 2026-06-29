from qdrant_client import QdrantClient

def check_unrecoverable_content():
    """Check if the 16 'unrecoverable' sources actually contain meaningful unique data
    that doesn't exist elsewhere, or if they're just short identifiers referencing 
    content that's been superseded."""
    
    client = QdrantClient(url="http://localhost:6333")
    
    unrecoverable = [
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
    
    total_chunks = 0
    
    for source_id in unrecoverable:
        # Try to find this source in the healthy namespaces
        try:
            # Search by scrolling general namespace looking for this source
            res, _ = client.scroll(
                collection_name="keystone_unified",
                scroll_filter={
                    "must": [
                        {"key": "source", "match": {"value": source_id}}
                    ]
                },
                limit=100,
                with_payload=True,
                with_vectors=False
            )
            
            chunk_count = len(res)
            total_chunks += chunk_count
            
            if res:
                first_doc = res[0].payload.get("document", "")[:200]
                ns = res[0].payload.get("tenant_id", "?")
                print(f"\n--- {source_id} ({chunk_count} chunks, ns={ns}) ---")
                print(f"  Preview: {first_doc}...")
            else:
                print(f"\n--- {source_id} (0 chunks found via scroll) ---")
                
        except Exception as e:
            print(f"\n--- {source_id} (ERROR reading: {e}) ---")
    
    print(f"\n\nTotal chunks in unrecoverable sources: {total_chunks}")

if __name__ == "__main__":
    check_unrecoverable_content()
