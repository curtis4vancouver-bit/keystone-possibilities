import json
import os
import time
from typing import Dict, Any, List, Optional
from core.state_store import StateStore

class SelfKnowledgeManager:
    """
    Manages agent self-modeling, self-correction registry, and dynamic rule loading.
    Synchronizes flat correction journals into the persistent state store.
    """
    def __init__(self, state_store: StateStore):
        self.state_store = state_store
        self._init_table()

    def _init_table(self):
        """Creates self-knowledge tables in SQLite."""
        schema = """
        CREATE TABLE IF NOT EXISTS self_knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tendency TEXT NOT NULL,
            correction TEXT NOT NULL,
            context TEXT,
            timestamp REAL,
            access_count INTEGER DEFAULT 0
        );
        """
        self.state_store._execute_write(schema)

    def sync_journal_to_db(self, journal_path: str):
        """
        Synchronizes existing correction journal entries from a flat JSON file
        into the SQLite state store.
        """
        if not os.path.exists(journal_path):
            return

        try:
            with open(journal_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            entries = data.get("entries", [])
            
            for entry in entries:
                # Map old structure to self-knowledge schema
                error_type = entry.get("error_type", entry.get("category", "unknown"))
                fix_description = entry.get("fix_description", entry.get("fix", entry.get("fix_applied", "")))
                original_context = entry.get("original_context", entry.get("description", ""))
                
                # Check if this correction already exists in the database
                check_sql = "SELECT id FROM self_knowledge WHERE tendency = ? AND correction = ?"
                with self.state_store.lock:
                    with self.state_store._get_connection() as conn:
                        cursor = conn.execute(check_sql, (error_type, fix_description))
                        exists = cursor.fetchone() is not None
                
                if not exists:
                    insert_sql = """
                    INSERT INTO self_knowledge (tendency, correction, context, timestamp)
                    VALUES (?, ?, ?, ?)
                    """
                    self.state_store._execute_write(insert_sql, (error_type, fix_description, original_context, time.time()))
                    
            print(f"[SelfKnowledge] Synced {len(entries)} correction journal entries to SQLite.")
        except Exception as e:
            print(f"[SelfKnowledge] Error syncing correction journal: {e}")

    def record_self_correction(self, tendency: str, correction: str, context: str = None) -> int:
        """Records a new behavioral self-correction directive."""
        query = """
        INSERT INTO self_knowledge (tendency, correction, context, timestamp)
        VALUES (?, ?, ?, ?)
        """
        cursor = self.state_store._execute_write(query, (tendency, correction, context, time.time()))
        return cursor.lastrowid

    def get_rules_prompt(self, limit: int = 15) -> str:
        """
        Compiles the recorded self-corrections into a formatted system prompt block.
        Ensures the agent is fed its own lessons dynamically on startup.
        """
        sql = "SELECT tendency, correction, context FROM self_knowledge ORDER BY id DESC LIMIT ?"
        
        with self.state_store.lock:
            with self.state_store._get_connection() as conn:
                cursor = conn.execute(sql, (limit,))
                rules = [dict(row) for row in cursor.fetchall()]

        if not rules:
            return ""

        prompt_lines = [
            "\n<self-knowledge-directives>",
            "[System Directive: You must adhere to the following learned behavioral rules based on past execution reviews.]"
        ]
        
        for i, rule in enumerate(rules, 1):
            tendency = rule.get("tendency", "")
            correction = rule.get("correction", "")
            ctx = rule.get("context", "")
            context_str = f" in context '{ctx}'" if ctx else ""
            prompt_lines.append(f"{i}. Avoid tendency '{tendency}'{context_str}. Correction: {correction}")
            
        prompt_lines.append("</self-knowledge-directives>\n")
        return "\n".join(prompt_lines)

    def self_audit(self, query: str) -> List[Dict[str, Any]]:
        """Queries self-knowledge database to check if past fixes match query terms."""
        sql = """
        SELECT tendency, correction, context 
        FROM self_knowledge 
        WHERE tendency LIKE ? OR correction LIKE ? OR context LIKE ?
        ORDER BY id DESC
        """
        like_pattern = f"%{query}%"
        
        with self.state_store.lock:
            with self.state_store._get_connection() as conn:
                cursor = conn.execute(sql, (like_pattern, like_pattern, like_pattern))
                return [dict(row) for row in cursor.fetchall()]
