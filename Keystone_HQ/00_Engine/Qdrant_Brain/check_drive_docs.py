"""
Ingest key Google Docs from G:\My Drive into the Main brain.
These are Wayne's master strategy documents that all agents should know about.
"""
import os
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")
client.set_model("BAAI/bge-small-en-v1.5")

DRIVE_PATH = r"G:\My Drive"

# Key docs to ingest (the .gdoc files are just pointers, look for actual content files)
key_docs = []
for f in os.listdir(DRIVE_PATH):
    if f.endswith(".gdoc") and "Keystone" in f:
        key_docs.append(f)

print(f"Found {len(key_docs)} Keystone Google Docs in Drive:")
for d in key_docs:
    print(f"  - {d}")

print("\nNote: .gdoc files are Google Docs shortcuts - they contain URLs, not content.")
print("To ingest their content, open them in Chrome and export as .md or .txt.")
print("Spark can do this automatically via its native Google Docs access.")
