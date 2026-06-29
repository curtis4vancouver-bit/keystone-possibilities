import json
import re
import time
from typing import List, Dict, Any, Tuple, Optional
from core.state_store import StateStore

class ConversationCompressor:
    """
    Three-tier context compaction engine designed to manage context window pressure
    by pruning tool outputs, performing middle-window summarizations, and tracking effectiveness.
    """
    def __init__(self, state_store: StateStore, model_client: Any = None):
        self.state_store = state_store
        self.model_client = model_client  # Optional Google GenAI client
        self.ineffective_count = 0
        self.last_saved_ratio = 0.0

    def prune_tool_output(self, tool_name: str, output: str) -> str:
        """
        Tier 1: Prunes verbose tool outputs without using an LLM.
        Replaces long stdout or files read with concise execution metadata summaries.
        """
        if not output:
            return ""
        
        output_len = len(output)
        if output_len < 300:
            return output  # Skip pruning for small outputs
            
        # Common pruning templates based on tool names
        if tool_name in ("run_command", "execute_command"):
            # Extract exit code or last line
            lines = [l.strip() for l in output.split("\n") if l.strip()]
            exit_code = 0
            if "exit code" in output.lower():
                match = re.search(r"exit code:?\s*(\d+)", output, re.IGNORECASE)
                if match:
                    exit_code = int(match.group(1))
            last_lines = "\n".join(lines[-3:]) if len(lines) >= 3 else output
            return f"[Pruned Stdio] Tool '{tool_name}' completed (Exit Code: {exit_code}, {output_len} chars output).\nLast lines:\n{last_lines}"
            
        elif tool_name in ("view_file", "read_file"):
            return f"[Pruned File Read] Tool '{tool_name}' read file content ({output_len} chars total, first 100 chars: '{output[:100].strip()}...')"
            
        elif tool_name in ("grep_search", "search_files", "search_master_brain"):
            # Count result blocks
            matches_count = len(re.findall(r"Result \d+|match|{", output, re.IGNORECASE))
            return f"[Pruned Search Results] Tool '{tool_name}' returned {matches_count} matches ({output_len} chars output)."
            
        # Default pruning fallback
        return f"[Pruned Output] Tool '{tool_name}' completed. Trimmed output from {output_len} to 100 chars: '{output[:100].strip()}...'"

    def compress_tier1(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Applies Tier 1 pruning to all historical tool response messages in the list.
        """
        pruned_msgs = []
        for msg in messages:
            new_msg = dict(msg)
            if msg.get("role") == "tool" or msg.get("tool_name"):
                tool_name = msg.get("tool_name") or "unknown_tool"
                new_msg["content"] = self.prune_tool_output(tool_name, msg.get("content", ""))
            # Strip images/media references from historical messages
            if new_msg.get("content") and isinstance(new_msg["content"], str):
                new_msg["content"] = re.sub(r"!\[.*?\]\(.*?\)", "[Image Stripped]", new_msg["content"])
            pruned_msgs.append(new_msg)
        return pruned_msgs

    def _generate_heuristic_summary(self, middle_messages: List[Dict[str, Any]], previous_summary: str = "") -> str:
        """
        Programmatic fallback summarizer. Analyzes turns, tool calls, and outputs
        to compile a rich history report without making API calls.
        """
        tool_counts = {}
        files_accessed = set()
        errors_logged = []
        
        for msg in middle_messages:
            content = msg.get("content", "")
            role = msg.get("role", "")
            tool_name = msg.get("tool_name") or ""
            
            if tool_name:
                tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
            
            # Extract target files/paths if visible
            if "TargetFile" in content or "file:///" in content:
                paths = re.findall(r"(?:TargetFile|file:///)([^\s\"']+\.[a-zA-Z0-9]+)", content)
                for p in paths:
                    files_accessed.add(p.split("/")[-1].split("\\")[-1])
            
            if role == "tool" and ("error" in content.lower() or "fail" in content.lower() or "exception" in content.lower()):
                errors_logged.append(tool_name or "command")

        # Compile programmatic summary text
        summary_lines = []
        if previous_summary:
            summary_lines.append(f"Previous compaction summary: {previous_summary.replace('[CONTEXT COMPACTION — REFERENCE ONLY]', '').strip()}")
            
        summary_lines.append(f"Executed {sum(tool_counts.values())} operations across middle turns.")
        if tool_counts:
            ops = ", ".join(f"{k} ({v}x)" for k, v in tool_counts.items())
            summary_lines.append(f"Operations profile: {ops}.")
        if files_accessed:
            summary_lines.append(f"Modified/accessed resources: {', '.join(files_accessed)}.")
        if errors_logged:
            summary_lines.append(f"Encountered runtime failures in: {', '.join(set(errors_logged))}.")
            
        summary_body = " ".join(summary_lines)
        return f"[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted to save token space. Summary of past actions: {summary_body}"

    def compress_tier2_and_3(self, messages: List[Dict[str, Any]], previous_summary: str = "") -> List[Dict[str, Any]]:
        """
        Tier 2 & 3: Compacts conversation history by replacing middle turns with a summary.
        - Protects head: First system message + First user message + First assistant reply.
        - Protects tail: Last 4 messages.
        - Summarizes everything in between using GenAI API if available, or falls back to heuristic generation.
        """
        if len(messages) <= 7:
            # Not enough turns to compact
            return messages

        head = messages[:3]
        tail = messages[-4:]
        middle = messages[3:-4]

        # Group tool calls with their tool responses so we don't sever pairs
        # If the first item of middle is a tool response whose caller is in head, protect it
        adjusted_head = list(head)
        while middle and (middle[0].get("role") == "tool" or middle[0].get("tool_call_id")):
            adjusted_head.append(middle.pop(0))
            
        # Similarly, if tail starts with a tool response, pull the matching tool calls from middle
        adjusted_tail = list(tail)
        while middle and (adjusted_tail[0].get("role") == "tool" or adjusted_tail[0].get("tool_call_id")):
            # Grab from end of middle
            adjusted_tail.insert(0, middle.pop())

        if len(middle) < 3:
            # After adjusting, middle is too small to compact
            return messages

        # Generate summary
        summary_text = ""
        if self.model_client:
            try:
                # Construct summarization prompt
                history_text = "\n".join(f"{m.get('role', 'unknown')}: {m.get('content', '')}" for m in middle)
                prompt = (
                    "Summarize the actions taken, files modified, tool calls made, and key decisions "
                    f"in this conversation transcript snippet. Keep it under 200 words:\n\n{history_text}"
                )
                
                # Check for google-genai Client vs google-generativeai client
                if hasattr(self.model_client, "models"):
                    response = self.model_client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=prompt
                    )
                    summary_text = f"[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted: {response.text.strip()}"
                elif hasattr(self.model_client, "generate_content"):
                    # google-generativeai fallback
                    response = self.model_client.generate_content(prompt)
                    summary_text = f"[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted: {response.text.strip()}"
            except Exception as e:
                print(f"[ConversationCompressor] LLM summarization failed: {e}. Falling back to programmatic heuristic.")
                
        if not summary_text:
            # Fall back to heuristic summarizer
            summary_text = self._generate_heuristic_summary(middle, previous_summary)

        # Assemble new compacted history
        compacted = []
        compacted.extend(adjusted_head)
        compacted.append({
            "role": "system",
            "content": summary_text,
            "timestamp": time.time()
        })
        compacted.extend(adjusted_tail)

        return compacted

    def evaluate_and_compact_session(self, session_id: str, threshold_chars: int = 150000) -> bool:
        """
        Saves compacted history to database and tracks compaction efficiency.
        Triggers session chaining if needed. Returns True if compaction occurred.
        """
        # 1. Fetch current active messages
        sql = "SELECT * FROM messages WHERE session_id = ? AND active = 1 ORDER BY id ASC"
        with self.state_store.lock:
            with self.state_store._get_connection() as conn:
                cursor = conn.execute(sql, (session_id,))
                messages = [dict(row) for row in cursor.fetchall()]

        if not messages:
            return False

        # Calculate character count as a token proxy
        total_chars = sum(len(m.get("content", "") or "") for m in messages)
        if total_chars < threshold_chars:
            return False

        # Anti-thrashing check
        if self.ineffective_count >= 2:
            print("[ConversationCompressor] ⚠️ Compaction skipped due to consecutive ineffective cycles.")
            return False

        print(f"[ConversationCompressor] 📦 Cumulative history exceeds threshold ({total_chars} chars). Compacting...")

        # 2. Extract previous summary from messages if exists
        prev_summary = ""
        for m in messages:
            content = m.get("content", "")
            if content and "[CONTEXT COMPACTION" in content:
                prev_summary = content
                break

        # 3. Apply Tier 1 and Tier 2/3 Compaction
        pruned_messages = self.compress_tier1(messages)
        compacted_messages = self.compress_tier2_and_3(pruned_messages, prev_summary)

        new_chars = sum(len(m.get("content", "") or "") for m in compacted_messages)
        saved_ratio = (total_chars - new_chars) / total_chars

        print(f"[ConversationCompressor] Compaction stats: {total_chars} -> {new_chars} chars. Saved: {saved_ratio * 100:.1f}%.")

        # 4. Check saving effectiveness
        if saved_ratio < 0.10:
            self.ineffective_count += 1
        else:
            self.ineffective_count = 0  # Reset
            
        # 5. Save changes to DB (soft-delete old, insert new compacted records)
        # To maintain lineage, we mark the old messages as inactive, and insert the compacted messages
        # Session chaining: if compaction occurs, update session metadata
        self.state_store._execute_write(
            "UPDATE messages SET active = 0 WHERE session_id = ?", (session_id,)
        )
        
        for msg in compacted_messages:
            # Preserve original IDs if possible or insert as new active messages
            self.state_store.add_message(
                session_id=session_id,
                role=msg.get("role", "system"),
                content=msg.get("content", ""),
                tool_call_id=msg.get("tool_call_id"),
                tool_calls=json.loads(msg.get("tool_calls")) if msg.get("tool_calls") else None,
                tool_name=msg.get("tool_name"),
                token_count=msg.get("token_count")
            )
            
        return True
