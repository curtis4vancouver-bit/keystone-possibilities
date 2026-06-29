"""
Nightly Orchestrator
=====================

Master sequencer for the 1 AM – 6 AM overnight cycle.
Executes each phase in order, logs results, and writes
a persistent run log so the morning bootstrap can verify
the cycle completed.

Usage:
    python nightly_orchestrator.py
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from config import SCRIPTS_DIR, MASTER_BRAIN, LEARNINGS, logger, ensure_directories


# ---------------------------------------------------------─
# SCRIPT RUNNER
# ---------------------------------------------------------─
def _run_script(script_name: str, *args: str) -> bool:
    """
    Execute a sibling Python script via subprocess.

    Sets ``cwd`` to MASTER_BRAIN so that ``from config import …``
    resolves correctly regardless of how the orchestrator was launched
    (e.g., from Windows Task Scheduler or a cron job).
    """
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        logger.error("Script not found: %s", script_path)
        return False

    cmd = [sys.executable, str(script_path)] + list(args)
    logger.info("Running: %s %s", script_name, " ".join(args))

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            cwd=str(MASTER_BRAIN),
            timeout=300,           # 5-minute safety valve per script
        )
        for line in result.stdout.splitlines():
            stripped = line.strip()
            if stripped:
                logger.info("  [%s] %s", script_name, stripped)
        return True

    except subprocess.TimeoutExpired:
        logger.error("TIMEOUT running %s (exceeded 300 s)", script_name)
        return False

    except subprocess.CalledProcessError as exc:
        logger.error("FAILED %s (exit code %d)", script_name, exc.returncode)
        if exc.stdout:
            logger.error("stdout: %s", exc.stdout[:500])
        if exc.stderr:
            logger.error("stderr: %s", exc.stderr[:500])
        return False


# ---------------------------------------------------------─
# NIGHTLY SEQUENCE
# ---------------------------------------------------------─
_PHASES = [
    # (phase_name, script, args)
    ("Brain Sync",           "sync_brain_to_drive.py",        []),
    ("Research Prompts",     "nightly_research_scheduler.py",  []),
    ("Brain Redistribution", "redistribute_brain.py",         ["--execute"]),
    ("Dream Consolidation",  "dream_engine.py",               ["--dream"]),
    ("Stale Data Check",     "stale_data_pruner.py",          ["--safe"]),
    ("Skill Evolution",      "self_evolution.py",             ["--evolve"]),
    ("Health Check",         "self_evolution.py",             ["--health"]),
]


def run_nightly() -> dict:
    """Execute the full nightly sequence and return a summary."""
    logger.info("=======================================")
    logger.info("   NIGHTLY ORCHESTRATOR STARTED")
    logger.info("=======================================")
    ensure_directories()

    results: dict[str, bool] = {}
    start_time = datetime.now()

    for idx, (name, script, args) in enumerate(_PHASES, 1):
        logger.info("")
        logger.info("--- Phase %d/%d: %s ---", idx, len(_PHASES), name)
        success = _run_script(script, *args)
        results[name] = success
        if not success:
            logger.warning("Phase '%s' failed — continuing with next phase.", name)

    # Phase for Chrome deep research (handled by Antigravity scheduling)
    logger.info("")
    logger.info("--- Chrome Deep Research ---")
    logger.info("  This phase is handled by the Antigravity /schedule command.")
    logger.info("  The 'keystone-chrome-research-automation' skill reads")
    logger.info("  tonight_research_prompts.json and executes 3-tab sessions.")

    elapsed = (datetime.now() - start_time).total_seconds()
    passed  = sum(1 for v in results.values() if v)
    failed  = sum(1 for v in results.values() if not v)

    logger.info("")
    logger.info("=======================================")
    logger.info("   NIGHTLY ORCHESTRATOR COMPLETE")
    logger.info("   Passed: %d | Failed: %d | Time: %.1fs", passed, failed, elapsed)
    logger.info("=======================================")

    # Persistent run log
    run_log = {
        "timestamp":     datetime.now().isoformat(),
        "elapsed_s":     round(elapsed, 1),
        "phases_total":  len(_PHASES),
        "phases_passed": passed,
        "phases_failed": failed,
        "results":       {k: ("PASS" if v else "FAIL") for k, v in results.items()},
        "status":        "complete" if failed == 0 else "partial",
    }
    log_file = LEARNINGS / "last_nightly_run.json"
    log_file.write_text(
        json.dumps(run_log, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.info("Run log saved: %s", log_file.name)

    return run_log


if __name__ == "__main__":
    run_nightly()
