import uuid
from qdrant_client import models

class SandboxContext:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.active_sandboxes = {}

    def create_sandbox(self, name: str, parent_namespace: str) -> str:
        sandbox_id = f"{parent_namespace}_sandbox_{name}_{str(uuid.uuid4())[:8]}"
        self.active_sandboxes[sandbox_id] = {
            "parent": parent_namespace
        }
        return sandbox_id

    def commit_sandbox(self, sandbox_id: str) -> bool:
        if sandbox_id not in self.active_sandboxes:
            if "_sandbox_" in sandbox_id:
                parent = sandbox_id.split("_sandbox_")[0]
            else:
                return False
        else:
            parent = self.active_sandboxes[sandbox_id]["parent"]
        
        client = self.memory_manager.client
        collection_name = self.memory_manager.collection_name
        
        offset = None
        count = 0
        while True:
            records, next_offset = client.scroll(
                collection_name=collection_name,
                scroll_filter=models.Filter(
                    must=[models.FieldCondition(key="tenant_id", match=models.MatchValue(value=sandbox_id))]
                ),
                limit=100,
                with_payload=True,
                with_vectors=False
            )
            for rec in records:
                payload = rec.payload
                payload["tenant_id"] = parent
                client.set_payload(collection_name=collection_name, payload=payload, points=[rec.id])
                count += 1
                
            if next_offset is None:
                break
            offset = next_offset
            
        if sandbox_id in self.active_sandboxes:
            del self.active_sandboxes[sandbox_id]
        return True

    def rollback_sandbox(self, sandbox_id: str) -> bool:
        client = self.memory_manager.client
        collection_name = self.memory_manager.collection_name
        
        client.delete(
            collection_name=collection_name,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[models.FieldCondition(key="tenant_id", match=models.MatchValue(value=sandbox_id))]
                )
            )
        )
        if sandbox_id in self.active_sandboxes:
            del self.active_sandboxes[sandbox_id]
        return True

