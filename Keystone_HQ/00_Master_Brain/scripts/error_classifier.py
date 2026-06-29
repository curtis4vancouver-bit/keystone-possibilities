"""
Error Classification Engine
============================

Hermes-inspired error classification and recovery system.
Classifies errors by pattern matching and correction journal lookup,
returning structured recovery instructions for the agent fleet.

Usage:
    from error_classifier import classify_error, get_recovery_action

    result = classify_error("Rate limit exceeded", error_code=429)
    # => {"type": "rate_limit", "retryable": True, "action": "jittered_backoff", ...}
"""

import re
from typing import Any

from config import (
    ERROR_TYPES,
    CORRECTION_JOURNAL,
    ERRORS_DIR,
    load_json,
    save_json,
    logger,
)
from datetime import datetime


# ---------------------------------------------------------─
# SIMILARITY ENGINE
# ---------------------------------------------------------─
_STRIP_RE = re.compile(r"[^a-z\s]+")


def _normalise(text: str) -> set[str]:
    """Lowercase, strip non-alpha, split into word set."""
    return set(_STRIP_RE.sub(" ", text.lower()).split())


def similar_error(error1: str, error2: str, threshold: float = 0.65) -> bool:
    """
    Return True if two error strings share ≥ *threshold* word overlap.

    The threshold is intentionally loose (0.65) so it matches the same
    root cause even when timestamps, IDs, or file paths in the error
    message differ between occurrences.
    """
    if not error1 or not error2:
        return False
    words1 = _normalise(str(error1))
    words2 = _normalise(str(error2))
    if not words1 or not words2:
        return False
    overlap = len(words1 & words2)
    return overlap / max(len(words1), len(words2)) >= threshold


# ---------------------------------------------------------─
# CLASSIFIER
# ---------------------------------------------------------─
# Order matters — more specific patterns first, generic last.
_PATTERNS: list[tuple[str, list[str], list[int]]] = [
    # (error_type, text_keywords, http_codes)
    ("rate_limit",             ["rate limit", "too many requests", "throttl"],       [429]),
    ("context_overflow",       ["context.*overflow", "context.*exceeded",
                                "token limit", "max.*token"],                        []),
    ("timeout",                ["timeout", "timed out", "deadline exceeded"],        [408, 504]),
    ("auth",                   ["auth", "unauthorized", "unauthenticated",
                                "invalid.*credential", "token expired"],             [401, 403]),
    ("billing",                ["billing", "quota exceeded", "payment required"],    [402]),
    ("overloaded",             ["overloaded", "capacity", "service unavailable"],    [503]),
    ("payload_too_large",      ["payload too large", "request entity too large",
                                "body.*too large"],                                  [413]),
    ("content_policy_blocked", ["policy", "blocked", "content filter",
                                "safety", "harmful"],                                []),
    ("permission_denied",      ["permission denied", "access denied", "forbidden"],  [403]),
    ("not_found",              ["not found", "does not exist", "404"],               [404]),
    ("network_error",          ["connection refused", "dns", "network",
                                "unreachable", "ssl"],                               []),
    ("format_error",           ["format", "parse", "json", "decode",
                                "malformed", "invalid syntax"],                      [400]),
    ("server_error",           [],                                                   [500, 502]),
]


def classify_error(
    error_message: str,
    error_code: int | None = None,
) -> dict[str, Any]:
    """
    Classify an error and return structured recovery instructions.

    1. Check the correction journal for a known fix first.
    2. Walk the pattern table (most-specific → least-specific).
    3. Fall back to ``unknown``.
    """
    error_str = str(error_message).lower()

    # -- Step 1: Journal lookup -----------------------------
    journal = load_json(CORRECTION_JOURNAL)
    for entry in journal:
        if similar_error(error_message, entry.get("error", "")):
            logger.info("Matched known error in correction journal.")
            return {
                "type":      "known_journal_error",
                "retryable": True,
                "action":    "apply_known_fix",
                "fix":       entry.get("fix", ""),
            }

    # -- Step 2: Pattern matching ---------------------------
    for err_type, keywords, codes in _PATTERNS:
        if error_code and error_code in codes:
            return {"type": err_type, **ERROR_TYPES[err_type]}
        for kw in keywords:
            if re.search(kw, error_str):
                return {"type": err_type, **ERROR_TYPES[err_type]}

    # -- Step 3: Generic HTTP 5xx ---------------------------
    if error_code and error_code >= 500:
        return {"type": "server_error", **ERROR_TYPES["server_error"]}

    return {"type": "unknown", **ERROR_TYPES["unknown"]}


def get_recovery_action(
    error_message: str,
    error_code: int | None = None,
) -> str:
    """Convenience: return just the action string."""
    return classify_error(error_message, error_code).get("action", "log_and_notify")


def log_error(
    error_message: str,
    error_code: int | None = None,
    source: str = "unknown",
) -> dict[str, Any]:
    """Classify, log to .learnings/errors/, and return the classification."""
    classification = classify_error(error_message, error_code)

    record = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "error": str(error_message)[:500],
        "code": error_code,
        "classification": classification,
    }

    ERRORS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_json(ERRORS_DIR / f"{ts}_{classification['type']}.json", record)
    logger.info("Error logged: %s → %s", classification["type"], classification["action"])

    return classification


# ---------------------------------------------------------─
# SELF-TEST
# ---------------------------------------------------------─
if __name__ == "__main__":
    print("--- Error Classifier Self-Test ---")
    tests = [
        ("Rate limit exceeded for API",            429),
        ("Context length overflow. Reduce tokens.", None),
        ("Connection refused to localhost:6333",    None),
        ("Permission denied: /etc/shadow",          403),
        ("Unknown weird error occurred.",            None),
        ("Timeout waiting for response",            504),
        ("Payload too large for upload",            413),
    ]
    for msg, code in tests:
        result = classify_error(msg, code)
        print(f"  [{result['type']:>25}] {result['action']:<30} | {msg[:50]}")
