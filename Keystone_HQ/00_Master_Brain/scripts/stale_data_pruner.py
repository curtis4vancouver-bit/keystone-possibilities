"""
Stale Data Pruner
==================

Finds and flags outdated or bloated data in the Master Brain.
Operates in **safe mode by default** — never deletes anything without
Wayne's explicit approval.

Commands:
    python stale_data_pruner.py          # safe mode (default)
    python stale_data_pruner.py --safe   # same as above
    python stale_data_pruner.py --force  # aggressive mode (not yet implemented)
"""

import argparse
import os
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path

from config import (
    RESEARCH_ARCHIVES, MASTER_BRAIN, LEARNINGS, INSIGHTS_DIR,
    STALE_RESEARCH_DAYS, BLOAT_THRESHOLD_BYTES,
    load_json, save_json, logger, ensure_directories,
)


# ---------------------------------------------------------─
# SCANNING
# ---------------------------------------------------------─
def _find_stale_files(directory: Path, days_old: int) -> list[dict]:
    """Find files older than *days_old* days. Returns metadata dicts."""
    if not directory.exists():
        return []
    cutoff = datetime.now() - timedelta(days=days_old)
    results = []
    for root, _, files in os.walk(directory):
        for name in files:
            path = Path(root) / name
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if mtime < cutoff:
                    age = (datetime.now() - mtime).days
                    results.append({
                        "file":     str(path.relative_to(directory)),
                        "age_days": age,
                        "size_kb":  round(path.stat().st_size / 1024, 1),
                    })
            except OSError:
                pass
    return results


def _find_bloat_files(threshold_bytes: int) -> list[dict]:
    """Find files exceeding the bloat threshold anywhere in Master Brain."""
    bloated = []
    # Known bloat candidates
    candidates = [
        MASTER_BRAIN / "SCRAPED_GOOGLE_DOCS.txt",
        MASTER_BRAIN / "09_UNIFIED_MARKETING_MASTER_PLAN.txt",
    ]
    # Also scan insights for oversized files
    if INSIGHTS_DIR.exists():
        candidates.extend(INSIGHTS_DIR.glob("*"))

    for path in candidates:
        if path.exists() and path.is_file() and path.stat().st_size > threshold_bytes:
            bloated.append({
                "file":    path.name,
                "path":    str(path.relative_to(MASTER_BRAIN)),
                "size_mb": round(path.stat().st_size / (1024 * 1024), 2),
            })
    return bloated


def _find_superseded_research() -> list[dict]:
    """
    Detect research files where a newer version exists.

    Looks for patterns like ``2024_building_code.md`` alongside
    ``2026_building_code.md`` — the older one is superseded.
    """
    if not RESEARCH_ARCHIVES.exists():
        return []

    # Group files by their non-date portion of the filename
    year_re = re.compile(r"(20\d{2})")
    groups: dict[str, list[tuple[int, Path]]] = {}

    for f in RESEARCH_ARCHIVES.rglob("*"):
        if not f.is_file():
            continue
        match = year_re.search(f.stem)
        if match:
            year = int(match.group(1))
            key = year_re.sub("YYYY", f.stem)
            groups.setdefault(key, []).append((year, f))

    superseded = []
    for key, versions in groups.items():
        if len(versions) > 1:
            versions.sort(key=lambda x: x[0])
            # All but the latest are superseded
            for year, path in versions[:-1]:
                superseded.append({
                    "file":         path.name,
                    "year":         year,
                    "superseded_by": versions[-1][1].name,
                })
    return superseded


def _find_duplicate_files(directory: Path) -> list[dict]:
    """Find files that have identical content based on MD5 hashing."""
    if not directory.exists():
        return []
    hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = Path(root) / name
            try:
                # Skip small files to avoid hashing overhead and false positives
                if path.stat().st_size < 1024:
                    continue
                h = hashlib.md5()
                with open(path, "rb") as f:
                    for chunk in iter(lambda: f.read(8192), b""):
                        h.update(chunk)
                file_hash = h.hexdigest()
                hashes.setdefault(file_hash, []).append(path)
            except OSError:
                pass
    
    duplicates = []
    for file_hash, paths in hashes.items():
        if len(paths) > 1:
            # Sort by modification time to keep the oldest file as primary
            paths.sort(key=lambda x: x.stat().st_mtime)
            primary = paths[0]
            for duplicate in paths[1:]:
                duplicates.append({
                    "file":         str(duplicate.relative_to(directory)),
                    "duplicate_of": str(primary.relative_to(directory)),
                    "size_kb":      round(duplicate.stat().st_size / 1024, 1),
                    "hash":         file_hash,
                })
    return duplicates


# ---------------------------------------------------------─
# MAIN PRUNER
# ---------------------------------------------------------─
def prune_data(safe_mode: bool = True) -> dict:
    """
    Run the stale data pruner and generate a report.

    In safe mode (default), nothing is deleted — a JSON report is
    written for Wayne to review on the next bootstrap.
    """
    logger.info("=== STALE DATA PRUNER ===")
    logger.info("Mode: %s", "SAFE (report only)" if safe_mode else "AGGRESSIVE")
    ensure_directories()

    report = {
        "timestamp":  datetime.now().isoformat(),
        "safe_mode":  safe_mode,
        "superseded": _find_superseded_research(),
        "outdated":   _find_stale_files(RESEARCH_ARCHIVES, STALE_RESEARCH_DAYS),
        "bloat":      _find_bloat_files(BLOAT_THRESHOLD_BYTES),
        "duplicates": _find_duplicate_files(RESEARCH_ARCHIVES),
    }

    # Add action_required prompts
    for item in report["outdated"]:
        item["action_required"] = "Run deep research to update? [Y/N]"
    for item in report["bloat"]:
        item["action_required"] = "Archive to Drive and remove locally? [Y/N]"
    for item in report["superseded"]:
        item["action_required"] = f"Delete old version (superseded by {item['superseded_by']})? [Y/N]"
    for item in report["duplicates"]:
        item["action_required"] = f"Delete duplicate file (original: {item['duplicate_of']})? [Y/N]"

    # Save
    ts = datetime.now().strftime("%Y-%m-%d")
    report_file = LEARNINGS / f"stale_report_{ts}.json"
    save_json(report_file, report)

    # Summary
    logger.info("Outdated files:   %d", len(report["outdated"]))
    logger.info("Bloated files:    %d", len(report["bloat"]))
    logger.info("Superseded files: %d", len(report["superseded"]))
    logger.info("Duplicate files:  %d", len(report["duplicates"]))
    logger.info("Report saved: %s", report_file.name)

    if safe_mode:
        logger.info("Safe mode active. No files were deleted or moved.")
        logger.info("Wayne will review the report on the next bootstrap.")

    return report


# ---------------------------------------------------------─
# CLI
# ---------------------------------------------------------─
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stale Data Pruner")
    parser.add_argument(
        "--force", action="store_false", dest="safe_mode",
        help="Aggressive mode (not yet implemented — still safe)",
    )
    parser.add_argument(
        "--safe", action="store_true", dest="safe_mode",
        help="Safe mode: generate report only (default)",
    )
    parser.set_defaults(safe_mode=True)
    args = parser.parse_args()
    prune_data(safe_mode=args.safe_mode)
