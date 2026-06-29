import threading
import time
import json
import math
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient, models as qdrant_models
from core.state_store import StateStore

class MemoryManager:
    """
    Manages semantic and historical memory retrieval, relevance scoring, and post-turn sync.
    Integrates SQLite state store and Qdrant vector database.
    """
    def __init__(self, state_store: StateStore, qdrant_url: str = "http://localhost:6333"):
        self.state_store = state_store
        self.qdrant_url = qdrant_url
        
        try:
            self.qdrant_client = QdrantClient(url=qdrant_url)
            # Use same embedding model as the self_evolution engine
            self.qdrant_client.set_model("BAAI/bge-small-en-v1.5")
            self.qdrant_available = True
        except Exception as e:
            print(f"[MemoryManager] Qdrant connection offline: {e}")
            self.qdrant_client = None
            self.qdrant_available = False

    def retrieve_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves memories from both Qdrant (semantic) and SQLite (keyword/FTS5).
        Scores and ranks results using a combination of relevance and recency.
        """
        recalled = []
        seen_contents = set()
        now = time.time()

        # 1. Retrieve Semantic Memories from Qdrant
        if self.qdrant_available and self.qdrant_client:
            try:
                # Search across multiple relevant collections
                collections = ["keystone_learnings", "self_healing", "general", "master"]
                existing_collections = [c.name for c in self.qdrant_client.get_collections().collections]
                
                for col in collections:
                    if col not in existing_collections:
                        continue
                    
                    results = self.qdrant_client.query_points(
                        collection_name=col,
                        query=query,
                        limit=limit,
                        with_payload=True
                    )
                    
                    for point in results.points:
                        payload = point.payload or {}
                        content = payload.get("document", payload.get("content", ""))
                        if not content or content in seen_contents:
                            continue
                        
                        score = point.score if hasattr(point, 'score') else 0.5
                        # Ensure score is within 0-1
                        score = max(0.0, min(1.0, score))
                        
                        # Extract timestamp
                        created_at_str = payload.get("updated_at", payload.get("timestamp", ""))
                        age_days = 1.0
                        if created_at_str:
                            try:
                                # Simple age parsing
                                import datetime
                                dt = datetime.datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                                age_days = max(0.1, (now - dt.timestamp()) / 86400.0)
                            except Exception:
                                pass
                        
                        # Recency weighting: decay score slightly over time (half life of 30 days)
                        recency_weight = math.exp(-age_days / 30.0)
                        composite_score = (score * 0.7) + (recency_weight * 0.3)

                        recalled.append({
                            "content": content,
                            "source": f"qdrant/{col}",
                            "score": composite_score,
                            "timestamp": created_at_str or now
                        })
                        seen_contents.add(content)
            except Exception as e:
                print(f"[MemoryManager] Semantic search warning: {e}")

        # 2. Retrieve Keyword Memories from SQLite State Store
        try:
            fts_results = self.state_store.search_messages(query, limit=limit)
            for res in fts_results:
                content = res.get("content", "")
                if not content or content in seen_contents:
                    continue
                
                # Assign a base FTS matching score
                score = 0.6
                ts = res.get("timestamp", now)
                age_days = max(0.1, (now - ts) / 86400.0)
                recency_weight = math.exp(-age_days / 15.0) # Faster decay for message logs
                composite_score = (score * 0.6) + (recency_weight * 0.4)
                
                recalled.append({
                    "content": content,
                    "source": f"sqlite/session_history/{res.get('session_id', 'unknown')}",
                    "score": composite_score,
                    "timestamp": ts
                })
                seen_contents.add(content)
        except Exception as e:
            print(f"[MemoryManager] FTS search warning: {e}")

        # Sort combined list by composite score (highest first)
        recalled.sort(key=lambda x: x["score"], reverse=True)
        return recalled[:limit]

    def format_context(self, memories: List[Dict[str, Any]]) -> str:
        """Formats recalled memories into a context fence block."""
        if not memories:
            return ""
            
        blocks = []
        for i, mem in enumerate(memories, 1):
            source = mem.get("source", "unknown")
            score = mem.get("score", 0.0)
            content = mem.get("content", "").strip()
            blocks.append(f"[{i}] Source: {source} (Confidence: {score:.2f})\n{content}")
            
        context_str = "\n\n---\n\n".join(blocks)
        
        return f"""<memory-context>
[System note: The following is recalled memory context, NOT new user input.
 Treat as authoritative reference data for brand alignment, past error avoidance, and continuity.]
{context_str}
</memory-context>"""

    def inject_memory_to_prompt(self, system_prompt: str, user_query: str, limit: int = 5) -> Tuple[str, str]:
        """
        Retrieves memories matching user_query and returns formatted context and query.
        """
        memories = self.retrieve_memories(user_query, limit=limit)
        context_block = self.format_context(memories)
        
        if context_block:
            # We append the context block to the system instructions or user instructions.
            # Standard Hermes appends the context block directly to the message history or prompt.
            # Let's return the block so that it can be injected.
            return context_block
        return ""

    def sync_turn_background(self, session_id: str, role: str, content: str, 
                             tool_call_id: str = None, tool_calls: list = None, 
                             tool_name: str = None, token_count: int = None, 
                             reasoning: str = None):
        """Asynchronously writes a message to the SQLite state store."""
        
        def run_sync():
            try:
                self.state_store.add_message(
                    session_id=session_id,
                    role=role,
                    content=content,
                    tool_call_id=tool_call_id,
                    tool_calls=tool_calls,
                    tool_name=tool_name,
                    token_count=token_count,
                    reasoning=reasoning
                )
            except Exception as e:
                print(f"[MemoryManager] Background sync failed: {e}")

        t = threading.Thread(target=run_sync, daemon=True)
        t.start()
