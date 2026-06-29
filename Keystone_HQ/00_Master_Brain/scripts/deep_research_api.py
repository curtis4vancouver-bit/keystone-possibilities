import os
import sys
import asyncio
import json
import logging
import argparse
import datetime
import uuid
import re
from pathlib import Path
from typing import Optional, Callable, Dict, Any, Union

import dotenv
from google import genai
from google.genai import types

# Setup path to import brain MCP tools
script_dir = Path(__file__).resolve().parent
workspace_root = script_dir.parent
brain_path = workspace_root.parent / "00_Engine" / "Qdrant_Brain"
if str(brain_path) not in sys.path:
    sys.path.append(str(brain_path))

# Setup logging
log_file = script_dir / "deep_research.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("deep_research_api")

# Load environment variables
dotenv.load_dotenv(workspace_root / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    logger.error("GEMINI_API_KEY not found in environment or .env file.")

# Define models
MODES = {
    "fast": "deep-research-preview-04-2026",
    "max": "deep-research-max-preview-04-2026"
}

# Helper to run API calls with exponential backoff retries
async def call_with_retry(func, *args, **kwargs):
    max_retries = 3
    base_delay = 2
    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt)
            logger.warning(f"API call failed: {e}. Retrying in {delay:.1f} seconds...")
            await asyncio.sleep(delay)

def get_client() -> genai.Client:
    """Initialize and return the GenAI client."""
    if not API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured.")
    return genai.Client(api_key=API_KEY)

async def default_cli_feedback_callback(plan_text: str) -> str:
    """Default interactive callback for CLI collaborative planning."""
    print("\n" + "="*20 + " PROPOSED RESEARCH PLAN " + "="*20)
    print(plan_text)
    print("="*64 + "\n")
    
    # Run blocking input in executor
    loop = asyncio.get_running_loop()
    feedback = await loop.run_in_executor(
        None, 
        lambda: input("Review the plan above. Press [Enter] to approve, or type your adjustments: ")
    )
    if not feedback.strip():
        return "Approved. Proceed with deep research."
    return feedback

async def run_deep_research(
    query: str, 
    mode: str = "fast", 
    collaborative: bool = False,
    feedback_callback: Optional[Callable[[str], Any]] = None
) -> str:
    """
    Fires Deep Research query programmatically using Interactions API and polls for completion.
    
    Args:
        query: The research topic query.
        mode: "fast" or "max" mode.
        collaborative: If True, enables collaborative planning.
        feedback_callback: Custom callback for collaborative planning feedback.
        
    Returns:
        The full cited research report text.
    """
    client = get_client()
    agent_model = MODES.get(mode.lower(), MODES["fast"])
    
    logger.info(f"Starting deep research. Mode: {mode} ({agent_model}), Collaborative: {collaborative}")
    logger.info(f"Query: '{query}'")
    
    create_kwargs = {
        "input": query,
        "agent": agent_model,
        "background": True,
    }
    if collaborative:
        create_kwargs["agent_config"] = {
            "type": "deep-research",
            "collaborative_planning": True
        }
        
    # Start the interaction
    logger.info("Initializing interaction...")
    interaction = await call_with_retry(
        client.aio.interactions.create,
        **create_kwargs
    )
    
    interaction_id = interaction.id
    logger.info(f"Interaction created. ID: {interaction_id}")
    
    while True:
        await asyncio.sleep(15)
        
        # Poll interaction status
        interaction = await call_with_retry(
            client.aio.interactions.get,
            id=interaction_id
        )
        
        status = interaction.status
        logger.info(f"Polling interaction {interaction_id}... Status: {status}")
        
        if status == "completed":
            # Extract final text report
            logger.info("Research completed successfully.")
            report_text = getattr(interaction, "output_text", "")
            if not report_text and hasattr(interaction, "outputs") and interaction.outputs:
                for out in reversed(interaction.outputs):
                    if hasattr(out, 'text') and out.text:
                        report_text = out.text
                        break
            if not report_text:
                raise RuntimeError("Interaction completed but no report output was found.")
            return report_text
            
        elif status == "requires_action":
            # Extract latest output (proposed plan)
            plan_text = getattr(interaction, "output_text", "")
            if not plan_text and hasattr(interaction, "outputs") and interaction.outputs:
                for out in reversed(interaction.outputs):
                    if hasattr(out, 'text') and out.text:
                        plan_text = out.text
                        break
            
            logger.info("Interaction requires action: Proposed plan generated.")
            
            # Resolve feedback
            if collaborative:
                callback = feedback_callback or default_cli_feedback_callback
                feedback = await callback(plan_text)
                logger.info(f"Submitting collaborative feedback: '{feedback}'")
                
                # Resume interaction with feedback
                interaction = await call_with_retry(
                    client.aio.interactions.create,
                    input=feedback,
                    agent=agent_model,
                    background=True,
                    previous_interaction_id=interaction_id
                )
                interaction_id = interaction.id
                logger.info(f"Interaction resumed with new ID: {interaction_id}")
            else:
                # Auto-approve if not in collaborative mode but API somehow asked
                logger.info("Auto-approving proposed plan...")
                interaction = await call_with_retry(
                    client.aio.interactions.create,
                    input="Approved. Proceed.",
                    agent=agent_model,
                    background=True,
                    previous_interaction_id=interaction_id
                )
                interaction_id = interaction.id
                logger.info(f"Interaction resumed with new ID: {interaction_id}")
                
        elif status in ("failed", "cancelled", "incomplete"):
            raise RuntimeError(f"Interaction {interaction_id} ended with status: {status}")

async def research_and_ingest(
    query: str, 
    namespace: str, 
    mode: str = "fast",
    collaborative: bool = False
) -> str:
    """
    Runs deep research and automatically ingests the report into the specified brain namespace.
    """
    logger.info(f"Requesting research and ingestion. Namespace: {namespace}")
    
    # Try importing brain MCP tool
    try:
        from keystone_brain_v2_mcp import ingest_to_brain
    except ImportError as e:
        logger.error(f"Cannot import keystone_brain_v2_mcp: {e}. Check Qdrant_Brain path.")
        raise
        
    # Run the research
    report_text = await run_deep_research(
        query=query, 
        mode=mode, 
        collaborative=collaborative
    )
    
    # Ingest into vector brain
    # Generate clean source_id from query
    clean_query = re.sub(r'[^a-zA-Z0-9_\-]+', '_', query).strip('_')[:50]
    source_id = f"deep_research_{clean_query}_{datetime.date.today().isoformat()}"
    
    logger.info(f"Ingesting research report into namespace '{namespace}' with source ID '{source_id}'...")
    
    # Call ingest_to_brain in an executor to avoid blocking the event loop
    ingest_result = await asyncio.to_thread(
        ingest_to_brain,
        source_id=source_id,
        content=report_text,
        namespace=namespace,
        memory_layer="semantic"
    )
    
    logger.info(f"Ingestion result: {ingest_result}")
    
    # Log to scripts/research_log.jsonl
    log_entry = {
        "query": query,
        "namespace": namespace,
        "mode": mode,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source_id": source_id,
        "status": "completed",
        "report_length": len(report_text)
    }
    
    log_file_jsonl = script_dir / "research_log.jsonl"
    try:
        with open(log_file_jsonl, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        logger.info(f"Research entry appended to {log_file_jsonl}")
    except Exception as e:
        logger.error(f"Failed to write to research log file: {e}")
        
    return report_text

async def main():
    parser = argparse.ArgumentParser(description="Programmatic Google Deep Research API Client.")
    parser.add_argument("--query", type=str, required=True, help="Research query topic")
    parser.add_argument("--namespace", type=str, default="general", help="Target brain namespace for ingestion")
    parser.add_argument("--mode", type=str, choices=["fast", "max"], default="fast", help="Research depth mode")
    parser.add_argument("--collaborative", action="store_true", help="Enable collaborative planning mode")
    parser.add_argument("--no-ingest", action="store_true", help="Only run research and output text, do not ingest")
    
    args = parser.parse_args()
    
    try:
        if args.no_ingest:
            report = await run_deep_research(
                query=args.query, 
                mode=args.mode, 
                collaborative=args.collaborative
            )
            print("\n" + "="*20 + " RESEARCH REPORT " + "="*20)
            print(report)
            print("="*57 + "\n")
        else:
            await research_and_ingest(
                query=args.query,
                namespace=args.namespace,
                mode=args.mode,
                collaborative=args.collaborative
            )
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # If running as script, run main
    asyncio.run(main())
