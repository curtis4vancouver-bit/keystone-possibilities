"""
Keystone Working Memory v2.0 (Context Engram Protocol)
=======================================================
Fast, ephemeral key-value store for active task state, now with 3-tier
memory classification and Ebbinghaus-inspired staleness detection.

Tier 1 — SESSION:   Volatile workspace, cleared after task completion (TTL: 1-4h)
Tier 2 — EPISODIC:  Checkpoint-style resumption, execution traces (TTL: 24-48h)
Tier 3 — SEMANTIC:  Permanent distilled facts and operational rules (no expiry)

Agents write variables here during work; other agents read them on boot.
Entries auto-expire after a configurable TTL (default 24h).

Uses SQLite — zero dependencies, zero Docker, zero installs.

Research Source: 20260610_AGENT_ARCH_context_engram_protocol
Reference: Josselyn & Tonegawa (2020) — Memory engrams, Science 367

Usage (from Python):
    from working_memory import WorkingMemory
    wm = WorkingMemory()
    
    # Original API (unchanged):
    wm.set("video_id", "LNlAiAu5YOo", namespace="upload_task")
    wm.get("video_id", namespace="upload_task")  # -> "LNlAiAu5YOo"
    wm.list_active()                              # -> all active entries
    wm.clear_namespace("upload_task")             # -> wipe a finished task
    
    # NEW — Context Engram API:
    wm.mem_save("bc_step_code", "Section 9.36.4 — energy efficiency", tier="SEMANTIC")
    wm.mem_save("current_task", {"step": 3, "tool": "resolve"}, tier="SESSION")
    results = wm.mem_search("step code BC building")     # searches all tiers
    results = wm.mem_search("energy", tier="SEMANTIC")   # searches specific tier
    wm.consolidate()                                      # promotes episodic → semantic
    wm.decay_score("some_key")                            # Ebbinghaus staleness check

Usage (from CLI):
    python working_memory.py set video_id LNlAiAu5YOo --ns upload_task
    python working_memory.py get video_id --ns upload_task
    python working_memory.py list
    python working_memory.py clear --ns upload_task
    python working_memory.py prune
    python working_memory.py status
    python working_memory.py mem-save my_key "my value" --tier EPISODIC
    python working_memory.py mem-search "search query" --tier SEMANTIC
    python working_memory.py consolidate
    python working_memory.py decay-report
"""
import os
import sys
import json
import sqlite3
import hashlib
import math
import argparse
import datetime
from typing import Optional, List, Dict, Any

# Force UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(PROJECT_ROOT, ".learnings", "working_memory.db")
DEFAULT_TTL_HOURS = 24

# ─── Memory Tier Constants ───────────────────────────────────────────────
# Research Source: Context Engram Protocol — 3-tier graph memory architecture

class MemoryTier:
    """Memory classification tiers following the Context Engram Protocol."""
    SESSION = "SESSION"      # Volatile — cleared after task (TTL: 1-4h)
    EPISODIC = "EPISODIC"    # Checkpoint — execution traces (TTL: 24-48h)
    SEMANTIC = "SEMANTIC"    # Permanent — distilled facts (no expiry)

TIER_TTL_DEFAULTS = {
    MemoryTier.SESSION: 4,       # 4 hours
    MemoryTier.EPISODIC: 48,     # 48 hours
    MemoryTier.SEMANTIC: 876000, # ~100 years (effectively permanent)
}

# Ebbinghaus forgetting curve constants
# R = e^(-t/S) where t = time since last access, S = stability
EBBINGHAUS_BASE_STABILITY = {
    MemoryTier.SESSION: 1.0,    # Decays fast (hours)
    MemoryTier.EPISODIC: 24.0,  # Moderate decay (days)
    MemoryTier.SEMANTIC: 720.0, # Very slow decay (months)
}

# Consolidation threshold: minimum access_count for EPISODIC → SEMANTIC promotion
CONSOLIDATION_ACCESS_THRESHOLD = 3
# Consolidation threshold: minimum age in hours before eligible for promotion
CONSOLIDATION_AGE_THRESHOLD_HOURS = 12


class WorkingMemory:
    """Fast ephemeral key-value store with 3-tier Context Engram memory classification."""

    def __init__(self, db_path: str = DB_PATH, ttl_hours: int = DEFAULT_TTL_HOURS):
        self.db_path = db_path
        self.ttl_hours = ttl_hours
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
        self._migrate_schema()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS working_mem (
                key TEXT NOT NULL,
                namespace TEXT NOT NULL DEFAULT 'default',
                value TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                ttl_hours INTEGER DEFAULT 24,
                PRIMARY KEY (key, namespace)
            )
        """)
        conn.commit()
        conn.close()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ─── Schema Migration (v1.0 → v2.0) ─────────────────────────────────
    
    def _migrate_schema(self):
        """Adds tier, access_count, and content_hash columns if they don't exist yet.
        
        Safe to run repeatedly — uses PRAGMA table_info to check existing columns.
        Does NOT drop or recreate the table, preserving all existing data.
        """
        conn = self._conn()
        cursor = conn.execute("PRAGMA table_info(working_mem)")
        existing_columns = {row[1] for row in cursor.fetchall()}
        
        migrations = []
        if "tier" not in existing_columns:
            migrations.append("ALTER TABLE working_mem ADD COLUMN tier TEXT DEFAULT 'EPISODIC'")
        if "access_count" not in existing_columns:
            migrations.append("ALTER TABLE working_mem ADD COLUMN access_count INTEGER DEFAULT 0")
        if "content_hash" not in existing_columns:
            migrations.append("ALTER TABLE working_mem ADD COLUMN content_hash TEXT DEFAULT ''")
        
        for sql in migrations:
            try:
                conn.execute(sql)
            except sqlite3.OperationalError:
                pass  # Column already exists (race condition safety)
        
        if migrations:
            conn.commit()
            print(f"[WorkingMemory] Schema migrated v1.0 → v2.0 ({len(migrations)} columns added)")
        conn.close()

    # ─── Original API (Unchanged) ────────────────────────────────────────

    def set(self, key: str, value, namespace: str = "default", ttl_hours: int = None):
        """Write a key-value pair to working memory."""
        if ttl_hours is None:
            ttl_hours = self.ttl_hours

        # Serialize complex types to JSON
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        else:
            value = str(value)

        conn = self._conn()
        conn.execute("""
            INSERT INTO working_mem (key, namespace, value, updated_at, ttl_hours)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
            ON CONFLICT(key, namespace) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP,
                ttl_hours = excluded.ttl_hours
        """, (key, namespace, value, ttl_hours))
        conn.commit()
        conn.close()

    def get(self, key: str, namespace: str = "default") -> str:
        """Read a value from working memory. Returns None if expired or missing."""
        self._prune_expired()
        conn = self._conn()
        cursor = conn.execute(
            "SELECT value FROM working_mem WHERE key = ? AND namespace = ?",
            (key, namespace)
        )
        row = cursor.fetchone()
        
        # Increment access counter for engram tracking
        if row is not None:
            conn.execute(
                "UPDATE working_mem SET access_count = COALESCE(access_count, 0) + 1 WHERE key = ? AND namespace = ?",
                (key, namespace)
            )
            conn.commit()
        conn.close()

        if row is None:
            return None

        # Try to deserialize JSON
        val = row[0]
        try:
            return json.loads(val)
        except (json.JSONDecodeError, TypeError):
            return val

    def list_active(self, namespace: str = None) -> list:
        """List all active (non-expired) entries."""
        self._prune_expired()
        conn = self._conn()
        if namespace:
            cursor = conn.execute(
                "SELECT key, namespace, value, updated_at, ttl_hours FROM working_mem WHERE namespace = ? ORDER BY updated_at DESC",
                (namespace,)
            )
        else:
            cursor = conn.execute(
                "SELECT key, namespace, value, updated_at, ttl_hours FROM working_mem ORDER BY namespace, updated_at DESC"
            )
        rows = cursor.fetchall()
        conn.close()

        entries = []
        for key, ns, value, updated, ttl in rows:
            # Truncate long values for display
            display_val = value[:80] + "..." if len(value) > 80 else value
            entries.append({
                "key": key,
                "namespace": ns,
                "value": display_val,
                "updated_at": updated,
                "ttl_hours": ttl,
            })
        return entries

    def list_namespaces(self) -> list:
        """List all active namespaces."""
        conn = self._conn()
        cursor = conn.execute("SELECT DISTINCT namespace FROM working_mem")
        names = [row[0] for row in cursor.fetchall()]
        conn.close()
        return names

    def clear_namespace(self, namespace: str) -> int:
        """Wipe all entries for a completed task namespace."""
        conn = self._conn()
        cursor = conn.execute("DELETE FROM working_mem WHERE namespace = ?", (namespace,))
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted

    def clear_all(self) -> int:
        """Nuclear option — wipe everything."""
        conn = self._conn()
        cursor = conn.execute("DELETE FROM working_mem")
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted

    def _prune_expired(self) -> int:
        """Remove entries that have exceeded their TTL (skips SEMANTIC tier)."""
        conn = self._conn()
        cursor = conn.execute("""
            DELETE FROM working_mem
            WHERE datetime(updated_at, '+' || ttl_hours || ' hours') < datetime('now')
            AND COALESCE(tier, 'EPISODIC') != 'SEMANTIC'
        """)
        pruned = cursor.rowcount
        if pruned > 0:
            conn.commit()
        conn.close()
        return pruned

    def status(self) -> dict:
        """Quick health status of working memory."""
        pruned = self._prune_expired()
        conn = self._conn()
        total = conn.execute("SELECT COUNT(*) FROM working_mem").fetchone()[0]
        namespaces = conn.execute("SELECT COUNT(DISTINCT namespace) FROM working_mem").fetchone()[0]

        # Oldest entry
        oldest = conn.execute("SELECT MIN(updated_at) FROM working_mem").fetchone()[0]

        # Tier breakdown
        tier_counts = {}
        try:
            cursor = conn.execute("SELECT COALESCE(tier, 'EPISODIC') as t, COUNT(*) FROM working_mem GROUP BY t")
            for row in cursor.fetchall():
                tier_counts[row[0]] = row[1]
        except sqlite3.OperationalError:
            pass  # tier column doesn't exist yet

        # DB file size
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        conn.close()

        return {
            "total_entries": total,
            "active_namespaces": namespaces,
            "oldest_entry": oldest or "none",
            "expired_pruned": pruned,
            "db_size_kb": round(db_size / 1024, 1),
            "db_path": self.db_path,
            "tier_breakdown": tier_counts,
        }

    # ─── Context Engram API (v2.0) ───────────────────────────────────────
    # Research Source: 20260610_AGENT_ARCH_context_engram_protocol
    # Three-tier memory: SESSION → EPISODIC → SEMANTIC with Ebbinghaus decay

    def mem_save(self, key: str, value: Any, tier: str = "EPISODIC",
                 namespace: str = "default", ttl_hours: int = None) -> str:
        """
        Context Engram save — commits state to the local hybrid store.
        
        Generates a deterministic content hash for O(1) engram retrieval.
        Automatically assigns TTL based on memory tier if not specified.
        
        Args:
            key: Unique key for this memory
            value: Value to store (str, dict, list)
            tier: Memory tier — SESSION, EPISODIC, or SEMANTIC
            namespace: Namespace grouping (default: 'default')
            ttl_hours: Override TTL (otherwise uses tier defaults)
        
        Returns:
            Content hash (engram_hash) for this entry
        """
        # Validate tier
        tier = tier.upper()
        if tier not in (MemoryTier.SESSION, MemoryTier.EPISODIC, MemoryTier.SEMANTIC):
            tier = MemoryTier.EPISODIC
        
        # Apply tier-default TTL if not specified
        if ttl_hours is None:
            ttl_hours = TIER_TTL_DEFAULTS.get(tier, DEFAULT_TTL_HOURS)
        
        # Serialize complex types
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value)
        else:
            value_str = str(value)
        
        # Generate deterministic content hash
        content_hash = hashlib.sha256(f"{key}:{value_str}".encode('utf-8')).hexdigest()[:16]
        
        conn = self._conn()
        
        # Conflict-detection gate: check for existing engram
        cursor = conn.execute("SELECT content_hash FROM working_mem WHERE key = ? AND namespace = ?", (key, namespace))
        existing_row = cursor.fetchone()
        if existing_row and existing_row[0] != content_hash:
            print(f"[WorkingMemory] 🛡️ Staleness Prevention: Deprecating old engram hash {existing_row[0]} for new baseline {content_hash}")
        
        conn.execute("""
            INSERT INTO working_mem (key, namespace, value, updated_at, ttl_hours, tier, access_count, content_hash)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?, ?, 0, ?)
            ON CONFLICT(key, namespace) DO UPDATE SET
                value = excluded.value,
                updated_at = CURRENT_TIMESTAMP,
                ttl_hours = excluded.ttl_hours,
                tier = excluded.tier,
                content_hash = excluded.content_hash
        """, (key, namespace, value_str, ttl_hours, tier, content_hash))
        conn.commit()
        conn.close()
        
        return content_hash

    def mem_search(self, query: str, tier: str = None,
                   namespace: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Context Engram search — retrieves memories matching a query string.
        
        Performs substring matching against key and value fields.
        Filters by tier and/or namespace if specified.
        Results are ranked by access_count (most accessed first) and recency.
        
        Args:
            query: Search string to match against keys and values
            tier: Optional tier filter (SESSION, EPISODIC, SEMANTIC)
            namespace: Optional namespace filter
            limit: Maximum results to return (default 10)
        
        Returns:
            List of matching memory entries with decay scores
        """
        self._prune_expired()
        
        # Build query with optional filters
        conditions = ["(key LIKE ? OR value LIKE ?)"]
        params: list = [f"%{query}%", f"%{query}%"]
        
        if tier:
            tier = tier.upper()
            conditions.append("COALESCE(tier, 'EPISODIC') = ?")
            params.append(tier)
        
        if namespace:
            conditions.append("namespace = ?")
            params.append(namespace)
        
        where_clause = " AND ".join(conditions)
        
        conn = self._conn()
        cursor = conn.execute(f"""
            SELECT key, namespace, value, updated_at, ttl_hours,
                   COALESCE(tier, 'EPISODIC') as tier,
                   COALESCE(access_count, 0) as access_count,
                   COALESCE(content_hash, '') as content_hash
            FROM working_mem
            WHERE {where_clause}
            ORDER BY access_count DESC, updated_at DESC
            LIMIT ?
        """, params + [limit])
        
        rows = cursor.fetchall()
        
        # Increment access count for all matched entries
        for row in rows:
            conn.execute(
                "UPDATE working_mem SET access_count = COALESCE(access_count, 0) + 1 WHERE key = ? AND namespace = ?",
                (row[0], row[1])
            )
        if rows:
            conn.commit()
        conn.close()
        
        results = []
        for key, ns, value, updated, ttl, entry_tier, access_count, content_hash in rows:
            # Calculate Ebbinghaus decay score
            decay = self._calculate_decay(updated, entry_tier)
            
            # Try to deserialize JSON value
            try:
                parsed_value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                parsed_value = value
            
            results.append({
                "key": key,
                "namespace": ns,
                "value": parsed_value,
                "tier": entry_tier,
                "access_count": access_count,
                "updated_at": updated,
                "content_hash": content_hash,
                "decay_score": round(decay, 4),
                "is_stale": decay < 0.3,  # Below 30% retention = stale
            })
        
        return results

    def decay_score(self, key: str, namespace: str = "default") -> Optional[Dict[str, Any]]:
        """
        Calculate the Ebbinghaus-inspired staleness/decay score for a specific entry.
        
        Uses R = e^(-t/S) where:
          t = hours since last access
          S = stability factor based on tier and access frequency
        
        Returns:
            Dict with retention score (0.0-1.0), staleness assessment, and details
        """
        conn = self._conn()
        cursor = conn.execute(
            """SELECT key, value, updated_at, COALESCE(tier, 'EPISODIC') as tier,
                      COALESCE(access_count, 0) as access_count
               FROM working_mem WHERE key = ? AND namespace = ?""",
            (key, namespace)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row is None:
            return None
        
        _, value, updated_at, tier, access_count = row
        decay = self._calculate_decay(updated_at, tier, access_count)
        
        return {
            "key": key,
            "namespace": namespace,
            "tier": tier,
            "access_count": access_count,
            "updated_at": updated_at,
            "retention_score": round(decay, 4),
            "staleness": "FRESH" if decay > 0.7 else ("AGING" if decay > 0.3 else "STALE"),
            "recommendation": (
                "Keep" if decay > 0.5 else
                "Consider consolidating to SEMANTIC" if tier == MemoryTier.EPISODIC and access_count >= CONSOLIDATION_ACCESS_THRESHOLD else
                "Candidate for pruning"
            ),
        }

    def _calculate_decay(self, updated_at: str, tier: str, access_count: int = 0) -> float:
        """
        Ebbinghaus forgetting curve: R = e^(-t/S)
        
        Stability (S) is boosted by access_count — more frequent access = slower decay.
        """
        try:
            if isinstance(updated_at, str):
                last_access = datetime.datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            else:
                last_access = updated_at
            
            # Make both timezone-naive for comparison
            if last_access.tzinfo is not None:
                last_access = last_access.replace(tzinfo=None)
            
            hours_elapsed = (datetime.datetime.now() - last_access).total_seconds() / 3600.0
        except (ValueError, TypeError):
            hours_elapsed = 24.0  # Default assumption
        
        # Base stability from tier
        base_stability = EBBINGHAUS_BASE_STABILITY.get(tier, 24.0)
        
        # Boost stability by access frequency (each access adds 20% to stability)
        boosted_stability = base_stability * (1.0 + 0.2 * min(access_count, 10))
        
        # R = e^(-t/S)
        retention = math.exp(-hours_elapsed / boosted_stability)
        return max(0.0, min(1.0, retention))

    def consolidate(self) -> Dict[str, Any]:
        """
        Memory consolidation — promotes eligible EPISODIC memories to SEMANTIC tier.
        
        Promotion criteria:
          1. access_count >= CONSOLIDATION_ACCESS_THRESHOLD (frequently accessed)
          2. Age >= CONSOLIDATION_AGE_THRESHOLD_HOURS (not too new)
          3. Retention score > 0.3 (not completely forgotten)
        
        Also prunes stale SESSION entries.
        
        Returns:
            Report of promotions and pruning actions
        """
        conn = self._conn()
        
        # 1. Find EPISODIC entries eligible for promotion
        cursor = conn.execute("""
            SELECT key, namespace, value, updated_at,
                   COALESCE(access_count, 0) as access_count,
                   created_at
            FROM working_mem
            WHERE COALESCE(tier, 'EPISODIC') = 'EPISODIC'
            AND COALESCE(access_count, 0) >= ?
        """, (CONSOLIDATION_ACCESS_THRESHOLD,))
        
        candidates = cursor.fetchall()
        promoted = 0
        pruned_session = 0
        
        for key, namespace, value, updated_at, access_count, created_at in candidates:
            # Check age threshold
            try:
                if created_at:
                    created = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                    if created.tzinfo:
                        created = created.replace(tzinfo=None)
                    age_hours = (datetime.datetime.now() - created).total_seconds() / 3600.0
                else:
                    age_hours = CONSOLIDATION_AGE_THRESHOLD_HOURS + 1  # Assume eligible
            except (ValueError, TypeError):
                age_hours = CONSOLIDATION_AGE_THRESHOLD_HOURS + 1
            
            if age_hours < CONSOLIDATION_AGE_THRESHOLD_HOURS:
                continue
            
            # Check retention score
            decay = self._calculate_decay(updated_at, MemoryTier.EPISODIC, access_count)
            if decay < 0.3:
                continue
            
            # Promote to SEMANTIC
            conn.execute("""
                UPDATE working_mem
                SET tier = 'SEMANTIC',
                    ttl_hours = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE key = ? AND namespace = ?
            """, (TIER_TTL_DEFAULTS[MemoryTier.SEMANTIC], key, namespace))
            promoted += 1
            print(f"[WorkingMemory] 📈 Promoted EPISODIC → SEMANTIC: {namespace}:{key} (access_count={access_count})")
        
        # 2. Prune stale SESSION entries (decay < 0.1)
        session_cursor = conn.execute("""
            SELECT key, namespace, updated_at, COALESCE(access_count, 0)
            FROM working_mem
            WHERE COALESCE(tier, 'EPISODIC') = 'SESSION'
        """)
        
        for key, namespace, updated_at, access_count in session_cursor.fetchall():
            decay = self._calculate_decay(updated_at, MemoryTier.SESSION, access_count)
            if decay < 0.1:
                conn.execute("DELETE FROM working_mem WHERE key = ? AND namespace = ?", (key, namespace))
                pruned_session += 1
        
        conn.commit()
        conn.close()
        
        report = {
            "episodic_candidates": len(candidates),
            "promoted_to_semantic": promoted,
            "stale_sessions_pruned": pruned_session,
            "timestamp": datetime.datetime.now().isoformat(),
        }
        
        print(f"[WorkingMemory] Consolidation complete: {promoted} promoted, {pruned_session} sessions pruned")
        return report

    def decay_report(self) -> List[Dict[str, Any]]:
        """Generate a full decay report for all entries across all tiers."""
        conn = self._conn()
        cursor = conn.execute("""
            SELECT key, namespace, updated_at,
                   COALESCE(tier, 'EPISODIC') as tier,
                   COALESCE(access_count, 0) as access_count
            FROM working_mem
            ORDER BY tier, updated_at DESC
        """)
        rows = cursor.fetchall()
        conn.close()
        
        report = []
        for key, namespace, updated_at, tier, access_count in rows:
            decay = self._calculate_decay(updated_at, tier, access_count)
            report.append({
                "key": key,
                "namespace": namespace,
                "tier": tier,
                "access_count": access_count,
                "retention": round(decay, 4),
                "staleness": "FRESH" if decay > 0.7 else ("AGING" if decay > 0.3 else "STALE"),
            })
        return report


# ─── CLI Interface ───────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Keystone Working Memory v2.0 (Context Engram Protocol)")
    sub = parser.add_subparsers(dest="command")

    # set
    p_set = sub.add_parser("set", help="Write a key-value pair")
    p_set.add_argument("key", help="Key name")
    p_set.add_argument("value", help="Value to store")
    p_set.add_argument("--ns", default="default", help="Namespace (default: 'default')")
    p_set.add_argument("--ttl", type=int, default=24, help="TTL in hours (default: 24)")

    # get
    p_get = sub.add_parser("get", help="Read a value")
    p_get.add_argument("key", help="Key name")
    p_get.add_argument("--ns", default="default", help="Namespace")

    # list
    p_list = sub.add_parser("list", help="List all active entries")
    p_list.add_argument("--ns", default=None, help="Filter by namespace")

    # clear
    p_clear = sub.add_parser("clear", help="Clear a namespace")
    p_clear.add_argument("--ns", required=True, help="Namespace to clear")

    # prune
    sub.add_parser("prune", help="Remove expired entries")

    # status
    sub.add_parser("status", help="Show working memory health")

    # ─── NEW: Context Engram Commands ────────────────────────────────────

    # mem-save
    p_msave = sub.add_parser("mem-save", help="Save a memory with tier classification")
    p_msave.add_argument("key", help="Memory key")
    p_msave.add_argument("value", help="Value to store")
    p_msave.add_argument("--tier", default="EPISODIC", choices=["SESSION", "EPISODIC", "SEMANTIC"],
                         help="Memory tier (default: EPISODIC)")
    p_msave.add_argument("--ns", default="default", help="Namespace")
    p_msave.add_argument("--ttl", type=int, default=None, help="Override TTL in hours")

    # mem-search
    p_msearch = sub.add_parser("mem-search", help="Search memories across tiers")
    p_msearch.add_argument("query", help="Search query string")
    p_msearch.add_argument("--tier", default=None, choices=["SESSION", "EPISODIC", "SEMANTIC"],
                           help="Filter by tier")
    p_msearch.add_argument("--ns", default=None, help="Filter by namespace")
    p_msearch.add_argument("--limit", type=int, default=10, help="Max results")

    # consolidate
    sub.add_parser("consolidate", help="Promote eligible EPISODIC → SEMANTIC memories")

    # decay-report
    sub.add_parser("decay-report", help="Show decay/staleness report for all entries")

    args = parser.parse_args()
    wm = WorkingMemory()

    if args.command == "set":
        wm.set(args.key, args.value, namespace=args.ns, ttl_hours=args.ttl)
        print(f"[WorkingMemory] SET {args.ns}:{args.key} = {args.value} (TTL: {args.ttl}h)")

    elif args.command == "get":
        val = wm.get(args.key, namespace=args.ns)
        if val is not None:
            print(f"[WorkingMemory] {args.ns}:{args.key} = {val}")
        else:
            print(f"[WorkingMemory] {args.ns}:{args.key} = (not found or expired)")

    elif args.command == "list":
        entries = wm.list_active(namespace=args.ns)
        if entries:
            print(f"[WorkingMemory] {len(entries)} active entries:")
            for e in entries:
                print(f"  [{e['namespace']}] {e['key']} = {e['value']}  (updated: {e['updated_at']}, TTL: {e['ttl_hours']}h)")
        else:
            print("[WorkingMemory] No active entries.")

    elif args.command == "clear":
        deleted = wm.clear_namespace(args.ns)
        print(f"[WorkingMemory] Cleared {deleted} entries from namespace '{args.ns}'")

    elif args.command == "prune":
        pruned = wm._prune_expired()
        print(f"[WorkingMemory] Pruned {pruned} expired entries.")

    elif args.command == "status":
        s = wm.status()
        print(f"[WorkingMemory] Status:")
        print(f"  Active entries:    {s['total_entries']}")
        print(f"  Namespaces:        {s['active_namespaces']}")
        print(f"  Oldest entry:      {s['oldest_entry']}")
        print(f"  Just pruned:       {s['expired_pruned']} expired")
        print(f"  DB size:           {s['db_size_kb']} KB")
        print(f"  DB path:           {s['db_path']}")
        if s.get("tier_breakdown"):
            print(f"  Tier breakdown:    {json.dumps(s['tier_breakdown'])}")

    # ─── Context Engram Commands ─────────────────────────────────────────

    elif args.command == "mem-save":
        content_hash = wm.mem_save(args.key, args.value, tier=args.tier,
                                    namespace=args.ns, ttl_hours=args.ttl)
        print(f"[WorkingMemory] MEM_SAVE {args.tier}:{args.ns}:{args.key} (hash: {content_hash})")

    elif args.command == "mem-search":
        results = wm.mem_search(args.query, tier=args.tier, namespace=args.ns, limit=args.limit)
        if results:
            print(f"[WorkingMemory] {len(results)} matches for '{args.query}':")
            for r in results:
                stale_flag = " ⚠️STALE" if r["is_stale"] else ""
                val_preview = str(r["value"])[:60]
                print(f"  [{r['tier']}] {r['namespace']}:{r['key']} = {val_preview} "
                      f"(decay: {r['decay_score']}, accesses: {r['access_count']}{stale_flag})")
        else:
            print(f"[WorkingMemory] No matches for '{args.query}'")

    elif args.command == "consolidate":
        report = wm.consolidate()
        print(f"[WorkingMemory] Consolidation Report:")
        print(f"  Candidates evaluated: {report['episodic_candidates']}")
        print(f"  Promoted to SEMANTIC: {report['promoted_to_semantic']}")
        print(f"  Stale sessions pruned: {report['stale_sessions_pruned']}")

    elif args.command == "decay-report":
        report = wm.decay_report()
        if report:
            print(f"[WorkingMemory] Decay Report ({len(report)} entries):")
            for r in report:
                print(f"  [{r['tier']}] {r['namespace']}:{r['key']} — "
                      f"retention: {r['retention']}, status: {r['staleness']}, "
                      f"accesses: {r['access_count']}")
        else:
            print("[WorkingMemory] No entries to report.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

