import time
import random
from typing import Dict, Any, Callable, Optional
from core.state_store import StateStore
from core.conversation_compressor import ConversationCompressor
from core.error_classifier import ErrorClassifier, ErrorType, ClassifiedError

class SelfHealer:
    """
    Orchestrates recovery actions based on error classifications.
    Executes database repair, context compaction, and retry backoffs.
    """
    def __init__(self, state_store: StateStore, compressor: ConversationCompressor):
        self.state_store = state_store
        self.compressor = compressor

    def handle_error(self, session_id: str, error: Any, attempt: int = 1) -> Dict[str, Any]:
        """
        Main entry point for handling an execution error.
        Classifies the error, determines the recovery action, and executes it.
        Returns a dict indicating recovery status, action to take, and sleep duration if applicable.
        """
        classified = ErrorClassifier.classify(error)
        print(f"[SelfHealer] 🩺 Error classified: Type={classified.error_type.value} | Retryable={classified.retryable}")

        response = {
            "status": "unrecovered",
            "action": "halt",
            "error_type": classified.error_type.value,
            "sleep_seconds": 0
        }

        # Case 1: Context Overflow -> Auto-Compress
        if classified.error_type == ErrorType.CONTEXT_OVERFLOW or classified.should_compress:
            print("[SelfHealer] 🔄 Context overflow detected. Triggering conversation compressor...")
            compacted = self.compressor.evaluate_and_compact_session(session_id, threshold_chars=0) # Force compaction
            if compacted:
                response["status"] = "recovered"
                response["action"] = "retry"
                print("[SelfHealer] Context compacted successfully. Ready to retry.")
            else:
                print("[SelfHealer] Compaction could not save enough space. Halting.")

        # Case 2: Database Corruption -> Auto-Repair
        elif classified.error_type == ErrorType.DB_CORRUPTED:
            print("[SelfHealer] 🛠️ SQLite corruption detected. Running database repair protocol...")
            try:
                self.state_store.repair_database()
                response["status"] = "recovered"
                response["action"] = "retry"
                print("[SelfHealer] Database self-repair completed. Ready to retry.")
            except Exception as repair_err:
                print(f"[SelfHealer] Database repair failed: {repair_err}")

        # Case 3: Rate Limits & Write Contention & Server Errors -> Backoff
        elif classified.retryable:
            base_backoff = classified.backoff_seconds or 5
            # Exponential backoff: base * 2^attempt + jitter (0-2s)
            backoff = min(120.0, base_backoff * (2 ** (attempt - 1)) + random.uniform(0.1, 2.0))
            print(f"[SelfHealer] Retryable error ({classified.error_type.value}). Sleeping for {backoff:.2f}s before retry...")
            
            response["status"] = "recovered"
            response["action"] = "retry"
            response["sleep_seconds"] = backoff

        # Case 4: Fallback options
        elif classified.should_fallback:
            print(f"[SelfHealer] Non-retryable error ({classified.error_type.value}). Model fallback recommended.")
            response["status"] = "fallback"
            response["action"] = "change_model"

        return response

    def execute_with_recovery(self, session_id: str, operation: Callable[[], Any], max_attempts: int = 3) -> Any:
        """
        Wrapper that runs a callable within a self-healing loop.
        Applies exponential backoff and compaction retries automatically.
        """
        attempt = 0
        while attempt < max_attempts:
            attempt += 1
            try:
                result = operation()
                return result
            except Exception as e:
                if attempt >= max_attempts:
                    raise e
                
                recovery = self.handle_error(session_id, e, attempt)
                if recovery["status"] == "recovered" and recovery["action"] == "retry":
                    sleep_time = recovery.get("sleep_seconds", 0)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
                    continue
                else:
                    raise e
