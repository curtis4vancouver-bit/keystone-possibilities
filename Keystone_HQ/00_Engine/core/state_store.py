import os
import sqlite3
import time
import random
import threading
import json
from typing import Dict, Any, List, Optional, Tuple

class StateStore:
    """
    SQLite-backed thread-safe state store for agent sessions and message history.
    Implements WAL mode, FTS5 full-text indexing, write-contention retries with jitter,
    and automatic database repair.
    """
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Establishes connection and configures WAL mode and timeouts."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        # Enable WAL mode and foreign keys
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        return conn

    def _execute_write(self, query: str, params: tuple = (), retries: int = 15) -> sqlite3.Cursor:
        """Executes a write query with exponential backoff + jitter for handling contention."""
        last_err = None
        for attempt in range(retries):
            try:
                with self.lock:
                    with self._get_connection() as conn:
                        cursor = conn.execute(query, params)
                        conn.commit()
                        return cursor
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() or "busy" in str(e).lower():
                    last_err = e
                    # Jitter sleep: 20ms to 150ms
                    sleep_time = random.uniform(0.020, 0.150)
                    time.sleep(sleep_time)
                else:
                    raise e
        raise sqlite3.OperationalError(f"Database locked after {retries} retries. Original error: {last_err}")

    def _init_db(self):
        """Initializes tables, indexes, and triggers for FTS5 full-text indexing."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # 1. Create Core Tables
        sessions_schema = """
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            user_id TEXT,
            model TEXT,
            system_prompt TEXT,
            parent_session_id TEXT,
            started_at REAL,
            ended_at REAL,
            end_reason TEXT,
            message_count INTEGER DEFAULT 0,
            tool_call_count INTEGER DEFAULT 0,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            title TEXT,
            archived INTEGER DEFAULT 0
        );
        """
        
        messages_schema = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT REFERENCES sessions(id) ON DELETE CASCADE,
            role TEXT NOT NULL,
            content TEXT,
            tool_call_id TEXT,
            tool_calls TEXT,
            tool_name TEXT,
            timestamp REAL,
            token_count INTEGER,
            reasoning TEXT,
            active INTEGER DEFAULT 1
        );
        """
        
        fts_schema = """
        CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
            content,
            session_id UNINDEXED,
            role UNINDEXED,
            timestamp UNINDEXED,
            content='messages',
            content_rowid='id'
        );
        """

        # Triggers to keep FTS table in sync
        trigger_insert = """
        CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages BEGIN
            INSERT INTO messages_fts(rowid, content, session_id, role, timestamp)
            VALUES (new.id, new.content, new.session_id, new.role, new.timestamp);
        END;
        """
        
        trigger_delete = """
        CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages BEGIN
            INSERT INTO messages_fts(messages_fts, rowid, content, session_id, role, timestamp)
            VALUES('delete', old.id, old.content, old.session_id, old.role, old.timestamp);
        END;
        """
        
        trigger_update = """
        CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages BEGIN
            INSERT INTO messages_fts(messages_fts, rowid, content, session_id, role, timestamp)
            VALUES('delete', old.id, old.content, old.session_id, old.role, old.timestamp);
            INSERT INTO messages_fts(rowid, content, session_id, role, timestamp)
            VALUES (new.id, new.content, new.session_id, new.role, new.timestamp);
        END;
        """

        with self.lock:
            with self._get_connection() as conn:
                conn.execute(sessions_schema)
                conn.execute(messages_schema)
                conn.execute(fts_schema)
                conn.execute(trigger_insert)
                conn.execute(trigger_delete)
                conn.execute(trigger_update)
                conn.commit()

    def create_session(self, session_id: str, source: str = "cli", user_id: str = None, 
                       model: str = None, system_prompt: str = None, parent_session_id: str = None) -> str:
        """Creates a new session in the database."""
        query = """
        INSERT INTO sessions (id, source, user_id, model, system_prompt, parent_session_id, started_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            source=excluded.source, model=excluded.model, system_prompt=excluded.system_prompt;
        """
        self._execute_write(query, (session_id, source, user_id, model, system_prompt, parent_session_id, time.time()))
        return session_id

    def add_message(self, session_id: str, role: str, content: str, tool_call_id: str = None,
                    tool_calls: list = None, tool_name: str = None, token_count: int = None, 
                    reasoning: str = None) -> int:
        """Adds a message to the history. Updates session metrics automatically."""
        tool_calls_json = json.dumps(tool_calls) if tool_calls else None
        query = """
        INSERT INTO messages (session_id, role, content, tool_call_id, tool_calls, tool_name, timestamp, token_count, reasoning)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self._execute_write(query, (session_id, role, content, tool_call_id, tool_calls_json, tool_name, time.time(), token_count, reasoning))
        msg_id = cursor.lastrowid
        
        # Update session telemetry counters
        is_tool = 1 if role == "tool" or tool_name else 0
        update_session_query = """
        UPDATE sessions 
        SET message_count = message_count + 1,
            tool_call_count = tool_call_count + ?
        WHERE id = ?
        """
        self._execute_write(update_session_query, (is_tool, session_id))
        return msg_id

    def search_messages(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Queries the FTS5 full-text index across all messages."""
        sql = """
        SELECT m.id, m.session_id, m.role, m.content, m.timestamp, s.title as session_title
        FROM messages_fts f
        JOIN messages m ON m.id = f.rowid
        LEFT JOIN sessions s ON s.id = m.session_id
        WHERE messages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
        """
        with self.lock:
            with self._get_connection() as conn:
                cursor = conn.execute(sql, (query, limit))
                return [dict(row) for row in cursor.fetchall()]

    def get_session_chain(self, session_id: str) -> List[Dict[str, Any]]:
        """Traverses parent session IDs to assemble the full session lineage chain."""
        chain = []
        current_id = session_id
        
        with self.lock:
            with self._get_connection() as conn:
                while current_id:
                    cursor = conn.execute("SELECT * FROM sessions WHERE id = ?", (current_id,))
                    row = cursor.fetchone()
                    if not row:
                        break
                    session_info = dict(row)
                    chain.append(session_info)
                    current_id = session_info.get("parent_session_id")
        return list(reversed(chain))

    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieves recent sessions sorted by startup time."""
        sql = "SELECT * FROM sessions WHERE archived = 0 ORDER BY started_at DESC LIMIT ?"
        with self.lock:
            with self._get_connection() as conn:
                cursor = conn.execute(sql, (limit,))
                return [dict(row) for row in cursor.fetchall()]

    def close_session(self, session_id: str, end_reason: str = "normal", title: str = None):
        """Closes a session and stamps the end time and reason."""
        query = "UPDATE sessions SET ended_at = ?, end_reason = ?, title = ? WHERE id = ?"
        self._execute_write(query, (time.time(), end_reason, title, session_id))

    def repair_database(self):
        """Self-healing: creates backup, drops FTS index, vacuums, and rebuilds FTS."""
        backup_path = f"{self.db_path}.{int(time.time())}.bak"
        print(f"[StateStore] [Repair] Initiating DB self-repair. Backing up to {backup_path}...")
        
        with self.lock:
            # Create backup
            with self._get_connection() as conn:
                backup_conn = sqlite3.connect(backup_path)
                conn.backup(backup_conn)
                backup_conn.close()
            
            # Rebuild FTS
            conn = self._get_connection()
            try:
                conn.isolation_level = None  # Autocommit mode
                conn.execute("DROP TABLE IF EXISTS messages_fts;")
                conn.execute("""
                CREATE VIRTUAL TABLE messages_fts USING fts5(
                    content, session_id UNINDEXED, role UNINDEXED, timestamp UNINDEXED,
                    content='messages', content_rowid='id'
                );
                """)
                conn.execute("INSERT INTO messages_fts(messages_fts) VALUES('rebuild');")
                conn.execute("VACUUM;")
                print("[StateStore] DB self-repair and indexing rebuilt successfully.")
            finally:
                conn.close()
