"""
Redistribute Brain Data
========================

Generates an operations manifest to move vectors from the bloated
``general`` namespace into brand-specific namespaces based on keyword
matching.  The manifest is a JSON file that the Antigravity agent
reads and executes using its MCP ``keystone-brain`` tools.

Usage:
    python redistribute_brain.py --dry-run   # generate plan only (default)
    python redistribute_brain.py --execute   # generate plan (same output)
"""

import argparse
import json
from pathlib import Path

from config import NAMESPACE_KEYWORDS, SCRIPTS_DIR, logger


def generate_redistribution_plan(dry_run: bool = True) -> Path:
    """
    Build a redistribution operations manifest.

    For every keyword in every namespace, creates an operation record:
    ``{ action, source_namespace, target_namespace, query, min_score }``

    Returns the path to the generated JSON file.
    """
    logger.info("=== BRAIN REDISTRIBUTION PLAN ===")
    logger.info("Mode: %s", "DRY RUN" if dry_run else "EXECUTE")

    ops: list[dict] = []
    for namespace, keywords in NAMESPACE_KEYWORDS.items():
        logger.info("Mapping %d keywords → %s", len(keywords), namespace)
        for keyword in keywords:
            ops.append({
                "action":           "search_and_reingest",
                "source_namespace": "general",
                "target_namespace": namespace,
                "query":            keyword,
                "min_score":        0.7,
            })

    ops_file = SCRIPTS_DIR / "_redistribute_ops.json"
    ops_file.write_text(json.dumps(ops, indent=2, ensure_ascii=False), encoding="utf-8")

    logger.info("Generated %d redistribution operations.", len(ops))
    logger.info("Saved to: %s", ops_file)
    logger.info("Antigravity should read this file and execute the MCP tool calls.")

    if not dry_run:
        logger.info("Note: actual execution requires Antigravity to process the ops file.")

    return ops_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redistribute brain data")
    parser.add_argument(
        "--dry-run", action="store_true", default=True,
        help="Only generate the plan (default)",
    )
    parser.add_argument(
        "--execute", dest="dry_run", action="store_false",
        help="Generate plan for execution",
    )
    args = parser.parse_args()
    generate_redistribution_plan(dry_run=args.dry_run)
