#!/usr/bin/env python3
"""
Ingest Obsidian Markdown Files to Qdrant Unified Collection.
Reads markdown files in the workspace (excluding excluded directories),
chunks them, and inserts them into the 'keystone_unified' collection
with the named vector 'fast-bge-small-en-v1.5' and 'tenant_id' payload mapping.
Stores rich metadata including file path for hierarchical scoping.
"""

import os
import sys
import uuid
import datetime
from pathlib import Path
from typing import Dict, List, Any

# Ensure we print UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Exclude directories
EXCLUDE_DIRS = {
    ".git", ".obsidian", ".system_generated", "node_modules",
    "scratch", "__pycache__", "app", "davinci-resolve-mcp", "deprecated_scripts"
}

# Namespace mapping by parent directory
NAMESPACE_MAP = {
    "02_keystone_possibilities": "possibilities",
    "02_keystone_possibilities_construction": "possibilities",
    "06_music_recomposition": "music",
    "07_health_protocols": "protocol_brand",
    "09_youtube_operations": "content_pipeline",
    "content_production": "content_pipeline",
    "agent_fleet": "general",
    "master_docs": "master",
    "brand_constitution": "master",
    "research_archives": "general",
    "local_seo": "local_seo",
    "webmaster": "webmaster"
}

DEFAULT_NAMESPACE = "general"
UNIFIED_COLLECTION = "keystone_unified"
VECTOR_NAME = "fast-bge-small-en-v1.5"

try:
    from qdrant_client import QdrantClient, models
    from fastembed import TextEmbedding
    qdrant_available = True
except ImportError:
    qdrant_available = False


def chunk_markdown(content: str, max_chunk_size: int = 1500) -> List[str]:
    """Markdown-aware chunking based on headers and size."""
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in content.split('\n'):
        # Start new chunk on headers if current chunk has content
        if line.startswith('#') and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = len(line)
        # Split if size exceeds max
        elif current_size + len(line) > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_size = len(line)
        else:
            current_chunk.append(line)
            current_size += len(line)
            
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
        
    return [c.strip() for c in chunks if c.strip()]


def get_namespace_for_path(rel_path: Path) -> str:
    """Determine Qdrant namespace (tenant_id) based on file path."""
    parts = rel_path.parts
    if not parts:
        return DEFAULT_NAMESPACE
        
    # Check top-level directory name
    top_dir = parts[0].lower()
    
    # Direct folder name match
    if top_dir in NAMESPACE_MAP:
        return NAMESPACE_MAP[top_dir]
        
    # Sub-folder search
    for part in parts:
        part_lower = part.lower()
        if "seo" in part_lower:
            return "local_seo"
        if "webmaster" in part_lower:
            return "webmaster"
        if "music" in part_lower:
            return "music"
        if "protocol" in part_lower:
            return "protocol_brand"
        if "possibilit" in part_lower:
            return "possibilities"
        if "youtube" in part_lower or "pipeline" in part_lower:
            return "content_pipeline"
            
    return DEFAULT_NAMESPACE


def scan_and_ingest():
    if not qdrant_available:
        print("ERROR: qdrant-client or fastembed not installed. Please run: pip install qdrant-client fastembed")
        return
        
    client = QdrantClient(url="http://localhost:6333")
    embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
    
    # Verify connection
    try:
        if not client.collection_exists(collection_name=UNIFIED_COLLECTION):
            print(f"ERROR: Unified collection '{UNIFIED_COLLECTION}' does not exist.")
            return
        print(f"Connected to Qdrant. Unified collection '{UNIFIED_COLLECTION}' found.")
    except Exception as e:
        print(f"ERROR: Cannot connect to Qdrant at http://localhost:6333: {e}")
        return

    print("Scanning markdown files...")
    md_files = []
    for path in PROJECT_ROOT.rglob("*.md"):
        rel_parts = path.relative_to(PROJECT_ROOT).parts
        if any(part in EXCLUDE_DIRS for part in rel_parts):
            continue
        md_files.append(path)
        
    print(f"Found {len(md_files)} markdown files in Obsidian vault.")
    
    total_ingested = 0
    total_chunks = 0
    
    for filepath in md_files:
        rel_path = filepath.relative_to(PROJECT_ROOT)
        namespace = get_namespace_for_path(rel_path)
        
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception as e:
            print(f"Skipping {rel_path} due to read error: {e}")
            continue
            
        chunks = chunk_markdown(content)
        if not chunks:
            continue
            
        now_iso = datetime.datetime.now().isoformat() + "Z"
        
        # Generate embeddings
        try:
            embeddings = list(embed_model.embed(chunks))
        except Exception as e:
            print(f"Failed to generate embeddings for {rel_path}: {e}")
            continue
            
        points = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Deterministic UUID: same source + chunk_index = same point_id
            # Re-runs safely overwrite instead of creating duplicates
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{rel_path.as_posix()}:{idx}"))
            vec = embedding.tolist()
            
            # Form payloads strictly adhering to Unified collection schema
            payload = {
                "tenant_id": namespace,         # Multi-tenancy tenant key
                "source": rel_path.as_posix(),  # Attributed source
                "chunk_index": idx,
                "created_at": now_iso,
                "document": chunk,              # Text content field
                
                # Metadata for hierarchical scoping
                "path": rel_path.as_posix(),
                "parent_dir": filepath.parent.name,
                "filename": filepath.name,
                "type": "obsidian_note",
                "EEAT_tag": "Original Research" if "research" in str(rel_path).lower() else "Analysis",
                "topic": filepath.stem.replace("_", " ").replace("-", " ")
            }
            
            points.append(
                models.PointStruct(
                    id=point_id,
                    payload=payload,
                    vector={VECTOR_NAME: vec}
                )
            )
            
        try:
            client.upsert(collection_name=UNIFIED_COLLECTION, points=points)
            total_chunks += len(points)
            total_ingested += 1
            print(f"✓ Ingested '{rel_path.as_posix()}' into '{namespace}' namespace of '{UNIFIED_COLLECTION}' ({len(points)} chunks)")
        except Exception as e:
            print(f"✗ Failed to ingest '{rel_path.as_posix()}': {e}")
            
    print(f"\nIngestion finished successfully.")
    print(f"  Files processed: {total_ingested}")
    print(f"  Total chunks/vectors added: {total_chunks}")


if __name__ == "__main__":
    scan_and_ingest()
