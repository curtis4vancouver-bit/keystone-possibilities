import os
import sqlite3
import json
import time
import math
import re
from typing import Optional, Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "semantic_cache.db")

class SemanticCache:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite cache table and indexes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Core cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semantic_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL UNIQUE,
                normalized_query TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL
            )
        """)
        
        # Indexes for fast search
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_normalized ON semantic_cache(normalized_query)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_expires ON semantic_cache(expires_at)")
        
        conn.commit()
        conn.close()

    def _normalize_text(self, text: str) -> str:
        """Standardizes query casing, punctuation, and spacing to improve matching quality."""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = re.sub(r"[^\w\s]", "", text)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _get_tokens(self, text: str) -> List[str]:
        """Splits normalized text into a list of individual words/tokens."""
        return self._normalize_text(text).split()

    def _calculate_cosine_similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """Calculates token-level cosine similarity between two word sets."""
        if not tokens1 or not tokens2:
            return 0.0
            
        # Create vocabulary sets
        vec1: Dict[str, int] = {}
        vec2: Dict[str, int] = {}
        
        for t in tokens1:
            vec1[t] = vec1.get(t, 0) + 1
        for t in tokens2:
            vec2[t] = vec2.get(t, 0) + 1
            
        vocab = set(vec1.keys()).union(set(vec2.keys()))
        
        # Calculate dot product and magnitudes
        dot_product = 0.0
        mag1 = 0.0
        mag2 = 0.0
        
        for word in vocab:
            val1 = vec1.get(word, 0)
            val2 = vec2.get(word, 0)
            dot_product += val1 * val2
            mag1 += val1 * val1
            mag2 += val2 * val2
            
        mag1 = math.sqrt(mag1)
        mag2 = math.sqrt(mag2)
        
        if mag1 == 0.0 or mag2 == 0.0:
            return 0.0
            
        return dot_product / (mag1 * mag2)

    def get_cached_response(self, query: str, threshold: float = 0.75) -> Optional[str]:
        """
        Attempts to retrieve a cached response for the query.
        1. Checks for an exact match.
        2. Evaluates semantic cosine similarity on stored queries.
        Returns the response string if found and valid, otherwise None.
        """
        now = time.time()
        normalized_query = self._normalize_text(query)
        query_tokens = self._get_tokens(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # First: clean up expired cache entries to keep the DB compact
        cursor.execute("DELETE FROM semantic_cache WHERE expires_at < ?", (now,))
        conn.commit()
        
        # Try exact matching on normalized query first (O(1) look-up)
        cursor.execute(
            "SELECT response FROM semantic_cache WHERE normalized_query = ? AND expires_at >= ?",
            (normalized_query, now)
        )
        row = cursor.fetchone()
        if row:
            conn.close()
            print(f"[Semantic Cache] Exact Cache HIT for: '{query[:50]}...'")
            return row[0]
            
        # Second: evaluate semantic similarity on stored entries
        cursor.execute("SELECT query, response FROM semantic_cache WHERE expires_at >= ?", (now,))
        all_rows = cursor.fetchall()
        
        best_score = 0.0
        best_response = None
        best_matched_query = None
        
        for cached_query, response in all_rows:
            cached_tokens = self._get_tokens(cached_query)
            similarity = self._calculate_cosine_similarity(query_tokens, cached_tokens)
            
            if similarity > best_score:
                best_score = similarity
                best_response = response
                best_matched_query = cached_query
                
        conn.close()
        
        if best_score >= threshold:
            print(f"[Semantic Cache] Semantic Cache HIT (Score: {best_score:.4f}) matched with: '{best_matched_query[:50]}...'")
            return best_response
            
        print(f"[Semantic Cache] Cache MISS (Best similarity: {best_score:.4f})")
        return None

    def cache_response(self, query: str, response: str, ttl_seconds: int = 86400):
        """Stores a query-response pair in the semantic cache with a set TTL."""
        now = time.time()
        expires_at = now + ttl_seconds
        normalized_query = self._normalize_text(query)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                """
                INSERT OR REPLACE INTO semantic_cache (query, normalized_query, response, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (query, normalized_query, response, now, expires_at)
            )
            conn.commit()
            print(f"[Semantic Cache] Cached response successfully. TTL: {ttl_seconds}s")
        except Exception as e:
            print(f"[Semantic Cache] Error writing to cache: {str(e)}")
        finally:
            conn.close()

# Quick validation test
if __name__ == "__main__":
    cache = SemanticCache()
    
    # Store a test response
    test_query = "What is the best peptide stack for accelerating muscle recovery after custom building?"
    test_response = "Optimized Wolverine Stack: BPC-157 (250mcg BID) paired with TB-500 (2.5mg bi-weekly) for rapid tissue repair."
    
    cache.cache_response(test_query, test_response)
    
    # Test identical query
    res1 = cache.get_cached_response(test_query)
    print("Exact Match:", res1 == test_response)
    
    # Test semantically similar query
    similar_query = "peptide stack for custom building muscle recovery"
    res2 = cache.get_cached_response(similar_query, threshold=0.70)
    print("Semantic Match:", res2 == test_response)
