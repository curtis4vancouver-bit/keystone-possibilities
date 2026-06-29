"""
Keystone Hybrid Retrieval v2.0
================================
True hybrid search combining REAL Qdrant vector similarity with BM25 keyword
scoring and importance-weighted ranking.

v2.0 Upgrades over v1.0:
  - REAL vector search via Qdrant (replaces the fake keyword-based approximation)
  - Multi-namespace 'should' clause filtering for cross-brand queries
  - Deduplication between vector and keyword result sets
  - Enriched metadata extraction from Qdrant payloads
  - Confidence tiering (High/Medium/Low) on results

Scoring Formula (unchanged weights, now with real data):
  50% — Vector similarity (REAL cosine similarity from Qdrant HNSW index)
  30% — Keyword/FTS matching (BM25-style, same as v1.0)
  20% — Importance scoring (recency, access frequency, priority tags)

Usage:
  python hybrid_retrieval.py --query "Bill 44 ADU construction"
  python hybrid_retrieval.py --query "peptide protocols" --namespace protocol
  python hybrid_retrieval.py --query "thumbnail design" --top-k 10
  python hybrid_retrieval.py --query "tirzepatide titration" --cross-namespace master,protocol
"""
import os
import sys
import json
import re
import math
import argparse
import datetime
from collections import Counter
from typing import List, Optional, Dict, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ─── Qdrant & Embedding Initialization ─────────────────────────────────────
try:
    from qdrant_client import QdrantClient, models as qdrant_models
    _qdrant_client = QdrantClient(url="http://localhost:6333")
    _qdrant_client.set_model("BAAI/bge-small-en-v1.5")
    QDRANT_AVAILABLE = True
except Exception:
    _qdrant_client = None
    QDRANT_AVAILABLE = False

try:
    from fastembed import TextEmbedding
    _embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
except Exception:
    _embed_model = None

try:
    from sentence_transformers import CrossEncoder
    _cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    CROSS_ENCODER_AVAILABLE = True
except Exception:
    _cross_encoder = None
    CROSS_ENCODER_AVAILABLE = False

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MASTER_DOCS_DIR = os.path.join(PROJECT_ROOT, "Master_Docs")
BRAND_CONSTITUTION_DIR = os.path.join(PROJECT_ROOT, "Brand_Constitution")
LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
AGENT_FLEET_DIR = os.path.join(PROJECT_ROOT, "Agent_Fleet")

# All valid namespaces in the brain
VALID_NAMESPACES = [
    "general", "master", "possibilities", "protocol", "music",
    "webmaster", "self_healing", "research_scout", "legal_counsel",
    "tax_strategist", "site_superintendent", "keystone_learnings",
    "keystone_website", "local_seo", "recomposition_brand_push",
    "possibilities_leads", "operational_playbooks",
]


# ─── Qdrant Vector Search (REAL) ─────────────────────────────────────────

def qdrant_vector_search(
    query: str,
    namespace: Optional[str] = None,
    cross_namespaces: Optional[List[str]] = None,
    top_k: int = 10,
    scope: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Execute REAL vector similarity search against the unified Qdrant collection.

    Supports:
      - Single namespace filtering (tenant_id must match namespace)
      - Multi-namespace cross-brand queries (tenant_id matches any in cross_namespaces)
      - Hierarchical path scoping (Qdrant payload matching)
    """
    global _embed_model
    if not QDRANT_AVAILABLE or _qdrant_client is None:
        print("[Hybrid Search] ⚠️ Qdrant client unavailable — falling back to keyword-only mode")
        return []

    # Check if collection exists
    try:
        if not _qdrant_client.collection_exists(collection_name="keystone_unified"):
            print("[Hybrid Search] ⚠️ Collection 'keystone_unified' does not exist!")
            return []
    except Exception as e:
        print(f"[Hybrid Search] ⚠️ Qdrant connection error: {e}")
        return []

    # Build filters
    must_conditions = []
    
    if namespace:
        must_conditions.append(
            qdrant_models.FieldCondition(
                key="tenant_id",
                match=qdrant_models.MatchValue(value=namespace)
            )
        )
    elif cross_namespaces:
        should_conditions = [
            qdrant_models.FieldCondition(
                key="tenant_id",
                match=qdrant_models.MatchValue(value=ns)
            ) for ns in cross_namespaces
        ]
        must_conditions.append(
            qdrant_models.Filter(should=should_conditions)
        )

    if scope:
        scope_conditions = [
            qdrant_models.FieldCondition(
                key="parent_dir",
                match=qdrant_models.MatchValue(value=scope)
            ),
            qdrant_models.FieldCondition(
                key="path",
                match=qdrant_models.MatchText(text=scope)
            )
        ]
        must_conditions.append(
            qdrant_models.Filter(should=scope_conditions)
        )

    q_filter = qdrant_models.Filter(must=must_conditions) if must_conditions else None

    try:
        # Lazy load embed model if needed
        if _embed_model is None:
            from fastembed import TextEmbedding
            _embed_model = TextEmbedding("BAAI/bge-small-en-v1.5")
            
        query_embedding = list(_embed_model.embed([query]))[0].tolist()
        
        # Query unified collection
        results = _qdrant_client.query_points(
            collection_name="keystone_unified",
            query=query_embedding,
            using="fast-bge-small-en-v1.5",
            limit=top_k,
            query_filter=q_filter,
            with_payload=True
        )
        points = results.points if hasattr(results, 'points') else results
    except Exception as e:
        print(f"[Hybrid Search] ⚠️ Qdrant query_points failed: {e}")
        return []

    vector_results = []
    for point in points:
        payload = point.payload or {}
        doc_text = payload.get("document", "") or payload.get("text", "") or payload.get("content", "")
        snippet = doc_text[:200].replace('\n', ' ').strip() if doc_text else ""
        if len(doc_text) > 200:
            snippet += "..."
            
        vector_results.append({
            "source": payload.get("source", "Unknown"),
            "filename": payload.get("filename", payload.get("source", "result")),
            "snippet": snippet,
            "vector_score": point.score if hasattr(point, 'score') else 0.0,
            "namespace": payload.get("tenant_id", "unknown"),
            "metadata": payload,
            "origin": "qdrant",
            "eeat_tag": payload.get("EEAT_tag", payload.get("eeat_tag", "")),
            "topic": payload.get("topic", ""),
        })

    return vector_results


# ─── BM25-Style Keyword Scoring ─────────────────────────────────────────

def tokenize(text: str) -> list:
    """Simple whitespace + punctuation tokenizer."""
    return re.findall(r'\b\w+\b', text.lower())


def bm25_score(query_tokens: list, doc_tokens: list, k1: float = 1.5, b: float = 0.75, avg_dl: float = 200) -> float:
    """
    Simplified BM25 scoring for keyword relevance.
    """
    dl = len(doc_tokens)
    doc_freq = Counter(doc_tokens)
    score = 0.0

    for token in query_tokens:
        if token not in doc_freq:
            continue
        tf = doc_freq[token]
        # Simplified IDF (assume 100 docs, token appears in 10)
        idf = math.log((100 - 10 + 0.5) / (10 + 0.5) + 1)
        # BM25 term score
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * (dl / avg_dl))
        score += idf * (numerator / denominator)

    return score


# ─── Importance Scoring ──────────────────────────────────────────────────

def importance_from_metadata(metadata: dict) -> float:
    """Score importance 0.0-1.0 based on metadata signals."""
    score = 0.5

    # Recency boost
    timestamp = (metadata.get("timestamp") or metadata.get("created_at")
                 or metadata.get("date") or metadata.get("updated_at"))
    if timestamp:
        try:
            if isinstance(timestamp, str):
                dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
            else:
                dt = datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)
            hours_ago = (datetime.datetime.now(datetime.timezone.utc) - dt).total_seconds() / 3600
            if hours_ago < 24:
                score += 0.3
            elif hours_ago < 168:
                score += 0.15
            elif hours_ago < 720:  # 30 days
                score += 0.05
        except (ValueError, TypeError, OSError):
            pass

    # Priority boost
    priority = str(metadata.get("priority", "")).lower()
    if priority == "critical":
        score += 0.3
    elif priority == "high":
        score += 0.2

    # Source type boost
    source = str(metadata.get("source", "")).lower()
    if "brand" in source or "constitution" in source:
        score += 0.15
    elif "correction" in source or "error" in source:
        score += 0.2

    # EEAT tag boost (expertise signals from enriched payloads)
    eeat = str(metadata.get("EEAT_tag", "") or metadata.get("eeat_tag", "")).lower()
    if eeat in ("case study", "original research", "expert opinion"):
        score += 0.15
    elif eeat in ("tutorial", "how-to", "guide"):
        score += 0.1

    return min(max(score, 0.0), 1.0)


# ─── Local Document Search ──────────────────────────────────────────────

def search_local_docs(query: str, directories: list = None) -> list:
    """
    Search local markdown/json files for keyword matches.
    Returns scored results.
    """
    if directories is None:
        directories = [MASTER_DOCS_DIR, BRAND_CONSTITUTION_DIR, LEARNINGS_DIR]

    query_tokens = tokenize(query)
    results = []

    for directory in directories:
        if not os.path.exists(directory):
            continue

        for root, dirs, files in os.walk(directory):
            for fname in files:
                if not fname.endswith(('.md', '.json', '.jsonl', '.txt')):
                    continue

                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                except IOError:
                    continue

                doc_tokens = tokenize(content)
                kw_score = bm25_score(query_tokens, doc_tokens)

                if kw_score > 0:
                    # Check for exact phrase match bonus
                    if query.lower() in content.lower():
                        kw_score *= 1.5

                    # Extract a snippet around the first match
                    snippet = ""
                    idx = content.lower().find(query_tokens[0] if query_tokens else "")
                    if idx >= 0:
                        start = max(0, idx - 50)
                        end = min(len(content), idx + 150)
                        snippet = content[start:end].replace('\n', ' ').strip()
                        if start > 0:
                            snippet = "..." + snippet
                        if end < len(content):
                            snippet = snippet + "..."

                    results.append({
                        "source": fpath,
                        "filename": fname,
                        "keyword_score": kw_score,
                        "snippet": snippet,
                        "importance": importance_from_metadata({"source": fname}),
                        "origin": "local_file",
                    })

    results.sort(key=lambda r: r["keyword_score"], reverse=True)
    return results


# ─── Confidence Tiering ──────────────────────────────────────────────────

def confidence_tier(hybrid_score: float) -> str:
    """Assign a confidence tier based on the hybrid score."""
    if hybrid_score >= 0.75:
        return "🟢 HIGH"
    elif hybrid_score >= 0.45:
        return "🟡 MEDIUM"
    else:
        return "🔴 LOW"


# ─── Hybrid Merge (v2.0 — Real Vector + BM25 + Importance) ──────────────

def hybrid_search(
    query: str,
    namespace: Optional[str] = None,
    cross_namespaces: Optional[List[str]] = None,
    top_k: int = 5,
    scope: Optional[str] = None,
) -> list:
    """
    Execute TRUE hybrid search combining:
    - 50% vector similarity (REAL Qdrant cosine similarity)
    - 30% keyword/BM25 matching (local file search)
    - 20% importance scoring (recency, EEAT, priority)

    Args:
        query: Search query string
        namespace: Single namespace to filter (e.g., 'protocol', 'master')
        cross_namespaces: List of namespaces for cross-brand OR queries
        top_k: Number of results to return
        scope: Path-based directory scope to filter
    """
    print(f"\n[Hybrid Search v2.0] Query: '{query}'")
    if namespace:
        print(f"[Hybrid Search v2.0] Namespace: {namespace}")
    if cross_namespaces:
        print(f"[Hybrid Search v2.0] Cross-namespace query: {cross_namespaces}")
    if scope:
        print(f"[Hybrid Search v2.0] Scope: {scope}")
    print(f"[Hybrid Search v2.0] Top-K: {top_k}")
    print("-" * 60)

    # ──────────────────────────────────────────────────────────────
    # Phase 1: REAL Vector Search via Qdrant (50% weight)
    # ──────────────────────────────────────────────────────────────
    print("[Phase 1] 🧠 Qdrant vector search (REAL cosine similarity)...")
    vector_results = qdrant_vector_search(
        query=query,
        namespace=namespace,
        cross_namespaces=cross_namespaces,
        top_k=max(25, top_k * 5),  # Fetch a larger pool for hybrid fusion and reranking
        scope=scope,
    )

    # ──────────────────────────────────────────────────────────────
    # Phase 2: BM25 Keyword Search across local files (30% weight)
    # ──────────────────────────────────────────────────────────────
    print("[Phase 2] 📄 BM25 keyword search across local documents...")
    keyword_results = search_local_docs(query)

    # Also search agent fleet outputs
    print("[Phase 2b] 🤖 Searching agent fleet outputs...")
    fleet_results = search_local_docs(query, [AGENT_FLEET_DIR])
    keyword_results.extend(fleet_results)

    # ──────────────────────────────────────────────────────────────
    # Phase 3: Merge & Deduplicate
    # ──────────────────────────────────────────────────────────────
    print("[Phase 3] 🔀 Merging and deduplicating result sets...")

    # Build unified result pool
    merged = {}

    # Normalize vector scores (already 0-1 from Qdrant cosine similarity)
    max_vec = max((r["vector_score"] for r in vector_results), default=1.0)
    for r in vector_results:
        vec_norm = r["vector_score"] / max_vec if max_vec > 0 else 0
        key = r.get("source", "") or r.get("filename", "")
        importance = importance_from_metadata(r.get("metadata", {}))

        merged[key] = {
            "source": r["source"],
            "filename": r["filename"],
            "snippet": r["snippet"],
            "vector_norm": vec_norm,
            "keyword_norm": 0.0,  # May be filled by keyword phase
            "importance": importance,
            "origin": "qdrant",
            "namespace": r.get("namespace", ""),
            "eeat_tag": r.get("eeat_tag", ""),
            "topic": r.get("topic", ""),
            "raw_vector_score": r["vector_score"],
            "metadata": r.get("metadata", {}),
        }

    # Normalize keyword scores
    max_kw = max((r["keyword_score"] for r in keyword_results), default=1.0)
    for r in keyword_results:
        kw_norm = r["keyword_score"] / max_kw if max_kw > 0 else 0
        key = r.get("source", "") or r.get("filename", "")

        if key in merged:
            # Result exists from vector search — enrich with keyword score
            merged[key]["keyword_norm"] = max(merged[key]["keyword_norm"], kw_norm)
            merged[key]["importance"] = max(merged[key]["importance"], r["importance"])
            # Upgrade snippet if keyword snippet is richer
            if len(r.get("snippet", "")) > len(merged[key].get("snippet", "")):
                merged[key]["snippet"] = r["snippet"]
        else:
            # Keyword-only result (not in Qdrant)
            merged[key] = {
                "source": r["source"],
                "filename": r["filename"],
                "snippet": r.get("snippet", ""),
                "vector_norm": 0.0,  # No vector match
                "keyword_norm": kw_norm,
                "importance": r["importance"],
                "origin": "local_file",
                "namespace": "",
                "eeat_tag": "",
                "topic": "",
                "raw_vector_score": 0.0,
                "metadata": {},
            }

    # ──────────────────────────────────────────────────────────────
    # Phase 4: Compute Hybrid Scores (50/30/20 formula with REAL data)
    # ──────────────────────────────────────────────────────────────
    print("[Phase 4] ⚡ Computing hybrid scores (50% vector + 30% keyword + 20% importance)...")

    scored_results = []
    for key, r in merged.items():
        hybrid_score = (
            r["vector_norm"] * 0.50 +
            r["keyword_norm"] * 0.30 +
            r["importance"] * 0.20
        )
        r["hybrid_score"] = hybrid_score
        r["confidence"] = confidence_tier(hybrid_score)
        scored_results.append(r)

    # Sort by hybrid score descending
    scored_results.sort(key=lambda r: r["hybrid_score"], reverse=True)

    # ──────────────────────────────────────────────────────────────
    # Phase 5: Cross-Encoder Reranking (if available)
    # ──────────────────────────────────────────────────────────────
    if CROSS_ENCODER_AVAILABLE and _cross_encoder and scored_results:
        rerank_count = min(25, len(scored_results))
        print(f"[Phase 5] 🎯 Reranking top {rerank_count} candidates with Cross-Encoder...")
        rerank_pool = scored_results[:rerank_count]
        remaining = scored_results[rerank_count:]
        
        # Prepare input pairs
        pairs = []
        for r in rerank_pool:
            doc_text = r.get("metadata", {}).get("document") or r.get("metadata", {}).get("text")
            if not doc_text and os.path.exists(r["source"]):
                try:
                    with open(r["source"], "r", encoding="utf-8", errors="ignore") as f:
                        doc_text = f.read()
                except Exception:
                    pass
            if not doc_text:
                doc_text = r.get("snippet", "")
            pairs.append([query, doc_text])
            
        try:
            ce_scores = _cross_encoder.predict(pairs)
            for idx, r in enumerate(rerank_pool):
                raw_score = float(ce_scores[idx])
                # Sigmoid normalization (map logit to 0-1)
                ce_sigmoid = 1.0 / (1.0 + math.exp(-raw_score))
                
                # Blend Cross-Encoder score (80%) with metadata importance (20%)
                r["cross_encoder_score"] = ce_sigmoid
                r["hybrid_score"] = ce_sigmoid * 0.8 + r["importance"] * 0.2
                r["confidence"] = confidence_tier(r["hybrid_score"])
                r["origin"] = f"{r['origin']}+cross_encoder"
        except Exception as ce_err:
            print(f"[Hybrid Search] ⚠️ Cross-encoder reranking failed: {ce_err}")
            
        # Re-sort the pool by new blended score
        rerank_pool.sort(key=lambda r: r["hybrid_score"], reverse=True)
        scored_results = rerank_pool + remaining

    top_results = scored_results[:top_k]

    # ──────────────────────────────────────────────────────────────
    # Display Results
    # ──────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  HYBRID SEARCH RESULTS v2.0 — Top {len(top_results)}")
    print(f"{'='*60}")

    for i, r in enumerate(top_results, 1):
        ns_label = f" [{r['namespace']}]" if r.get("namespace") else ""
        eeat_label = f" ({r['eeat_tag']})" if r.get("eeat_tag") else ""
        print(f"\n  [{i}] {r['confidence']} Score: {r['hybrid_score']:.3f}{ns_label}{eeat_label}")
        print(f"      File: {r['filename']}")
        print(f"      Vector: {r['vector_norm']*0.5:.3f} | Keyword: {r['keyword_norm']*0.3:.3f} | Importance: {r['importance']*0.2:.3f}")
        print(f"      Origin: {r['origin']}")
        if r.get("snippet"):
            print(f"      Snippet: {r['snippet'][:120]}")

    if not top_results:
        print("\n  No results found. Try different keywords or check Qdrant is running.")

    # Stats
    vec_count = sum(1 for r in top_results if "qdrant" in r["origin"])
    kw_count = sum(1 for r in top_results if "local_file" in r["origin"])
    print(f"\n  📊 Sources: {vec_count} from Qdrant vector DB | {kw_count} from local files")
    print(f"  📊 Qdrant status: {'🟢 Connected' if QDRANT_AVAILABLE else '🔴 Unavailable (keyword-only mode)'}")

    return top_results


# ─── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Keystone Hybrid Retrieval v2.0")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--namespace", help="Restrict to namespace (master, protocol, possibilities, etc.)")
    parser.add_argument("--cross-namespace", help="Comma-separated namespaces for cross-brand OR query (e.g., master,protocol)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--scope", help="Directory or folder path scope to restrict query")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    cross_ns = args.cross_namespace.split(",") if args.cross_namespace else None

    results = hybrid_search(
        query=args.query,
        namespace=args.namespace,
        cross_namespaces=cross_ns,
        top_k=args.top_k,
        scope=args.scope,
    )

    if args.json:
        clean = [{
            "filename": r["filename"],
            "hybrid_score": round(r["hybrid_score"], 4),
            "vector_score": round(r.get("raw_vector_score", 0), 4),
            "confidence": r["confidence"],
            "namespace": r.get("namespace", ""),
            "snippet": r.get("snippet", ""),
            "source": r["source"],
            "origin": r["origin"],
        } for r in results]
        print(json.dumps(clean, indent=2))


if __name__ == "__main__":
    main()
