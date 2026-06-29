"""
Keystone Episodic Memory — SQLite FTS5
=======================================
Records exact conversation turns, task outcomes, and tool calls with timestamps.
Supports full-text search for temporal queries like "what did I do yesterday?"
that vector search cannot answer.

This complements the Qdrant vector brain:
- Qdrant = semantic search ("find documents about construction PM")  
- SQLite FTS5 = temporal/exact search ("what happened on June 12?")
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "episodic_memory.db"


def get_connection():
    """Get or create the episodic memory database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")  # Better concurrent read performance
    
    # Create tables if they don't exist
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS episodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
            agent_id TEXT DEFAULT 'chronos',
            action_type TEXT NOT NULL,  -- 'task_start', 'task_complete', 'tool_call', 'user_request', 'error', 'learning'
            namespace TEXT DEFAULT 'general',
            summary TEXT NOT NULL,
            details TEXT,  -- JSON blob for structured data
            outcome TEXT,  -- 'success', 'failure', 'partial', 'pending'
            risk_level TEXT DEFAULT 'LOW',  -- LOW, MEDIUM, HIGH
            session_id TEXT
        );
        
        -- FTS5 virtual table for full-text search
        CREATE VIRTUAL TABLE IF NOT EXISTS episodes_fts USING fts5(
            summary,
            details,
            action_type,
            namespace,
            content='episodes',
            content_rowid='id'
        );
        
        -- Triggers to keep FTS in sync
        CREATE TRIGGER IF NOT EXISTS episodes_ai AFTER INSERT ON episodes BEGIN
            INSERT INTO episodes_fts(rowid, summary, details, action_type, namespace)
            VALUES (new.id, new.summary, new.details, new.action_type, new.namespace);
        END;
        
        CREATE TRIGGER IF NOT EXISTS episodes_ad AFTER DELETE ON episodes BEGIN
            INSERT INTO episodes_fts(episodes_fts, rowid, summary, details, action_type, namespace)
            VALUES ('delete', old.id, old.summary, old.details, old.action_type, old.namespace);
        END;
        
        CREATE TRIGGER IF NOT EXISTS episodes_au AFTER UPDATE ON episodes BEGIN
            INSERT INTO episodes_fts(episodes_fts, rowid, summary, details, action_type, namespace)
            VALUES ('delete', old.id, old.summary, old.details, old.action_type, old.namespace);
            INSERT INTO episodes_fts(rowid, summary, details, action_type, namespace)
            VALUES (new.id, new.summary, new.details, new.action_type, new.namespace);
        END;
        
        -- Index for temporal queries
        CREATE INDEX IF NOT EXISTS idx_episodes_timestamp ON episodes(timestamp);
        CREATE INDEX IF NOT EXISTS idx_episodes_agent ON episodes(agent_id);
        CREATE INDEX IF NOT EXISTS idx_episodes_action ON episodes(action_type);
        CREATE INDEX IF NOT EXISTS idx_episodes_namespace ON episodes(namespace);
    """)
    
    return conn


def record_episode(
    action_type: str,
    summary: str,
    details: dict = None,
    namespace: str = "general",
    agent_id: str = "chronos",
    outcome: str = None,
    risk_level: str = "LOW",
    session_id: str = None,
):
    """Record a new episode to the episodic memory."""
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO episodes (agent_id, action_type, namespace, summary, details, outcome, risk_level, session_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                agent_id,
                action_type,
                namespace,
                summary,
                json.dumps(details) if details else None,
                outcome,
                risk_level,
                session_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def search_episodes(query: str, limit: int = 10):
    """Full-text search across episodic memory."""
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT e.id, e.timestamp, e.agent_id, e.action_type, e.namespace, 
                      e.summary, e.outcome, e.risk_level
               FROM episodes e
               JOIN episodes_fts f ON e.id = f.rowid
               WHERE episodes_fts MATCH ?
               ORDER BY rank
               LIMIT ?""",
            (query, limit),
        ).fetchall()
        return [
            {
                "id": r[0], "timestamp": r[1], "agent_id": r[2],
                "action_type": r[3], "namespace": r[4], "summary": r[5],
                "outcome": r[6], "risk_level": r[7],
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_recent_episodes(hours: int = 24, limit: int = 20):
    """Get episodes from the last N hours."""
    conn = get_connection()
    try:
        cutoff = (datetime.utcnow() - timedelta(hours=hours)).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = conn.execute(
            """SELECT id, timestamp, agent_id, action_type, namespace, summary, outcome, risk_level
               FROM episodes
               WHERE timestamp >= ?
               ORDER BY timestamp DESC
               LIMIT ?""",
            (cutoff, limit),
        ).fetchall()
        return [
            {
                "id": r[0], "timestamp": r[1], "agent_id": r[2],
                "action_type": r[3], "namespace": r[4], "summary": r[5],
                "outcome": r[6], "risk_level": r[7],
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_episodes_by_date(date_str: str, limit: int = 50):
    """Get all episodes for a specific date (YYYY-MM-DD format)."""
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT id, timestamp, agent_id, action_type, namespace, summary, outcome, risk_level
               FROM episodes
               WHERE timestamp LIKE ? || '%'
               ORDER BY timestamp ASC
               LIMIT ?""",
            (date_str, limit),
        ).fetchall()
        return [
            {
                "id": r[0], "timestamp": r[1], "agent_id": r[2],
                "action_type": r[3], "namespace": r[4], "summary": r[5],
                "outcome": r[6], "risk_level": r[7],
            }
            for r in rows
        ]
    finally:
        conn.close()


def get_failure_log(limit: int = 10):
    """Get recent failures for self-healing analysis."""
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT id, timestamp, agent_id, action_type, namespace, summary, details, risk_level
               FROM episodes
               WHERE outcome = 'failure'
               ORDER BY timestamp DESC
               LIMIT ?""",
            (limit,),
        ).fetchall()
        return [
            {
                "id": r[0], "timestamp": r[1], "agent_id": r[2],
                "action_type": r[3], "namespace": r[4], "summary": r[5],
                "details": json.loads(r[6]) if r[6] else None,
                "risk_level": r[7],
            }
            for r in rows
        ]
    finally:
        conn.close()


def prune_old_episodes(days: int = 90):
    """Remove episodes older than N days to bound memory footprint."""
    conn = get_connection()
    try:
        cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
        result = conn.execute("DELETE FROM episodes WHERE timestamp < ?", (cutoff,))
        deleted = result.rowcount
        conn.commit()
        return deleted
    finally:
        conn.close()


# Self-test on import
if __name__ == "__main__":
    print(f"Episodic Memory DB: {DB_PATH}")
    
    # Record a test episode
    record_episode(
        action_type="task_complete",
        summary="Qdrant unified collection migration completed - 14,258 vectors merged from 29 collections",
        details={
            "vectors_migrated": 14258,
            "collections_merged": 29,
            "collections_deleted": 29,
            "config": {"m": 0, "payload_m": 16, "is_tenant": True},
        },
        namespace="self_healing",
        outcome="success",
        risk_level="HIGH",
    )
    
    record_episode(
        action_type="task_complete",
        summary="MCP server rewritten to use unified collection with tenant_id filtering",
        details={"file": "keystone_brain_v2_mcp.py", "api": "query_points"},
        namespace="self_healing",
        outcome="success",
    )
    
    # Test search
    results = search_episodes("Qdrant migration")
    print(f"\nSearch 'Qdrant migration': {len(results)} results")
    for r in results:
        print(f"  [{r['timestamp']}] {r['summary'][:80]}")
    
    # Test recent
    recent = get_recent_episodes(hours=1)
    print(f"\nLast 1 hour: {len(recent)} episodes")
    for r in recent:
        print(f"  [{r['timestamp']}] {r['action_type']}: {r['summary'][:80]}")
    
    print("\nDone!")
