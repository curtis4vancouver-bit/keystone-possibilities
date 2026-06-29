"""
Sync Brain to Drive
====================

Compiles local brain updates into a JSON operations manifest for
the Antigravity agent to push to Google Drive.  This keeps Spark
and NotebookLM in sync with the local Master Brain state.

Usage:
    python sync_brain_to_drive.py
"""

import json
from datetime import datetime
from pathlib import Path

from config import (
    BRAIN_DOCS, INSIGHTS_DIR, CORRECTION_JOURNAL,
    IMPROVEMENT_QUEUE, PENDING_PROPOSALS, SCRIPTS_DIR,
    load_json, logger, ensure_directories,
)


def generate_sync_operations() -> Path:
    """
    Generate JSON operations for Antigravity to push brain updates
    to the corresponding Google Docs.

    Returns the path to the generated operations file.
    """
    logger.info("=== BRAIN SYNC OPERATIONS ===")
    ensure_directories()

    ops: list[dict] = []
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Sync Correction Journal (latest entry only)
    try:
        journal = load_json(CORRECTION_JOURNAL)
        if journal:
            latest = journal[-1]
            text = (
                f"\n\n## Update {today}\n"
                f"**Error:** {latest.get('error', '')}\n"
                f"**Fix:** {latest.get('fix', '')}\n"
                f"**Prevention:** {latest.get('prevention', 'N/A')}\n"
            )
            ops.append({
                "action": "appendToGoogleDoc",
                "docId":  BRAIN_DOCS["correction_journal"],
                "text":   text,
            })
    except Exception as exc:
        logger.warning("Error reading journal for sync: %s", exc)

    # 2. Sync Daily Digest → Operations Manual
    digest_path = INSIGHTS_DIR / f"{today}-daily-digest.md"
    if digest_path.exists():
        try:
            digest_text = digest_path.read_text(encoding="utf-8")[:2000]
            ops.append({
                "action": "appendToGoogleDoc",
                "docId":  BRAIN_DOCS["operations_manual"],
                "text":   f"\n\n## Daily Digest {today}\n{digest_text}",
            })
        except OSError as exc:
            logger.warning("Could not read digest: %s", exc)

    # 3. Sync Pending Proposals → Content Pipeline doc
    proposals = load_json(PENDING_PROPOSALS)
    pending = [p for p in proposals if isinstance(p, dict) and p.get("status") == "pending_review"]
    if pending:
        proposal_text = f"\n\n## Pending Proposals ({today}) — {len(pending)} items\n"
        for p in pending[:5]:
            proposal_text += f"- **Skill:** {p.get('skill', '?')} — {str(p.get('error', ''))[:100]}\n"
        ops.append({
            "action": "appendToGoogleDoc",
            "docId":  BRAIN_DOCS["content_pipeline"],
            "text":   proposal_text,
        })

    # Write operations manifest
    ops_file = SCRIPTS_DIR / "_sync_operations.json"
    ops_file.write_text(json.dumps(ops, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Generated %d sync operations.", len(ops))
    logger.info("Saved to: %s", ops_file)
    logger.info("Antigravity agent should process this file to update Drive.")

    return ops_file


if __name__ == "__main__":
    generate_sync_operations()
