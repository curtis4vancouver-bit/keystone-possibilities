import uuid
import math
from datetime import datetime, timezone
from qdrant_client import models

class WorkingLayer:
    name = "working"
    def __init__(self, session_id: str):
        self.session_id = session_id
        
class EpisodicLayer:
    name = "episodic"
    def __init__(self, source_id: str, namespace: str):
        self.source_id = source_id
        self.namespace = namespace

class SemanticLayer:
    name = "semantic"
    def __init__(self, source_id: str, namespace: str):
        self.source_id = source_id
        self.namespace = namespace

class ProceduralLayer:
    name = "procedural"
    def __init__(self, skill_name: str, version: str):
        self.skill_name = skill_name
        self.version = version

class MemoryManager:
    def __init__(self, client, collection_name, embed_model, vector_name, sparse_embed_model=None, sparse_vector_name=None):
        self.client = client
        self.collection_name = collection_name
        self.embed_model = embed_model
        self.vector_name = vector_name
        self.sparse_embed_model = sparse_embed_model
        self.sparse_vector_name = sparse_vector_name

    def _markdown_aware_chunk(self, text: str, max_size: int = 1500) -> list[str]:
        chunks = []
        current_chunk = []
        current_size = 0
        for line in text.split('\n'):
            if line.startswith('#') and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = len(line)
            elif current_size + len(line) > max_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = len(line)
            else:
                current_chunk.append(line)
                current_size += len(line)
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        return chunks

    def _embed_and_upsert(self, docs: list[str], layer_name: str, payload_base: dict, namespace: str):
        if not docs:
            return 0
            
        now_iso = datetime.utcnow().isoformat() + "Z"
        brand = f"Keystone | {namespace}"
        clean_source = payload_base.get("source", "unknown").replace('.md', '').replace('_', ' ')
        context_prefix = f"[{brand} | Source: {clean_source} | Layer: {layer_name}]"
        enriched_docs = [f"{context_prefix} {doc}" for doc in docs]
        
        embeddings = list(self.embed_model.embed(enriched_docs))
        
        sparse_embeddings = None
        if self.sparse_embed_model is not None:
            try:
                sparse_embeddings = list(self.sparse_embed_model.embed(enriched_docs))
            except Exception:
                pass
                
        points = []
        for i, (doc_text, embedding) in enumerate(zip(docs, embeddings)):
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{layer_name}:{payload_base.get('source', '')}:{payload_base.get('session_id', '')}:{i}"))
            
            vec_dict = {self.vector_name: embedding.tolist()}
            if sparse_embeddings is not None:
                svec = sparse_embeddings[i]
                vec_dict[self.sparse_vector_name] = models.SparseVector(
                    indices=svec.indices.tolist(),
                    values=svec.values.tolist(),
                )
                
            payload = payload_base.copy()
            payload["memory_layer"] = layer_name
            payload["tenant_id"] = namespace
            payload["chunk_index"] = i
            payload["created_at"] = now_iso
            payload["document"] = doc_text
            
            points.append(
                models.PointStruct(
                    id=point_id,
                    payload=payload,
                    vector=vec_dict,
                )
            )
            
        self.client.upsert(collection_name=self.collection_name, points=points)
        return len(points)

    def store_working(self, content: str, session_id: str):
        docs = self._markdown_aware_chunk(content)
        payload = {"session_id": session_id, "ttl": 3600 * 24}
        return self._embed_and_upsert(docs, WorkingLayer.name, payload, namespace="working_memory")

    def store_episodic(self, content: str, source_id: str, namespace: str):
        docs = self._markdown_aware_chunk(content)
        payload = {"source": source_id}
        return self._embed_and_upsert(docs, EpisodicLayer.name, payload, namespace)

    def store_semantic(self, content: str, source_id: str, namespace: str):
        docs = self._markdown_aware_chunk(content)
        payload = {"source": source_id}
        return self._embed_and_upsert(docs, SemanticLayer.name, payload, namespace)

    def store_procedural(self, content: str, skill_name: str, version: str):
        docs = self._markdown_aware_chunk(content)
        payload = {"source": skill_name, "version": version}
        return self._embed_and_upsert(docs, ProceduralLayer.name, payload, namespace="procedural")

    def search_with_decay(self, query: str, namespace: str, limit: int = 5, layer: str = None):
        query_vector = list(self.embed_model.embed([query]))[0]
        
        must_conds = []
        if namespace and namespace != "auto":
            must_conds.append(models.FieldCondition(key="tenant_id", match=models.MatchValue(value=namespace)))
        if layer:
            must_conds.append(models.FieldCondition(key="memory_layer", match=models.MatchValue(value=layer)))
            
        scroll_filter = models.Filter(must=must_conds) if must_conds else None
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=(self.vector_name, query_vector.tolist()),
            query_filter=scroll_filter,
            limit=limit * 2,
            with_payload=True
        )
        
        now = datetime.utcnow()
        decayed_results = []
        for res in results:
            score = res.score
            if res.payload and res.payload.get("memory_layer") == "episodic":
                created_at = res.payload.get("created_at")
                if created_at:
                    try:
                        created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00")).replace(tzinfo=None)
                        age_days = (now - created_dt).total_seconds() / (24 * 3600)
                        decay_factor = math.exp(-age_days / 30.0)
                        score *= decay_factor
                    except ValueError:
                        pass
            decayed_results.append((res, score))
            
        decayed_results.sort(key=lambda x: x[1], reverse=True)
        return decayed_results[:limit]

    def promote_memory(self, point_id: str, to_layer: str):
        records = self.client.retrieve(collection_name=self.collection_name, ids=[point_id], with_payload=True)
        if not records:
            return False
        
        payload = records[0].payload
        payload["memory_layer"] = to_layer
        self.client.set_payload(
            collection_name=self.collection_name,
            payload=payload,
            points=[point_id]
        )
        return True

    def cleanup_working(self, session_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(key="memory_layer", match=models.MatchValue(value="working")),
                        models.FieldCondition(key="session_id", match=models.MatchValue(value=session_id))
                    ]
                )
            )
        )

    def decay_episodic(self):
        offset = None
        now = datetime.utcnow()
        deleted = 0
        promoted = 0
        
        while True:
            records, next_offset = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=models.Filter(
                    must=[models.FieldCondition(key="memory_layer", match=models.MatchValue(value="episodic"))]
                ),
                limit=100,
                with_payload=True,
                with_vectors=False,
                offset=offset
            )
            
            for record in records:
                created_at = record.payload.get("created_at")
                if created_at:
                    try:
                        created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00")).replace(tzinfo=None)
                        age_days = (now - created_dt).total_seconds() / (24 * 3600)
                        
                        if age_days > 30:
                            self.client.delete(collection_name=self.collection_name, points_selector=[record.id])
                            deleted += 1
                    except ValueError:
                        pass
                        
            if next_offset is None:
                break
            offset = next_offset
            
        return deleted, promoted
