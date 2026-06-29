"""
Keystone Sovereign Self-Evolution Engine v2.0
==============================================
Autonomous self-healing, learning, and continuous improvement system.

Core capabilities:
  1. Structured error recording with pattern detection
  2. Self-healing retry loops with exponential backoff
  3. Correction journal that learns from past fixes (error→fix mappings)
  4. Automatic daily digest consolidation of learnings
  5. Performance trend tracking across evolution cycles
  6. Stale error pruning and health scoring
"""

import os
import sys
import datetime
import uuid
import json
import traceback
import subprocess
import hashlib
import ast
import time
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from qdrant_client import QdrantClient, models

try:
    client = QdrantClient(url="http://localhost:6333")
    client.set_model("BAAI/bge-small-en-v1.5")
except Exception:
    client = None

# Force UTF-8 output on Windows to handle emojis in logs and print statements
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from evaluation_harness import execute_fixture_tests, EvaluationResult
from security_sandbox import SecurityValidator, SecurityException
from multiplexer_sync import sync_dynamic_skills_to_multiplexer

# Base directories
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
ERRORS_DIR = os.path.join(LEARNINGS_DIR, "errors")
CORRECTIONS_DIR = os.path.join(LEARNINGS_DIR, "corrections")
INSIGHTS_DIR = os.path.join(LEARNINGS_DIR, "insights")
DYNAMIC_SKILLS_DIR = os.path.join(PROJECT_ROOT, "dynamic_skills")
CORRECTION_JOURNAL = os.path.join(LEARNINGS_DIR, "correction_journal.json")

# Import Hermes transplant components
try:
    from core.brain_init import init_brain_transplant
    brain_components = init_brain_transplant()
    state_store = brain_components["state_store"]
    self_knowledge_manager = brain_components["self_knowledge_manager"]
except Exception as e:
    print(f"[Self-Evolution] Hermes brain transplant offline: {e}")
    state_store = None
    self_knowledge_manager = None

# Configure environment directories
for d in [ERRORS_DIR, CORRECTIONS_DIR, INSIGHTS_DIR, DYNAMIC_SKILLS_DIR]:
    os.makedirs(d, exist_ok=True)

def verify_syntax(code_str: str) -> bool:
    """Pre-write gate to verify that Python code is syntactically valid."""
    try:
        ast.parse(code_str)
        return True
    except SyntaxError as e:
        print(f"[Self-Evolution] Syntax Error: {e}")
        return False

class SkillManifest(BaseModel):
    name: str
    description: str
    code: str
    test_fixtures: list

class CorrectionEntry(BaseModel):
    error_fingerprint: str
    error_type: str
    original_context: str
    fix_description: str
    fix_applied_at: str
    success: bool
    retry_count: int


# ─── Circuit Breaker (Hardware-Enforced Agent Fault Tolerance) ────────────
# Research Source: 20260610_AGENT_ARCH_circuit_breaker_patterns_for_autonomous_agents
# Implements: No-Progress Trigger, Same-Error Fingerprint (SHA-256), Token Decline Metric
# Three states: CLOSED (healthy) → OPEN (broken) → HALF_OPEN (testing recovery)

class CircuitBreakerState:
    """Enum-like states for the circuit breaker."""
    CLOSED = "CLOSED"        # Healthy — all operations pass through
    OPEN = "OPEN"            # Broken — all operations are blocked
    HALF_OPEN = "HALF_OPEN"  # Testing — single probe allowed to test recovery

class AgentCircuitBreaker:
    """
    Keystone Sovereign: Hardware-enforced agent circuit breaker.
    
    Detects infinite loops, no-progress states, and repeated error fingerprints
    in long-running agent tasks. Automatically opens the circuit when thresholds
    are exceeded, and attempts auto-recovery after a cooldown period.
    
    Three diagnostic heuristics:
      1. No-Progress Trigger — state hash comparison across consecutive ticks
      2. Same-Error Fingerprint — SHA-256 of (tool + args + error) deduplication
      3. Token Decline Metric — tracks output token velocity collapse
    
    Version: 1.2.0 (Keystone Sovereign)
    """
    
    def __init__(self, max_stalls: int = 3, max_error_repeats: int = 2,
                 token_floor: int = 50, cooldown_seconds: int = 120,
                 half_open_max_probes: int = 1):
        # Thresholds
        self.max_stalls = max_stalls
        self.max_error_repeats = max_error_repeats
        self.token_floor = token_floor
        self.cooldown_seconds = cooldown_seconds
        self.half_open_max_probes = half_open_max_probes
        
        # State management
        self.state = CircuitBreakerState.CLOSED
        self._opened_at: Optional[datetime.datetime] = None
        self._half_open_probes = 0
        self._trip_reason: Optional[str] = None
        
        # Heuristic trackers
        self.state_hashes: List[str] = []
        self.error_ledger: Dict[str, int] = {}
        self.token_velocity: List[int] = []
        
        # Metrics
        self._trip_count = 0
        self._recovery_count = 0
        self._last_trip_time: Optional[str] = None
        
        # Persistent state file
        self._state_file = os.path.join(LEARNINGS_DIR, "circuit_breaker_state.json")
        self._load_persisted_state()
    
    def _hash_payload(self, payload: str) -> str:
        """Generates a stable SHA-256 hash for fingerprinting."""
        return hashlib.sha256(payload.encode('utf-8')).hexdigest()
    
    def _load_persisted_state(self):
        """Loads persisted circuit breaker metrics from disk."""
        if os.path.exists(self._state_file):
            try:
                with open(self._state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._trip_count = data.get("trip_count", 0)
                self._recovery_count = data.get("recovery_count", 0)
                self._last_trip_time = data.get("last_trip_time")
            except Exception:
                pass
    
    def _save_persisted_state(self):
        """Persists circuit breaker metrics to disk."""
        data = {
            "state": self.state,
            "trip_count": self._trip_count,
            "recovery_count": self._recovery_count,
            "last_trip_time": self._last_trip_time,
            "error_ledger_size": len(self.error_ledger),
            "updated_at": datetime.datetime.now().isoformat(),
        }
        try:
            with open(self._state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass
    
    # ─── Heuristic 1: No-Progress Trigger ─────────────────────────────
    
    def check_no_progress(self, current_state: str) -> bool:
        """Trips if the state hash remains identical for max_stalls consecutive ticks."""
        state_hash = self._hash_payload(current_state)
        self.state_hashes.append(state_hash)
        
        # Keep buffer bounded
        if len(self.state_hashes) > self.max_stalls * 2:
            self.state_hashes = self.state_hashes[-self.max_stalls * 2:]
        
        if len(self.state_hashes) >= self.max_stalls:
            recent = self.state_hashes[-self.max_stalls:]
            if len(set(recent)) == 1:
                return True
        return False
    
    # ─── Heuristic 2: Same-Error Fingerprint ──────────────────────────
    
    def check_error_fingerprint(self, tool: str, args: str, error: str) -> bool:
        """Trips if the exact same error+payload combination occurs max_error_repeats times."""
        fingerprint = f"{tool}|{args}|{error}"
        error_hash = self._hash_payload(fingerprint)
        
        self.error_ledger[error_hash] = self.error_ledger.get(error_hash, 0) + 1
        return self.error_ledger[error_hash] >= self.max_error_repeats
    
    # ─── Heuristic 3: Token Decline Metric ────────────────────────────
    
    def check_token_decline(self, tokens: int) -> bool:
        """Trips if generated token count falls below token_floor for 3 consecutive steps."""
        self.token_velocity.append(tokens)
        
        # Keep buffer bounded
        if len(self.token_velocity) > 10:
            self.token_velocity = self.token_velocity[-10:]
        
        if len(self.token_velocity) >= 3:
            recent = self.token_velocity[-3:]
            if all(t < self.token_floor for t in recent):
                return True
        return False
    
    # ─── State Machine ────────────────────────────────────────────────
    
    def _trip(self, reason: str):
        """Opens the circuit breaker due to a detected failure pattern."""
        self.state = CircuitBreakerState.OPEN
        self._opened_at = datetime.datetime.now()
        self._trip_reason = reason
        self._trip_count += 1
        self._last_trip_time = self._opened_at.isoformat()
        self._half_open_probes = 0
        self._save_persisted_state()
        print(f"[CircuitBreaker] 🔴 TRIPPED → OPEN | Reason: {reason} | Total trips: {self._trip_count}")
    
    def _check_cooldown_expired(self) -> bool:
        """Returns True if the cooldown period has elapsed since the circuit opened."""
        if self._opened_at is None:
            return True
        elapsed = (datetime.datetime.now() - self._opened_at).total_seconds()
        return elapsed >= self.cooldown_seconds
    
    def _attempt_recovery(self) -> bool:
        """Transitions from OPEN → HALF_OPEN if cooldown has expired."""
        if self.state == CircuitBreakerState.OPEN and self._check_cooldown_expired():
            self.state = CircuitBreakerState.HALF_OPEN
            self._half_open_probes = 0
            print(f"[CircuitBreaker] 🟡 Cooldown expired → HALF_OPEN | Testing recovery...")
            return True
        return False
    
    def record_success(self):
        """Records a successful operation — used to close a HALF_OPEN breaker."""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.CLOSED
            self._opened_at = None
            self._trip_reason = None
            self._recovery_count += 1
            # Reset heuristic trackers after recovery
            self.state_hashes.clear()
            self.error_ledger.clear()
            self.token_velocity.clear()
            self._save_persisted_state()
            print(f"[CircuitBreaker] 🟢 Recovery confirmed → CLOSED | Total recoveries: {self._recovery_count}")
    
    def is_open(self) -> bool:
        """Check if the circuit is currently blocking operations."""
        if self.state == CircuitBreakerState.OPEN:
            # Auto-attempt recovery if cooldown has passed
            self._attempt_recovery()
        return self.state == CircuitBreakerState.OPEN
    
    def allow_request(self) -> bool:
        """Returns True if the current request should be allowed through."""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        if self.state == CircuitBreakerState.OPEN:
            if self._check_cooldown_expired():
                self._attempt_recovery()
            if self.state == CircuitBreakerState.HALF_OPEN:
                # Allow limited probes in HALF_OPEN
                pass
            else:
                return False
        if self.state == CircuitBreakerState.HALF_OPEN:
            self._half_open_probes += 1
            if self._half_open_probes <= self.half_open_max_probes:
                return True
            return False
        return True
    
    # ─── Master Evaluation Gate ───────────────────────────────────────
    
    def evaluate_cycle(self, state: str, tokens: int = 0,
                       tool_data: Dict[str, Any] = None) -> str:
        """
        Master evaluation gate. Run this after every agent tick.
        Returns one of: CLEAR, TRIP_NO_PROGRESS, TRIP_SAME_ERROR, TRIP_TOKEN_DECLINE, BLOCKED
        """
        # If circuit is OPEN and cooldown hasn't expired, block
        if self.state == CircuitBreakerState.OPEN:
            if not self._check_cooldown_expired():
                return "BLOCKED"
            self._attempt_recovery()
        
        # Run heuristics
        if self.check_no_progress(state):
            self._trip("TRIP_NO_PROGRESS")
            return "TRIP_NO_PROGRESS"
        
        if tool_data and 'error' in tool_data:
            if self.check_error_fingerprint(
                tool_data.get('name', ''),
                str(tool_data.get('args', '')),
                tool_data['error']
            ):
                self._trip("TRIP_SAME_ERROR")
                return "TRIP_SAME_ERROR"
        
        if tokens > 0 and self.check_token_decline(tokens):
            self._trip("TRIP_TOKEN_DECLINE")
            return "TRIP_TOKEN_DECLINE"
        
        # If we're in HALF_OPEN and we passed all checks, recover
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.record_success()
        
        return "CLEAR"
    
    # ─── Health Metrics ───────────────────────────────────────────────
    
    def get_health_metrics(self) -> dict:
        """Returns circuit breaker health metrics for integration with system health scoring."""
        return {
            "circuit_state": self.state,
            "trip_count": self._trip_count,
            "recovery_count": self._recovery_count,
            "last_trip_time": self._last_trip_time,
            "unique_error_fingerprints": len(self.error_ledger),
            "state_hash_buffer_size": len(self.state_hashes),
            "token_velocity_buffer": self.token_velocity[-5:] if self.token_velocity else [],
            "cooldown_seconds": self.cooldown_seconds,
            "trip_reason": self._trip_reason,
            # Penalty: deduct points for open circuit or high trip count
            "health_penalty": 30 if self.state == CircuitBreakerState.OPEN else (
                15 if self.state == CircuitBreakerState.HALF_OPEN else 0
            ),
        }
    
    def reset(self):
        """Force-reset the circuit breaker to CLOSED state. Use sparingly."""
        self.state = CircuitBreakerState.CLOSED
        self._opened_at = None
        self._trip_reason = None
        self._half_open_probes = 0
        self.state_hashes.clear()
        self.error_ledger.clear()
        self.token_velocity.clear()
        self._save_persisted_state()
        print("[CircuitBreaker] 🔄 Force-reset to CLOSED state.")


class SovereignSelfEvolution:
    def __init__(self):
        print("[Sovereign Self-Evolution v2.0] System Online. Self-healing + learning active.")
        self.validator = SecurityValidator()
        self.correction_journal = self._load_correction_journal()
        self.circuit_breaker = AgentCircuitBreaker()

    # ─── Correction Journal (Persistent Error→Fix Memory) ────────────────

    def _load_correction_journal(self) -> dict:
        """Loads the persistent correction journal mapping error fingerprints to known fixes."""
        if os.path.exists(CORRECTION_JOURNAL):
            try:
                with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"entries": [], "stats": {"total_errors": 0, "total_fixes": 0, "auto_healed": 0}}

    def _save_correction_journal(self):
        """Persists the correction journal to disk."""
        with open(CORRECTION_JOURNAL, "w", encoding="utf-8") as f:
            json.dump(self.correction_journal, f, indent=2, ensure_ascii=False)

    def _compute_error_fingerprint(self, error_type: str, context: str, traceback_str: str) -> str:
        """Creates a stable fingerprint for an error to enable deduplication and pattern matching."""
        # Extract the core error message (last line of traceback usually)
        core = traceback_str.strip().split("\n")[-1] if traceback_str else ""
        raw = f"{error_type}::{context}::{core}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _find_known_fix(self, fingerprint: str) -> Optional[dict]:
        """Searches the correction journal for a known fix for this error pattern."""
        for entry in self.correction_journal.get("entries", []):
            # Safe get to prevent KeyErrors on older or manual entries
            entry_fingerprint = entry.get("error_fingerprint") or entry.get("fingerprint")
            if entry_fingerprint == fingerprint and entry.get("success", False):
                return entry
        return None

    def _find_semantic_fix(self, error_message: str) -> Optional[dict]:
        """Searches the Qdrant 'self_healing' collection for semantically similar past fixes.
        
        Uses tiered confidence thresholds:
          - HIGH (>0.85): Auto-apply candidate — near-identical past error
          - MEDIUM (>0.70): Strong suggestion — similar error pattern
          - LOW (>0.55): Weak signal — loosely related, manual review needed
        """
        if not error_message or client is None:
            return None
        try:
            if not client.collection_exists(collection_name="self_healing"):
                return None
            results = client.query_points(
                collection_name="self_healing",
                query=models.Document(text=error_message),
                limit=3,  # v2.0: fetch top 3 for tiered comparison
                with_payload=True
            )
            if results.points:
                point = results.points[0]
                score = point.score if hasattr(point, 'score') else 0.0
                if score > 0.55:  # v2.0: lowered floor to catch more candidates
                    payload = point.payload or {}
                    # Determine confidence tier
                    if score > 0.85:
                        confidence = "HIGH"
                    elif score > 0.70:
                        confidence = "MEDIUM"
                    else:
                        confidence = "LOW"
                    return {
                        "error_type": payload.get("error_type", "Unknown"),
                        "fix_description": payload.get("fix_description", "No description"),
                        "fix_applied_at": payload.get("fix_applied_at", ""),
                        "retry_count": payload.get("retry_count", 1),
                        "score": score,
                        "confidence": confidence,
                        "namespace": payload.get("namespace", "self_healing"),
                        "eeat_tag": payload.get("EEAT_tag", ""),
                        "alternatives": len(results.points) - 1,  # How many other candidates exist
                    }
        except Exception as e:
            print(f"[Self-Evolution] Qdrant query error: {e}")
        return None

    def _find_cross_namespace_fix(self, error_message: str, context: str) -> Optional[dict]:
        """Search beyond self_healing — look in master/general for relevant context.
        
        This enables the self-healer to find brand knowledge, operational playbooks,
        or past research that's relevant to the error even if it's not a direct fix.
        """
        if not error_message or client is None:
            return None
        try:
            # Search the main brain collection for related context
            brain_collection = "keystone_brain"
            collections = client.get_collections().collections
            if not any(c.name == brain_collection for c in collections):
                return None

            results = client.query_points(
                collection_name=brain_collection,
                query=models.Document(text=f"{context} {error_message}"),
                query_filter=models.Filter(
                    should=[
                        models.FieldCondition(
                            key="namespace",
                            match=models.MatchValue(value="master"),
                        ),
                        models.FieldCondition(
                            key="namespace",
                            match=models.MatchValue(value="operational_playbooks"),
                        ),
                        models.FieldCondition(
                            key="namespace",
                            match=models.MatchValue(value="keystone_learnings"),
                        ),
                    ]
                ),
                limit=1,
                with_payload=True,
            )
            if results.points:
                point = results.points[0]
                score = point.score if hasattr(point, 'score') else 0.0
                if score > 0.6:
                    payload = point.payload or {}
                    return {
                        "source": "cross_namespace",
                        "namespace": payload.get("namespace", "unknown"),
                        "content_snippet": (payload.get("document", "") or "")[:200],
                        "score": score,
                        "topic": payload.get("topic", ""),
                    }
        except Exception as e:
            print(f"[Self-Evolution] Cross-namespace search error: {e}")
        return None

    def _record_correction(self, fingerprint: str, error_type: str, context: str,
                           fix_description: str, success: bool, retry_count: int,
                           error_message: str = "", severity: str = "Warning",
                           namespace: str = "self_healing"):
        """Records a correction attempt in the journal and Qdrant cache with enriched metadata.
        
        v2.0 Enhancements:
          - Namespace tagging for brand-aware error tracking
          - EEAT_tag classification (Case Study for successful fixes)
          - Severity level propagation into vector payload
          - Topic extraction from context for better semantic retrieval
        """
        now_iso = datetime.datetime.now().isoformat()
        entry = {
            "error_fingerprint": fingerprint,
            "error_type": error_type,
            "original_context": context,
            "fix_description": fix_description,
            "fix_applied_at": now_iso,
            "success": success,
            "retry_count": retry_count,
            "severity": severity,
            "namespace": namespace,
        }
        self.correction_journal["entries"].append(entry)
        self.correction_journal["stats"]["total_errors"] += 1
        if success:
            self.correction_journal["stats"]["total_fixes"] += 1
            self.correction_journal["stats"]["auto_healed"] += 1
            
            # Ingest into Qdrant self_healing collection with enriched metadata
            if client is not None:
                try:
                    if not client.collection_exists(collection_name="self_healing"):
                        client.create_collection(
                            collection_name="self_healing",
                            vectors_config=client.get_fastembed_vector_params()
                        )
                    doc = f"Error Type: {error_type}\nContext: {context}\nError Details: {error_message}\nFix Applied: {fix_description}"
                    
                    # v2.0: Enriched metadata payload
                    meta = {
                        "fingerprint": fingerprint,
                        "error_type": error_type,
                        "fix_description": fix_description,
                        "fix_applied_at": now_iso,
                        "retry_count": retry_count,
                        "namespace": namespace,
                        "severity": severity,
                        "EEAT_tag": "Case Study",  # Successful fixes are experiential evidence
                        "topic": f"{error_type} in {context}",
                        "updated_at": now_iso,
                    }
                    client.add(
                        collection_name="self_healing",
                        documents=[doc],
                        metadata=[meta]
                    )
                    print(f"[Self-Evolution] Semantic fix cached in Qdrant (namespace: {namespace}, EEAT: Case Study)")
                except Exception as e:
                    print(f"[Self-Evolution] Failed to cache fix in Qdrant: {e}")
                    
        self._save_correction_journal()

    # ─── Error Recording ─────────────────────────────────────────────────

    def record_runtime_error(self, error_type: str, severity: str, context: str,
                              query: str, traceback_str: str, parameters: dict) -> str:
        """Writes a structured error card and checks for known/semantic fixes."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        uuid_str = str(uuid.uuid4())[:8]
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        fingerprint = self._compute_error_fingerprint(error_type, context, traceback_str)

        # Check if we've seen this before (exact match → semantic → cross-namespace)
        known_fix = self._find_known_fix(fingerprint)
        semantic_fix = None
        cross_ns_context = None
        if not known_fix:
            semantic_fix = self._find_semantic_fix(traceback_str)
        if not known_fix and not semantic_fix:
            cross_ns_context = self._find_cross_namespace_fix(traceback_str, context)
            
        known_fix_section = ""
        if known_fix:
            known_fix_section = f"""
## 🔄 Known Fix Found (Auto-Heal Candidate)
This error pattern was previously resolved:
- **Fix Applied:** {known_fix['fix_description']}
- **Applied At:** {known_fix['fix_applied_at']}
- **Previous Retries:** {known_fix['retry_count']}

**Recommendation:** Apply the same fix automatically.
"""
        elif semantic_fix:
            confidence = semantic_fix.get('confidence', 'UNKNOWN')
            alternatives = semantic_fix.get('alternatives', 0)
            known_fix_section = f"""
## 🔄 Semantically Similar Past Fix Found
- **Confidence:** {confidence} (Score: {semantic_fix['score']:.4f})
- **Similar Error Type:** {semantic_fix['error_type']}
- **Past Fix Applied:** {semantic_fix['fix_description']}
- **Applied At:** {semantic_fix['fix_applied_at']}
- **Alternative candidates:** {alternatives}

**Recommendation:** {'Apply automatically (HIGH confidence).' if confidence == 'HIGH' else 'Review and consider applying.' if confidence == 'MEDIUM' else 'Weak match — manual review required.'}
"""
        if cross_ns_context:
            known_fix_section += f"""
## 📚 Related Brain Context Found
Relevant knowledge from the **{cross_ns_context.get('namespace', 'unknown')}** namespace:
- **Topic:** {cross_ns_context.get('topic', 'N/A')}
- **Relevance Score:** {cross_ns_context.get('score', 0):.4f}
- **Snippet:** {cross_ns_context.get('content_snippet', 'N/A')}
"""

        filename = f"{date_str}-{error_type}-{uuid_str}.md"
        filepath = os.path.join(ERRORS_DIR, filename)

        error_card = f"""# Error: Tool Call Execution Failure
Timestamp: {timestamp}
Type: {error_type}
Severity: {severity}
Fingerprint: {fingerprint}

## What Happened
The dynamic coordinator encountered a runtime connection or execution error.

## Execution Context
Context ID: {context}
Trigger Query: {query}
Parameters: {json.dumps(parameters, indent=2)}

## Root Cause Analysis
```python
{traceback_str}
```
{known_fix_section}
## Recommended Mitigations
1. Isolate the failing command and parameter mapping.
2. Formulate dynamic test case using fixture assertions.
3. Invoke reflection compiler to synthesize corrected skill replacement.
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(error_card)
        print(f"[Self-Evolution] Error card compiled: {filepath} (fingerprint: {fingerprint})")

        # Save to SQLite state store
        if state_store:
            try:
                state_store.create_session("evolution_session", source="self_evolution", system_prompt="Self-Evolution Error Log")
                state_store.add_message(
                    session_id="evolution_session",
                    role="system",
                    content=f"Error Type: {error_type}\nContext: {context}\nFingerprint: {fingerprint}\nTraceback: {traceback_str}\nParameters: {json.dumps(parameters)}"
                )
            except Exception as db_err:
                print(f"[Self-Evolution] Failed to log error to state.db: {db_err}")

        # Feed error to circuit breaker for fingerprint tracking
        cb_result = self.circuit_breaker.evaluate_cycle(
            state=json.dumps({"error_type": error_type, "context": context, "fingerprint": fingerprint}),
            tokens=0,
            tool_data={"name": context, "args": json.dumps(parameters, default=str), "error": traceback_str[:500]}
        )
        if cb_result.startswith("TRIP"):
            print(f"[Self-Evolution] ⚡ Circuit breaker tripped during error recording: {cb_result}")

        return fingerprint

    # ─── Error Pattern Analysis ──────────────────────────────────────────

    def analyze_error_patterns(self) -> dict:
        """Scans all error cards and returns frequency analysis and recurring patterns."""
        error_files = [f for f in os.listdir(ERRORS_DIR) if f.endswith(".md")]
        patterns = {}
        recent_errors = []

        for f in error_files:
            # Extract error type from filename: YYYY-MM-DD-ErrorType-UUID.md
            parts = f.replace(".md", "").split("-")
            if len(parts) >= 5:
                error_type = parts[3]
                date_str = f"{parts[0]}-{parts[1]}-{parts[2]}"
                patterns[error_type] = patterns.get(error_type, 0) + 1

                # Check recency
                try:
                    error_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                    age_days = (datetime.datetime.now() - error_date).days
                    if age_days <= 7:
                        recent_errors.append({"file": f, "type": error_type, "age_days": age_days})
                except ValueError:
                    pass

        # Sort by frequency
        sorted_patterns = sorted(patterns.items(), key=lambda x: -x[1])

        return {
            "total_error_cards": len(error_files),
            "pattern_frequency": dict(sorted_patterns),
            "recent_errors_7d": recent_errors,
            "top_recurring": sorted_patterns[:3] if sorted_patterns else [],
            "health_score": max(0, 100 - (len(recent_errors) * 10))
        }

    # ─── Stale Error Pruning ─────────────────────────────────────────────

    def prune_stale_errors(self, max_age_days: int = 30) -> int:
        """Archives error cards older than max_age_days to prevent bloat."""
        archive_dir = os.path.join(ERRORS_DIR, "_archive")
        os.makedirs(archive_dir, exist_ok=True)
        pruned = 0

        for f in os.listdir(ERRORS_DIR):
            if not f.endswith(".md"):
                continue
            filepath = os.path.join(ERRORS_DIR, f)
            if not os.path.isfile(filepath):
                continue
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            age_days = (datetime.datetime.now() - mtime).days
            if age_days > max_age_days:
                dest = os.path.join(archive_dir, f)
                os.rename(filepath, dest)
                pruned += 1

        if pruned:
            print(f"[Self-Evolution] Pruned {pruned} stale error cards (>{max_age_days} days old)")
        return pruned

    # ─── Daily Digest Consolidation ──────────────────────────────────────

    def generate_daily_digest(self) -> str:
        """Consolidates today's learnings into a daily digest insight."""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        patterns = self.analyze_error_patterns()
        journal_stats = self.correction_journal.get("stats", {})

        digest = f"""# 📊 Daily Self-Evolution Digest — {today}

## System Health Score: {patterns['health_score']}/100

## Error Landscape
- Total error cards on file: {patterns['total_error_cards']}
- Errors in last 7 days: {len(patterns['recent_errors_7d'])}
- Top recurring patterns: {', '.join(f'{k} ({v}x)' for k, v in patterns['top_recurring']) if patterns['top_recurring'] else 'None'}

## Correction Journal Stats
- Total errors tracked: {journal_stats.get('total_errors', 0)}
- Total fixes applied: {journal_stats.get('total_fixes', 0)}
- Auto-healed: {journal_stats.get('auto_healed', 0)}
- Auto-heal rate: {(journal_stats.get('auto_healed', 0) / max(journal_stats.get('total_errors', 1), 1) * 100):.1f}%

## Recent Corrections
"""
        recent_corrections = self.correction_journal.get("entries", [])[-5:]
        if recent_corrections:
            for c in reversed(recent_corrections):
                status = "✅" if c.get("success", True) else "❌"
                error_type = c.get("error_type", c.get("category", "Unknown"))
                fix_desc = c.get("fix_description", c.get("fix_applied", c.get("fix", "No description")))
                fix_time = c.get("fix_applied_at", c.get("timestamp", c.get("date", "Unknown time")))
                digest += f"- {status} [{error_type}] {fix_desc} ({fix_time[:10]})\n"
        else:
            digest += "- No corrections recorded yet.\n"

        digest += f"""
## Recommendations
"""
        if patterns['health_score'] < 70:
            digest += "- ⚠️ Health score below 70. Review recurring error patterns.\n"
        if len(patterns['recent_errors_7d']) > 5:
            digest += "- 🔧 High error volume this week. Consider running full diagnostic suite.\n"
        if patterns['health_score'] >= 90:
            digest += "- 🟢 System is healthy. No immediate action needed.\n"

        digest_path = os.path.join(INSIGHTS_DIR, f"{today}-daily-digest.md")
        with open(digest_path, "w", encoding="utf-8") as f:
            f.write(digest)
        print(f"[Self-Evolution] Daily digest generated: {digest_path}")

        # DSPy-inspired: Auto-run the Prompt Self-Refiner to regenerate prevention rules
        try:
            refiner_path = os.path.join(PROJECT_ROOT, "prompt_refiner.py")
            if os.path.exists(refiner_path):
                result = subprocess.run(
                    [sys.executable, refiner_path, "--generate-rules"],
                    capture_output=True, text=True, timeout=30, cwd=PROJECT_ROOT
                )
                if result.returncode == 0:
                    print("[Self-Evolution] Prompt refiner updated prevention rules.")
                else:
                    print(f"[Self-Evolution] Prompt refiner warning: {result.stderr.strip()[:200]}")
        except Exception as e:
            print(f"[Self-Evolution] Prompt refiner skipped: {str(e)}")

        return digest

    # ─── Evolution Cycle (Core Self-Healing Loop) ────────────────────────

    def run_evolution_cycle(self, module_name: str, function_name: str,
                           candidate_code: str, test_fixtures: list,
                           max_retries: int = 3) -> bool:
        """
        Coordinates full isolated evaluation cycle with self-healing retries:
        AST check → sandboxed subprocess → test run → git commit/rollback.
        If the first attempt fails, retries with exponential backoff.
        """
        # Save fixtures to a temporary path
        fixtures_path = os.path.join(PROJECT_ROOT, "scratch", f"{module_name}_fixtures.json")
        os.makedirs(os.path.dirname(fixtures_path), exist_ok=True)
        with open(fixtures_path, "w", encoding="utf-8") as f:
            json.dump(test_fixtures, f, indent=2)

        # Target skill location
        skill_path = os.path.join(DYNAMIC_SKILLS_DIR, f"{module_name}.py")

        # Git check & active branch retrieval
        git_active = False
        original_branch = "main"
        sandbox_branch = None
        try:
            res_worktree = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True, cwd=PROJECT_ROOT)
            if res_worktree.returncode == 0 and res_worktree.stdout.strip() == "true":
                git_active = True
                res_branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, cwd=PROJECT_ROOT)
                if res_branch.returncode == 0:
                    original_branch = res_branch.stdout.strip()
        except Exception:
            pass

        if git_active:
            sandbox_branch = f"sandbox-{module_name}-{uuid.uuid4().hex[:8]}"
            print(f"[Self-Evolution] Creating pre-eval Git sandbox branch: {sandbox_branch} from {original_branch}...")
            subprocess.run(["git", "checkout", "-b", sandbox_branch], capture_output=True, cwd=PROJECT_ROOT)

        attempt = 0
        last_result = None
        last_error_message = ""

        while attempt < max_retries:
            attempt += 1
            print(f"\n[Self-Evolution] Attempt {attempt}/{max_retries} for {module_name}.{function_name}")

            try:
                # 1. AST Safety Check (Verify syntax first, then validate safety constraints)
                if not verify_syntax(candidate_code):
                    print(f"[Self-Evolution] ⚠️ Attempt {attempt} failed: Syntax error in generated code.")
                    last_error_message = "SyntaxError: Generated code does not compile."
                    
                    # Wolverine self-healing: mutate code for next attempt
                    if attempt < max_retries:
                        healed_code = self._heal_candidate_code(module_name, function_name, candidate_code, last_error_message)
                        if healed_code != candidate_code:
                            candidate_code = healed_code
                    
                    # Sleep before retry
                    wait_sec = 2 ** attempt
                    print(f"[Self-Evolution] Retrying in {wait_sec}s (exponential backoff)...")
                    time.sleep(wait_sec)
                    continue

                self.validator.validate_code(candidate_code)

                # Save candidate code
                with open(skill_path, "w", encoding="utf-8") as f:
                    f.write(candidate_code)

                # 2. Run Test Fixtures
                result = execute_fixture_tests(module_name, function_name, fixtures_path)
                last_result = result

                if result.is_valid and result.performance_score > 0.5:
                    print(f"[Self-Evolution] ✅ Success! Performance: {result.performance_score:.4f}")

                    # Record successful correction
                    fingerprint = self._compute_error_fingerprint(
                        "EvolutionCycle", module_name, last_error_message)
                    self._record_correction(
                        fingerprint, "EvolutionCycle", module_name,
                        f"Successfully deployed {module_name}.{function_name} on attempt {attempt}",
                        success=True, retry_count=attempt, error_message=last_error_message
                    )

                    # Save correction log file to .learnings/corrections/
                    try:
                        corr_log_path = os.path.join(CORRECTIONS_DIR, f"correction_{module_name}_{int(time.time())}_success.json")
                        with open(corr_log_path, "w", encoding="utf-8") as lf:
                            json.dump({
                                "module_name": module_name,
                                "function_name": function_name,
                                "status": "success",
                                "attempt": attempt,
                                "candidate_code": candidate_code,
                                "performance_score": result.performance_score,
                                "error_message": last_error_message,
                                "timestamp": datetime.datetime.now().isoformat()
                            }, lf, indent=2)
                    except Exception as log_err:
                        print(f"[Self-Evolution] Warning: failed to write success correction log: {log_err}")

                    # Dynamic hot reloading and multiplexer sync
                    sync_dynamic_skills_to_multiplexer()

                    # Commit and merge successful evolution
                    if git_active and sandbox_branch:
                        print(f"[Self-Evolution] Success! Committing to sandbox branch {sandbox_branch}...")
                        subprocess.run(["git", "add", skill_path], capture_output=True, cwd=PROJECT_ROOT)
                        subprocess.run(["git", "commit", "-m",
                                         f"evolution: deployed optimized skill {module_name}.{function_name} (attempt {attempt})"],
                                       capture_output=True, cwd=PROJECT_ROOT)
                        print(f"[Self-Evolution] Switching back to {original_branch} and merging sandbox...")
                        subprocess.run(["git", "checkout", original_branch], capture_output=True, cwd=PROJECT_ROOT)
                        subprocess.run(["git", "merge", sandbox_branch], capture_output=True, cwd=PROJECT_ROOT)
                        subprocess.run(["git", "branch", "-d", sandbox_branch], capture_output=True, cwd=PROJECT_ROOT)
                    return True
                else:
                    print(f"[Self-Evolution] ⚠️ Attempt {attempt} failed: {result.message}")
                    last_error_message = result.message
                    
                    # Wolverine self-healing: mutate code for next attempt
                    if attempt < max_retries:
                        healed_code = self._heal_candidate_code(module_name, function_name, candidate_code, result.message)
                        if healed_code != candidate_code:
                            candidate_code = healed_code
                    
                    fingerprint = self.record_runtime_error(
                        error_type="ValidationFailure",
                        severity="Warning",
                        context=f"run_evolution_cycle:{module_name}:attempt_{attempt}",
                        query="Execute dynamic test validation suite",
                        traceback_str=result.message,
                        parameters={"accuracy": result.accuracy_score, "score": result.performance_score}
                    )

                    if attempt < max_retries:
                        wait_sec = 2 ** attempt
                        print(f"[Self-Evolution] Retrying in {wait_sec}s (exponential backoff)...")
                        time.sleep(wait_sec)

            except SecurityException as sec_err:
                print(f"[Self-Evolution] 🛑 AST validation blocked: {str(sec_err)}")
                last_error_message = str(sec_err)
                self.record_runtime_error(
                    error_type="SecuritySandboxViolation",
                    severity="Critical",
                    context=f"security_sandbox_block:{module_name}",
                    query="Static Abstract Syntax Tree scan",
                    traceback_str=str(sec_err),
                    parameters={"module": module_name}
                )
                # Security violations are non-retryable
                break

            except Exception as e:
                tb = traceback.format_exc()
                print(f"[Self-Evolution] ❌ Unexpected error: {str(e)}")
                last_error_message = tb
                
                # Wolverine self-healing: mutate code for next attempt
                if attempt < max_retries:
                    healed_code = self._heal_candidate_code(module_name, function_name, candidate_code, tb)
                    if healed_code != candidate_code:
                        candidate_code = healed_code
                
                self.record_runtime_error(
                    error_type="OrchestratorCrash",
                    severity="Critical",
                    context=f"runtime_crash:{module_name}:attempt_{attempt}",
                    query="Sovereign self-improvement validation pipeline",
                    traceback_str=tb,
                    parameters={"module": module_name, "attempt": attempt}
                )

                if attempt < max_retries:
                    wait_sec = 2 ** attempt
                    print(f"[Self-Evolution] Retrying in {wait_sec}s...")
                    time.sleep(wait_sec)

        # All attempts exhausted — rollback
        print(f"[Self-Evolution] ❌ All {max_retries} attempts failed for {module_name}")

        # Record failed correction
        fingerprint = self._compute_error_fingerprint("EvolutionCycle", module_name, last_error_message)
        self._record_correction(
            fingerprint, "EvolutionCycle", module_name,
            f"Failed to deploy {module_name}.{function_name} after {max_retries} attempts",
            success=False, retry_count=max_retries, error_message=last_error_message
        )

        # Save correction log file to .learnings/corrections/
        try:
            corr_log_path = os.path.join(CORRECTIONS_DIR, f"correction_{module_name}_{int(time.time())}_failed.json")
            with open(corr_log_path, "w", encoding="utf-8") as lf:
                json.dump({
                    "module_name": module_name,
                    "function_name": function_name,
                    "status": "failed",
                    "attempt": attempt,
                    "candidate_code": candidate_code,
                    "performance_score": -1.0,
                    "error_message": last_error_message,
                    "timestamp": datetime.datetime.now().isoformat()
                }, lf, indent=2)
        except Exception as log_err:
            print(f"[Self-Evolution] Warning: failed to write failed correction log: {log_err}")

        # Cleanup
        if os.path.exists(skill_path):
            try:
                os.remove(skill_path)
            except Exception:
                pass
        if git_active and sandbox_branch:
            print(f"[Self-Evolution] Reverting workspace. Switching back to {original_branch}...")
            subprocess.run(["git", "checkout", original_branch], capture_output=True, cwd=PROJECT_ROOT)
            print(f"[Self-Evolution] Deleting sandbox branch {sandbox_branch}...")
            subprocess.run(["git", "branch", "-D", sandbox_branch], capture_output=True, cwd=PROJECT_ROOT)
            subprocess.run(["git", "reset", "--hard", "HEAD"], capture_output=True, cwd=PROJECT_ROOT)

        # Cleanup fixtures
        if os.path.exists(fixtures_path):
            try:
                os.remove(fixtures_path)
            except Exception:
                pass

        return False

    def _heal_candidate_code(self, module_name: str, function_name: str, 
                             code: str, error_message: str) -> str:
        """Wolverine-style generative code self-healer.
        Uses Vertex AI to review the failing code and traceback, and generate a corrected version.
        """
        # Set GCS credentials for Vertex AI if not set
        key_path = os.path.join(PROJECT_ROOT, "scratch", "gcs_key.json")
        if os.path.exists(key_path) and "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
            
        try:
            from google import genai
            client = genai.Client(vertexai=True, project="semiotic-ion-458504-e9", location="us-central1")
        except Exception as e:
            print(f"[Self-Healer] Error initializing GenAI client: {e}")
            return code

        prompt = f"""
You are the Wolverine Self-Healing Debugger for the Keystone Agent Fleet.
We compiled and ran a dynamic skill function `{module_name}.{function_name}`, but the execution failed.

Here is the source code that failed:
```python
{code}
```

Here is the test failure or runtime crash message:
```
{error_message}
```

Please identify the bug, correct the code, and return the COMPLETE corrected python code.
Ensure that:
1. You keep the original function name and signature.
2. The code passes AST security sandboxing rules (no ClassDef or AsyncFunctionDef nodes allowed inside sandboxed skills).
3. Do not include any explanations, markdown code blocks, or preamble. Return ONLY valid, executable Python code.
"""
        print(f"[Self-Healer] Sending failing code of {module_name}.{function_name} to Gemini for self-healing...")
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            healed = response.text.strip()
            # Clean markdown code blocks if present
            if healed.startswith("```python"):
                healed = healed[9:]
            elif healed.startswith("```"):
                healed = healed[3:]
            if healed.endswith("```"):
                healed = healed[:-3]
            healed = healed.strip()
            
            # Simple fallback check: if it looks like code, return it
            if "def " in healed:
                print(f"[Self-Healer] ✅ Generated repaired code candidate for {module_name}.{function_name}")
                return healed
            else:
                print(f"[Self-Healer] ⚠️ Generated output did not look like python code. Reverting to original.")
                return code
        except Exception as e:
            print(f"[Self-Healer] ⚠️ Self-healing API request failed: {e}")
            return code

    def run_weekly_compaction(self) -> dict:
        """
        Scans Transcripts/ log files and compresses them into high-level digests.
        Prunes files older than 7 days, maintaining context bounds below 135k tokens.
        """
        transcripts_dir = os.path.join(PROJECT_ROOT, "Transcripts")
        os.makedirs(transcripts_dir, exist_ok=True)
        
        log_files = [f for f in os.listdir(transcripts_dir) if f.endswith(".log")]
        compaction_report = []
        total_freed_bytes = 0
        pruned_count = 0
        
        print(f"[Compaction Sweep] Evaluating {len(log_files)} subagent logs in {transcripts_dir}...")
        
        # Compile summaries
        summary_records = []
        for f in log_files:
            filepath = os.path.join(transcripts_dir, f)
            stat = os.stat(filepath)
            size_bytes = stat.st_size
            
            # Check age (stale if > 7 days)
            mtime = datetime.datetime.fromtimestamp(stat.st_mtime)
            age_days = (datetime.datetime.now() - mtime).days
            
            if age_days >= 7 or size_bytes > 500000: # Over ~125k tokens / 500kb size
                pruned_count += 1
                total_freed_bytes += size_bytes
                
                # Extract first 500 chars and last 500 chars to form a quick contextual digest
                try:
                    with open(filepath, "r", encoding="utf-8") as log_f:
                        content = log_f.read()
                    
                    summary = f"Log {f} (Age: {age_days}d, Size: {size_bytes} bytes):\n"
                    if len(content) > 1000:
                        summary += f"HEAD:\n{content[:500]}\n...\nTAIL:\n{content[-500:]}\n"
                    else:
                        summary += content
                    summary_records.append(summary)
                    
                    # Delete raw stale log to reclaim token context
                    os.remove(filepath)
                    compaction_report.append(f"Compacted & Pruned: {f} ({size_bytes} bytes reclaimed)")
                except Exception as log_ex:
                    compaction_report.append(f"Error processing {f}: {log_ex}")
                    
        if summary_records:
            digest_file = os.path.join(INSIGHTS_DIR, f"compacted-logs-{datetime.date.today().isoformat()}.md")
            with open(digest_file, "w", encoding="utf-8") as dig_out:
                dig_out.write("# Compacted Agent Execution History\n\n")
                dig_out.write(f"Generated on {datetime.date.today().isoformat()}\n\n")
                dig_out.write("\n\n---\n\n".join(summary_records))
            compaction_report.append(f"Master digest compiled at: {digest_file}")
            
        print(f"[Compaction Sweep] Pruned {pruned_count} files. Freed {total_freed_bytes} bytes of context bloat.")
        
        return {
            "files_evaluated": len(log_files),
            "files_compacted_and_pruned": pruned_count,
            "context_freed_bytes": total_freed_bytes,
            "compaction_logs": compaction_report
        }

    # ─── System Doctor Diagnostics ────────────────────────────────────────

    def run_doctor(self, fix: bool = False, lint: bool = False) -> dict:
        """Runs the doctor diagnostics on the Keystone Agent Fleet environment."""
        import urllib.request
        import urllib.error
        import time
        
        status = {}
        issues = []
        repairs = []
        
        # 1. Check Directory Integrity
        required_dirs = [
            "dynamic_skills",
            "scratch",
            ".learnings",
            ".learnings/errors",
            ".learnings/insights",
            "Master_Docs"
        ]
        status["directories"] = {}
        for d in required_dirs:
            if d == "Master_Docs":
                path = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "00_Master_Brain", d))
            else:
                path = os.path.join(PROJECT_ROOT, d)
            exists = os.path.exists(path)
            status["directories"][d] = exists
            if not exists:
                issues.append(f"Directory missing: {d}")
                if fix:
                    try:
                        os.makedirs(path, exist_ok=True)
                        status["directories"][d] = True
                        repairs.append(f"Created directory: {d}")
                    except Exception as e:
                        issues.append(f"Failed to create directory {d}: {e}")
                        
        # 2. Check Qdrant Connection
        status["qdrant_online"] = False
        try:
            req = urllib.request.Request("http://localhost:6333/dashboard", method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                if resp.status == 200:
                    status["qdrant_online"] = True
        except Exception:
            issues.append("Qdrant service is offline on port 6333")
            if fix:
                repairs.append("Suggested fix: Run 'docker-compose up -d' to start Qdrant container")

        # 3. Check .env file
        env_path = os.path.join(PROJECT_ROOT, ".env")
        status["env_exists"] = os.path.exists(env_path)
        if not status["env_exists"]:
            issues.append(".env file is missing in the workspace root")
            if fix:
                try:
                    with open(env_path, "w", encoding="utf-8") as f:
                        f.write("# Keystone Environment Variables\nQDRANT_URL=http://localhost:6333\n")
                    status["env_exists"] = True
                    repairs.append("Created a template .env file")
                except Exception as e:
                    issues.append(f"Failed to create .env: {e}")

        # 4. Check Token Freshness
        token_files = [
            "youtube_token.json",
            "youtube_token_possibilities.json",
            "youtube_token_protocols.json",
            "youtube_token_oac.json",
            "social_tokens.json"
        ]
        status["tokens"] = {}
        for tf in token_files:
            t_path = os.path.join(PROJECT_ROOT, tf)
            exists = os.path.exists(t_path)
            status["tokens"][tf] = {"exists": exists}
            if exists:
                mtime = os.path.getmtime(t_path)
                age_days = (time.time() - mtime) / 86400.0
                status["tokens"][tf]["age_days"] = round(age_days, 1)
                if age_days > 60:
                    issues.append(f"Token file {tf} is stale ({round(age_days, 1)} days old)")
            else:
                if tf != "youtube_token.json":
                    issues.append(f"Token file missing: {tf}")

        # 5. Check Circuit Breaker Status
        cb_path = os.path.join(PROJECT_ROOT, ".learnings", "circuit_breaker_state.json")
        status["circuit_breaker_ok"] = True
        if os.path.exists(cb_path):
            try:
                with open(cb_path, "r", encoding="utf-8") as f:
                    cb_data = json.load(f)
                state = cb_data.get("state", "CLOSED")
                status["circuit_breaker_state"] = state
                if state == "OPEN":
                    status["circuit_breaker_ok"] = False
                    issues.append(f"Circuit breaker is in OPEN (tripped) state since {cb_data.get('tripped_at')}")
                    if fix:
                        cb_data["state"] = "CLOSED"
                        cb_data["consecutive_failures"] = 0
                        with open(cb_path, "w", encoding="utf-8") as f:
                            json.dump(cb_data, f, indent=2)
                        status["circuit_breaker_ok"] = True
                        repairs.append("Reset circuit breaker state to CLOSED")
            except Exception as e:
                issues.append(f"Error reading circuit_breaker_state.json: {e}")

        # Final score calculation
        base_score = 100
        penalty = len(issues) * 15
        health_score = max(0, base_score - penalty)

        report = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "health_score": health_score,
            "status": "healthy" if health_score > 70 else "degraded",
            "details": status,
            "issues": issues,
            "repairs_applied": repairs
        }
        
        if lint:
            return report
            
        print("\n=== KEYSTONE DOCTOR DIAGNOSTICS ===")
        print(f"Health Score: {health_score}/100 ({report['status'].upper()})")
        print(f"Timestamp: {report['timestamp']}\n")
        
        if issues:
            print("⚠️ Issues Found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ No issues found. Environment is optimal!")
            
        if repairs:
            print("\n🔧 Repairs Applied:")
            for repair in repairs:
                print(f"  - {repair}")
                
        return report

    # ─── Full System Health Check ────────────────────────────────────────

    def run_full_health_check(self) -> dict:
        """Runs a comprehensive health check of the self-evolution subsystem."""
        patterns = self.analyze_error_patterns()
        pruned = self.prune_stale_errors()
        digest = self.generate_daily_digest()

        # Integrate circuit breaker health metrics
        cb_metrics = self.circuit_breaker.get_health_metrics()
        adjusted_health = max(0, patterns["health_score"] - cb_metrics["health_penalty"])

        return {
            "health_score": adjusted_health,
            "raw_health_score": patterns["health_score"],
            "total_errors": patterns["total_error_cards"],
            "recent_errors_7d": len(patterns["recent_errors_7d"]),
            "stale_errors_pruned": pruned,
            "correction_journal_entries": len(self.correction_journal.get("entries", [])),
            "auto_heal_rate": f"{(self.correction_journal.get('stats', {}).get('auto_healed', 0) / max(self.correction_journal.get('stats', {}).get('total_errors', 1), 1) * 100):.1f}%",
            "daily_digest_generated": True,
            "circuit_breaker": cb_metrics,
        }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Keystone Sovereign Self-Evolution Engine")
    parser.add_argument("--health", action="store_true", help="Run full health check")
    parser.add_argument("--digest", action="store_true", help="Generate daily digest")
    parser.add_argument("--patterns", action="store_true", help="Analyze error patterns")
    parser.add_argument("--prune", action="store_true", help="Prune stale errors")
    parser.add_argument("--compact", action="store_true", help="Run weekly log compaction sweep")
    parser.add_argument("--test", action="store_true", help="Run test evolution cycle")
    parser.add_argument("--doctor", action="store_true", help="Run system diagnostics and verify environment")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-repair any issues found by the doctor")
    parser.add_argument("--lint", action="store_true", help="Output doctor diagnostics as a clean JSON lint report")
    args = parser.parse_args()

    engine = SovereignSelfEvolution()

    if args.doctor:
        result = engine.run_doctor(fix=args.fix, lint=args.lint)
        if args.lint:
            print(json.dumps(result, indent=2))
    elif args.health:
        result = engine.run_full_health_check()
        print(json.dumps(result, indent=2))
    elif args.digest:
        engine.generate_daily_digest()
    elif args.patterns:
        patterns = engine.analyze_error_patterns()
        print(json.dumps(patterns, indent=2))
    elif args.prune:
        engine.prune_stale_errors()
    elif args.compact:
        result = engine.run_weekly_compaction()
        print(json.dumps(result, indent=2))
    elif args.test:
        # Mock candidate verification skill compilation test
        test_code = """
def calculate_keyword_density(text: str, target_word: str) -> dict:
    if not text or not target_word:
        return {"density": 0.0, "count": 0}
    words = text.lower().split()
    count = words.count(target_word.lower())
    density = count / len(words) if len(words) > 0 else 0.0
    return {
        "density": density,
        "count": count,
        "total_words": len(words)
    }
"""
        fixtures = [
            {
                "input": {"text": "Wayne Stevenson General Contractor Squamish local Squamish builder", "target_word": "Squamish"},
                "assertions": [
                    {"type": "schema", "keys": ["density", "count", "total_words"]},
                    {"type": "exact", "value": 2, "target": "count"}
                ]
            }
        ]
        engine.run_evolution_cycle("seo_analyzer", "calculate_keyword_density", test_code, fixtures)
    else:
        # Default: run health check
        result = engine.run_full_health_check()
        print(json.dumps(result, indent=2))
