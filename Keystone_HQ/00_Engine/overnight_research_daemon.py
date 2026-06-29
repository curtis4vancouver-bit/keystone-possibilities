"""
Keystone Overnight Chrome Research Daemon v1.0
==============================================
Automates Google Deep Research via Chrome DevTools MCP.

Strategy:
  - Opens 3 Chrome tabs with Deep Research prompts
  - Waits for research to complete (~5-10 min per prompt)
  - Extracts the research results
  - Ingests into the brain vector DB
  - Closes tabs, opens 3 new ones
  - Repeats on a credit-aware timer

Usage:
  python overnight_research_daemon.py --start      # Full overnight run
  python overnight_research_daemon.py --dry-run     # Simulate without Chrome
  python overnight_research_daemon.py --status      # Show queue status
  python overnight_research_daemon.py --report      # Generate morning report

NOTE: This script is designed to be called BY Antigravity, not standalone.
      The actual Chrome automation runs through the Chrome DevTools MCP.
      This script manages the queue, timing, and ingestion pipeline.
"""

import os
import sys
import json
import time
import datetime
import hashlib
import subprocess

# Force UTF-8 output on Windows to handle emojis in reports
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
QUEUE_FILE = os.path.join(PROJECT_ROOT, "learning_queue.json")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "Deep_Research_Results")
OVERNIGHT_LOG = os.path.join(PROJECT_ROOT, ".learnings", "insights", "overnight_session_log.json")
BRAIN_INGEST_SCRIPT = os.path.join(PROJECT_ROOT, "scratch", "ingest_deep_research.py")
CREDIT_STATE_FILE = os.path.join(PROJECT_ROOT, ".learnings", "insights", "credit_state.json")

os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OVERNIGHT_LOG), exist_ok=True)


class OvernightResearchDaemon:
    def __init__(self):
        self.queue = self._load_queue()
        self.session_log = {
            "session_start": datetime.datetime.now().isoformat(),
            "session_end": None,
            "topics_researched": [],
            "topics_failed": [],
            "total_brain_chunks_added": 0,
            "credit_pauses": 0,
            "cycles_completed": 0
        }

    def _load_queue(self) -> dict:
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"queue": []}

    def _save_queue(self):
        self.queue["last_updated"] = datetime.datetime.now().isoformat()
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.queue, f, indent=2, ensure_ascii=False)

    def _save_session_log(self):
        with open(OVERNIGHT_LOG, "w", encoding="utf-8") as f:
            json.dump(self.session_log, f, indent=2, ensure_ascii=False)

    def get_next_batch(self, batch_size: int = 3) -> list:
        """
        Pulls the next batch of unresearched topics from the queue.
        Prioritizes by domain priority (1 = highest).
        Returns list of {"domain": ..., "topic": ..., "prompt": ...}
        """
        batch = []
        # Sort domains by priority
        sorted_domains = sorted(self.queue["queue"], key=lambda d: d.get("priority", 99))

        for domain in sorted_domains:
            if len(batch) >= batch_size:
                break
            completed = set(domain.get("completed", []))
            for topic in domain.get("topics", []):
                if topic not in completed and len(batch) < batch_size:
                    # Build the Deep Research prompt
                    prompt = self._build_research_prompt(domain["domain"], topic)
                    batch.append({
                        "domain": domain["domain"],
                        "topic": topic,
                        "prompt": prompt,
                        "domain_description": domain.get("description", "")
                    })
        return batch

    def _build_research_prompt(self, domain: str, topic: str) -> str:
        """Builds an optimized Google Deep Research prompt for a topic."""
        return (
            f"Activate Deep Research. Thoroughly analyze: {topic}. "
            f"Context: This research is for an autonomous AI agent system (Keystone Sovereign) "
            f"that manages a construction business, YouTube channels, and health content empire. "
            f"Domain area: {domain.replace('_', ' ')}. "
            f"Provide actionable, specific technical details, code examples where applicable, "
            f"current best practices as of May 2026, and any tools, libraries, or services mentioned. "
            f"Include specific version numbers, URLs, and configuration details."
        )

    def mark_topic_completed(self, domain_name: str, topic: str, success: bool = True):
        """Marks a topic as completed in the queue."""
        for domain in self.queue["queue"]:
            if domain["domain"] == domain_name:
                if "completed" not in domain:
                    domain["completed"] = []
                if topic not in domain["completed"]:
                    domain["completed"].append(topic)

                # Check if all topics in domain are done
                if len(domain["completed"]) >= len(domain["topics"]):
                    domain["status"] = "completed"

                # Update stats
                if success:
                    self.session_log["topics_researched"].append({
                        "domain": domain_name,
                        "topic": topic,
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                else:
                    self.session_log["topics_failed"].append({
                        "domain": domain_name,
                        "topic": topic,
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                break
        self._save_queue()

    def save_research_result(self, domain: str, topic: str, content: str) -> str:
        """
        Saves research results as markdown in Deep_Research_Results/ for brain ingestion.
        Returns the filepath.
        """
        # Create a clean filename
        safe_name = topic.lower()
        for char in [" ", "/", "\\", ":", "?", "*", '"', "<", ">", "|"]:
            safe_name = safe_name.replace(char, "_")
        safe_name = safe_name[:60]  # Truncate long names
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"{date_str}_{domain}_{safe_name}.md"
        filepath = os.path.join(RESULTS_DIR, filename)

        md_content = f"""# Deep Research: {topic}
**Domain:** {domain.replace('_', ' ').title()}
**Researched:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
**Source:** Google Deep Research via Chrome Automation

---

{content}

---
*Auto-ingested into Keystone Brain Vector DB*
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"[Overnight Daemon] Research saved: {filepath}")
        return filepath

    def trigger_brain_ingestion(self):
        """Triggers the brain ingestion pipeline to absorb new research."""
        if os.path.exists(BRAIN_INGEST_SCRIPT):
            try:
                result = subprocess.run(
                    [sys.executable, BRAIN_INGEST_SCRIPT],
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if result.returncode == 0:
                    print("[Overnight Daemon] Brain ingestion successful.")
                else:
                    print(f"[Overnight Daemon] Ingestion warning: {result.stderr[:200]}")
            except Exception as e:
                print(f"[Overnight Daemon] Ingestion error: {e}")
        else:
            print(f"[Overnight Daemon] Ingestion script not found at {BRAIN_INGEST_SCRIPT}")

    # ==================== CREDIT STATE PERSISTENCE ====================
    # This is the fix for the 2:40 AM crash bug. Previously, credit state
    # lived only in-memory and was lost when the agent context compacted.
    # Now everything persists to credit_state.json on disk.

    def _load_credit_state(self) -> dict:
        """Load persisted credit tracking state from disk."""
        if os.path.exists(CREDIT_STATE_FILE):
            try:
                with open(CREDIT_STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self._fresh_credit_state()

    def _fresh_credit_state(self) -> dict:
        """Create a fresh credit state for a new window."""
        return {
            "window_start": datetime.datetime.now().isoformat(),
            "prompts_used": 0,
            "max_prompts_per_window": 30,
            "window_hours": 5.0,       # Full credit window is 5 hours
            "check_interval_hours": 1.0, # Check every 1 hour if credits are back
            "paused_at": None,
            "resume_at": None,
            "total_pauses": 0,
            "total_checks": 0
        }

    def _save_credit_state(self, state: dict):
        """Persist credit state to disk so it survives agent restarts."""
        with open(CREDIT_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def record_prompts_used(self, count: int = 3):
        """
        Call this after each sweep completes to track credit usage.
        Persists to disk so state survives agent context loss.
        """
        state = self._load_credit_state()

        # Check if the window has expired and auto-reset
        window_start = datetime.datetime.fromisoformat(state["window_start"])
        hours_elapsed = (datetime.datetime.now() - window_start).total_seconds() / 3600
        if hours_elapsed >= state.get("window_hours", 5.0):
            # Window has refreshed — reset the counter
            state = self._fresh_credit_state()

        state["prompts_used"] += count
        self._save_credit_state(state)
        return state

    def should_wait_for_credits(self) -> dict:
        """
        The core credit-gate method. Call this BEFORE starting a new sweep.
        Returns a dict with:
          - can_continue: bool — whether to proceed with next batch
          - wait_seconds: int — how long to sleep/schedule before retrying
          - resume_at: str — human-readable time when credits refresh
          - recommendation: str — action guidance for the agent

        THE FIX: When credits are exhausted, this writes the resume_at
        timestamp to disk. The Antigravity agent reads this and sets a
        /schedule timer. Even if the agent context is lost and restored,
        it can read credit_state.json to know when to resume.
        """
        state = self._load_credit_state()

        # 1. Check consecutive errors circuit breaker (enforces safe gateway limits)
        if state.get("consecutive_errors", 0) >= 3:
            return {
                "can_continue": False,
                "prompts_used": state["prompts_used"],
                "prompts_remaining": 0,
                "wait_seconds": 999999,
                "resume_at": "MANUAL_RESET_REQUIRED",
                "recommendation": (
                    "CRITICAL: Gateway Circuit Breaker tripped due to 3 consecutive execution errors. "
                    "Overnight research cycles are physically severed upstream to prevent runaway credit burn. "
                    "Please check logs in Transcripts/ and reset consecutive_errors to 0 in credit_state.json to resume."
                )
            }

        # Check if the 5-hour window has fully elapsed — if so, credits are definitely back
        window_start = datetime.datetime.fromisoformat(state["window_start"])
        hours_since_window = (datetime.datetime.now() - window_start).total_seconds() / 3600
        if hours_since_window >= state.get("window_hours", 5.0):
            state = self._fresh_credit_state()
            self._save_credit_state(state)

        # Check if we have enough credits for another batch
        remaining = state["max_prompts_per_window"] - state["prompts_used"]
        can_continue = remaining >= 3  # Need at least 3 for a batch

        if not can_continue:
            # Credits exhausted. Don't blindly wait 5 hours.
            # Instead, check every 1 hour to see if they're back.
            # You typically hit the cap at ~3hrs, reset is at 5hrs,
            # so there's a ~2hr dead zone. Checking hourly catches the reset.
            check_interval = state.get("check_interval_hours", 1.0)
            next_check = datetime.datetime.now() + datetime.timedelta(hours=check_interval)
            state["paused_at"] = datetime.datetime.now().isoformat()
            state["resume_at"] = next_check.isoformat()
            state["total_pauses"] = state.get("total_pauses", 0) + 1
            state["total_checks"] = state.get("total_checks", 0) + 1
            self._save_credit_state(state)

            self.session_log["credit_pauses"] += 1

            wait_secs = int(check_interval * 3600)
            return {
                "can_continue": False,
                "prompts_used": state["prompts_used"],
                "prompts_remaining": 0,
                "wait_seconds": wait_secs,
                "resume_at": next_check.strftime("%H:%M"),
                "check_number": state.get("total_checks", 1),
                "recommendation": (
                    f"Credits exhausted ({state['prompts_used']} used). "
                    f"CHECK #{state.get('total_checks', 1)}: Set a 1-hour timer ({wait_secs}s). "
                    f"Next check at {next_check.strftime('%H:%M')}. "
                    f"When timer fires: open a Gemini tab, try a test prompt. "
                    f"If it works → credits are back, resume loop. "
                    f"If still blocked → call should_wait_for_credits() again for another 1hr timer. "
                    f"CRITICAL: Use schedule() tool with DurationSeconds={wait_secs} "
                    f"and Prompt='Hourly credit check. Open gemini.google.com tab, try a test prompt. "
                    f"If credits work, resume overnight research loop. If not, call should_wait_for_credits() again.'"
                )
            }

        return {
            "can_continue": True,
            "prompts_used": state["prompts_used"],
            "prompts_remaining": remaining,
            "wait_seconds": 0,
            "resume_at": "N/A",
            "recommendation": f"Continue with next batch. {remaining} prompts remaining in this window."
        }

    def calculate_credit_timing(self, prompts_used_this_window: int,
                                 max_prompts_per_window: int = 30,
                                 refresh_hours: float = 5.0) -> dict:
        """
        Legacy credit-aware scheduling calculator.
        DEPRECATED: Use should_wait_for_credits() instead — it persists state to disk.
        Kept for backward compatibility.
        """
        remaining = max_prompts_per_window - prompts_used_this_window
        can_continue = remaining > 3  # Need at least 3 for a batch

        return {
            "prompts_remaining": remaining,
            "can_continue": can_continue,
            "wait_seconds": int(refresh_hours * 3600) if not can_continue else 0,
            "next_refresh_at": (
                datetime.datetime.now() + datetime.timedelta(hours=refresh_hours)
            ).strftime("%H:%M") if not can_continue else "N/A",
            "recommendation": (
                "Continue with next batch"
                if can_continue
                else f"Pause and wait until credit refresh at ~{refresh_hours}h window"
            )
        }

    def get_queue_status(self) -> dict:
        """Returns a summary of the learning queue status."""
        total_topics = 0
        completed_topics = 0
        domain_status = {}

        for domain in self.queue.get("queue", []):
            topics = domain.get("topics", [])
            completed = domain.get("completed", [])
            total_topics += len(topics)
            completed_topics += len(completed)
            pct = (len(completed) / max(len(topics), 1)) * 100
            domain_status[domain["domain"]] = {
                "priority": domain.get("priority", 99),
                "total": len(topics),
                "completed": len(completed),
                "remaining": len(topics) - len(completed),
                "progress": f"{pct:.0f}%",
                "status": domain.get("status", "pending")
            }

        return {
            "total_topics": total_topics,
            "completed": completed_topics,
            "remaining": total_topics - completed_topics,
            "overall_progress": f"{(completed_topics / max(total_topics, 1) * 100):.1f}%",
            "domains": domain_status
        }

    def generate_morning_report(self) -> str:
        """Generates a human-readable morning report of overnight research."""
        self.session_log["session_end"] = datetime.datetime.now().isoformat()
        self._save_session_log()

        status = self.get_queue_status()

        report = f"""# 🌅 Overnight Research Report — {datetime.datetime.now().strftime("%B %d, %Y")}

## Session Summary
- **Started:** {self.session_log['session_start'][:16]}
- **Ended:** {self.session_log['session_end'][:16]}
- **Topics Researched:** {len(self.session_log['topics_researched'])}
- **Topics Failed:** {len(self.session_log['topics_failed'])}
- **Credit Pauses:** {self.session_log['credit_pauses']}
- **Cycles Completed:** {self.session_log['cycles_completed']}

## What I Learned
"""
        for item in self.session_log["topics_researched"]:
            report += f"- ✅ **[{item['domain']}]** {item['topic']}\n"

        if self.session_log["topics_failed"]:
            report += "\n## Failed Topics (Need Retry)\n"
            for item in self.session_log["topics_failed"]:
                report += f"- ❌ **[{item['domain']}]** {item['topic']}\n"

        report += f"""
## Knowledge Queue Status
- **Overall Progress:** {status['overall_progress']}
- **Topics Remaining:** {status['remaining']}

### Domain Breakdown
| Domain | Priority | Progress | Remaining |
|--------|----------|----------|-----------|
"""
        for domain, info in sorted(status["domains"].items(), key=lambda x: x[1]["priority"]):
            report += f"| {domain.replace('_', ' ').title()} | P{info['priority']} | {info['progress']} | {info['remaining']} |\n"

        report += """
## Recommendations for Today
"""
        # Find highest priority domains with remaining topics
        for domain, info in sorted(status["domains"].items(), key=lambda x: x[1]["priority"]):
            if info["remaining"] > 0 and info["priority"] <= 2:
                report += f"- 🎯 Continue researching **{domain.replace('_', ' ').title()}** ({info['remaining']} topics remaining)\n"

        report_path = os.path.join(
            PROJECT_ROOT, ".learnings", "insights",
            f"{datetime.datetime.now().strftime('%Y-%m-%d')}-morning-report.md"
        )
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[Overnight Daemon] Morning report generated: {report_path}")
        return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Keystone Overnight Chrome Research Daemon")
    parser.add_argument("--start", action="store_true", help="Start overnight research session")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without Chrome")
    parser.add_argument("--status", action="store_true", help="Show queue status")
    parser.add_argument("--report", action="store_true", help="Generate morning report")
    parser.add_argument("--next-batch", action="store_true", help="Show next 3 topics to research")
    args = parser.parse_args()

    daemon = OvernightResearchDaemon()

    if args.status:
        status = daemon.get_queue_status()
        print(json.dumps(status, indent=2))
    elif args.report:
        print(daemon.generate_morning_report())
    elif args.next_batch:
        batch = daemon.get_next_batch(3)
        for i, item in enumerate(batch, 1):
            print(f"\n--- Topic {i} ---")
            print(f"Domain: {item['domain']}")
            print(f"Topic: {item['topic']}")
            print(f"Prompt: {item['prompt'][:200]}...")
    elif args.dry_run:
        print("[Overnight Daemon] DRY RUN — Simulating research cycle...")
        batch = daemon.get_next_batch(3)
        for item in batch:
            print(f"  Would research: [{item['domain']}] {item['topic']}")
            daemon.mark_topic_completed(item["domain"], item["topic"], success=True)
            daemon.save_research_result(
                item["domain"], item["topic"],
                f"[DRY RUN] Simulated research output for: {item['topic']}"
            )
        print("\n[Overnight Daemon] Dry run complete. Generating report...")
        daemon.session_log["cycles_completed"] = 1
        print(daemon.generate_morning_report())
    elif args.start:
        print("[Overnight Daemon] Starting overnight research session...")
        print("[Overnight Daemon] NOTE: This daemon manages the queue.")
        print("[Overnight Daemon] Actual Chrome automation is handled by Antigravity agents.")
        print("[Overnight Daemon] Use /schedule in Antigravity to launch the Chrome research loop.")
        status = daemon.get_queue_status()
        print(f"\nQueue status: {status['remaining']} topics remaining across {len(status['domains'])} domains")
        batch = daemon.get_next_batch(3)
        print(f"\nNext batch ({len(batch)} topics):")
        for item in batch:
            print(f"  [{item['domain']}] {item['topic']}")
    else:
        # Default: show status
        status = daemon.get_queue_status()
        print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
