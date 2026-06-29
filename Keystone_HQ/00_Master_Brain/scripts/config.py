"""
Keystone Self-Evolution Engine — Shared Configuration
=====================================================

Central source of truth for all paths, Google Drive IDs, namespace keyword
mappings, error taxonomy, and utility helpers used across the self-evolution
script suite.

Author:  Keystone Master Brain (auto-generated)
Version: 2.0.0
Date:    2026-06-16
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------─
# LOGGING — unified formatter for all scripts
# ---------------------------------------------------------─
_LOG_FORMAT = "[%(asctime)s] %(levelname)-7s %(message)s"
_LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=_LOG_FORMAT,
    datefmt=_LOG_DATEFMT,
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("keystone")


# ---------------------------------------------------------─
# FILESYSTEM PATHS
# ---------------------------------------------------------─
MASTER_BRAIN = Path(
    r"C:\Users\Curtis\New folder\construction-website"
    r"\Keystone_HQ\00_Master_Brain"
)

LEARNINGS       = MASTER_BRAIN / ".learnings"
CORRECTION_JOURNAL = LEARNINGS / "correction_journal.json"
IMPROVEMENT_QUEUE  = LEARNINGS / "improvement_queue.json"
PENDING_PROPOSALS  = LEARNINGS / "pending_proposals.json"
INSIGHTS_DIR    = LEARNINGS / "insights"
DREAM_LOGS      = LEARNINGS / "dream_logs"
ERRORS_DIR      = LEARNINGS / "errors"
SCRIPTS_DIR     = MASTER_BRAIN / "scripts"
RESEARCH_ARCHIVES = MASTER_BRAIN / "Research_Archives"
CONTENT_PRODUCTION = MASTER_BRAIN / "Content_Production"

SKILLS_DIR = Path(r"C:\Users\Curtis\.gemini\config\skills")


# ---------------------------------------------------------─
# GOOGLE DRIVE IDs (live — confirmed 2026-06-16)
# ---------------------------------------------------------─
BRAIN_EXPORT_FOLDER  = "1o8B6-NQTU1jnPJLBZ3tXfUJD6kKXxhd9"
SPARK_INBOX          = "1VFU98Xssw7sIZxXk6r7l6v1mTBHdqYYE"
SPARK_COMMAND_CENTER = "11UdK4WUSoymm2MIQX290KMAyhqtDOXbv"

BRAIN_DOCS = {
    "brand_identity":     "177cTdJb85WpprCuXW-J4C72LuPq-_XBBV4qsVHwB4B4",
    "operations_manual":  "114MWnoqLub6Evxu2UfBvO2opr4bEKZII621tihWvk88",
    "correction_journal": "1MtV6hDQ-bFSb_aTEzQDdE82kTKyazFSFnBqKN0pQWVQ",
    "content_pipeline":   "1oUrYbr7AtUuPNsnss0JqrAaIqSQvYL2oeUza55AiRao",
    "seo_strategy":       "16U-NWxgFLRHPFO3T3MLCGguOQd8PQJFK1TaRplV90cg",
    "mcp_inventory":      "1N5dpHBe-e_uRraw3tj9ZUyGPpsuhGvSTaL_SJ76YgyU",
}

RESEARCH_DOCS = {
    "building_codes":    "1iz31BO8DgXKA21_Z9I92ed5ENCHKsvcOy5VFZ_tJCSE",
    "seo_trends":        "1moC08AqQKOnZG3GohDFWi0Ch2fNJYz3SOZe-uzl1xzQ",
    "music_trends":      "1ghtt256H9bPP0j0u8KSOBPaCI2eXEKm2Ky8BSCq8tzs",
    "ai_systems":        "1By1peqiu7nfRevp7UQizU2-y-etehPcHFHbSTK2x2t8",
    "client_strategies": "1kmGdzAlPERehP57dzeMS_AuHKKb731KqYV09ii2Ptuk",
    "social_trending":   "1zoCs9RrtiqB2LeqaEyghsBKZ9LV4_QyQuNWprHLeel4",
    "contractor_audit":  "16x5WV09AMhRQk2orrlksM-8Lr78OmH8PS77hC5z8ub0",
}

TRACKER_SHEETS = {
    "recomp_outreach":     "1lGFQoxSnm9lra6--kDrv2v4TdOkRjPiwfagvPGo8Ma0",
    "poss_outreach":       "16IFSVUUY0mLzma1uBaHaVqVEjt-3RWLZaLrs1wdTLFk",
    "recomp_backlinks":    "1f_EdVhosugRlCJPLPHpjBuBuXOjm5HWgd9IpbuFgAJQ",
    "poss_backlinks":      "1uXtx8oNH_4ZTEfKC_qEGqPJap_cyKfF9jlpx5cLxsVo",
    "realtor_leads":       "1byzFblxplCDG4ByTRC-9bwEiwiObd7VFx8IfwL_p5V4",
    "competitor_hashtags": "16R3MkVQfRXqI-abWwaHlLe103D7k1X0-gtb_kiHIDyY",
}


# ---------------------------------------------------------─
# BRAIN NAMESPACES & KEYWORD ROUTING
# ---------------------------------------------------------─
NAMESPACE_KEYWORDS: dict[str, list[str]] = {
    "possibilities": [
        "construction", "project management", "civil contractor", "excavation",
        "foundation", "framing", "Bill 44", "building code", "Step Code",
        "zoning", "permit", "WorkSafeBC", "National Home Warranty",
        "Keystone Possibilities", "Sea-to-Sky", "Squamish", "Whistler",
        "realtor", "architect", "engineer", "BC Hydro", "WBI",
        "BCBC", "VBBL", "District of Squamish", "RMOW",
    ],
    "music": [
        "Recomposition music", "Spotify", "streaming", "432 Hz", "frequency",
        "ambient", "focus mix", "recovery track", "solfeggio", "TooLost",
        "MusicBrainz", "ISRC", "waveform", "deep house", "album art",
        "Ana Stevenson", "DJ set", "binaural",
    ],
    "protocol_brand": [
        "peptide", "BPC-157", "TB-500", "Wolverine Stack", "biohacking",
        "protocol", "semaglutide", "tirzepatide", "GLP-1", "sarcopenia",
        "mTOR", "angiogenesis", "testosterone", "metabolic", "longevity",
        "Wayne weight", "recovery protocol", "Recomposition Protocol",
        "retatrutide", "creatine", "zinc carnosine",
    ],
    "content_pipeline": [
        "Google Flow", "DaVinci Resolve", "timeline assembly", "B-roll",
        "thumbnail", "script format", "video production", "upload",
        "YouTube metadata", "avatar", "Victoria", "Ana", "HeyGen",
        "Omi", "teleprompter",
    ],
}


# ---------------------------------------------------------─
# CORRECTION JOURNAL SCHEMA
# ---------------------------------------------------------─
CORRECTION_JOURNAL_SCHEMA = {
    "id": str,
    "tried": str,
    "wrong_because": str,
    "fix": str,
    "prevention_rule": str,
    "category": str,  # upload|scripting|visual|api|memory|orchestration|research
    "severity": str,  # low|medium|high|critical
    "agent": str,
    "timestamp": str, # ISO 8601
    "resolved": bool
}

# ---------------------------------------------------------─
# MEMORY DECAY & PROMOTION RULES
# ---------------------------------------------------------─
MEMORY_DECAY_HALF_LIFE_DAYS = 30.0
MEMORY_PROMOTION_THRESHOLD = 0.6
MEMORY_PRUNE_THRESHOLD = 0.1
MEMORY_PRUNE_MIN_AGE_DAYS = 14

# ---------------------------------------------------------─
# ERROR CLASSIFICATION TAXONOMY (Hermes architecture)
# ---------------------------------------------------------─
ERROR_TYPES: dict[str, dict] = {
    "auth":                   {"retryable": False, "action": "rotate_credential"},
    "auth_permanent":         {"retryable": False, "action": "notify_wayne"},
    "billing":                {"retryable": False, "action": "rotate_provider"},
    "rate_limit":             {"retryable": True,  "action": "jittered_backoff",
                               "base_s": 5, "cap_s": 120},
    "overloaded":             {"retryable": True,  "action": "backoff",
                               "base_s": 10},
    "server_error":           {"retryable": True,  "action": "retry",
                               "max_retries": 3},
    "timeout":                {"retryable": True,  "action": "exponential_backoff",
                               "max_retries": 3},
    "context_overflow":       {"retryable": False, "action": "compress_context"},
    "payload_too_large":      {"retryable": False, "action": "chunk_and_retry"},
    "content_policy_blocked": {"retryable": False, "action": "log_and_skip"},
    "format_error":           {"retryable": True,  "action": "check_journal_then_retry"},
    "network_error":          {"retryable": True,  "action": "retry",
                               "max_retries": 5},
    "permission_denied":      {"retryable": False, "action": "notify_wayne"},
    "not_found":              {"retryable": False, "action": "log_and_skip"},
    "unknown":                {"retryable": False, "action": "log_and_notify"},
}

# Map error keywords to the skill most likely to need the fix.
SKILL_ERROR_ROUTING: dict[str, str] = {
    "youtube":     "upload_quality_gate",
    "upload":      "upload_quality_gate",
    "davinci":     "keystone_davinci_timeline_assembly",
    "timeline":    "keystone_davinci_timeline_assembly",
    "flow":        "google_flow_automation",
    "avatar":      "google_flow_automation",
    "seo":         "11_webmaster",
    "sitemap":     "11_webmaster",
    "indexing":    "11_webmaster",
    "music":       "08_music_brand",
    "spotify":     "08_music_brand",
    "isrc":        "08_music_brand",
    "protocol":    "05_protocol_script_studio",
    "peptide":     "05_protocol_script_studio",
    "legal":       "12_legal_counsel",
    "compliance":  "12_legal_counsel",
    "contract":    "12_legal_counsel",
    "tax":         "13_tax_strategist",
    "deduction":   "13_tax_strategist",
    "brain":       "keystone_session_bootstrap",
    "vector":      "keystone_session_bootstrap",
    "qdrant":      "keystone_session_bootstrap",
    "bootstrap":   "keystone_session_bootstrap",
    "research":    "keystone_chrome_research_automation",
    "chrome":      "keystone_chrome_research_automation",
    "blueprint":   "15_site_superintendent",
    "inspection":  "15_site_superintendent",
}

# Bloat thresholds (bytes)
BLOAT_THRESHOLD_BYTES = 10_000_000   # 10 MB
INSIGHT_ARCHIVE_DAYS  = 90
STALE_RESEARCH_DAYS   = 180


# ---------------------------------------------------------─
# HELPER FUNCTIONS
# ---------------------------------------------------------─
def load_json(path: Path) -> list | dict:
    """Safely load a JSON file, returning [] or {} on any error."""
    if not path.exists():
        return _default_for(path)
    try:
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            return _default_for(path)
        return json.loads(text)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        logger.warning("Failed to load %s: %s", path.name, exc)
        return _default_for(path)


def _default_for(path: Path) -> list | dict:
    """Return the appropriate empty container for a given JSON file."""
    list_files = {
        "correction_journal.json",
        "improvement_queue.json",
        "pending_proposals.json",
    }
    if path.name in list_files or path.name.endswith("s.json"):
        return []
    return {}


def save_json(path: Path, data: list | dict) -> None:
    """Atomically write JSON data to *path*, creating parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)          # atomic on Windows NTFS
    except OSError:
        # Fallback: direct write
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def log(msg: str) -> None:
    """Legacy convenience wrapper — prefer ``logger.info()`` in new code."""
    logger.info(msg)


def query_correction_journal(task_keywords: str) -> list[dict]:
    """
    Search the correction journal for entries matching the provided keywords.
    Keywords should be a space-separated string of terms.
    """
    journal = load_json(CORRECTION_JOURNAL)
    if not isinstance(journal, list):
        return []
        
    keywords = [k.lower() for k in task_keywords.split() if len(k) > 2]
    if not keywords:
        return []
        
    results = []
    for entry in journal:
        # Check against text fields
        search_text = f"{entry.get('error', '')} {entry.get('fix', '')} {entry.get('prevention_rule', '')} {entry.get('category', '')}".lower()
        
        # Simple overlap scoring
        score = sum(1 for k in keywords if k in search_text)
        if score > 0:
            # Create a copy with score for sorting
            result_entry = dict(entry)
            result_entry['_score'] = score
            results.append(result_entry)
            
    # Sort by score descending
    results.sort(key=lambda x: x['_score'], reverse=True)
    
    # Remove temporary score key
    for r in results:
        del r['_score']
        
    return results

def ensure_directories() -> None:
    """Create all required Master Brain subdirectories if missing."""
    dirs = [
        LEARNINGS,
        INSIGHTS_DIR,
        INSIGHTS_DIR / "_archive",
        DREAM_LOGS,
        ERRORS_DIR,
        ERRORS_DIR / "_archive",
        SCRIPTS_DIR,
        RESEARCH_ARCHIVES,
        CONTENT_PRODUCTION,
        MASTER_BRAIN / "Omi_Inbox",
        MASTER_BRAIN / "Agent_Panels",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
