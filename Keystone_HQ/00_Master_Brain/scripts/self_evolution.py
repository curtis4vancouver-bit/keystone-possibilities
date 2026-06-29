"""
Self-Evolution Engine Backbone
===============================

Core engine implementing health checks, data compaction, diagnostics,
and propose-only skill evolution for the Keystone Master Brain.

Commands:
    python self_evolution.py --health     System health check
    python self_evolution.py --compact    Archive old insights, flag bloat
    python self_evolution.py --doctor     Deep diagnostics + systemic error detection
    python self_evolution.py --evolve     Generate PROPOSED_UPDATE.md for skills
"""

import argparse
import os
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from config import (
    MASTER_BRAIN, LEARNINGS, CORRECTION_JOURNAL, IMPROVEMENT_QUEUE,
    INSIGHTS_DIR, DREAM_LOGS, ERRORS_DIR, SKILLS_DIR, PENDING_PROPOSALS,
    SCRIPTS_DIR, SKILL_ERROR_ROUTING, BLOAT_THRESHOLD_BYTES,
    INSIGHT_ARCHIVE_DAYS,
    load_json, save_json, logger, ensure_directories,
)


# ---------------------------------------------------------─
# UTILITIES
# ---------------------------------------------------------─
def _dir_size(path: Path) -> int:
    """Calculate total size of a directory tree in bytes."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                try:
                    total += os.path.getsize(fp)
                except OSError:
                    pass
    return total


def _find_skill_for_error(error_text: str) -> str:
    """Route an error to the most likely responsible skill."""
    lower = str(error_text).lower()
    for keyword, skill_name in SKILL_ERROR_ROUTING.items():
        if keyword in lower:
            return skill_name
    return "00_keystone_foundation"


# ---------------------------------------------------------─
# HEALTH CHECK
# ---------------------------------------------------------─
def health_check() -> dict:
    """Verify system health and report status."""
    logger.info("=== SYSTEM HEALTH CHECK ===")
    ensure_directories()

    checks: dict[str, bool | int | float] = {}

    # Directory existence
    for label, path in [
        ("learnings_dir", LEARNINGS),
        ("insights_dir",  INSIGHTS_DIR),
        ("dream_logs_dir", DREAM_LOGS),
        ("errors_dir",    ERRORS_DIR),
    ]:
        checks[label] = path.exists()

    # JSON file integrity
    for label, path in [
        ("correction_journal", CORRECTION_JOURNAL),
        ("improvement_queue",  IMPROVEMENT_QUEUE),
        ("pending_proposals",  PENDING_PROPOSALS),
    ]:
        try:
            load_json(path)
            checks[label] = True
        except Exception:
            checks[label] = False

    # Counts
    checks["insights_count"]    = len(list(INSIGHTS_DIR.glob("*.md")))
    checks["dream_logs_count"]  = len(list(DREAM_LOGS.glob("*.md")))
    checks["error_logs_count"]  = len(list(ERRORS_DIR.glob("*.json")))
    checks["brain_size_mb"]     = round(_dir_size(MASTER_BRAIN) / (1024 * 1024), 2)

    scraped = MASTER_BRAIN / "SCRAPED_GOOGLE_DOCS.txt"
    checks["scraped_docs_mb"] = (
        round(scraped.stat().st_size / (1024 * 1024), 2)
        if scraped.exists() else 0
    )

    # Last nightly run
    last_run_file = LEARNINGS / "last_nightly_run.json"
    if last_run_file.exists():
        last_run = load_json(last_run_file)
        checks["last_nightly_run"] = last_run.get("timestamp", "never")
    else:
        checks["last_nightly_run"] = "never"

    # Display
    for key, val in checks.items():
        if isinstance(val, bool):
            status = "GREEN" if val else "RED"
        elif isinstance(val, (int, float)):
            status = "GREEN" if val > 0 else "YELLOW"
        else:
            status = "INFO"
        print(f"  [{status:>6}] {key}: {val}")

    return checks


# ---------------------------------------------------------─
# COMPACT
# ---------------------------------------------------------─
def compact() -> int:
    """Archive old insights and flag oversized files."""
    logger.info("=== COMPACTION STARTED ===")
    ensure_directories()

    archived = 0
    cutoff = datetime.now() - timedelta(days=INSIGHT_ARCHIVE_DAYS)
    archive_dir = INSIGHTS_DIR / "_archive"
    archive_dir.mkdir(exist_ok=True)

    for f in INSIGHTS_DIR.glob("*.md"):
        if f.name == "INDEX.md":
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < cutoff:
                dest = archive_dir / f.name
                f.rename(dest)
                archived += 1
                logger.info("  Archived: %s", f.name)
        except OSError as exc:
            logger.warning("  Could not archive %s: %s", f.name, exc)

    logger.info("Archived %d old insight files.", archived)

    # Flag oversized files
    logger.info("Scanning for files >1 MB in .learnings/ ...")
    for f in LEARNINGS.rglob("*"):
        if f.is_file() and f.stat().st_size > 1_000_000:
            size_mb = round(f.stat().st_size / (1024 * 1024), 2)
            print(f"  [WARNING] Oversized: {f.name} ({size_mb} MB)")

    return archived


# ---------------------------------------------------------─
# DOCTOR
# ---------------------------------------------------------─
def doctor() -> None:
    """Deep diagnostics: health check + systemic error detection."""
    logger.info("=== DOCTOR DIAGNOSTICS ===")

    # Auto-run prompt refiner to ensure rules are fully compiled
    try:
        import subprocess
        import sys
        refiner_path = Path(__file__).parent / "prompt_refiner.py"
        if refiner_path.exists():
            subprocess.run(
                [sys.executable, str(refiner_path)],
                capture_output=True, text=True, timeout=30, cwd=str(refiner_path.parent)
            )
    except Exception as e:
        logger.error("Failed to run prompt refiner during doctor: %s", e)

    health_check()

    # Correction journal analysis
    journal = load_json(CORRECTION_JOURNAL)
    if not journal:
        logger.info("Correction journal is empty.")
    else:
        logger.info("Analysing %d correction entries...", len(journal))
        # Cluster by first 60 chars of error text
        buckets = Counter(
            str(entry.get("error", ""))[:60] for entry in journal
        )
        for pattern, count in buckets.most_common(5):
            if count >= 2:
                print(f"  [SYSTEMIC] Seen {count}× : {pattern}…")

    # Dream engine freshness
    try:
        latest_dream = max(DREAM_LOGS.glob("*.md"), key=os.path.getmtime)
        age = (datetime.now() - datetime.fromtimestamp(latest_dream.stat().st_mtime)).days
        if age > 3:
            print(f"  [WARNING] Dream engine hasn't run in {age} days.")
        else:
            print(f"  [  OK  ] Last dream report: {age} day(s) ago.")
    except ValueError:
        print("  [WARNING] No dream logs found.")

    # Error log freshness
    error_files = sorted(ERRORS_DIR.glob("*.json"), key=os.path.getmtime, reverse=True)
    if error_files:
        print(f"  [  INFO ] {len(error_files)} error log(s); latest: {error_files[0].name}")
    else:
        print("  [  OK  ] No error logs recorded.")

    # Bloat check
    scraped = MASTER_BRAIN / "SCRAPED_GOOGLE_DOCS.txt"
    if scraped.exists() and scraped.stat().st_size > BLOAT_THRESHOLD_BYTES:
        size_mb = round(scraped.stat().st_size / (1024 * 1024), 2)
        print(f"  [WARNING] SCRAPED_GOOGLE_DOCS.txt is {size_mb} MB — consider archiving.")


# ---------------------------------------------------------─
# EVOLVE (PROPOSE ONLY)
# ---------------------------------------------------------─
def evolve() -> int:
    """
    Read unprocessed correction journal entries and generate
    PROPOSED_UPDATE.md files in the relevant skill directory.

    Returns the number of new proposals generated.
    """
    logger.info("=== EVOLUTION PROPOSER ===")
    journal = load_json(CORRECTION_JOURNAL)
    proposals: list[dict] = []
    updated_journal: list[dict] = []

    for entry in journal:
        # Skip already-processed entries
        if entry.get("skill_updated", False):
            updated_journal.append(entry)
            continue

        skill = _find_skill_for_error(entry.get("error", ""))
        proposal = {
            "skill":        skill,
            "error":        entry.get("error", ""),
            "proposed_fix": entry.get("prevention", entry.get("fix", "")),
            "timestamp":    entry.get("timestamp", ""),
            "status":       "pending_review",
        }
        proposals.append(proposal)

        # Write PROPOSED_UPDATE.md in the skill directory
        skill_dir = SKILLS_DIR / skill
        if skill_dir.exists():
            prop_file = skill_dir / "PROPOSED_UPDATE.md"
            with open(prop_file, "a", encoding="utf-8") as fh:
                fh.write(
                    f"\n## Proposed Prevention Rule "
                    f"({datetime.now().strftime('%Y-%m-%d')})\n"
                    f"**Error:** {proposal['error']}\n"
                    f"**Prevention:** {proposal['proposed_fix']}\n"
                )
            logger.info("  Proposal written → %s/PROPOSED_UPDATE.md", skill)

        entry["skill_updated"] = True
        updated_journal.append(entry)

    # Persist
    save_json(CORRECTION_JOURNAL, updated_journal)

    existing = load_json(PENDING_PROPOSALS)
    if not isinstance(existing, list):
        existing = []
    existing.extend(proposals)
    save_json(PENDING_PROPOSALS, existing)

    logger.info("Generated %d new skill improvement proposals.", len(proposals))
    if proposals:
        logger.info("Wayne MUST review these with a high-tier model before applying.")

    # DSPy-inspired: Auto-run Prompt Self-Refiner to compile new prevention rules
    try:
        import subprocess
        import sys
        refiner_path = Path(__file__).parent / "prompt_refiner.py"
        if refiner_path.exists():
            logger.info("Auto-running prompt refiner to sync prevention rules...")
            subprocess.run(
                [sys.executable, str(refiner_path)],
                capture_output=True, text=True, timeout=30, cwd=str(refiner_path.parent)
            )
    except Exception as e:
        logger.error("Failed to run prompt refiner: %s", e)

    return len(proposals)


# ---------------------------------------------------------─
# ADD CORRECTION
# ---------------------------------------------------------─
def add_correction(tried: str, wrong_because: str, fix: str, category: str = "orchestration", severity: str = "medium", agent: str = "master") -> None:
    """Add a new structured entry to the correction journal."""
    import uuid
    from config import CORRECTION_JOURNAL_SCHEMA
    
    if not tried or not wrong_because or not fix:
        logger.error("Missing required arguments for correction journal entry.")
        return
        
    journal = load_json(CORRECTION_JOURNAL)
    if not isinstance(journal, list):
        journal = []
        
    entry = {
        "id": f"CJ-{uuid.uuid4().hex[:8]}",
        "tried": tried,
        "wrong_because": wrong_because,
        "fix": fix,
        "prevention_rule": fix,  # Default prevention to fix
        "category": category,
        "severity": severity,
        "agent": agent,
        "timestamp": datetime.now().isoformat(),
        "resolved": True
    }
    
    journal.append(entry)
    save_json(CORRECTION_JOURNAL, journal)
    logger.info("Successfully added correction journal entry: %s", entry["id"])

def verify_code(filepath: str) -> bool:
    """
    Perform an isolated compilation check using ast.parse and execute
    the unit test suite using pytest to verify system stability.
    """
    import ast
    import subprocess
    
    # 1. AST compilation check
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            ast.parse(f.read())
        logger.info(f"[Safe-Compile] AST parse successful for: {filepath}")
    except Exception as e:
        logger.error(f"[Safe-Compile] Syntax validation FAILED for {filepath}: {e}")
        return False

    # 2. Run unit tests via pytest
    try:
        cmd = [
            "python", "-m", "pytest",
            "--ignore=scratch",
            "--ignore=build",
            "--ignore=dist"
        ]
        logger.info(f"[Safe-Compile] Running unit tests via: {' '.join(cmd)}")
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        # returncode 0 means all tests passed, 5 means no tests collected (which is safe)
        if res.returncode in (0, 5):
            logger.info(f"[Safe-Compile] Unit tests passed or no tests collected (exit code {res.returncode})")
            return True
        else:
            logger.error(f"[Safe-Compile] Unit tests FAILED with exit code {res.returncode}")
            if res.stdout:
                logger.error(f"[Safe-Compile] Test stdout:\n{res.stdout[-1000:]}")
            if res.stderr:
                logger.error(f"[Safe-Compile] Test stderr:\n{res.stderr[-1000:]}")
            return False
    except Exception as e:
        logger.error(f"[Safe-Compile] Error executing test suite: {e}")
        return False

# ---------------------------------------------------------─
# CLI
# ---------------------------------------------------------─
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Keystone Self-Evolution Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--health",  action="store_true", help="Run health checks")
    parser.add_argument("--compact", action="store_true", help="Compact old data")
    parser.add_argument("--doctor",  action="store_true", help="Run deep diagnostics")
    parser.add_argument("--evolve",  action="store_true", help="Propose skill updates")
    parser.add_argument("--verify",  type=str, help="Verify syntax and tests of a python file")
    parser.add_argument("--add-correction", action="store_true", help="Add a structured correction entry")
    parser.add_argument("--tried", type=str, help="What action was attempted")
    parser.add_argument("--wrong-because", type=str, help="Why it failed — root cause")
    parser.add_argument("--fix", type=str, help="The exact fix that resolved it")
    args = parser.parse_args()

    if args.health:
        health_check()
    elif args.compact:
        compact()
    elif args.doctor:
        doctor()
    elif args.evolve:
        evolve()
    elif args.verify:
        import sys
        success = verify_code(args.verify)
        sys.exit(0 if success else 1)
    elif args.add_correction:
        add_correction(args.tried, args.wrong_because, args.fix)
    else:
        parser.print_help()
