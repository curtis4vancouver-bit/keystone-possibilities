import os
import sys
import json
import datetime
from pathlib import Path
from typing import Any

# Force UTF-8
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Import Master Brain config
try:
    from config import LEARNINGS, CORRECTION_JOURNAL, logger
except ImportError:
    # Fallback paths
    PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__))).parent
    LEARNINGS = PROJECT_ROOT / ".learnings"
    CORRECTION_JOURNAL = LEARNINGS / "correction_journal.json"
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("keystone")

RULES_OUTPUT = LEARNINGS / "refined_prevention_rules.json"

def load_json_file(path: Path, default_val: Any) -> Any:
    if not path.exists():
        return default_val
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"[Refiner] Error loading {path.name}: {e}")
        return default_val

def save_json_file(path: Path, data: Any):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"[Refiner] Saved data to: {path}")
    except Exception as e:
        logger.error(f"[Refiner] Error saving {path.name}: {e}")

def run_prompt_refinement() -> int:
    logger.info("=== STARTING PROMPT REFINEMENT ===")
    
    # Load existing rules to preserve bootstrap or manually added rules
    existing_rules = load_json_file(RULES_OUTPUT, [])
    if not isinstance(existing_rules, list):
        # If it was in the v1 dict format, extract the list
        if isinstance(existing_rules, dict) and "rules" in existing_rules:
            existing_rules = existing_rules["rules"]
        else:
            existing_rules = []
            
    # Normalize existing rules by rule text for deduplication
    existing_text_map = {}
    max_id_num = 0
    for r in existing_rules:
        rule_text = r.get("rule", "").strip()
        if rule_text:
            existing_text_map[rule_text.lower()] = r
        # Try to parse rule ID (e.g. PREV-014 or PR-014) to find the max number
        r_id = r.get("id", "")
        for prefix in ["PREV-", "PR-", "PR"]:
            if r_id.startswith(prefix):
                try:
                    num = int(r_id[len(prefix):])
                    if num > max_id_num:
                        max_id_num = num
                except ValueError:
                    pass

    # Load correction journal
    journal = load_json_file(CORRECTION_JOURNAL, [])
    if isinstance(journal, dict):
        journal = journal.get("entries", [])
        
    new_rules_added = 0
    
    for entry in journal:
        # Get prevention rule text
        prev = entry.get("prevention_rule", entry.get("prevention", "")).strip()
        if not prev:
            continue
            
        # Deduplicate: check if this rule text is already present
        if prev.lower() in existing_text_map:
            continue
            
        # Create a new rule
        max_id_num += 1
        new_rule_id = f"PREV-{max_id_num:03d}"
        
        # Get timestamp safely
        timestamp = entry.get("timestamp", entry.get("fix_applied_at", ""))
        created_date = timestamp[:10] if timestamp else datetime.date.today().isoformat()
        
        new_rule = {
            "id": new_rule_id,
            "rule": prev,
            "source": "correction_journal",
            "created": created_date,
            "severity": entry.get("severity", "medium")
        }
        
        existing_rules.append(new_rule)
        existing_text_map[prev.lower()] = new_rule
        new_rules_added += 1
        logger.info(f"  [NEW RULE] {new_rule_id}: {prev[:80]}...")
        
    if new_rules_added > 0:
        save_json_file(RULES_OUTPUT, existing_rules)
        logger.info(f"Refined rules updated: promoted {new_rules_added} new prevention rules.")
    else:
        logger.info("No new prevention rules needed.")
        
    return new_rules_added

if __name__ == "__main__":
    run_prompt_refinement()
