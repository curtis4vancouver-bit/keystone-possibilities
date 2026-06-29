"""
Keystone Deep Research Ingestion Pipeline v2
=============================================
Ingests new Deep Research reports from Deep_Research_Results/ into the 
UNIFIED keystone_unified Qdrant collection with proper tenant_id payloads.
After ingestion, archives files to Research_Archives/.

FIXED: Now targets keystone_unified (not the old keystone_brain).
Uses fastembed + named vectors to match the unified collection schema.
"""
import os
import shutil
import datetime
import uuid
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding

# Define absolute paths
PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
DEEP_RESEARCH_RESULTS = os.path.join(PROJECT_ROOT, "Deep_Research_Results")
RESEARCH_ARCHIVES = os.path.join(PROJECT_ROOT, "Research_Archives")

# Qdrant config — must match keystone_brain_v2_mcp.py
COLLECTION_NAME = "keystone_unified"
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_NAME = "fast-bge-small-en-v1.5"

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def determine_tenant(filename):
    """Map filename patterns to tenant_id values matching keystone_unified schema."""
    fn = filename.lower()
    
    # Agent architecture & system optimization
    if any(k in fn for k in ["agent_arch", "sys_0", "mcp_", "qdrant", "context_", "instruction_",
                              "self-heal", "security_pattern", "observability", "overnight_auto",
                              "planning_and_reasoning", "future-proof", "knowledge_graph",
                              "multi-agent", "skill_system", "embedding_model", "episodic_memory"]):
        return "webmaster"  # System-level knowledge → webmaster tenant
    
    # Video production & DaVinci Resolve
    if any(k in fn for k in ["video_prod", "davinci", "resolve", "timeline", "render", "color_grad",
                              "subtitle", "caption", "thumbnail", "fusion", "elevenlabs", "omi_ai",
                              "google_flow"]):
        return "content_pipeline"
    
    # YouTube growth & channel management & video SEO
    if any(k in fn for k in ["youtube_growth", "youtube_algo", "youtube_short", "youtube_seo",
                              "youtube_data_api", "youtube_analytics", "youtube_community",
                              "youtube_competitor", "youtube_music_channel", "youtube_live",
                              "youtube_monetiz", "youtube_playlist", "youtube_ai-generated",
                              "youtube-to-website", "managing_multiple_youtube", "content_calendar",
                              "video_seo", "video_indexing", "search_console_optimization"]):
        return "content_pipeline"
    
    # SEO & local search
    if any(k in fn for k in ["seo", "local_seo", "knowledge_panel", "citation", "google_business",
                              "schema_markup", "structured_data", "serp", "backlink", "ranking"]):
        return "local_seo"
    
    # Website & WordPress
    if any(k in fn for k in ["website", "wordpress", "landing_page", "woocommerce", "shopify",
                              "web_performance", "cdn", "caching"]):
        return "webmaster"
    
    # Music & Spotify
    if any(k in fn for k in ["music", "spotify", "lyrics", "musicbrainz", "streaming",
                              "audio", "dj", "flow_prompt"]):
        return "music"
    
    # Protocol/health/wellness
    if any(k in fn for k in ["protocol", "peptide", "wellness", "health", "ghk", "longevity",
                              "retreat", "biohack"]):
        return "protocol_brand"
    
    return "webmaster"  # Default fallback

def main():
    print("====================================================")
    print("Keystone Brain: Deep Research Ingestion v2 (UNIFIED)")
    print("====================================================")
    
    os.makedirs(DEEP_RESEARCH_RESULTS, exist_ok=True)
    os.makedirs(RESEARCH_ARCHIVES, exist_ok=True)

    # Scan for md files
    files = [f for f in os.listdir(DEEP_RESEARCH_RESULTS) if f.endswith(".md")]
    
    if not files:
        print("No new research results found in Deep_Research_Results/.")
        return

    print(f"Found {len(files)} file(s) to ingest.")

    # Initialize
    client = QdrantClient(url="http://localhost:6333")
    embedder = TextEmbedding(model_name=EMBED_MODEL_NAME)

    total_chunks = 0
    
    for file_name in files:
        src_path = os.path.join(DEEP_RESEARCH_RESULTS, file_name)
        dest_path = os.path.join(RESEARCH_ARCHIVES, file_name)
        
        tenant_id = determine_tenant(file_name)
        source_name = os.path.splitext(file_name)[0]
        
        print(f"\nProcessing: {file_name} -> tenant: '{tenant_id}'")
        
        with open(src_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        chunks = chunk_text(content)
        print(f"  Chunked into {len(chunks)} fragments.")
        
        # Embed all chunks
        embeddings = list(embedder.embed(chunks))
        
        # Build points with proper schema
        points = []
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                payload={
                    "tenant_id": tenant_id,
                    "document": chunk,
                    "source": f"deep_research/{source_name}",
                    "filename": file_name,
                    "chunk_index": i,
                    "created_at": datetime.datetime.now().isoformat()
                },
                vector={VECTOR_NAME: emb.tolist()}
            )
            points.append(point)
        
        # Upsert in batches of 100
        for batch_start in range(0, len(points), 100):
            batch = points[batch_start:batch_start + 100]
            client.upsert(collection_name=COLLECTION_NAME, points=batch)
        
        total_chunks += len(chunks)
        print(f"  [OK] Uploaded {len(chunks)} vectors to {COLLECTION_NAME}")
        
        # Archive
        shutil.move(src_path, dest_path)
        print(f"  Archived to: {dest_path}")

    print(f"\n{'='*52}")
    print(f"COMPLETE: Ingested {total_chunks} chunks from {len(files)} files")
    print(f"Collection: {COLLECTION_NAME}")
    
    # Final count
    info = client.get_collection(COLLECTION_NAME)
    print(f"Total vectors in {COLLECTION_NAME}: {info.points_count}")

if __name__ == "__main__":
    main()
