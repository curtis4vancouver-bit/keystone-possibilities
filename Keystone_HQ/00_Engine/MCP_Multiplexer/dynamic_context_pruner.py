import json
import numpy as np

class DynamicContextPruner:
    """
    Implements a simplified version of Kadane's Algorithm for Dialogue (KadaneDial)
    to truncate log bloat and maintain dense semantic contexts.
    """
    def __init__(self, threshold=0.6):
        self.threshold = threshold

    def _mock_relevance_score(self, message: dict, current_query: str) -> float:
        """
        In production, this embeds the message and query to calculate cosine similarity.
        For now, returns a synthetic score based on string matching and length.
        """
        content = message.get("content", "").lower()
        query_terms = set(current_query.lower().split())
        
        # Penalize massive system logs or dumps
        if len(content) > 2000 and "traceback" not in content and "error" not in content:
            return 0.2
            
        score = 0.5
        for term in query_terms:
            if term in content:
                score += 0.1
                
        return min(1.0, score)

    def prune_context(self, history: list, current_query: str) -> list:
        """
        Scans historical turns and extracts contiguous spans of high relevance,
        compressing or stripping irrelevant logs to save tokens and credits.
        """
        if not history:
            return []

        pruned = []
        for msg in history:
            role = msg.get("role", "")
            # Always keep system prompts and the most recent few messages
            if role == "system" or msg == history[-1] or msg == history[-2]:
                pruned.append(msg)
                continue

            score = self._mock_relevance_score(msg, current_query)
            if score >= self.threshold:
                pruned.append(msg)
            else:
                # Replace massive irrelevant logs with a compressed placeholder
                if len(msg.get("content", "")) > 500:
                    compressed_msg = {
                        "role": role,
                        "content": f"[{role.upper()} LOG COMPRESSED BY KADANE-DIAL PRUNER]"
                    }
                    pruned.append(compressed_msg)
                else:
                    pruned.append(msg)
                    
        return pruned

# Example usage
if __name__ == "__main__":
    pruner = DynamicContextPruner(threshold=0.6)
    dummy_history = [
        {"role": "system", "content": "You are Hermes, a sovereign AI."},
        {"role": "user", "content": "Run the audit."},
        {"role": "tool", "content": "SUCCESS: Output of 10000 lines of console logs..."},
        {"role": "user", "content": "What is the result of the database architecture?"}
    ]
    optimized = pruner.prune_context(dummy_history, "database architecture")
    print("Pruned Payload:")
    print(json.dumps(optimized, indent=2))
