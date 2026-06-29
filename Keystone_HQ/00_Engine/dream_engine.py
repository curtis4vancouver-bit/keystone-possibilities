"""
Keystone Dream Engine v1.0
============================
Biologically-inspired memory consolidation system.
Runs overnight to score, consolidate, and decay memories
using Ebbinghaus forgetting curves.

Usage:
  python dream_engine.py --consolidate     # Full consolidation cycle
  python dream_engine.py --score           # Score all memories (dry run)
  python dream_engine.py --prune           # Remove decayed memories
  python dream_engine.py --promote         # Promote high-value working→episodic→semantic
  python dream_engine.py --report          # Generate consolidation report
  python dream_engine.py --dream           # Full dream cycle (score→consolidate→prune→promote→report)

Inspired by: Bitterbot Dream Engine, Ebbinghaus forgetting curves, Mnemosyne consolidation
"""
import os
import sys
import json
import math
import argparse
import datetime
import glob
from collections import defaultdict

try:
    from self_learning import record_insight, promote_crystalized_memories
    SELF_LEARNING_AVAILABLE = True
except ImportError:
    SELF_LEARNING_AVAILABLE = False

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
AGENT_FLEET_DIR = os.path.join(PROJECT_ROOT, "Agent_Fleet")
LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
INSIGHTS_DIR = os.path.join(LEARNINGS_DIR, "insights")
CORRECTION_JOURNAL = os.path.join(LEARNINGS_DIR, "correction_journal.json")
WORKING_MEMORY_DB = os.path.join(PROJECT_ROOT, "working_memory.db")
DREAM_LOG_DIR = os.path.join(LEARNINGS_DIR, "dream_logs")
BRAND_CONSTITUTION_DIR = os.path.join(PROJECT_ROOT, "Brand_Constitution")

# Ensure directories exist
for d in [DREAM_LOG_DIR, INSIGHTS_DIR, LEARNINGS_DIR]:
    os.makedirs(d, exist_ok=True)

# ─── Ebbinghaus Forgetting Curve ────────────────────────────────────────
# R = e^(-t/S) where R=retention, t=time since last access, S=memory strength
# Memory strength increases with each successful recall (spaced repetition)

def retention_score(hours_since_access: float, access_count: int, base_strength: float = 1.0) -> float:
    """
    Calculate memory retention using Ebbinghaus forgetting curve.
    
    Args:
        hours_since_access: Hours since this memory was last accessed
        access_count: How many times this memory has been accessed
        base_strength: Base memory strength (importance multiplier)
    
    Returns:
        Float 0.0-1.0 representing retention strength
    """
    # Memory strength increases with repetition (spaced repetition effect)
    # Each access roughly doubles the stability
    strength = base_strength * (1.0 + math.log2(max(access_count, 1)))
    
    # Ebbinghaus: R = e^(-t/S)
    retention = math.exp(-hours_since_access / max(strength * 24, 1))  # Normalize to days
    
    return min(max(retention, 0.0), 1.0)


def importance_score(memory: dict) -> float:
    """
    Score a memory's importance on a 0.0-1.0 scale based on multiple factors.
    """
    score = 0.5  # Base importance
    
    # Factor 1: Explicit priority tags
    priority = memory.get("priority", "medium").lower()
    if priority == "critical":
        score += 0.4
    elif priority == "high":
        score += 0.3
    elif priority == "medium":
        score += 0.1
    elif priority == "low":
        score -= 0.2
    
    # Factor 2: Access frequency
    access_count = memory.get("access_count", 1)
    if access_count > 10:
        score += 0.2
    elif access_count > 5:
        score += 0.1
    
    # Factor 3: Recency of creation
    created = memory.get("created_at") or memory.get("timestamp")
    if created:
        try:
            if isinstance(created, str):
                created_dt = datetime.datetime.fromisoformat(created.replace("Z", "+00:00"))
            else:
                created_dt = datetime.datetime.fromtimestamp(created)
            age_hours = (datetime.datetime.now(datetime.timezone.utc) - created_dt).total_seconds() / 3600
            if age_hours < 24:
                score += 0.15  # Very recent
            elif age_hours < 168:  # 1 week
                score += 0.05
        except (ValueError, TypeError, OSError):
            pass
    
    # Factor 4: Content richness (longer = likely more valuable)
    content = memory.get("content", "") or memory.get("message", "") or memory.get("finding", "")
    if len(content) > 500:
        score += 0.1
    elif len(content) > 200:
        score += 0.05
    
    # Factor 5: Action required flag
    if memory.get("action_required"):
        score += 0.15
    
    # Factor 6: Error/fix pairs are highly valuable
    if memory.get("error") and memory.get("fix"):
        score += 0.25
    
    return min(max(score, 0.0), 1.0)


# ─── Memory Collectors ──────────────────────────────────────────────────

def collect_correction_journal() -> list:
    """Load correction journal entries as scoreable memories."""
    if not os.path.exists(CORRECTION_JOURNAL):
        return []
    
    try:
        with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
    
    entries = data if isinstance(data, list) else data.get("entries", [])
    memories = []
    for entry in entries:
        memories.append({
            "source": "correction_journal",
            "type": "episodic",
            "content": json.dumps(entry, default=str),
            "timestamp": entry.get("timestamp") or entry.get("date"),
            "priority": "high",  # Error/fix pairs are always valuable
            "access_count": entry.get("access_count", 1),
            "error": entry.get("error", ""),
            "fix": entry.get("fix", ""),
            "raw": entry,
        })
    return memories


def collect_agent_inboxes() -> list:
    """Collect all agent inbox messages as scoreable memories."""
    memories = []
    if not os.path.exists(AGENT_FLEET_DIR):
        return memories
    
    for agent_dir in os.listdir(AGENT_FLEET_DIR):
        inbox_path = os.path.join(AGENT_FLEET_DIR, agent_dir, "INBOX.json")
        if os.path.exists(inbox_path):
            try:
                with open(inbox_path, "r", encoding="utf-8") as f:
                    inbox = json.load(f)
                for msg in inbox.get("messages", []):
                    memories.append({
                        "source": f"agent_inbox/{agent_dir}",
                        "type": "episodic",
                        "content": msg.get("message", ""),
                        "timestamp": msg.get("date"),
                        "priority": msg.get("priority", "medium"),
                        "access_count": 1,
                        "action_required": msg.get("action_required", False),
                        "raw": msg,
                    })
            except (json.JSONDecodeError, IOError):
                continue
    return memories


def collect_output_logs() -> list:
    """Collect all agent output logs as scoreable memories."""
    memories = []
    if not os.path.exists(AGENT_FLEET_DIR):
        return memories
    
    for agent_dir in os.listdir(AGENT_FLEET_DIR):
        log_path = os.path.join(AGENT_FLEET_DIR, agent_dir, "OUTPUT_LOG.jsonl")
        if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            entry = json.loads(line)
                            memories.append({
                                "source": f"output_log/{agent_dir}",
                                "type": "episodic",
                                "content": json.dumps(entry, default=str),
                                "timestamp": entry.get("timestamp"),
                                "priority": "medium",
                                "access_count": 1,
                                "raw": entry,
                            })
            except (json.JSONDecodeError, IOError):
                continue
    return memories


def collect_working_memory() -> list:
    """Collect working memory entries (ephemeral, highest decay rate)."""
    memories = []
    if not os.path.exists(WORKING_MEMORY_DB):
        return memories
    
    try:
        import sqlite3
        conn = sqlite3.connect(WORKING_MEMORY_DB)
        cursor = conn.execute("SELECT key, value, namespace, created_at, expires_at FROM working_memory")
        for row in cursor.fetchall():
            memories.append({
                "source": "working_memory",
                "type": "working",
                "content": f"{row[0]}={row[1]}",
                "timestamp": row[3],
                "priority": "low",
                "access_count": 1,
                "namespace": row[2],
                "expires_at": row[4],
                "raw": {"key": row[0], "value": row[1], "namespace": row[2]},
            })
        conn.close()
    except Exception:
        pass
    
    return memories


def collect_brand_evolution_log() -> list:
    """Collect brand evolution log entries."""
    log_path = os.path.join(BRAND_CONSTITUTION_DIR, "BRAND_EVOLUTION_LOG.jsonl")
    memories = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entry = json.loads(line)
                        memories.append({
                            "source": "brand_evolution",
                            "type": "semantic",
                            "content": entry.get("change", "") or json.dumps(entry, default=str),
                            "timestamp": entry.get("date") or entry.get("timestamp"),
                            "priority": "critical",  # Brand changes are always critical
                            "access_count": 5,  # Treat as frequently accessed
                            "raw": entry,
                        })
        except (json.JSONDecodeError, IOError):
            pass
    return memories


# ─── Dream Cycle Operations ─────────────────────────────────────────────

def score_all_memories() -> list:
    """Collect and score all memories across the entire system."""
    print("[Dream] Collecting memories from all sources...")
    
    all_memories = []
    all_memories.extend(collect_correction_journal())
    all_memories.extend(collect_agent_inboxes())
    all_memories.extend(collect_output_logs())
    all_memories.extend(collect_working_memory())
    all_memories.extend(collect_brand_evolution_log())
    
    now = datetime.datetime.now(datetime.timezone.utc)
    
    for mem in all_memories:
        # Calculate hours since last access/creation
        ts = mem.get("timestamp")
        hours_ago = 24  # Default
        if ts:
            try:
                if isinstance(ts, str):
                    dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=datetime.timezone.utc)
                else:
                    dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
                hours_ago = max((now - dt).total_seconds() / 3600, 0.1)
            except (ValueError, TypeError, OSError):
                pass
        
        mem["hours_since_access"] = hours_ago
        mem["importance"] = importance_score(mem)
        mem["retention"] = retention_score(hours_ago, mem.get("access_count", 1), mem["importance"])
        mem["composite_score"] = (mem["importance"] * 0.6) + (mem["retention"] * 0.4)
    
    # Sort by composite score (highest first)
    all_memories.sort(key=lambda m: m["composite_score"], reverse=True)
    
    print(f"[Dream] Scored {len(all_memories)} memories across {len(set(m['source'] for m in all_memories))} sources")
    return all_memories


def consolidate_memories(memories: list) -> dict:
    """
    Consolidate memories: merge similar entries, promote high-value ones,
    mark low-value ones for decay.
    """
    print("[Dream] Consolidating memories...")
    
    results = {
        "crystalized": [],    # High-value, permanently stored
        "maintained": [],     # Medium-value, kept as-is
        "decaying": [],       # Low-value, marked for future pruning
        "expired": [],        # Below threshold, ready for deletion
    }
    
    for mem in memories:
        score = mem["composite_score"]
        
        if score >= 0.75:
            results["crystalized"].append(mem)
        elif score >= 0.45:
            results["maintained"].append(mem)
        elif score >= 0.20:
            results["decaying"].append(mem)
        else:
            results["expired"].append(mem)
    
    print(f"[Dream] Results:")
    print(f"  Crystalized (permanent): {len(results['crystalized'])}")
    print(f"  Maintained (stable):     {len(results['maintained'])}")
    print(f"  Decaying (fading):       {len(results['decaying'])}")
    print(f"  Expired (prunable):      {len(results['expired'])}")
    
    return results


def prune_expired(memories: list, dry_run: bool = False) -> int:
    """
    Remove expired working memory entries and clean stale inbox messages.
    Never prunes correction journal entries or brand evolution logs.
    """
    print("[Dream] Pruning expired memories...")
    
    pruned = 0
    
    # Only prune working memory entries that have expired
    if os.path.exists(WORKING_MEMORY_DB):
        try:
            import sqlite3
            conn = sqlite3.connect(WORKING_MEMORY_DB)
            if not dry_run:
                cursor = conn.execute(
                    "DELETE FROM working_memory WHERE expires_at IS NOT NULL AND expires_at < ?",
                    (datetime.datetime.now().isoformat(),)
                )
                pruned += cursor.rowcount
                conn.commit()
            else:
                cursor = conn.execute(
                    "SELECT COUNT(*) FROM working_memory WHERE expires_at IS NOT NULL AND expires_at < ?",
                    (datetime.datetime.now().isoformat(),)
                )
                pruned += cursor.fetchone()[0]
            conn.close()
        except Exception as e:
            print(f"  [Warning] Working memory prune failed: {e}")
    
    # Clean old inbox messages (keep only last 10 per agent)
    if os.path.exists(AGENT_FLEET_DIR):
        for agent_dir in os.listdir(AGENT_FLEET_DIR):
            inbox_path = os.path.join(AGENT_FLEET_DIR, agent_dir, "INBOX.json")
            if os.path.exists(inbox_path):
                try:
                    with open(inbox_path, "r", encoding="utf-8") as f:
                        inbox = json.load(f)
                    msgs = inbox.get("messages", [])
                    if len(msgs) > 10:
                        old_count = len(msgs)
                        # Keep actionable + last 10
                        actionable = [m for m in msgs if m.get("action_required")]
                        recent = msgs[-10:]
                        combined = {json.dumps(m, sort_keys=True, default=str): m 
                                   for m in actionable + recent}
                        inbox["messages"] = list(combined.values())
                        
                        if not dry_run:
                            with open(inbox_path, "w", encoding="utf-8") as f:
                                json.dump(inbox, f, indent=2)
                        pruned += old_count - len(inbox["messages"])
                except (json.JSONDecodeError, IOError):
                    continue
    
    print(f"[Dream] {'Would prune' if dry_run else 'Pruned'} {pruned} expired entries")
    return pruned


def generate_dream_report(memories: list, consolidated: dict) -> str:
    """Generate a dream consolidation report."""
    now = datetime.datetime.now()
    report_name = f"{now.strftime('%Y-%m-%d_%H%M')}-dream-report.md"
    report_path = os.path.join(DREAM_LOG_DIR, report_name)
    
    # Source breakdown
    source_counts = defaultdict(int)
    for mem in memories:
        source_counts[mem["source"]] += 1
    
    # Top memories
    top_5 = memories[:5] if memories else []
    
    report = f"""# Dream Engine Consolidation Report
## {now.strftime('%Y-%m-%d %H:%M')}

### Summary
- **Total Memories Scored:** {len(memories)}
- **Crystalized (permanent):** {len(consolidated.get('crystalized', []))}
- **Maintained (stable):** {len(consolidated.get('maintained', []))}
- **Decaying (fading):** {len(consolidated.get('decaying', []))}
- **Expired (pruned):** {len(consolidated.get('expired', []))}

### Memory Sources
"""
    for source, count in sorted(source_counts.items()):
        report += f"- `{source}`: {count} memories\n"
    
    report += "\n### Top 5 Highest-Value Memories\n"
    for i, mem in enumerate(top_5, 1):
        content_preview = (mem.get("content", "")[:100] + "...") if len(mem.get("content", "")) > 100 else mem.get("content", "")
        report += f"""
**{i}. [{mem['source']}]** (Score: {mem['composite_score']:.2f})
- Importance: {mem['importance']:.2f} | Retention: {mem['retention']:.2f}
- Content: {content_preview}
"""
    
    report += f"\n### Health Assessment\n"
    if len(consolidated.get('expired', [])) > len(memories) * 0.3:
        report += "> [!WARNING]\n> Over 30% of memories are expired. The brain needs more active engagement.\n\n"
    elif len(consolidated.get('crystalized', [])) > len(memories) * 0.5:
        report += "> [!TIP]\n> Over 50% of memories are crystalized. The brain is healthy and well-maintained.\n\n"
    else:
        report += "> [!NOTE]\n> Memory health is normal. Regular consolidation cycles will maintain quality.\n\n"
    
    report += f"---\n*Generated by Dream Engine v1.0 at {now.isoformat()}*\n"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"[Dream] Report saved to: {report_path}")
    return report_path


# ─── Full Dream Cycle ────────────────────────────────────────────────────

def full_dream_cycle():
    """Execute the complete dream consolidation cycle."""
    print("\n" + "=" * 65)
    print("  KEYSTONE DREAM ENGINE v1.1 — Consolidation Cycle")
    print("  " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 65)
    
    print("\n[Phase 1/5] Scoring all memories...")
    memories = score_all_memories()
    
    print("\n[Phase 2/5] Consolidating...")
    consolidated = consolidate_memories(memories)
    
    print("\n[Phase 3/5] Pruning expired entries...")
    pruned = prune_expired(memories)
    
    print("\n[Phase 3.5/5] Compacting deep conversation histories in state.db...")
    try:
        from core.brain_init import init_brain_transplant, state_store, conversation_compressor
        init_brain_transplant()
        if state_store and conversation_compressor:
            sessions = state_store.get_recent_sessions(limit=50)
            compacted_count = 0
            for sess in sessions:
                sess_id = sess["id"]
                if conversation_compressor.evaluate_and_compact_session(sess_id, threshold_chars=150000):
                    compacted_count += 1
            print(f"  [Compaction] Checked {len(sessions)} sessions. Compacted {compacted_count} sessions.")
    except Exception as comp_err:
        print(f"  [Skip] Context compaction failed: {comp_err}")
    
    print("\n[Phase 4/5] Promoting crystalized memories to vector DB...")
    promoted = 0
    if SELF_LEARNING_AVAILABLE:
        # Promote crystalized memories that aren't yet in Qdrant
        promoted = promote_crystalized_memories()
        
        # Also vectorize the top 5 highest-value non-crystal memories
        # that have content worth preserving
        for mem in consolidated.get("maintained", [])[:5]:
            content = mem.get("content", "")
            if len(content) > 100 and mem.get("composite_score", 0) > 0.6:
                try:
                    source_label = mem.get("source", "dream_promotion")
                    record_insight(
                        content=content[:2000],
                        namespace="keystone_learnings",
                        eeat_type="insight",
                        topic=source_label,
                        source=f"dream_promotion:{source_label}",
                        priority="medium" if mem["composite_score"] < 0.7 else "high",
                    )
                    promoted += 1
                except Exception:
                    pass
    else:
        print("  [Skip] self_learning module not available")
    
    print("\n[Phase 4.5/5] Running GEPA Prompt Evolution...")
    try:
        refiner_gepa_path = os.path.join(PROJECT_ROOT, "prompt_refiner_gepa.py")
        if os.path.exists(refiner_gepa_path):
            import subprocess
            result = subprocess.run(
                [sys.executable, refiner_gepa_path],
                capture_output=True, text=True, timeout=120, cwd=PROJECT_ROOT
            )
            if result.returncode == 0:
                print("  [GEPA] Prompt evolution completed successfully.")
            else:
                print(f"  [GEPA] Warning: {result.stderr.strip()[:200]}")
    except Exception as gepa_err:
        print(f"  [Skip] GEPA prompt evolution failed: {gepa_err}")
        
    print("\n[Phase 5/5] Generating dream report...")
    report_path = generate_dream_report(memories, consolidated)
    
    print("\n" + "=" * 65)
    print(f"  DREAM CYCLE COMPLETE")
    print(f"  Memories: {len(memories)} scored | {pruned} pruned | {promoted} promoted to Qdrant")
    print(f"  Crystals: {len(consolidated['crystalized'])} | Decaying: {len(consolidated['decaying'])}")
    print(f"  Report: {report_path}")
    print("=" * 65)


# ─── CLI ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Keystone Dream Engine v1.0")
    parser.add_argument("--dream", action="store_true", help="Full dream cycle")
    parser.add_argument("--score", action="store_true", help="Score all memories (dry run)")
    parser.add_argument("--consolidate", action="store_true", help="Consolidate memories")
    parser.add_argument("--prune", action="store_true", help="Prune expired memories")
    parser.add_argument("--report", action="store_true", help="Generate report only")
    args = parser.parse_args()
    
    if args.dream:
        full_dream_cycle()
    elif args.score:
        memories = score_all_memories()
        for mem in memories[:10]:
            print(f"  [{mem['composite_score']:.2f}] [{mem['source']:30s}] {mem.get('content', '')[:80]}")
    elif args.consolidate:
        memories = score_all_memories()
        consolidate_memories(memories)
    elif args.prune:
        memories = score_all_memories()
        prune_expired(memories)
    elif args.report:
        memories = score_all_memories()
        consolidated = consolidate_memories(memories)
        generate_dream_report(memories, consolidated)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
