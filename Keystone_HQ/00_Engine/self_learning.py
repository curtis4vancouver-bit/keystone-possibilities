"""
Keystone Self-Learning Engine v1.0
===================================
Closes the biggest gap in the brain: it only learned from FAILURES.

This module captures SUCCESSES — things that worked, discoveries that were
made, techniques that proved effective — and vectorizes them into the Qdrant
brain for future retrieval.

Three learning modes:
  1. record_insight()   — Capture an ad-hoc discovery or learning
  2. record_success()   — Capture a successful operation (tool call, upload, etc.)
  3. promote_memories() — Promote high-value dream engine crystals into Qdrant

CLI Usage:
  python self_learning.py --record "Bill 44 requires 2 suites per lot in RS zones" --namespace possibilities
  python self_learning.py --promote         # Promote crystalized memories to vector DB
  python self_learning.py --gaps            # Find knowledge gaps (empty namespaces)
  python self_learning.py --stats           # Show learning statistics
"""
import os
import sys
import re
import json
import datetime
import argparse
from typing import Optional, Dict, Any

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
INSIGHTS_DIR = os.path.join(LEARNINGS_DIR, "insights")
LEARNING_LOG = os.path.join(LEARNINGS_DIR, "learning_log.jsonl")
CORRECTION_JOURNAL = os.path.join(LEARNINGS_DIR, "correction_journal.json")
DREAM_LOG_DIR = os.path.join(LEARNINGS_DIR, "dream_logs")

# Ensure directories exist
for d in [LEARNINGS_DIR, INSIGHTS_DIR, DREAM_LOG_DIR]:
    os.makedirs(d, exist_ok=True)

# ─── Qdrant Client ──────────────────────────────────────────────────────
try:
    from qdrant_client import QdrantClient, models as qdrant_models
    _client = QdrantClient(url="http://localhost:6333")
    _client.set_model("BAAI/bge-small-en-v1.5")
    QDRANT_AVAILABLE = True
except Exception:
    _client = None
    QDRANT_AVAILABLE = False

# All valid Qdrant collections (these are the real per-namespace collections)
KNOWN_COLLECTIONS = [
    "general", "master", "possibilities", "protocol", "music",
    "webmaster", "self_healing", "research_scout", "legal_counsel",
    "tax_strategist", "site_superintendent", "keystone_learnings",
    "keystone_website", "local_seo", "recomposition_brand_push",
    "possibilities_leads", "operational_playbooks",
]

# EEAT tag taxonomy for categorizing learnings
EEAT_TAGS = {
    "discovery": "Original Research",    # New finding not previously known
    "technique": "Expert Opinion",       # A method that proved effective
    "success": "Case Study",             # Successful operation worth repeating
    "insight": "Analysis",               # Pattern or trend identified
    "correction": "Case Study",          # Error→fix pair (from correction journal)
    "external": "Literature Review",     # Knowledge from external research
}


# ─── Learning Record ────────────────────────────────────────────────────

def record_insight(
    content: str,
    namespace: str = "keystone_learnings",
    eeat_type: str = "discovery",
    topic: str = "",
    source: str = "agent",
    priority: str = "medium",
    metadata: Optional[Dict] = None,
) -> Optional[str]:
    """
    Record a new learning or insight into the brain.

    This is the primary self-learning function. Call it whenever:
    - An agent discovers something new
    - A technique proves effective
    - External research reveals useful information
    - A successful pattern is worth remembering

    Args:
        content: The learning content (what was discovered/learned)
        namespace: Which brain namespace to store in
        eeat_type: One of: discovery, technique, success, insight, correction, external
        topic: Topic label (e.g., "Bill 44", "tirzepatide", "SEO")
        source: Where this learning came from
        priority: critical, high, medium, low
        metadata: Additional metadata to store

    Returns:
        The learning ID, or None if storage failed
    """
    now = datetime.datetime.now()
    learning_id = f"LEARN-{now.strftime('%Y%m%d-%H%M%S')}"

    eeat_tag = EEAT_TAGS.get(eeat_type, "Analysis")

    entry = {
        "id": learning_id,
        "content": content,
        "namespace": namespace,
        "eeat_type": eeat_type,
        "EEAT_tag": eeat_tag,
        "topic": topic,
        "source": source,
        "priority": priority,
        "timestamp": now.isoformat(),
        "metadata": metadata or {},
    }

    # 1. Append to learning log (persistent, never pruned)
    try:
        with open(LEARNING_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except IOError as e:
        print(f"[Self-Learning] ⚠️ Failed to write learning log: {e}")

    # 2. Vectorize into Qdrant
    if QDRANT_AVAILABLE and _client:
        try:
            collection = namespace if namespace in KNOWN_COLLECTIONS else "keystone_learnings"

            # Ensure collection exists
            collections = [c.name for c in _client.get_collections().collections]
            if collection not in collections:
                _client.create_collection(
                    collection_name=collection,
                    vectors_config=_client.get_fastembed_vector_params(),
                )
                print(f"[Self-Learning] Created new collection: {collection}")

            # Build rich document for embedding
            doc_text = f"Topic: {topic}\n{content}\nSource: {source}\nType: {eeat_type}"

            # Payload with full metadata
            payload = {
                "id": learning_id,
                "namespace": namespace,
                "EEAT_tag": eeat_tag,
                "topic": topic,
                "source": source,
                "priority": priority,
                "eeat_type": eeat_type,
                "timestamp": now.isoformat(),
                "type": "learning",
            }
            if metadata:
                payload.update(metadata)

            _client.add(
                collection_name=collection,
                documents=[doc_text],
                metadata=[payload],
            )
            print(f"[Self-Learning] ✅ Vectorized into '{collection}': {learning_id}")
            print(f"  Topic: {topic} | EEAT: {eeat_tag} | Priority: {priority}")

        except Exception as e:
            print(f"[Self-Learning] ⚠️ Qdrant vectorization failed: {e}")
    else:
        print(f"[Self-Learning] ⚠️ Qdrant unavailable — saved to log only")

    return learning_id


def record_success(
    operation: str,
    result: str,
    namespace: str = "keystone_learnings",
    topic: str = "",
    metadata: Optional[Dict] = None,
) -> Optional[str]:
    """
    Record a successful operation as a learning.

    Call this after:
    - A video upload succeeds (what settings worked)
    - A search query returns great results (what query worked)
    - A code fix compiles and passes (what approach solved it)
    - A content piece gets high engagement (what format/style worked)

    Args:
        operation: What was done (e.g., "YouTube upload", "hybrid search")
        result: What happened (e.g., "Upload succeeded with privacy=public")
        namespace: Brain namespace
        topic: Topic label
        metadata: Additional details
    """
    content = f"Successful Operation: {operation}\nResult: {result}"
    return record_insight(
        content=content,
        namespace=namespace,
        eeat_type="success",
        topic=topic or operation,
        source=f"success_record:{operation}",
        priority="medium",
        metadata=metadata,
    )


# ─── Dream Engine Integration ───────────────────────────────────────────

def promote_crystalized_memories() -> int:
    """
    Scan dream engine reports for crystalized (high-value) memories
    and promote them into the Qdrant vector DB.

    This closes the gap where the dream engine scores memories but
    never actually vectorizes the valuable ones.
    """
    if not QDRANT_AVAILABLE:
        print("[Self-Learning] ⚠️ Qdrant unavailable — cannot promote memories")
        return 0

    promoted_count = 0

    # 1. Promote high-value correction journal entries
    print("[Self-Learning] Scanning correction journal for promotable entries...")
    if os.path.exists(CORRECTION_JOURNAL):
        try:
            with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
                journal = json.load(f)

            entries = journal if isinstance(journal, list) else journal.get("entries", [])
            for entry in entries:
                # Only promote successful fixes
                if not entry.get("success", False):
                    continue

                # Check if already vectorized (has a learning_id marker)
                if entry.get("_promoted_to_qdrant"):
                    continue

                content = (
                    f"Error: {entry.get('error_type', 'Unknown')}\n"
                    f"Context: {entry.get('original_context', '')}\n"
                    f"Fix: {entry.get('fix_description', '')}"
                )

                record_insight(
                    content=content,
                    namespace="self_healing",
                    eeat_type="correction",
                    topic=entry.get("error_type", "error_fix"),
                    source="correction_journal_promotion",
                    priority="high",
                    metadata={
                        "fingerprint": entry.get("error_fingerprint", ""),
                        "retry_count": entry.get("retry_count", 1),
                    },
                )
                entry["_promoted_to_qdrant"] = True
                promoted_count += 1

            # Save updated journal with promotion markers
            if promoted_count > 0:
                journal_data = journal if isinstance(journal, list) else journal
                if isinstance(journal_data, dict):
                    journal_data["entries"] = entries
                with open(CORRECTION_JOURNAL, "w", encoding="utf-8") as f:
                    json.dump(journal_data, f, indent=2, ensure_ascii=False)

        except (json.JSONDecodeError, IOError) as e:
            print(f"[Self-Learning] ⚠️ Failed to read correction journal: {e}")

    # 2. Promote insights from daily digests
    print("[Self-Learning] Scanning insights directory for unvectorized content...")
    if os.path.exists(INSIGHTS_DIR):
        for fname in os.listdir(INSIGHTS_DIR):
            if not fname.endswith(".md"):
                continue

            fpath = os.path.join(INSIGHTS_DIR, fname)
            marker_path = fpath + ".promoted"

            # Skip already-promoted files
            if os.path.exists(marker_path):
                continue

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()

                if len(content) < 50:
                    continue  # Skip trivial files

                record_insight(
                    content=content[:2000],  # Cap at 2000 chars for embedding
                    namespace="keystone_learnings",
                    eeat_type="insight",
                    topic=fname.replace(".md", "").replace("-", " "),
                    source=f"insight_promotion:{fname}",
                    priority="medium",
                )

                # Mark as promoted
                with open(marker_path, "w") as f:
                    f.write(datetime.datetime.now().isoformat())

                promoted_count += 1
            except IOError:
                continue

    print(f"[Self-Learning] Promoted {promoted_count} memories to Qdrant")
    return promoted_count


# ─── Knowledge Gap Analysis ─────────────────────────────────────────────

def analyze_knowledge_gaps() -> Dict[str, Any]:
    """
    Identify knowledge gaps — brain namespaces with few or no vectors.
    This helps prioritize what the research scout should investigate next.
    """
    if not QDRANT_AVAILABLE or not _client:
        print("[Self-Learning] ⚠️ Qdrant unavailable")
        return {}

    print("\n[Self-Learning] Analyzing knowledge gaps across all namespaces...")

    gaps = {
        "empty": [],         # 0 vectors
        "sparse": [],        # <10 vectors
        "adequate": [],      # 10-100 vectors
        "rich": [],          # >100 vectors
    }

    try:
        collections = _client.get_collections().collections
        for collection in collections:
            name = collection.name
            try:
                info = _client.get_collection(name)
                count = info.points_count
            except Exception:
                count = 0

            bucket = {
                "name": name,
                "vectors": count,
            }

            if count == 0:
                gaps["empty"].append(bucket)
            elif count < 10:
                gaps["sparse"].append(bucket)
            elif count <= 100:
                gaps["adequate"].append(bucket)
            else:
                gaps["rich"].append(bucket)

    except Exception as e:
        print(f"[Self-Learning] ⚠️ Failed to analyze gaps: {e}")
        return gaps

    # Display
    print(f"\n{'='*55}")
    print(f"  KNOWLEDGE GAP ANALYSIS")
    print(f"{'='*55}")

    print(f"\n  🔴 EMPTY (need content):")
    for g in gaps["empty"]:
        print(f"      {g['name']}: {g['vectors']} vectors")

    print(f"\n  🟡 SPARSE (<10 vectors):")
    for g in gaps["sparse"]:
        print(f"      {g['name']}: {g['vectors']} vectors")

    print(f"\n  🟢 ADEQUATE (10-100):")
    for g in gaps["adequate"]:
        print(f"      {g['name']}: {g['vectors']} vectors")

    print(f"\n  🏆 RICH (>100):")
    for g in gaps["rich"]:
        print(f"      {g['name']}: {g['vectors']} vectors")

    # Recommendations
    print(f"\n  📋 RECOMMENDATIONS:")
    if gaps["empty"]:
        names = ", ".join(g["name"] for g in gaps["empty"])
        print(f"      → Priority: Populate empty namespaces: {names}")
    if gaps["sparse"]:
        names = ", ".join(g["name"] for g in gaps["sparse"])
        print(f"      → Enrich sparse namespaces: {names}")

    return gaps


# ─── Learning Statistics ─────────────────────────────────────────────────

def learning_stats() -> Dict[str, Any]:
    """Show learning pipeline statistics."""
    stats = {
        "total_learnings": 0,
        "by_type": {},
        "by_namespace": {},
        "by_source": {},
        "recent_24h": 0,
        "recent_7d": 0,
    }

    if not os.path.exists(LEARNING_LOG):
        print("[Self-Learning] No learning log found — brain has recorded 0 learnings")
        return stats

    now = datetime.datetime.now(datetime.timezone.utc)

    try:
        with open(LEARNING_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                stats["total_learnings"] += 1

                # Count by type
                etype = entry.get("eeat_type", "unknown")
                stats["by_type"][etype] = stats["by_type"].get(etype, 0) + 1

                # Count by namespace
                ns = entry.get("namespace", "unknown")
                stats["by_namespace"][ns] = stats["by_namespace"].get(ns, 0) + 1

                # Count by source
                src = entry.get("source", "unknown").split(":")[0]
                stats["by_source"][src] = stats["by_source"].get(src, 0) + 1

                # Recency
                ts = entry.get("timestamp")
                if ts:
                    try:
                        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=datetime.timezone.utc)
                        hours_ago = (now - dt).total_seconds() / 3600
                        if hours_ago < 24:
                            stats["recent_24h"] += 1
                        if hours_ago < 168:
                            stats["recent_7d"] += 1
                    except (ValueError, TypeError):
                        pass

    except IOError:
        pass

    # Display
    print(f"\n{'='*55}")
    print(f"  SELF-LEARNING STATISTICS")
    print(f"{'='*55}")
    print(f"\n  Total Learnings: {stats['total_learnings']}")
    print(f"  Last 24 Hours:   {stats['recent_24h']}")
    print(f"  Last 7 Days:     {stats['recent_7d']}")

    if stats["by_type"]:
        print(f"\n  By Type:")
        for t, c in sorted(stats["by_type"].items(), key=lambda x: -x[1]):
            bar = "█" * min(c, 30)
            print(f"      {t:20s} {c:3d}  {bar}")

    if stats["by_namespace"]:
        print(f"\n  By Namespace:")
        for ns, c in sorted(stats["by_namespace"].items(), key=lambda x: -x[1]):
            print(f"      {ns:30s} {c:3d}")

    return stats


def crystallize_skill_from_transcript(conversation_id: str) -> bool:
    """
    Parses the conversation transcript JSONL file, extracts successful tool execution sequences,
    compiles a structured markdown skill, and saves it in the dynamic_skills/ folder.
    Also vectorizes the skill into Qdrant.
    """
    # 1. Locate transcript
    brain_dir = os.environ.get("ANTIGRAVITY_BRAIN_DIR", "C:/Users/Curtis/.gemini/antigravity/brain")
    convo_dir = os.path.join(brain_dir, conversation_id)
    transcript_path = os.path.join(convo_dir, ".system_generated", "logs", "transcript.jsonl")

    if not os.path.exists(transcript_path):
        print(f"[Self-Learning] ⚠️ Transcript not found at: {transcript_path}")
        # Try local alternative
        transcript_path = os.path.join(PROJECT_ROOT, "Transcripts", f"{conversation_id}.jsonl")
        if not os.path.exists(transcript_path):
            return False

    print(f"[Self-Learning] Parsing transcript: {transcript_path}...")
    
    user_request = ""
    tool_calls = []
    success = False

    try:
        with open(transcript_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    step = json.loads(line)
                except json.JSONDecodeError:
                    continue

                step_type = step.get("type")
                step_status = step.get("status")

                if step_type == "USER_INPUT" and not user_request:
                    user_request = step.get("content", "")

                # Check for tool calls
                if "tool_calls" in step:
                    for tc in step["tool_calls"]:
                        name = tc.get("name")
                        args = tc.get("args", {})
                        tool_calls.append({
                            "name": name,
                            "args": args,
                            "status": step_status
                        })

                # If we see a final step indicating success, or general successful termination
                if step_status == "DONE" or step_status == "SUCCESS":
                    success = True

    except Exception as e:
        print(f"[Self-Learning] ⚠️ Failed to parse transcript: {e}")
        return False

    if not user_request:
        user_request = "Unknown request"

    # Clean up request for description and filename
    # e.g., "crystallize skill crystallization, install crawler..." -> "skill_crystallization_and_crawler"
    cleaned_title = re.sub(r'[^a-zA-Z0-9\s_]', '', user_request.lower())
    title_words = cleaned_title.split()
    short_title = "_".join(title_words[:5]) if title_words else f"crystallized_{conversation_id[:8]}"
    
    skill_name = f"crystallized_{short_title}"
    skill_filename = f"{skill_name}.md"
    skill_path = os.path.join(PROJECT_ROOT, "dynamic_skills", skill_filename)

    # Format workflow
    workflow_steps = []
    commands = []
    files_modified = []

    for tc in tool_calls:
        name = tc["name"]
        args = tc["args"]
        if name == "run_command" or name == "execute_command":
            cmd = args.get("CommandLine", args.get("command", ""))
            if cmd and cmd not in commands:
                commands.append(cmd)
        elif name in ["replace_file_content", "multi_replace_file_content", "write_to_file"]:
            fpath = args.get("TargetFile", args.get("filepath", ""))
            if fpath:
                basename = os.path.basename(fpath)
                if basename not in files_modified:
                    files_modified.append(basename)

    # Compile Markdown content
    markdown_content = [
        "---",
        f"name: {skill_name}",
        f"description: \"Crystallized workflow for: {user_request[:100]}...\"",
        "---",
        "",
        f"# Crystallized Skill: {short_title.replace('_', ' ').title()}",
        "",
        "## Summary",
        f"- **Conversation ID:** {conversation_id}",
        f"- **Original User Request:** \"{user_request}\"",
        f"- **Status:** {'Success' if success else 'Completed'}",
        "",
        "## Files Modified",
    ]
    for fm in files_modified:
        markdown_content.append(f"- `{fm}`")

    if commands:
        markdown_content.extend([
            "",
            "## Commands Executed",
            "```bash",
        ])
        for cmd in commands:
            markdown_content.append(cmd)
        markdown_content.extend([
            "```",
        ])

    # Save to dynamic_skills/
    try:
        os.makedirs(os.path.dirname(skill_path), exist_ok=True)
        with open(skill_path, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_content))
        print(f"[Self-Learning] ✅ Crystallized skill saved to: {skill_path}")
    except IOError as e:
        print(f"[Self-Learning] ⚠️ Failed to save skill file: {e}")
        return False

    # Ingest to Qdrant
    skill_text = "\n".join(markdown_content[4:]) # Strip YAML frontmatter for search snippet
    record_insight(
        content=skill_text,
        namespace="keystone_learnings",
        eeat_type="technique",
        topic=short_title.replace('_', ' '),
        source=f"crystallization:{conversation_id[:8]}",
        priority="high",
        metadata={
            "skill_name": skill_name,
            "convo_id": conversation_id
        }
    )
    return True


# ─── CLI ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Keystone Self-Learning Engine v1.0")
    parser.add_argument("--record", type=str, help="Record a new learning/insight")
    parser.add_argument("--namespace", default="keystone_learnings", help="Target namespace")
    parser.add_argument("--topic", default="", help="Topic label")
    parser.add_argument("--type", default="discovery", choices=list(EEAT_TAGS.keys()), help="Learning type")
    parser.add_argument("--promote", action="store_true", help="Promote crystalized memories to Qdrant")
    parser.add_argument("--gaps", action="store_true", help="Analyze knowledge gaps")
    parser.add_argument("--stats", action="store_true", help="Show learning statistics")
    parser.add_argument("--crystallize", type=str, help="Crystallize a new skill from a conversation ID")
    args = parser.parse_args()

    if args.record:
        lid = record_insight(
            content=args.record,
            namespace=args.namespace,
            eeat_type=args.type,
            topic=args.topic,
        )
        if lid:
            print(f"\n✅ Learning recorded: {lid}")
    elif args.promote:
        count = promote_crystalized_memories()
        print(f"\n✅ Promoted {count} memories to vector DB")
    elif args.gaps:
        analyze_knowledge_gaps()
    elif args.stats:
        learning_stats()
    elif args.crystallize:
        ok = crystallize_skill_from_transcript(args.crystallize)
        if ok:
            print(f"\n✅ Skill crystallization successful.")
        else:
            print(f"\n❌ Skill crystallization failed.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
