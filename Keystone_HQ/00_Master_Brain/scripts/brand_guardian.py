"""
Brand Guardian
===============

Validates changes to Brand Constitution files before they're committed.
Prevents accidental modification of core brand identity documents.

Usage:
    python brand_guardian.py --check            # Verify brand file integrity
    python brand_guardian.py --propose FILE     # Stage a change for review
"""

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path

from config import MASTER_BRAIN, LEARNINGS, logger, save_json, load_json


BRAND_DIR = MASTER_BRAIN / "Brand_Constitution"

# Core brand files that should never be modified without review
PROTECTED_FILES = [
    "BRAND_VOICE.md",
    "BRAND_VISUAL.md",
    "CURRENT_DIRECTION.md",
    "possibilities/IDENTITY.md",
    "protocol/IDENTITY.md",
    "music/IDENTITY.md",
    "shared/AVATAR_RULES.md",
    "shared/PLATFORM_STANDARDS.md",
]


def _hash_file(path: Path) -> str:
    """SHA-256 hash of file contents."""
    if not path.exists():
        return "MISSING"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def check_integrity() -> dict:
    """Check all protected brand files exist and report their hashes."""
    logger.info("=== BRAND GUARDIAN CHECK ===")
    status = {}

    for rel_path in PROTECTED_FILES:
        full_path = BRAND_DIR / rel_path
        if full_path.exists():
            h = _hash_file(full_path)
            size = full_path.stat().st_size
            status[rel_path] = {"exists": True, "hash": h, "size": size}
            logger.info("  [OK] %s (%s, %d bytes)", rel_path, h, size)
        else:
            status[rel_path] = {"exists": False}
            logger.warning("  [MISSING] %s", rel_path)

    # Save snapshot for drift detection
    snapshot_file = LEARNINGS / "brand_integrity_snapshot.json"
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "files": status,
    }
    save_json(snapshot_file, snapshot)
    logger.info("Snapshot saved to %s", snapshot_file.name)

    return status


def propose_change(file_path: str, description: str = "") -> None:
    """Stage a proposed brand change for Wayne's review."""
    logger.info("=== BRAND CHANGE PROPOSAL ===")
    proposals = load_json(LEARNINGS / "brand_change_proposals.json")
    if not isinstance(proposals, list):
        proposals = []

    proposals.append({
        "file": file_path,
        "description": description,
        "timestamp": datetime.now().isoformat(),
        "status": "pending_review",
    })

    save_json(LEARNINGS / "brand_change_proposals.json", proposals)
    logger.info("Proposal staged for: %s", file_path)
    logger.info("Wayne must review and approve before changes are applied.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brand Guardian")
    parser.add_argument("--check", action="store_true", help="Check brand file integrity")
    parser.add_argument("--propose", type=str, help="File to propose changes for")
    parser.add_argument("--description", type=str, default="", help="Change description")
    args = parser.parse_args()

    if args.check:
        check_integrity()
    elif args.propose:
        propose_change(args.propose, args.description)
    else:
        parser.print_help()
