import sys
import os

# ── CRITICAL: MCP STDOUT GUARD ──────────────────────────────────────
# MCP uses JSON-RPC over stdout. ANY print/progress bar to stdout during
# import will corrupt the protocol and crash the server.
#
# tqdm (used by HuggingFace) bypasses sys.stdout and writes directly to
# the file descriptor, so we must suppress at BOTH levels:
#   1. Environment variables to disable progress bars entirely
#   2. sys.stdout redirect as a safety net
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TQDM_DISABLE"] = "1"
os.environ["OMP_NUM_THREADS"] = "2"
os.environ["MKL_NUM_THREADS"] = "2"
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["VECLIB_MAXIMUM_THREADS"] = "2"
os.environ["NUMEXPR_NUM_THREADS"] = "2"

import warnings
warnings.filterwarnings("ignore")

import logging
# Disable ALL logging during init — httpx, sentence_transformers, huggingface_hub
# all use Python logging with stdout handlers that corrupt MCP JSON-RPC
logging.disable(logging.CRITICAL)

_original_stdout = sys.stdout
sys.stdout = sys.stderr

from mcp.server.fastmcp import FastMCP
from qdrant_client import QdrantClient, models
from fastembed import TextEmbedding
import uuid
import tempfile
import json
from typing import Annotated

# NOTE: stdout stays redirected until AFTER all model/client initialization below

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from mcp_error_handler import safe_mcp_tool
except ImportError:
    # Fallback if execution environment differs
    def safe_mcp_tool(func): return func

# Initialize FastMCP Server
mcp = FastMCP("Keystone Brain v2")

# Embedding model name (used as named vector key in Qdrant)
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
VECTOR_NAME = "fast-bge-small-en-v1.5"

# UNIFIED COLLECTION — all namespaces merged with tenant_id-based multitenancy
# Config: m=0 (no global graph), payload_m=16 (per-tenant sub-graphs), is_tenant=true
UNIFIED_COLLECTION = "keystone_unified"

# AUTO-ROUTING: Content-based namespace detection prevents data from landing
# in the wrong bucket. Each namespace has keywords that trigger routing.
NAMESPACE_ROUTES = {
    "possibilities": [
        "construction", "builder", "contractor", "permit", "bill 44", "bill 25",
        "building code", "bcbc", "zoning", "renovation", "framing", "foundation",
        "keystone possibilities", "project management", "sea-to-sky", "squamish",
        "whistler", "pemberton", "site superintendent", "step code", "single egress",
        "ses ", "residential", "densification", "missing middle", "ocp",
    ],
    "protocol_brand": [
        "peptide", "bpc-157", "bpc157", "wolverine stack", "glp-1", "glp1",
        "semaglutide", "tirzepatide", "recomposition protocol", "wellness",
        "biohack", "testosterone", "hormone", "supplement", "dosing", "health protocol",
        "apollo", "longevity", "anti-aging", "recovery protocol", "stack",
    ],
    "music": [
        "spotify", "toolost", "music production", "recomposition music", "track",
        "album art", "isrc", "musicbrainz", "musixmatch", "beats per minute",
        "ambient", "chillout", "jazz", "lounge", "frequency", "432 hz",
        "music video", "visualizer", "lyrics",
    ],
    "content_pipeline": [
        "davinci resolve", "timeline", "google flow", "b-roll", "script",
        "video production", "thumbnail", "upload", "youtube short", "omi transcript",
        "render", "color grading", "fusion", "editing workflow", "veo",
    ],
    "master": [
        "agent fleet", "chronos", "self-evolution", "bootstrap", "mcp server",
        "brain architecture", "qdrant", "obsidian", "system infrastructure",
        "correction journal", "dream engine",
    ],
}

def _auto_route_namespace(content: str, source_id: str = "") -> str:
    """
    Analyze content + source_id to determine the best namespace.
    Returns the namespace with the most keyword matches.
    Falls back to 'general' only if nothing matches.
    """
    text = (content[:3000] + " " + source_id).lower()
    scores = {}
    for ns, keywords in NAMESPACE_ROUTES.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[ns] = score
    if scores:
        return max(scores, key=scores.get)
    return "general"


def _auto_route_namespaces(content: str, source_id: str = "") -> list[str]:
    """
    Analyze content + source_id to determine matching namespaces.
    Returns all namespaces with at least 1 keyword match, sorted by score.
    Falls back to ['general'] if nothing matches.
    """
    text = (content[:3000] + " " + source_id).lower()
    scores = {}
    for ns, keywords in NAMESPACE_ROUTES.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[ns] = score
    if scores:
        sorted_ns = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
        highest_score = scores[sorted_ns[0]]
        # Include namespaces that have close to the highest keyword match score
        return [ns for ns in sorted_ns if scores[ns] >= max(1, highest_score - 1)]
    return ["general"]


# DATA-PLANE ISOLATION: Large outputs saved to disk, return URI pointers
DATA_PLANE_DIR = os.path.join(
    os.path.dirname(__file__), "data_plane_output"
)
os.makedirs(DATA_PLANE_DIR, exist_ok=True)
DATA_PLANE_THRESHOLD = 5000  # chars — outputs larger than this get written to disk

# INSTRUCTION REINSERTION: Critical directives re-injected on every tool response.
# Prevents instruction drift in long sessions.
SYSTEM_DIRECTIVES = (
    "[SYSTEM] Remember: All social accounts use curtis4vancouver@gmail.com. "
    "Protocol brand inherits tokens from Recomposition. "
    "3 YouTube channels: Possibilities, OAC (Recomposition), Protocols. "
    "Use correct namespace when searching brain. "
    "Record important outcomes to episodic memory."
)

def _maybe_to_data_plane(output: str, label: str = "output") -> str:
    """If output exceeds threshold, save to disk and return file URI."""
    if len(output) <= DATA_PLANE_THRESHOLD:
        return output
    
    filename = f"{label}_{uuid.uuid4().hex[:8]}.txt"
    filepath = os.path.join(DATA_PLANE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output)
    
    # Return truncated preview + file pointer
    preview = output[:2000]
    return (
        f"{preview}\n\n"
        f"[DATA-PLANE] Full output ({len(output)} chars) saved to: file:///{filepath.replace(os.sep, '/')}\n"
        f"{SYSTEM_DIRECTIVES}"
    )

_qdrant_loaded = False
_dense_loaded = False
_sparse_loaded = False
_reranker_loaded = False
_memory_manager_loaded = False

embed_model = None
rerank_results = None
client = None
sparse_embed_model = None
memory_manager = None
sandbox_context = None
SPARSE_MODEL_NAME = "prithivida/Splade_PP_en_v1"
SPARSE_VECTOR_NAME = "fast-sparse-splade_pp_en_v1"

def _ensure_qdrant():
    global _qdrant_loaded, client
    if _qdrant_loaded: return
    _qdrant_loaded = True
    try:
        client = QdrantClient(url="http://localhost:6333")
        client.set_model(EMBED_MODEL_NAME)
        try:
            client.set_sparse_model(SPARSE_MODEL_NAME)
        except Exception:
            pass
    except Exception as e:
        client = None
        print(f"Failed to connect to Qdrant: {e}", file=sys.stderr)

def _ensure_dense():
    global _dense_loaded, embed_model
    if _dense_loaded: return
    _dense_loaded = True
    try:
        _real_stdout = sys.stdout
        sys.stdout = sys.stderr
        embed_model = TextEmbedding(EMBED_MODEL_NAME)
        sys.stdout = _real_stdout
    except Exception as e:
        embed_model = None
        try:
            sys.stdout = _real_stdout
        except: pass

def _ensure_sparse():
    global _sparse_loaded, sparse_embed_model
    if _sparse_loaded: return
    _sparse_loaded = True
    try:
        from fastembed import SparseTextEmbedding
        _real_stdout = sys.stdout
        sys.stdout = sys.stderr
        sparse_embed_model = SparseTextEmbedding(SPARSE_MODEL_NAME)
        sys.stdout = _real_stdout
        print(f"Sparse model loaded: {SPARSE_MODEL_NAME}", file=sys.stderr)
    except Exception as e:
        sparse_embed_model = None
        try:
            sys.stdout = _real_stdout
        except: pass

def _ensure_reranker():
    global _reranker_loaded, rerank_results
    if _reranker_loaded: return
    _reranker_loaded = True
    try:
        from reranker import rerank_results as rr, reranker_model
        rerank_results = rr
        if reranker_model:
            print("Reranker loaded successfully.", file=sys.stderr)
    except Exception as e:
        rerank_results = None
        print(f"Failed to load reranker.py: {e}", file=sys.stderr)

def _ensure_memory_manager():
    global _memory_manager_loaded, memory_manager, sandbox_context
    if _memory_manager_loaded: return
    _ensure_qdrant()
    _ensure_dense()
    _ensure_sparse()
    _memory_manager_loaded = True
    try:
        from memory_layers import MemoryManager
        if client:
            memory_manager = MemoryManager(
                client=client,
                collection_name=UNIFIED_COLLECTION,
                embed_model=embed_model,
                vector_name=VECTOR_NAME,
                sparse_embed_model=sparse_embed_model,
                sparse_vector_name=SPARSE_VECTOR_NAME
            )
        from sandbox import SandboxContext
        if memory_manager:
            sandbox_context = SandboxContext(memory_manager)
    except ImportError:
        memory_manager = None
        sandbox_context = None

# ── RESTORE STDOUT & LOGGING ──────────────────────────────────────
# All models loaded, all clients connected. Safe to restore now.
sys.stdout = _original_stdout
logging.disable(logging.NOTSET)
# Suppress httpx INFO logs going forward (they'd still corrupt on tool calls)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

@mcp.tool()
@safe_mcp_tool
def search_master_brain(
    query: Annotated[str, "Natural language search query. Be descriptive for best results."],
    namespace: Annotated[str, "Domain filter. Use 'auto' for automatic routing, or specify explicitly: possibilities, content_pipeline, general, protocol_brand, master, music."] = "auto",
    limit: Annotated[int, "Max results to return (1-20). Default 5."] = 5,
    memory_layer: Annotated[str, "Optional layer filter: semantic, episodic, working, procedural"] = "",
    deep_rerank: Annotated[bool, "Use the cross-encoder to deeply rerank results. Slower but more accurate."] = False
) -> str:
    """
    Semantic search across the Keystone vector knowledge base. Returns the most relevant documents matching the query within a specific namespace. Use natural language queries, not keywords.
    
    GUIDELINES:
    - Always specify the correct namespace to avoid cross-domain noise.
    - Start with limit=3 for focused results, increase to 10 for broad surveys.
    - Results include source attribution and relevance scores (0-1).
    - Large results auto-save to disk with a file URI pointer.
    
    LIMITATIONS:
    - Cannot answer temporal questions ('what happened yesterday?') — use search_episodes instead.
    - Scores below 0.3 indicate weak semantic match.
    - Max 384-dim dense vectors; very short queries (<3 words) may return poor matches.
    """
    _ensure_qdrant()
    _ensure_dense()
    _ensure_sparse()
    if deep_rerank:
        _ensure_reranker()

    if client is None:
        return "Error: Local vector database is offline. Check Docker container."
        
    try:
        # Support single string, comma-separated string, or list of namespaces
        if isinstance(namespace, str):
            if namespace == "auto":
                namespaces_list = _auto_route_namespaces(query)
            else:
                namespaces_list = [ns.strip() for ns in namespace.split(",") if ns.strip()]
        elif isinstance(namespace, list):
            namespaces_list = namespace
        else:
            namespaces_list = ["general"]

        # Build tenant filter using MatchAny if there are multiple, otherwise MatchValue
        if len(namespaces_list) > 1:
            tenant_cond = models.FieldCondition(
                key="tenant_id",
                match=models.MatchAny(any=namespaces_list),
            )
        else:
            tenant_cond = models.FieldCondition(
                key="tenant_id",
                match=models.MatchValue(value=namespaces_list[0]),
            )

        # Build tenant filter for the unified collection
        must_conds = [tenant_cond]
        if memory_layer:
            must_conds.append(
                models.FieldCondition(
                    key="memory_layer",
                    match=models.MatchValue(value=memory_layer),
                )
            )
        tenant_filter = models.Filter(must=must_conds)

        # RERANKING STRATEGY: Over-fetch candidates, then rerank with cross-encoder
        # Fetch 3× the requested limit to give the reranker a good candidate pool
        fetch_limit = limit * 3 if deep_rerank and rerank_results is not None else limit

        # Try with temporal boost first (prefer recent results)
        try:
            from datetime import datetime, timedelta
            time_boundary = datetime.utcnow() - timedelta(days=30)
            
            temporal_must = list(must_conds)
            temporal_must.append(
                models.FieldCondition(
                    key="created_at",
                    range=models.Range(gte=time_boundary.timestamp())
                )
            )
            temporal_filter = models.Filter(must=temporal_must)
            results = _do_query(query, fetch_limit, temporal_filter, namespaces=namespaces_list)
            # If temporal filter returns nothing, fall back to tenant-only
            if not results:
                results = _do_query(query, fetch_limit, tenant_filter, namespaces=namespaces_list)
        except Exception:
            results = _do_query(query, fetch_limit, tenant_filter, namespaces=namespaces_list)
        
        if not results:
            return f"No results found in namespaces {namespaces_list} for query '{query}'."
        
        # CROSS-ENCODER RERANKING
        if deep_rerank and rerank_results is not None and len(results) > 1:
            try:
                results = rerank_results(query, results, limit)
                reranked = True
                
                # Extract scores for formatting
                rerank_scores_final = [getattr(r, 'score', 0) for r in results]
            except Exception as e:
                reranked = False
                rerank_scores_final = []
                results = results[:limit]
        else:
            reranked = False
            results = results[:limit]
            
        output = [f"Found {len(results)} matches in {namespaces_list}" + 
                  (" (reranked)" if reranked else "") + ":\n"]
        for idx, point in enumerate(results):
            # Handle both query() .metadata and query_points() .payload
            payload = getattr(point, 'payload', None) or getattr(point, 'metadata', None) or {}
            source = payload.get('source', 'Unknown')
            content = payload.get('document', payload.get('text', str(payload)))
            vec_score = point.score if hasattr(point, 'score') else 0.0
            score_label = f"VecScore: {vec_score:.3f}"
            if reranked:
                score_label += f", Rerank: {rerank_scores_final[idx]:.3f}"
            output.append(f"--- Result {idx+1} (Source: {source}, {score_label}) ---")
            output.append(str(content))
            output.append("\n")
        
        # Neo4j GraphRAG Augmentation (1st and 2nd-degree neighbors)
        graph_context = []
        try:
            from neo4j import GraphDatabase
            NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
            NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
            NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "keystonesovereign")
            
            driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
            with driver.session() as session:
                # 1. Fetch all entity names
                res_entities = session.run("MATCH (e:Entity) RETURN e.name AS name")
                all_entity_names = [record["name"] for record in res_entities]
                
                # Collect content of all results to scan
                all_results_text = ""
                for point in results:
                    payload = getattr(point, 'payload', None) or getattr(point, 'metadata', None) or {}
                    all_results_text += " " + payload.get('document', payload.get('text', str(payload)))
                
                # Match entities mentioned in results
                discovered_entities = []
                for name in all_entity_names:
                    if name.lower() in all_results_text.lower():
                        discovered_entities.append(name)
                        
                if discovered_entities:
                    # 2. Query 1st-degree relationships
                    res_1st = session.run("""
                        MATCH (e:Entity)-[r]->(neighbor:Entity)
                        WHERE e.name IN $names OR neighbor.name IN $names
                        RETURN e.name AS source, e.type AS source_type, r.relation AS relation, type(r) AS rel_type, neighbor.name AS target, neighbor.type AS target_type
                    """, names=discovered_entities)
                    
                    direct_relations = []
                    related_set = set(discovered_entities)
                    seen_edges = set()
                    
                    for record in res_1st:
                        edge = (record["source"], record["rel_type"], record["target"])
                        if edge not in seen_edges:
                            direct_relations.append(record)
                            seen_edges.add(edge)
                            related_set.add(record["source"])
                            related_set.add(record["target"])
                            
                    # 3. Query 2nd-degree relationships connecting to discovered/related entities
                    res_2nd = session.run("""
                        MATCH (e:Entity)-[r]->(neighbor:Entity)
                        WHERE (e.name IN $related OR neighbor.name IN $related)
                        RETURN e.name AS source, e.type AS source_type, r.relation AS relation, type(r) AS rel_type, neighbor.name AS target, neighbor.type AS target_type
                    """, related=list(related_set))
                    
                    second_relations = []
                    for record in res_2nd:
                        edge = (record["source"], record["rel_type"], record["target"])
                        if edge not in seen_edges:
                            second_relations.append(record)
                            seen_edges.add(edge)
                            
                    # Format graph context to append
                    if direct_relations or second_relations:
                        graph_context.append("\n--- Knowledge Graph Context ---")
                        if direct_relations:
                            graph_context.append("Direct Entity Relationships:")
                            for r in direct_relations:
                                rel_desc = r["relation"] or r["rel_type"].lower().replace("_", " ")
                                graph_context.append(f"  • ({r['source']}:{r['source_type']}) ──[{rel_desc}]──> ({r['target']}:{r['target_type']})")
                        if second_relations:
                            graph_context.append("Secondary Contextual Relationships:")
                            for r in second_relations:
                                rel_desc = r["relation"] or r["rel_type"].lower().replace("_", " ")
                                graph_context.append(f"  • ({r['source']}:{r['source_type']}) ──[{rel_desc}]──> ({r['target']}:{r['target_type']})")
            driver.close()
        except Exception as graph_err:
            # Graph failure shouldn't crash the vector search
            graph_context.append(f"\n⚠️ GraphRAG lookup disabled: {graph_err}")
            
        if graph_context:
            output.append("\n".join(graph_context))
            output.append("\n")
        
        raw_output = "\n".join(output)
        # DATA-PLANE: Large results saved to disk, return URI
        result = _maybe_to_data_plane(raw_output, label=f"search_{'_'.join(namespaces_list)}")
        # INSTRUCTION REINSERTION: Append critical directives
        if len(raw_output) <= DATA_PLANE_THRESHOLD:
            result += f"\n{SYSTEM_DIRECTIVES}"
        return result
    except Exception as e:
        return f"Database query failed: {str(e)}"


def _do_query(query_text, limit, q_filter, namespaces=None):
    """Execute hybrid query: dense + sparse vectors fused via Reciprocal Rank Fusion (RRF).
    Falls back to dense-only if sparse model is unavailable."""
    if namespaces is None:
        namespaces = ["general"]

    try:
        # Embed the query using fastembed (named vectors require raw embedding)
        if embed_model is None:
            raise RuntimeError("Embedding model not loaded")
        query_embedding = list(embed_model.embed([query_text]))[0].tolist()

        # Dynamic prefetch limit calculations based on namespace intent
        SPARSE_DOMINANT_NAMESPACES = {"webmaster", "music", "local_seo"}
        DENSE_DOMINANT_NAMESPACES = {"protocol_brand", "content_pipeline", "general", "master", "possibilities"}

        # Count matching classifications
        sparse_count = sum(1 for ns in namespaces if ns in SPARSE_DOMINANT_NAMESPACES)
        dense_count = sum(1 for ns in namespaces if ns in DENSE_DOMINANT_NAMESPACES)

        if sparse_count > 0 and dense_count == 0:
            # Pure technical/keyword lookup: focus heavily on sparse keywords
            dense_limit = limit
            sparse_limit = limit * 4
        elif dense_count > 0 and sparse_count == 0:
            # Pure conceptual lookup: focus heavily on dense semantics
            dense_limit = limit * 4
            sparse_limit = limit
        else:
            # Mixed namespaces or default: balanced prefetch limits
            dense_limit = limit * 2
            sparse_limit = limit * 2
        
        # HYBRID SEARCH: If sparse model is available, do dense+sparse with RRF
        if sparse_embed_model is not None:
            try:
                # Generate sparse query embedding
                sparse_result = list(sparse_embed_model.embed([query_text]))[0]
                sparse_query = models.SparseVector(
                    indices=sparse_result.indices.tolist(),
                    values=sparse_result.values.tolist(),
                )
                
                # Use Qdrant's prefetch + fusion API for hybrid search
                # This fetches candidates from BOTH dense and sparse indexes,
                # then fuses them with RRF (Reciprocal Rank Fusion)
                results = client.query_points(
                    collection_name=UNIFIED_COLLECTION,
                    prefetch=[
                        # Dense vector search (semantic similarity)
                        models.Prefetch(
                            query=query_embedding,
                            using=VECTOR_NAME,
                            limit=dense_limit,
                            filter=q_filter,
                        ),
                        # Sparse vector search (keyword/term matching)
                        models.Prefetch(
                            query=sparse_query,
                            using=SPARSE_VECTOR_NAME,
                            limit=sparse_limit,
                            filter=q_filter,
                        ),
                    ],
                    # RRF fusion: combines rankings from both searches
                    query=models.FusionQuery(fusion=models.Fusion.RRF),
                    limit=limit,
                    with_payload=True,
                    search_params=models.SearchParams(
                        acorn=models.AcornSearchParams(
                            enable=True
                        )
                    ),
                )
                return results.points if hasattr(results, 'points') else results
            except Exception:
                # Sparse search failed — fall back to dense-only
                pass
        
        # Dense-only fallback
        results = client.query_points(
            collection_name=UNIFIED_COLLECTION,
            query=query_embedding,
            using=VECTOR_NAME,
            limit=limit,
            query_filter=q_filter,
            search_params=models.SearchParams(
                acorn=models.AcornSearchParams(
                    enable=True
                )
            ),
        )
        # query_points returns ScoredPoint objects in results.points
        return results.points if hasattr(results, 'points') else results
    except Exception as e:
        raise



@mcp.tool()
@safe_mcp_tool
def list_brain_namespaces() -> str:
    """
    Inventory all namespaces (tenant domains) and their vector counts. Call this before searching if unsure which namespace to target.
    
    GUIDELINES:
    - Returns sorted list with vector counts per namespace.
    - Large namespaces (1000+) contain rich, broad knowledge.
    - Small namespaces (<10) are specialized or recently created.
    
    LIMITATIONS:
    - Scrolls entire unified collection; may take 2-3 seconds on 14K+ vectors.
    - Does not show content previews, only counts.
    """
    _ensure_qdrant()
    if client is None:
        return "Error: Database offline."
        
    try:
        # FAST PATH: Use Qdrant count() with tenant_id filter per known namespace.
        # Old code scrolled ALL 15K+ vectors (152+ round trips, 17 min hang).
        # New code: ~12 fast count() calls, completes in <1 second.
        KNOWN_NAMESPACES = [
            "agent_arch", "content_pipeline", "general", "keystone_ops",
            "master", "music", "possibilities", "protocol", "protocol_brand",
            "research", "spark_updates", "webmaster",
        ]
        
        tenant_counts = {}
        for ns in KNOWN_NAMESPACES:
            try:
                result = client.count(
                    collection_name=UNIFIED_COLLECTION,
                    count_filter=models.Filter(
                        must=[models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns),
                        )]
                    ),
                    exact=True,
                )
                if result.count > 0:
                    tenant_counts[ns] = result.count
            except Exception:
                pass
        
        # Also get total to catch any unlisted namespaces
        try:
            total_result = client.count(
                collection_name=UNIFIED_COLLECTION,
                exact=True,
            )
            total = total_result.count
        except Exception:
            total = sum(tenant_counts.values())
        
        lines = ["Available Namespaces:"]
        for tid in sorted(tenant_counts.keys()):
            lines.append(f"  - {tid}: {tenant_counts[tid]} vectors")
        
        known_total = sum(tenant_counts.values())
        unlisted = total - known_total
        if unlisted > 0:
            lines.append(f"  - (unlisted): {unlisted} vectors")
        
        lines.append(f"\nTotal: {total} vectors across {len(tenant_counts)} namespaces (unified collection)")
        return "\n".join(lines)
    except Exception as e:
        return f"Error fetching namespaces: {str(e)}"


@mcp.tool()
@safe_mcp_tool
def ingest_to_brain(
    source_id: Annotated[str, "Unique identifier for this knowledge source. Use format 'topic_YYYY-MM-DD'."],
    content: Annotated[str, "The text content to store. Markdown preferred."],
    namespace: Annotated[str, "Target domain. Use 'auto' for automatic routing, or specify explicitly: 'possibilities', 'content_pipeline', 'protocol_brand', 'music', 'master', 'general'"] = "auto",
    memory_layer: Annotated[str, "Memory persistence layer: semantic, episodic, working, procedural"] = "semantic"
) -> str:
    """
    Permanently store new knowledge in the Qdrant vector brain. Content is embedded, chunked, and indexed for future semantic retrieval.
    
    GUIDELINES:
    - Check list_brain_sources() first to avoid ingesting duplicates.
    - Content auto-chunks at 1500 chars with header-aware splitting.
    
    LIMITATIONS:
    - Cannot update existing entries — ingesting the same content creates duplicates.
    - Max practical content size ~50KB per call.
    """
    _ensure_memory_manager()
    if client is None:
        return "Error: Local vector database is offline."
        
    try:
        # Auto-route namespace if not explicitly specified
        if namespace == "auto":
            namespace = _auto_route_namespace(content, source_id)
        
        # Ensure unified collection exists
        if not client.collection_exists(collection_name=UNIFIED_COLLECTION):
            return "Error: Unified collection does not exist. Run migration first."
            
        if memory_manager is not None:
            if memory_layer == "semantic":
                count = memory_manager.store_semantic(content, source_id, namespace)
            elif memory_layer == "episodic":
                count = memory_manager.store_episodic(content, source_id, namespace)
            elif memory_layer == "working":
                count = memory_manager.store_working(content, session_id=source_id)
            elif memory_layer == "procedural":
                count = memory_manager.store_procedural(content, skill_name=source_id, version="1.0")
            else:
                return f"Error: Invalid memory_layer '{memory_layer}'"
            return f"Successfully ingested {count} chunk(s) into namespace '{namespace}' (layer: {memory_layer}) with source '{source_id}'."
        else:
            return "Error: MemoryManager not initialized."
    except Exception as e:
        return f"Ingestion failed: {str(e)}"


@mcp.tool()
@safe_mcp_tool
def list_brain_sources(
    namespace: Annotated[str, "Optional filter. If provided, only shows sources for that domain."] = ""
) -> str:
    """
    Audit all ingested sources and their chunk counts to prevent duplicates.
    
    GUIDELINES:
    - Call this BEFORE ingest_to_brain to check if content already exists.
    - Leave namespace empty to scan all domains (slower, ~14K vectors).
    - Output auto-saves to disk if very large.
    
    LIMITATIONS:
    - Scrolls through all points; scanning all namespaces may take 5-10 seconds.
    - Shows source IDs and chunk counts only, not content previews.
    """
    _ensure_qdrant()
    if client is None:
        return "Error: Local vector database is offline."
        
    try:
        # Build filter
        scroll_filter = None
        if namespace:
            scroll_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=namespace),
                    )
                ]
            )
        
        sources_by_tenant = {}
        offset = None
        max_scrolls = 200
        scroll_count = 0
        
        while scroll_count < max_scrolls:
            try:
                kwargs = {
                    "collection_name": UNIFIED_COLLECTION,
                    "limit": 100,
                    "with_payload": ["tenant_id", "source"],
                    "with_vectors": False,
                    "offset": offset,
                }
                if scroll_filter:
                    kwargs["scroll_filter"] = scroll_filter
                
                records, next_offset = client.scroll(**kwargs)
                for record in records:
                    if record.payload:
                        tid = record.payload.get("tenant_id", "unknown")
                        src = record.payload.get("source", "Unknown")
                        if tid not in sources_by_tenant:
                            sources_by_tenant[tid] = {}
                        sources_by_tenant[tid][src] = sources_by_tenant[tid].get(src, 0) + 1
                scroll_count += 1
                if next_offset is None:
                    break
                offset = next_offset
            except Exception as scroll_err:
                break
        
        output = ["Ingested Brain Sources:"]
        for tid in sorted(sources_by_tenant.keys()):
            sources = sources_by_tenant[tid]
            total = sum(sources.values())
            output.append(f"\nNamespace '{tid}' ({total} vectors):")
            for src, count in sorted(sources.items()):
                output.append(f"  - {src} ({count} chunks)")
                
        raw_output = "\n".join(output)
        return _maybe_to_data_plane(raw_output, label="brain_sources")
    except Exception as e:
        return f"Failed to list brain sources: {str(e)}"


@mcp.tool()
@safe_mcp_tool
def delete_brain_namespace(
    namespace: Annotated[str, "The tenant_id to delete all vectors for."],
    confirm: Annotated[bool, "Must be True to execute. Otherwise dry-run."] = False
) -> str:
    """
    Remove all vectors for a given namespace from the unified collection.
    
    GUIDELINES:
    - Always run WITHOUT confirm=True first to see the dry-run count.
    - Protected namespaces (general, keystone_brain, master, content_pipeline,
      webmaster, music, local_seo) CANNOT be deleted.
    - Use for cleanup of experimental or outdated namespaces.
    
    LIMITATIONS:
    - Irreversible. No undo. Data is permanently removed.
    - Cannot delete individual sources within a namespace (only full namespace).
    """
    _ensure_qdrant()
    if client is None:
        return "Error: Local vector database is offline."
    
    PROTECTED = {"general", "keystone_brain", "master", "content_pipeline", "webmaster", "music", "local_seo"}
    if namespace in PROTECTED:
        return f"Error: Namespace '{namespace}' is protected and cannot be deleted."
    
    try:
        # Count vectors for this tenant
        count_result = client.count(
            collection_name=UNIFIED_COLLECTION,
            count_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="tenant_id",
                        match=models.MatchValue(value=namespace),
                    )
                ]
            ),
            exact=True,
        )
        count = count_result.count
        
        if count == 0:
            return f"Namespace '{namespace}' has no vectors."
        
        if not confirm:
            return f"DRY RUN: Would delete {count} vectors from namespace '{namespace}'. Set confirm=True to execute."
        
        # Delete by filter
        client.delete(
            collection_name=UNIFIED_COLLECTION,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=namespace),
                        )
                    ]
                )
            ),
        )
        return f"Successfully deleted {count} vectors from namespace '{namespace}'."
    except Exception as e:
        return f"Delete failed: {str(e)}"


# ===== EPISODIC MEMORY TOOLS =====
# SQLite FTS5-based temporal memory for "what happened when?" queries

@mcp.tool()
@safe_mcp_tool
def record_episode(
    action_type: Annotated[str, "'task_start', 'task_complete', 'tool_call', 'user_request', 'error', 'learning'"],
    summary: Annotated[str, "A brief description of the episode."],
    namespace: Annotated[str, "The domain namespace."] = "general",
    outcome: Annotated[str, "'success', 'failure', 'partial', 'pending'"] = "success",
    risk_level: Annotated[str, "'LOW', 'MEDIUM', 'HIGH'"] = "LOW"
) -> str:
    """
    Records an episode to the temporal episodic memory. Use this to log task completions, errors, decisions, and learnings.
    """
    _ensure_memory_manager()
    try:
        from datetime import datetime
        content = f"Action: {action_type}\nOutcome: {outcome}\nRisk: {risk_level}\nSummary: {summary}"
        source_id = f"episode_{action_type}_{int(datetime.utcnow().timestamp())}"
        
        if memory_manager:
            memory_manager.store_episodic(content, source_id, namespace)
            return f"Episode recorded: [{action_type}] {summary[:80]}"
        else:
            return "Error: MemoryManager not initialized."
    except Exception as e:
        return f"Failed to record episode: {str(e)}"

@mcp.tool()
@safe_mcp_tool
def promote_memory(
    point_id: Annotated[str, "The point ID to promote."],
    to_layer: Annotated[str, "The target memory layer (e.g., 'semantic')."]
) -> str:
    """Promotes an episodic memory to semantic memory."""
    _ensure_memory_manager()
    if not memory_manager:
        return "Error: MemoryManager not initialized."
    success = memory_manager.promote_memory(point_id, to_layer)
    if success:
        return f"Successfully promoted point {point_id} to layer {to_layer}."
    return f"Failed to promote point {point_id}."

@mcp.tool()
@safe_mcp_tool
def run_memory_decay() -> str:
    """Triggers the decay cleanup for episodic memories."""
    _ensure_memory_manager()
    if not memory_manager:
        return "Error: MemoryManager not initialized."
    deleted, promoted = memory_manager.decay_episodic()
    return f"Memory decay complete. Deleted {deleted} episodic memories."

@mcp.tool()
@safe_mcp_tool
def get_memory_stats() -> str:
    """Returns vector counts per namespace and total brain stats."""
    _ensure_qdrant()
    if client is None:
        return "Error: Database offline."
    
    try:
        KNOWN_NAMESPACES = [
            "agent_arch", "content_pipeline", "general", "keystone_ops",
            "master", "music", "possibilities", "protocol", "protocol_brand",
            "research", "spark_updates", "webmaster",
        ]
        
        stats = {}
        for ns in KNOWN_NAMESPACES:
            try:
                result = client.count(
                    collection_name=UNIFIED_COLLECTION,
                    count_filter=models.Filter(
                        must=[models.FieldCondition(
                            key="tenant_id",
                            match=models.MatchValue(value=ns),
                        )]
                    ),
                    exact=True,
                )
                if result.count > 0:
                    stats[ns] = result.count
            except Exception:
                pass
        
        try:
            total_result = client.count(
                collection_name=UNIFIED_COLLECTION,
                exact=True,
            )
            total = total_result.count
        except Exception:
            total = sum(stats.values())
        
        lines = ["Memory Stats (Qdrant Brain):"]
        for ns in sorted(stats.keys()):
            lines.append(f"  {ns}: {stats[ns]} vectors")
        lines.append(f"\n  TOTAL: {total} vectors across {len(stats)} namespaces")
        return "\n".join(lines)
    except Exception as e:
        return f"Failed to get memory stats: {str(e)}"


@mcp.tool()
@safe_mcp_tool
def search_episodes(
    query: Annotated[str, "Full-text search query."],
    limit: Annotated[int, "Max results to return."] = 10
) -> str:
    """
    Full-text search across the episodic memory (SQLite FTS5). Use this for temporal queries that vector search can't answer, like 'what happened yesterday?' or 'when did we last upload?'
    """
    try:
        from episodic_memory import search_episodes as _search
        results = _search(query=query, limit=limit)
        if not results:
            return f"No episodes found for '{query}'."
        
        output = [f"Found {len(results)} episodes:\n"]
        for r in results:
            output.append(f"[{r['timestamp']}] {r['action_type']} ({r['outcome'] or '?'}) - {r['summary']}")
        return "\n".join(output)
    except Exception as e:
        return f"Episode search failed: {str(e)}"


@mcp.tool()
@safe_mcp_tool
def get_recent_activity(
    hours: Annotated[int, "Number of hours to look back."] = 24,
    limit: Annotated[int, "Max results to return."] = 20
) -> str:
    """
    Get recent episodes from the last N hours. Useful for session handoff, morning briefings, or understanding what happened overnight.
    """
    try:
        from episodic_memory import get_recent_episodes
        results = get_recent_episodes(hours=hours, limit=limit)
        if not results:
            return f"No activity in the last {hours} hours."
        
        output = [f"Activity in last {hours} hours ({len(results)} episodes):\n"]
        for r in results:
            risk = f" ⚠{r['risk_level']}" if r['risk_level'] != 'LOW' else ""
            output.append(f"[{r['timestamp']}] {r['action_type']}: {r['summary']}{risk}")
        return "\n".join(output)
    except Exception as e:
        return f"Failed to get recent activity: {str(e)}"

# ===== SANDBOX TOOLS =====

@mcp.tool()
@safe_mcp_tool
def create_sandbox(
    name: Annotated[str, "A short name for the sandbox."],
    parent_namespace: Annotated[str, "The parent namespace to branch from."]
) -> str:
    """
    Creates a temporary namespace prefix for isolated work.
    Data ingested here won't pollute the main brain until committed.
    """
    _ensure_memory_manager()
    if not sandbox_context:
        return "Error: Sandbox context not initialized."
    sandbox_id = sandbox_context.create_sandbox(name, parent_namespace)
    return f"Sandbox created. Use namespace '{sandbox_id}' for temporary work."

@mcp.tool()
@safe_mcp_tool
def commit_sandbox(
    sandbox_id: Annotated[str, "The ID of the sandbox to commit."]
) -> str:
    """
    Merges all isolated work from a sandbox into its parent namespace.
    """
    _ensure_memory_manager()
    if not sandbox_context:
        return "Error: Sandbox context not initialized."
    success = sandbox_context.commit_sandbox(sandbox_id)
    if success:
        return f"Successfully committed sandbox {sandbox_id}."
    return f"Failed to commit sandbox {sandbox_id}."

@mcp.tool()
@safe_mcp_tool
def rollback_sandbox(
    sandbox_id: Annotated[str, "The ID of the sandbox to rollback."]
) -> str:
    """
    Discards all isolated work within a sandbox, deleting it permanently.
    """
    _ensure_memory_manager()
    if not sandbox_context:
        return "Error: Sandbox context not initialized."
    success = sandbox_context.rollback_sandbox(sandbox_id)
    if success:
        return f"Successfully rolled back sandbox {sandbox_id}."
    return f"Failed to rollback sandbox {sandbox_id}."


if __name__ == "__main__":
    import sys
    transport = "stdio"
    port = 8000
    if len(sys.argv) > 1:
        if sys.argv[1] in ("sse", "streamable-http", "stdio"):
            transport = sys.argv[1]
        if len(sys.argv) > 2:
            try:
                port = int(sys.argv[2])
            except ValueError:
                pass
                
    if transport == "sse":
        mcp.settings.port = port
        mcp.run(transport="sse")
    else:
        mcp.run(transport=transport)

