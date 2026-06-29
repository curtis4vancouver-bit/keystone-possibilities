import sys
import os
import time
from pathlib import Path

brain_path = Path(__file__).parent.parent.parent / "00_Engine" / "Qdrant_Brain"
if str(brain_path) not in sys.path:
    sys.path.append(str(brain_path))

try:
    from keystone_brain_v2_mcp import search_master_brain, ingest_to_brain, list_brain_namespaces
    print("[+] Successfully imported Keystone Brain v2 MCP tools.", file=sys.stderr)
except Exception as e:
    print(f"[-] Failed to import brain MCP tools: {e}", file=sys.stderr)
    sys.exit(1)

def run_tests():
    print("=== STARTING BRAIN INFRASTRUCTURE VALIDATION ===")
    
    # Test 1: Namespace Listing
    print("\n--- Test 1: Namespace Listing ---")
    namespaces = list_brain_namespaces()
    print(namespaces)
    
    # Test 2: Ingesting Mock Episodic Memory
    print("\n--- Test 2: Ingesting Mock Episodic Memory ---")
    source_id = f"test_episodic_{int(time.time())}"
    content = "Test content detailing custom home civil engineering in Squamish Zone 5 targeting Step 3 requirements."
    ingest_res = ingest_to_brain(
        source_id=source_id,
        content=content,
        namespace="possibilities",
        memory_layer="episodic"
    )
    print(ingest_res)
    
    # Ingest a second document to trigger reranker (requires len(results) > 1)
    content2 = "Another test content for civil engineering and step code requirements."
    ingest_res2 = ingest_to_brain(
        source_id=source_id + "_2",
        content=content2,
        namespace="possibilities",
        memory_layer="episodic"
    )
    print(ingest_res2)
    
    # Test 3: Search and Rerank
    print("\n--- Test 3: Searching with Deep Reranking ---")
    search_res = search_master_brain(
        query="Squamish civil engineering step 3 requirements",
        namespace="possibilities",
        limit=3,
        memory_layer="episodic",
        deep_rerank=True
    )
    print(search_res)
    
    if "Rerank:" in search_res:
        print("\n[SUCCESS] Cross-encoder reranking is fully operational!")
    else:
        print("\n[WARNING] Reranking tag not found in search results. Check reranker.py setup.")
        
    print("\n=== VALIDATION TESTS COMPLETE ===")

if __name__ == "__main__":
    run_tests()
