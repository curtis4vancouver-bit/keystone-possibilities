#!/usr/bin/env python3
"""
Keystone Empire - Persistent Google Spark Antigravity Agent.
Automates 24/7 background lead monitoring, structured JSON extraction via Pydantic,
and local vector brain database synchronization.
"""

import os
import sys
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
import pydantic

from google import genai

# Paths Configuration
ROOT_DIR = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
INBOX_DIR = ROOT_DIR / "Agent_Inbox"
DATABASE_PATH = ROOT_DIR / "mydb.keystone"
LEXICON_PATH = ROOT_DIR / "Audiobook" / "04_Companion_Docs" / "lexicon.json"
RULES_DIR = ROOT_DIR / ".agents" / "rules"

# Set up logging to stdout and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(ROOT_DIR / "Transcripts" / "spark_agent.log", encoding="utf-8")
    ]
)

# 1. Structured Output Schema using Pydantic
class ConstructionLead(pydantic.BaseModel):
    client_name: str = pydantic.Field(description="Full name of the prospective client.")
    email: str = pydantic.Field(description="Email address of the prospect.")
    phone: str = pydantic.Field(description="Phone number of the prospect.")
    project_type: str = pydantic.Field(description="Type of construction (e.g. Custom Homes, Landscaping, Roofing, Civil).")
    location: str = pydantic.Field(description="Geographic location of the build project.")
    budget: float = pydantic.Field(description="Estimated project budget in USD/CAD.")
    timeline: str = pydantic.Field(description="Estimated start time or timeline (e.g., Immediate, Fall 2026, 3 months).")
    scope_of_work: str = pydantic.Field(description="Summary of requested engineering and architectural work.")
    confidence_score: float = pydantic.Field(description="Confidence score between 0.0 and 1.0 that this is a valid luxury lead.")


# 2. Local Database Mock Engine (Matches keystone_ingest.py format)
class LeadDatabase:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        
    def save_lead(self, lead: ConstructionLead) -> bool:
        """Saves structured lead metadata into the local database registry."""
        try:
            lead_id = f"lead_{int(asyncio.get_event_loop().time())}"
            record = {
                "id": lead_id,
                "timestamp": str(asyncio.get_event_loop().time()),
                "data": lead.dict()
            }
            
            # Simulated write to a JSON database file
            data_file = ROOT_DIR / "Transcripts" / "ingested_leads.jsonl"
            with open(data_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
                
            logging.info(f"[DB Sync] Lead successfully committed to {data_file.name}: {lead.client_name}")
            return True
        except Exception as e:
            logging.error(f"[DB Error] Failed to write to lead database: {e}")
            return False


# 3. Blackboard Memory Link
def update_sovereign_blackboard(lead: ConstructionLead):
    """Writes the captured lead context directly to the sovereign .agents/rules folder."""
    try:
        RULES_DIR.mkdir(parents=True, exist_ok=True)
        memory_file = RULES_DIR / "project-context.md"
        
        # Append lead info to local memory so future agent sessions bootstrap off of it
        markdown_entry = (
            f"\n### Ingested Spark Lead: {lead.client_name}\n"
            f"- **Email:** {lead.email}\n"
            f"- **Phone:** {lead.phone}\n"
            f"- **Project Type:** {lead.project_type}\n"
            f"- **Location:** {lead.location}\n"
            f"- **Budget:** ${lead.budget:,.2f}\n"
            f"- **Timeline:** {lead.timeline}\n"
            f"- **Scope:** {lead.scope_of_work}\n"
            f"- **Confidence:** {lead.confidence_score:.2f}\n"
            f"---\n"
        )
        
        with open(memory_file, "a", encoding="utf-8") as f:
            f.write(markdown_entry)
        logging.info("[Blackboard Sync] project-context.md successfully updated with new lead.")
    except Exception as e:
        logging.error(f"[Blackboard Error] Failed to sync memory context: {e}")


# 4. Background Periodic Lead Polling Trigger
async def poll_inbox_for_leads():
    """
    Trigger callback that executes periodically.
    Checks Agent_Inbox/ directory for raw email text dumps, processes them via Gemini,
    extracts structured leads, and syncs vector memory.
    """
    logging.info("[Spark Trigger] Checking Agent_Inbox for raw incoming leads...")
    
    inbox_files = list(INBOX_DIR.glob("*.txt"))
    if not inbox_files:
        logging.info("[Spark Trigger] No new lead files detected. Sleep cycle active.")
        return

    # Initialize lead database
    db = LeadDatabase(DATABASE_PATH)

    # Configure our Gemini client
    client = genai.Client()
    system_instruction = (
        "You are the Gemini Spark lead extraction agent.\n"
        "Your task is to analyze the raw email body text and extract construction lead metadata.\n"
        "Format the output strictly according to the ConstructionLead schema."
    )

    for lead_file in inbox_files:
        logging.info(f"[Spark Trigger] Processing lead file: {lead_file.name}")
        try:
            with open(lead_file, "r", encoding="utf-8") as f:
                email_body = f.read()

            # Normalization Hook against Lexicon
            lexicon = {}
            if LEXICON_PATH.exists():
                with open(LEXICON_PATH, "r", encoding="utf-8") as lex_f:
                    lexicon = json.load(lex_f)
                for key, val in lexicon.items():
                    email_body = email_body.replace(key, val)

            # Speak to the agent to parse the email text and return structured JSON
            logging.info("[Gemini Spark] Parsing email text via GenAI SDK...")
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Extract lead data from the following email text:\n\n{email_body}",
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=ConstructionLead,
                ),
            )
            structured_data = json.loads(response.text)

            if structured_data:
                # Convert dictionary to Pydantic object
                lead = ConstructionLead(**structured_data)
                logging.info(f"[Lead Extracted] Client: {lead.client_name} // Budget: ${lead.budget:,.2f}")
                
                # Commit to Database & Ingest vector memory
                db.save_lead(lead)
                update_sovereign_blackboard(lead)
                
                # Remove file from inbox to prevent double ingestion
                lead_file.unlink()
                logging.info(f"[Inbox Housekeeping] Cleaned processed file: {lead_file.name}")
            else:
                logging.error(f"[Extraction Failure] Gemini failed to parse structured output for: {lead_file.name}")

        except Exception as e:
            logging.error(f"[Processing Error] Failed to process lead file {lead_file.name}: {e}")


# 5. Main Loop Execution
async def main():
    logging.info("=" * 70)
    logging.info("GOOGLE SPARK AUTOPILOT DAEMON STARTED (GENAI SDK)")
    logging.info("=" * 70)
    
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    logging.info(f"Watching directory: {INBOX_DIR}")
    
    logging.info("[Autopilot Daemon] Triggers bound. Agent is actively listening...")
    
    while True:
        await poll_inbox_for_leads()
        await asyncio.sleep(30)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("[Autopilot Daemon] Stopped by keyboard interrupt.")
        sys.exit(0)
