"""
Dream Engine
=============

Overnight memory consolidation for the Keystone Master Brain.
Generates Dream Reports (comprehensive overnight summaries) and
Daily Digests (quick status snapshots for Spark/NotebookLM).

Commands:
    python dream_engine.py --dream    Generate Dream Report
    python dream_engine.py --digest   Generate Daily Digest
"""

import argparse
from datetime import datetime, date
from pathlib import Path

from config import (
    CORRECTION_JOURNAL, INSIGHTS_DIR, DREAM_LOGS, IMPROVEMENT_QUEUE,
    RESEARCH_ARCHIVES, ERRORS_DIR, MASTER_BRAIN,
    load_json, logger, ensure_directories,
)


# ---------------------------------------------------------─
# UTILITIES
# ---------------------------------------------------------─
def _recent_files(directory: Path, days: int, pattern: str = "*.md") -> list[Path]:
    """Return files in *directory* modified within the last *days* days."""
    if not directory.exists():
        return []
    cutoff = datetime.now().timestamp() - (days * 86400)
    return [f for f in directory.glob(pattern) if f.stat().st_mtime >= cutoff]


def _safe_read(path: Path, max_chars: int = 300) -> str:
    """Read up to *max_chars* from a file, returning '' on error."""
    try:
        return path.read_text(encoding="utf-8")[:max_chars]
    except (OSError, UnicodeDecodeError):
        return f"(could not read {path.name})"


# ---------------------------------------------------------─
# DREAM REPORT
# ---------------------------------------------------------─
def generate_dream_report() -> Path:
    """
    Generate a comprehensive overnight Dream Report.

    Sections:
      1. Correction Journal summary (last 5 entries)
      2. Today's insights
      3. Improvement queue (pending items)
      4. Error log summary
      5. Content production activity
    """
    logger.info("=== GENERATING DREAM REPORT ===")
    ensure_directories()

    today  = date.today().isoformat()
    now_ts = datetime.now().strftime("%H%M")

    lines = [f"# Dream Report — {today}\n"]

    # 1. Correction Journal
    journal = load_json(CORRECTION_JOURNAL)
    lines.append(f"## Correction Journal: {len(journal)} total entries\n")
    for entry in journal[-5:]:
        err  = str(entry.get("error", ""))[:120]
        fix  = str(entry.get("fix", ""))[:120]
        prev = str(entry.get("prevention", ""))[:120]
        lines.append(f"- **Error:** {err}")
        lines.append(f"  **Fix:** {fix}")
        if prev:
            lines.append(f"  **Prevention:** {prev}")
        lines.append("")

    # 2. Insights
    recent_insights = _recent_files(INSIGHTS_DIR, 1)
    lines.append(f"## Today's Insights: {len(recent_insights)} files\n")
    for f in recent_insights[:10]:
        lines.append(f"### {f.name}\n{_safe_read(f)}…\n")

    # 3. Improvement Queue
    queue   = load_json(IMPROVEMENT_QUEUE)
    pending = [q for q in queue if isinstance(q, dict) and q.get("status") == "pending"]
    lines.append(f"## Improvement Queue: {len(pending)} pending\n")
    for q in pending[:5]:
        prio    = q.get("priority", "low")
        friction = str(q.get("friction", q.get("description", "")))[:120]
        lines.append(f"- [{prio}] {friction}")

    # 4. Error logs
    recent_errors = _recent_files(ERRORS_DIR, 1, "*.json")
    lines.append(f"\n## Error Logs: {len(recent_errors)} in the last 24h\n")
    for ef in recent_errors[:5]:
        lines.append(f"- {ef.name}")

    # 5. Content Production
    if RESEARCH_ARCHIVES.exists():
        recent_research = _recent_files(RESEARCH_ARCHIVES, 7)
        lines.append(f"\n## Research Activity: {len(recent_research)} files (last 7d)\n")

    # 6. Memory Decay
    try:
        import sys
        brain_path = Path(__file__).parent.parent.parent / "00_Engine" / "Qdrant_Brain"
        if str(brain_path) not in sys.path:
            sys.path.append(str(brain_path))
        from keystone_brain_v2_mcp import memory_manager
        if memory_manager:
            deleted, promoted = memory_manager.decay_episodic()
            lines.append(f"\n## Memory Decay\n- Purged {deleted} old episodic memories from the vector brain.\n")
            logger.info(f"Memory decay complete: purged {deleted} memories.")
    except Exception as e:
        logger.error(f"Failed to run memory decay during dream cycle: {e}")
        lines.append(f"\n## Memory Decay\n- Failed to run decay: {e}\n")

    # Write
    report_path = DREAM_LOGS / f"{today}_{now_ts}-dream-report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Dream report saved: %s", report_path.name)
    return report_path


# ---------------------------------------------------------─
# DAILY DIGEST
# ---------------------------------------------------------─
def generate_daily_digest() -> Path:
    """
    Generate a concise daily status digest with real data.

    This digest is synced to Google Drive so that Spark and
    NotebookLM can read the latest system status.
    """
    logger.info("=== GENERATING DAILY DIGEST ===")
    ensure_directories()

    today = date.today().isoformat()
    digest_path = INSIGHTS_DIR / f"{today}-daily-digest.md"

    journal  = load_json(CORRECTION_JOURNAL)
    queue    = load_json(IMPROVEMENT_QUEUE)
    pending  = [q for q in queue if isinstance(q, dict) and q.get("status") == "pending"]
    research = _recent_files(RESEARCH_ARCHIVES, 7) if RESEARCH_ARCHIVES.exists() else []
    dreams   = _recent_files(DREAM_LOGS, 7)
    errors   = _recent_files(ERRORS_DIR, 7, "*.json")

    # Brain size
    scraped = MASTER_BRAIN / "SCRAPED_GOOGLE_DOCS.txt"
    scraped_mb = round(scraped.stat().st_size / (1024*1024), 2) if scraped.exists() else 0

    lines = [
        f"# Daily Digest: {today}\n",
        "## System Status",
        f"- **Correction Journal:** {len(journal)} total entries",
        f"- **Improvement Queue:** {len(pending)} pending proposals",
        f"- **Research files (last 7d):** {len(research)}",
        f"- **Dream reports (last 7d):** {len(dreams)}",
        f"- **Error logs (last 7d):** {len(errors)}",
        f"- **Scraped docs size:** {scraped_mb} MB\n",
    ]

    if journal:
        latest = journal[-1]
        lines.append("## Latest Correction")
        lines.append(f"- **Error:** {str(latest.get('error', ''))[:250]}")
        lines.append(f"- **Fix:** {str(latest.get('fix', ''))[:250]}")
        prev = latest.get("prevention", "")
        if prev:
            lines.append(f"- **Prevention:** {str(prev)[:250]}")
        lines.append("")

    digest_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Digest saved: %s", digest_path.name)
    return digest_path


# ---------------------------------------------------------─
# MEMORY CONSOLIDATION
# ---------------------------------------------------------─
def consolidate_memory():
    logger.info("=== RUNNING MEMORY CONSOLIDATION ===")
    try:
        import sys
        import re
        brain_path = Path(__file__).parent.parent.parent / "00_Engine" / "Qdrant_Brain"
        if str(brain_path) not in sys.path:
            sys.path.append(str(brain_path))
        from keystone_brain_v2_mcp import memory_manager
        import episodic_memory
        if not memory_manager:
            logger.error("MemoryManager not available. Skipping consolidation.")
            return 0, 0

        from config import MEMORY_DECAY_HALF_LIFE_DAYS, MEMORY_PROMOTION_THRESHOLD, MEMORY_PRUNE_THRESHOLD, MEMORY_PRUNE_MIN_AGE_DAYS
        import math

        client = memory_manager.client
        collection_name = memory_manager.collection_name
        from qdrant_client import models
        
        offset = None
        now = datetime.utcnow()
        promoted = 0
        pruned = 0
        
        while True:
            records, next_offset = client.scroll(
                collection_name=collection_name,
                scroll_filter=models.Filter(
                    must=[models.FieldCondition(key="memory_layer", match=models.MatchValue(value="episodic"))]
                ),
                limit=100,
                with_payload=True,
                with_vectors=True,
                offset=offset
            )
            
            for rec in records:
                payload = rec.payload
                created_at = payload.get("created_at")
                if not created_at: continue
                
                try:
                    created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00")).replace(tzinfo=None)
                    age_days = (now - created_dt).total_seconds() / (24 * 3600)
                    
                    doc_text = payload.get("document", payload.get("text", ""))
                    tenant_id = payload.get("tenant_id", "general")
                    
                    # 1. Frequency calculation via SQLite FTS5 search
                    frequency_weight = 1.0
                    if doc_text:
                        words = re.findall(r'\b[a-zA-Z]{4,}\b', doc_text)
                        if words:
                            query_terms = " OR ".join(words[:5])
                            try:
                                conn = episodic_memory.get_connection()
                                cur = conn.cursor()
                                cur.execute("SELECT COUNT(*) FROM episodes_fts WHERE episodes_fts MATCH ?", (query_terms,))
                                matches = cur.fetchone()[0]
                                frequency_weight = 1.0 + math.log1p(matches)
                                conn.close()
                            except Exception as fe:
                                logger.warning(f"Failed to query FTS matches: {fe}")
                                
                    # 2. Diversity calculation via Qdrant search
                    diversity_weight = 1.0
                    try:
                        vector_val = rec.vector.get(memory_manager.vector_name) if isinstance(rec.vector, dict) else rec.vector
                        if vector_val is not None:
                            # Search for similar points in same namespace
                            neighbors = client.search(
                                collection_name=collection_name,
                                query_vector=(memory_manager.vector_name, vector_val),
                                query_filter=models.Filter(
                                    must=[
                                        models.FieldCondition(key="tenant_id", match=models.MatchValue(value=tenant_id)),
                                        models.FieldCondition(key="memory_layer", match=models.MatchValue(value="episodic"))
                                    ]
                                ),
                                limit=10,
                                score_threshold=0.85
                            )
                            diversity_weight = 1.0 / max(len(neighbors), 1)
                    except Exception as de:
                        logger.warning(f"Failed to calculate diversity weight: {de}")
                        
                    recency_weight = math.exp(-age_days / MEMORY_DECAY_HALF_LIFE_DAYS)
                    
                    score = frequency_weight * recency_weight * diversity_weight
                    
                    if score > MEMORY_PROMOTION_THRESHOLD:
                        memory_manager.promote_memory(rec.id, "semantic")
                        promoted += 1
                        logger.info(f"Promoted episodic point {rec.id} to semantic (Score: {score:.3f}, F: {frequency_weight:.2f}, R: {recency_weight:.2f}, D: {diversity_weight:.2f})")
                    elif score < MEMORY_PRUNE_THRESHOLD and age_days > MEMORY_PRUNE_MIN_AGE_DAYS:
                        client.delete(collection_name=collection_name, points_selector=[rec.id])
                        pruned += 1
                        logger.info(f"Pruned episodic point {rec.id} (Score: {score:.3f}, F: {frequency_weight:.2f}, R: {recency_weight:.2f}, D: {diversity_weight:.2f})")
                except Exception as ex:
                    logger.error(f"Error processing record {rec.id}: {ex}")
                    
            if next_offset is None:
                break
            offset = next_offset
            
        logger.info(f"Consolidation complete. Promoted: {promoted}, Pruned: {pruned}")
        return promoted, pruned
    except Exception as e:
        logger.error(f"Consolidation failed: {e}")
        return 0, 0

def memory_health_check():
    logger.info("=== MEMORY HEALTH CHECK ===")
    try:
        import sys
        brain_path = Path(__file__).parent.parent.parent / "00_Engine" / "Qdrant_Brain"
        if str(brain_path) not in sys.path:
            sys.path.append(str(brain_path))
        from keystone_brain_v2_mcp import memory_manager
        if not memory_manager:
            logger.error("MemoryManager not available.")
            return

        client = memory_manager.client
        collection = client.get_collection(memory_manager.collection_name)
        logger.info(f"Total Vectors in '{memory_manager.collection_name}': {collection.points_count}")
        
        from qdrant_client import models
        for layer in ["working", "episodic", "semantic", "procedural"]:
            count = client.count(
                collection_name=memory_manager.collection_name,
                count_filter=models.Filter(
                    must=[models.FieldCondition(key="memory_layer", match=models.MatchValue(value=layer))]
                )
            ).count
            logger.info(f"Layer '{layer}': {count} vectors")
    except Exception as e:
        logger.error(f"Health check failed: {e}")

# ---------------------------------------------------------─
# CLI
# ---------------------------------------------------------─
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keystone Dream Engine")
    parser.add_argument("--dream",  action="store_true", help="Generate Dream Report")
    parser.add_argument("--digest", action="store_true", help="Generate Daily Digest")
    parser.add_argument("--consolidate", action="store_true", help="Run memory consolidation")
    parser.add_argument("--health", action="store_true", help="Run memory health check")
    args = parser.parse_args()

    if args.consolidate:
        consolidate_memory()
    elif args.health:
        memory_health_check()
    elif args.dream:
        consolidate_memory()
        generate_dream_report()
    elif args.digest:
        generate_daily_digest()
    else:
        parser.print_help()
