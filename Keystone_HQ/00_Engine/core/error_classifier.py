from enum import Enum
from typing import Dict, Any, Optional

class ErrorType(Enum):
    AUTH_FAILURE = "auth_failure"
    AUTH_PERMANENT = "auth_permanent"
    BILLING_LIMIT = "billing_limit"
    RATE_LIMIT = "rate_limit"
    API_OVERLOADED = "api_overloaded"
    SERVER_ERROR = "server_error"
    TIMEOUT_ERROR = "timeout_error"
    CONTEXT_OVERFLOW = "context_overflow"
    PAYLOAD_TOO_LARGE = "payload_too_large"
    IMAGE_TOO_LARGE = "image_too_large"
    MODEL_NOT_FOUND = "model_not_found"
    CONTENT_POLICY_BLOCKED = "content_policy_blocked"
    FORMAT_ERROR = "format_error"
    THINKING_SIGNATURE = "thinking_signature"
    DB_CORRUPTED = "db_corrupted"
    WRITE_CONTENTION = "write_contention"
    DESTRUCTIVE_COMMAND = "destructive_command"
    SKILL_COLLISION = "skill_collision"
    UNAUTHORIZED_DELEGATION = "unauthorized_delegation"
    COMPILATION_ERROR = "compilation_error"
    TEST_FAILURE = "test_failure"
    UNKNOWN = "unknown"

class ClassifiedError:
    """Classified runtime error encapsulating structural recovery hints."""
    def __init__(self, error_type: ErrorType, message: str, retryable: bool = False,
                 should_compress: bool = False, should_fallback: bool = False, backoff_seconds: int = 0):
        self.error_type = error_type
        self.message = message
        self.retryable = retryable
        self.should_compress = should_compress
        self.should_fallback = should_fallback
        self.backoff_seconds = backoff_seconds

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "retryable": self.retryable,
            "should_compress": self.should_compress,
            "should_fallback": self.should_fallback,
            "backoff_seconds": self.backoff_seconds
        }

class ErrorClassifier:
    """Classifies exceptions and raw error strings into structured recovery profiles."""
    
    @staticmethod
    def classify(error: Any) -> ClassifiedError:
        err_msg = str(error).strip()
        
        # Check patterns for categorization
        if not err_msg:
            return ClassifiedError(ErrorType.UNKNOWN, "Empty error string", should_fallback=True)

        err_lower = err_msg.lower()

        # Context Overflow
        if any(w in err_lower for w in ["context window", "context length exceeded", "too many tokens", "maximum context length"]):
            return ClassifiedError(ErrorType.CONTEXT_OVERFLOW, err_msg, should_compress=True, should_fallback=True)

        # Rate Limits
        if any(w in err_lower for w in ["rate limit", "429", "too many requests", "quota exceeded"]):
            return ClassifiedError(ErrorType.RATE_LIMIT, err_msg, retryable=True, backoff_seconds=5)

        # Billing
        if any(w in err_lower for w in ["billing", "credits exhausted", "no balance", "insufficient funds"]):
            return ClassifiedError(ErrorType.BILLING_LIMIT, err_msg, should_fallback=True)

        # Auth Failures
        if any(w in err_lower for w in ["invalid api key", "unauthorized", "invalid token", "401", "forbidden", "403"]):
            if "scope" in err_lower or "permanent" in err_lower:
                return ClassifiedError(ErrorType.AUTH_PERMANENT, err_msg)
            return ClassifiedError(ErrorType.AUTH_FAILURE, err_msg, should_fallback=True)

        # Destructive Command Check
        if "destructive command blocked" in err_lower or "destructivecommandblocked" in err_lower:
            return ClassifiedError(ErrorType.DESTRUCTIVE_COMMAND, err_msg)

        # Database Corruptions / Contentions
        if "database is locked" in err_lower or "db is locked" in err_lower or "sqlite3.operationalerror: database is locked" in err_lower:
            return ClassifiedError(ErrorType.WRITE_CONTENTION, err_msg, retryable=True, backoff_seconds=1)
        if any(w in err_lower for w in ["corrupt", "malformed database", "database disk image is malformed"]):
            return ClassifiedError(ErrorType.DB_CORRUPTED, err_msg)

        # Compilation & Test Failures
        if "syntaxerror" in err_lower or "indentationerror" in err_lower:
            return ClassifiedError(ErrorType.COMPILATION_ERROR, err_msg)
        if "assertionerror" in err_lower or "test failed" in err_lower:
            return ClassifiedError(ErrorType.TEST_FAILURE, err_msg)

        # Server Errors & Timeouts
        if any(w in err_lower for w in ["timeout", "timed out", "connection reset", "504", "502"]):
            return ClassifiedError(ErrorType.TIMEOUT_ERROR, err_msg, retryable=True, backoff_seconds=10)
        if any(w in err_lower for w in ["500", "internal server error", "503", "service unavailable"]):
            return ClassifiedError(ErrorType.SERVER_ERROR, err_msg, retryable=True, backoff_seconds=15, should_fallback=True)

        # Model Not Found
        if "model not found" in err_lower or "unknown model" in err_lower or "model_not_found" in err_lower:
            return ClassifiedError(ErrorType.MODEL_NOT_FOUND, err_msg, should_fallback=True)

        # Image limits
        if "image too large" in err_lower or "payload too large" in err_lower:
            return ClassifiedError(ErrorType.PAYLOAD_TOO_LARGE, err_msg)

        # Content blocked
        if "content policy" in err_lower or "blocked by safety" in err_lower or "finish_reason: safety" in err_lower:
            return ClassifiedError(ErrorType.CONTENT_POLICY_BLOCKED, err_msg)

        # Unauthorized subagent delegation
        if "subagent delegation blocked" in err_lower or "unauthorized_subagent_delegation" in err_lower:
            return ClassifiedError(ErrorType.UNAUTHORIZED_DELEGATION, err_msg)

        # Default fallback
        return ClassifiedError(ErrorType.UNKNOWN, err_msg, retryable=False)
