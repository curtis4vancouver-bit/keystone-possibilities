"""
Direct Clone Ingestion — Mirrors Main brain data into Clone (port 7333).
Simpler and more reliable than snapshot transfers.
"""
import os
from qdrant_client import QdrantClient

# Connect to CLONE brain — port 7333
client = QdrantClient(url="http://localhost:7333")
client.set_model("BAAI/bge-small-en-v1.5")

BASE_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def get_namespace(filepath):
    rel_path = os.path.relpath(filepath, BASE_DIR)
    parts = rel_path.split(os.sep)
    if len(parts) > 1:
        folder = parts[0].lower()
        if "possibilities" in folder:
            return "possibilities"
        elif "music" in folder:
            return "music"
        elif "protocol" in folder:
            return "protocol"
        elif "health" in folder:
            return "protocol"
        elif "master" in folder:
            return "master"
    return "general"

def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

collections_data = {}

print("Scanning Master Brain files...")
for root, dirs, files in os.walk(BASE_DIR):
    if "scripts" in root or "mcp" in root.lower() or "venv" in root:
        continue
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            namespace = get_namespace(filepath)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue
            chunks = chunk_text(content)
            if namespace not in collections_data:
                collections_data[namespace] = {"docs": [], "metadata": []}
            for i, chunk in enumerate(chunks):
                collections_data[namespace]["docs"].append(chunk)
                collections_data[namespace]["metadata"].append({
                    "source": file,
                    "filepath": filepath,
                    "chunk_index": i
                })

# Delete existing empty collections on Clone, then re-create and ingest
for namespace, data in collections_data.items():
    print(f"Ingesting {len(data['docs'])} chunks into Clone namespace: {namespace}...")
    
    # Wipe and recreate
    if client.collection_exists(collection_name=namespace):
        client.delete_collection(collection_name=namespace)
    
    client.create_collection(
        collection_name=namespace,
        vectors_config=client.get_fastembed_vector_params()
    )
    
    batch_size = 100
    docs = data["docs"]
    metadata = data["metadata"]
    
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i+batch_size]
        batch_meta = metadata[i:i+batch_size]
        client.add(
            collection_name=namespace,
            documents=batch_docs,
            metadata=batch_meta
        )
        print(f"  {i + len(batch_docs)} / {len(docs)}")

print("Clone ingestion complete!")
