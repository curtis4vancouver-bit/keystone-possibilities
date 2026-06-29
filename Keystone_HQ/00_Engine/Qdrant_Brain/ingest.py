import os
import json
import uuid
from qdrant_client import QdrantClient

# Connect to the local Qdrant instance
client = QdrantClient(url="http://localhost:6333")

# We will use the built-in fastembed support in qdrant_client
client.set_model("BAAI/bge-small-en-v1.5")

BASE_DIR = r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"

def get_namespace(filepath):
    # Determine the namespace/collection based on the folder path
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

# Dictionary to hold documents per namespace
collections_data = {}

for root, dirs, files in os.walk(BASE_DIR):
    # Skip script and mcp directories
    if "scripts" in root or "mcp" in root.lower() or "venv" in root:
        continue
        
    for file in files:
        if file.endswith(".md"):
            filepath = os.path.join(root, file)
            namespace = get_namespace(filepath)
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
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

# Ingest into Qdrant
for namespace, data in collections_data.items():
    print(f"Creating collection and ingesting {len(data['docs'])} chunks into namespace: {namespace}...")
    
    # Check if collection exists, if not create it
    if not client.collection_exists(collection_name=namespace):
        client.create_collection(
            collection_name=namespace,
            vectors_config=client.get_fastembed_vector_params()
        )
        
    # Add documents in batches
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
        print(f"  Ingested {i + len(batch_docs)} / {len(docs)}")

print("Ingestion complete!")
