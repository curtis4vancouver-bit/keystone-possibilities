import os
import sys
import asyncio
import json
import logging
import argparse
import datetime
import re
from pathlib import Path
from typing import Optional, Dict, List, Any

import dotenv
from google import genai

# Setup script directory imports
script_dir = Path(__file__).resolve().parent
if str(script_dir) not in sys.path:
    sys.path.append(str(script_dir))

import deep_research_api

# Setup logging
log_file = script_dir / "auto_learning.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("auto_learning_scheduler")

# Initial static learning topics configuration
LEARNING_TOPICS = {
    "possibilities": [
        "BC Bill 44 latest amendments multiplex construction 2026",
        "Design-Build standard contracts British Columbia",
        "Heavy civil construction best practices Sea-to-Sky corridor",
        "Construction client acquisition strategies small builder",
        "STEP code requirements BC residential construction",
    ],
    "protocol_brand": [
        "BPC-157 latest clinical research results 2026",
        "GLP-1 receptor agonist wellness applications non-diabetic",
        "Peptide therapy regulatory status Health Canada 2026",
        "YMYL content compliance Google health content guidelines",
    ],
    "music": [
        "Spotify algorithm optimization ambient electronic music 2026",
        "Training soundscape science binaural beats research",
        "Music metadata best practices MusicBrainz cataloging",
        "YouTube Music channel growth strategies instrumental",
    ],
    "webmaster": [
        "Core Web Vitals optimization techniques WordPress 2026",
        "Generative Engine Optimization GEO implementation guide",
        "Google Knowledge Panel optimization construction company",
        "Schema markup structured data local business SEO",
    ],
    "content_pipeline": [
        "YouTube Shorts algorithm ranking factors 2026",
        "YouTube thumbnail A/B testing data driven approach",
        "Video SEO best practices construction niche",
        "YouTube to blog traffic loop content repurposing",
    ],
    "general": [
        "AI agent self-improvement autonomous learning patterns 2026",
        "Google Antigravity SDK best practices agent development",
        "MCP Model Context Protocol advanced patterns",
    ],
}

PROGRESS_FILE = script_dir / "learning_progress.json"

def load_progress() -> Dict[str, Any]:
    """Load progress from JSON file."""
    if not PROGRESS_FILE.exists():
        return {}
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load progress file: {e}")
        return {}

def save_progress(progress_data: Dict[str, Any]):
    """Save progress to JSON file."""
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress_data, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save progress file: {e}")

def get_topics_for_namespace(namespace: str, progress_data: Dict[str, Any]) -> List[str]:
    """Get list of all topics for a namespace (combining static config + AI generated ones)."""
    topics = list(LEARNING_TOPICS.get(namespace, []))
    
    # Load AI generated topics if any exist
    gen_topics_dict = progress_data.get("_generated_topics", {})
    gen_topics = gen_topics_dict.get(namespace, [])
    
    # Merge and preserve order while ensuring uniqueness
    seen = set()
    merged = []
    for t in topics + gen_topics:
        if t not in seen:
            seen.add(t)
            merged.append(t)
    return merged

async def generate_new_topics(namespace: str, progress_data: Dict[str, Any]) -> List[str]:
    """Use Gemini to suggest 5 new research areas for a namespace based on completed research."""
    logger.info(f"Generating new topics for namespace '{namespace}' using Gemini...")
    
    completed_dict = progress_data.get(namespace, {})
    completed_topics = list(completed_dict.keys())
    
    prompt = f"""You are the Keystone Master Brain AI coordinator.
The agent namespace '{namespace}' has completed researching the following topics:
{json.dumps(completed_topics, indent=2)}

Based on these topics, suggest exactly 5 NEW, advanced, and logical research topics to continue the agent's education in this namespace.
The topics should be specific, actionable research queries suitable for Google Deep Research.
Respond with a raw JSON list of strings only, containing the 5 topics. Do not include markdown formatting or backticks.
"""
    
    try:
        # We use gemini-2.5-flash which is fast and supports JSON output mode or standard parsing
        client = deep_research_api.get_client()
        response = await deep_research_api.call_with_retry(
            client.aio.models.generate_content,
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        
        text = response.text.strip()
        # Clean potential markdown wrapping
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n", "", text)
            text = re.sub(r"\n```$", "", text)
            text = text.strip()
            
        new_topics = json.loads(text)
        if isinstance(new_topics, list) and len(new_topics) > 0:
            logger.info(f"Successfully generated {len(new_topics)} new topics: {new_topics}")
            return [str(t) for t in new_topics]
        else:
            logger.error("Gemini response is not a valid list of strings.")
            return []
    except Exception as e:
        logger.error(f"Failed to generate new topics with Gemini: {e}")
        return []

def get_learning_status() -> Dict[str, Any]:
    """Returns what's been learned, what's pending, and status statistics."""
    progress_data = load_progress()
    status = {}
    
    for ns in LEARNING_TOPICS.keys():
        all_topics = get_topics_for_namespace(ns, progress_data)
        completed_dict = progress_data.get(ns, {})
        completed_topics = [t for t in completed_dict.keys() if t in all_topics]
        pending_topics = [t for t in all_topics if t not in completed_dict]
        
        status[ns] = {
            "completed_count": len(completed_topics),
            "pending_count": len(pending_topics),
            "completed": completed_topics,
            "pending": pending_topics
        }
    return status

async def run_learning_cycle(namespace: Optional[str] = None, mode: str = "fast"):
    """
    Runs learning cycle. If namespace is given, learns for that namespace only.
    Otherwise, loops through all namespaces.
    For each namespace, executes the first pending topic, records progress, and ingests to brain.
    If all topics in a namespace are done, triggers generation of new topics.
    """
    progress_data = load_progress()
    namespaces_to_run = [namespace] if namespace else list(LEARNING_TOPICS.keys())
    
    logger.info(f"Starting learning cycle. Target Namespaces: {namespaces_to_run}")
    
    for ns in namespaces_to_run:
        all_topics = get_topics_for_namespace(ns, progress_data)
        completed_dict = progress_data.setdefault(ns, {})
        
        pending_topics = [t for t in all_topics if t not in completed_dict]
        
        if not pending_topics:
            logger.info(f"Namespace '{ns}' has no pending topics. Triggering topic rotation...")
            new_topics = await generate_new_topics(ns, progress_data)
            if new_topics:
                gen_topics_dict = progress_data.setdefault("_generated_topics", {})
                existing_gen = gen_topics_dict.setdefault(ns, [])
                for t in new_topics:
                    if t not in existing_gen and t not in completed_dict:
                        existing_gen.append(t)
                save_progress(progress_data)
                
                # Recalculate pending
                all_topics = get_topics_for_namespace(ns, progress_data)
                pending_topics = [t for t in all_topics if t not in completed_dict]
            
        if not pending_topics:
            logger.warning(f"No pending topics found for namespace '{ns}' even after rotation attempt.")
            continue
            
        # Select first pending topic
        topic = pending_topics[0]
        logger.info(f"Namespace '{ns}': Executing deep research for topic: '{topic}'")
        
        try:
            # Run Deep Research and auto-ingest
            report_text = await deep_research_api.research_and_ingest(
                query=topic,
                namespace=ns,
                mode=mode,
                collaborative=False
            )
            
            # Read chunks ingested from log file if possible, or estimate
            # Check research_log.jsonl to find vectors added
            vectors_added = 0
            log_file_jsonl = script_dir / "research_log.jsonl"
            if log_file_jsonl.exists():
                try:
                    with open(log_file_jsonl, "r", encoding="utf-8") as f:
                        for line in f:
                            try:
                                entry = json.loads(line.strip())
                                if entry.get("query") == topic:
                                    # Formulate vectors added based on report size if count not directly saved,
                                    # or parse the log message in deep_research.log.
                                    # keystone_brain_v2_mcp returns chunk count in message.
                                    # We can parse the deep_research.log for "Successfully ingested \d+ chunk"
                                    pass
                            except Exception:
                                pass
                except Exception:
                    pass
            
            # Read log file to find exact chunk count
            deep_log_file = script_dir / "deep_research.log"
            if deep_log_file.exists():
                try:
                    with open(deep_log_file, "r", encoding="utf-8") as f:
                        log_lines = f.readlines()
                    for line in reversed(log_lines[-20:]): # Look at last 20 lines
                        match = re.search(r"Successfully ingested (\d+) chunk", line)
                        if match:
                            vectors_added = int(match.group(1))
                            break
                except Exception as le:
                    logger.warning(f"Could not parse chunk count from log: {le}")
            
            # If still 0, estimate 1 chunk per 1500 characters
            if vectors_added == 0:
                vectors_added = max(1, len(report_text) // 1500)
                
            # Update progress
            completed_dict[topic] = {
                "completed": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "vectors_added": vectors_added
            }
            save_progress(progress_data)
            logger.info(f"Namespace '{ns}': Completed topic '{topic}'. Vectors added: {vectors_added}")
            
        except Exception as e:
            logger.error(f"Failed to execute learning topic '{topic}' for namespace '{ns}': {e}")
            # Continue to next namespace in loop

def display_status():
    """Prints a formatted report of learning progress."""
    status = get_learning_status()
    print("\n" + "="*20 + " AUTO-LEARNING PROGRESS " + "="*20)
    for ns, data in status.items():
        completed = data["completed_count"]
        pending = data["pending_count"]
        total = completed + pending
        percent = (completed / total * 100) if total > 0 else 0
        print(f"\nNamespace: {ns.upper()}")
        print(f"  Progress: {completed}/{total} ({percent:.1f}% completed)")
        
        if data["completed"]:
            print("  Completed Topics:")
            for t in data["completed"][-3:]: # Show last 3
                print(f"    [x] {t}")
            if len(data["completed"]) > 3:
                print(f"    ... and {len(data['completed']) - 3} more")
                
        if data["pending"]:
            print("  Pending Topics:")
            for t in data["pending"][:3]: # Show first 3
                print(f"    [ ] {t}")
            if len(data["pending"]) > 3:
                print(f"    ... and {len(data['pending']) - 3} more")
    print("\n" + "="*64)

async def main():
    parser = argparse.ArgumentParser(description="Keystone Master Brain Auto-Learning Scheduler.")
    parser.add_argument("--status", action="store_true", help="Show current learning progress and status")
    parser.add_argument("--run", action="store_true", help="Run the learning cycle")
    parser.add_argument("--namespace", type=str, help="Restrict run or topic generation to specific namespace")
    parser.add_argument("--generate-topics", action="store_true", help="Force AI generation of new topics")
    parser.add_argument("--mode", type=str, choices=["fast", "max"], default="fast", help="Research depth mode")
    
    args = parser.parse_args()
    
    if args.status:
        display_status()
        return
        
    if args.generate_topics:
        if not args.namespace:
            print("Error: --namespace is required when using --generate-topics")
            sys.exit(1)
        progress_data = load_progress()
        new_topics = await generate_new_topics(args.namespace, progress_data)
        if new_topics:
            gen_topics_dict = progress_data.setdefault("_generated_topics", {})
            existing_gen = gen_topics_dict.setdefault(args.namespace, [])
            for t in new_topics:
                if t not in existing_gen and t not in progress_data.get(args.namespace, {}):
                    existing_gen.append(t)
            save_progress(progress_data)
            print(f"Generated new topics for {args.namespace}:")
            for t in new_topics:
                print(f"  - {t}")
        return
        
    if args.run:
        await run_learning_cycle(namespace=args.namespace, mode=args.mode)
        return
        
    parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
