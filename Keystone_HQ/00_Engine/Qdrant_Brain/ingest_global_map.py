"""
Ingest the Global Tool Registry into ALL namespaces so every agent knows where the physical scripts are.
"""
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5")

GLOBAL_MAP = """
[CRITICAL SYSTEM UPDATE: MAY 28, 2026]
GLOBAL KEYSTONE INFRASTRUCTURE TOOL REGISTRY

The following tools have been successfully compiled and physically built into the local workspace. All Keystone Agents must use these physical paths when attempting to execute automated pipelines:

1. DAVINCI RESOLVE AUTOMATION SCRIPT
Path: C:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/video_builder.py
Purpose: Used by Protocol and Recomposition agents to automatically assemble AI video, ElevenLabs voice clones, and Melodic House music into a final rendered timeline.
Command Usage: python video_builder.py <video_file> <voiceover_file> <background_music> <output_timeline_name>

2. SELF-HEALING DIAGNOSTIC SERVER
Path: C:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/mcp_server.py
Purpose: If any command fails, send the error log to this FastAPI server (port 8642). It will use Gemini 3.5 Flash to automatically patch the script, write the fix to C:/Users/Curtis/.gemini/config/skills/healed_skills/, and execute the patch safely.

3. LOCAL SEO JSON-LD INJECTION
Path: C:/Users/Curtis/New folder/construction-website/possibilities-portal/src/app/layout.tsx
Purpose: The JSON-LD Schema (containing License #52603, YouTube links, and Spotify links) has already been permanently injected into the root layout of keystonepossibilities.ca. No further action is required by the Webmaster agent regarding the core E-E-A-T schema.
"""

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

chunks = chunk_text(GLOBAL_MAP)
metadata = [{"source": "system_global_map", "type": "infrastructure_registry"} for _ in chunks]

namespaces = ["master", "possibilities", "protocol", "music"]

for ns in namespaces:
    print(f"Ingesting into '{ns}' namespace...")
    # Ensure collection exists
    if not client.collection_exists(ns):
        client.create_collection(collection_name=ns, vectors_config=client.get_fastembed_vector_params())
    client.add(collection_name=ns, documents=chunks, metadata=metadata)

print("Done! Global Tool Registry broadcasted to all agents.")
