import os
import sys
import json
import re
import asyncio
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Ensure stdout uses UTF-8 to prevent encoding issues on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)-7s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\Agent_Fleet\client_outreach\outreach.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("outreach_engine")

# Workspace Paths and Constants
MASTER_BRAIN = Path(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
LEADS_FILE = MASTER_BRAIN / "Agent_Fleet" / "client_outreach" / "leads.json"
VOICE_OUTBOX = Path(r"C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt")
ENV_FILE = MASTER_BRAIN / ".env"
WORKSPACE_ACCOUNT = "keystone"

# --------------------------------------------------------------------------
# Environment Loading
# --------------------------------------------------------------------------
def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("GEMINI_API_KEY="):
                os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()
                break

load_env()

# --------------------------------------------------------------------------
# Lead Database Loader/Saver
# --------------------------------------------------------------------------
def load_leads():
    if LEADS_FILE.exists():
        try:
            data = json.loads(LEADS_FILE.read_text(encoding="utf-8"))
            if "leads" not in data:
                data = {"leads": []}
            return data
        except Exception as e:
            logger.error(f"Failed to parse leads.json: {e}")
            return {"leads": []}
    return {"leads": []}

def save_leads(data):
    try:
        LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
        LEADS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info("Successfully saved leads database.")
    except Exception as e:
        logger.error(f"Failed to save leads.json: {e}")

# --------------------------------------------------------------------------
# Date / Business Day Helpers
# --------------------------------------------------------------------------
def get_business_days_diff(start_dt, end_dt):
    if start_dt > end_dt:
        return 0
    current = start_dt
    days = 0
    while current.date() < end_dt.date():
        current += timedelta(days=1)
        if current.weekday() < 5:  # Monday - Friday
            days += 1
    return days

def add_business_days(start_dt, days):
    current = start_dt
    added = 0
    while added < days:
        current += timedelta(days=1)
        if current.weekday() < 5:
            added += 1
    return current

# --------------------------------------------------------------------------
# LLM Generators
# --------------------------------------------------------------------------
def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment or .env file.")
    return genai.Client(api_key=api_key)

def compose_outreach_email_llm(lead_name, lead_company, notes):
    try:
        client = get_gemini_client()
        prompt = f"""
You are Wayne Stevenson, owner of Keystone Possibilities (B2B construction and project management consulting in the Squamish / Sea-to-Sky corridor, BC builder licence #52603).
You are writing a cold B2B outreach email to a potential client/partner.

Recipient Details:
- Name: {lead_name}
- Company: {lead_company}
- Notes/Project details: {notes}

Brand Context / Details:
- Focus on heavy civil, residential builds, BC Bill 44 opportunities, or project management consulting.
- Service area is Vancouver to Whistler, specifically Squamish.
- Your tone must be: casual, knowledgeable, professional B2B (Wayne's natural voice: no corporate jargon, warm but confident, direct).
- Mention Keystone Possibilities naturally.
- Sign off as Wayne Stevenson.

Write the subject line on the first line (e.g. 'Subject: ...') and then the email body. Do not output anything else.
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        text = response.text.strip()
        subject = f"Project Collaboration - {lead_company}"
        body = text
        
        subject_match = re.match(r"^Subject:\s*(.*)", text, re.IGNORECASE)
        if subject_match:
            subject = subject_match.group(1).strip()
            body = text[subject_match.end():].strip()
            
        return subject, body
    except Exception as e:
        logger.error(f"Error composing outreach email via LLM: {e}")
        return f"Collaboration with {lead_company}", f"Hi {lead_name},\n\nI hope you're doing well. I wanted to reach out regarding potential construction project management opportunities in the Squamish area. Let me know if you have time to chat.\n\nBest regards,\nWayne Stevenson\nKeystone Possibilities"

def compose_reply_email_llm(lead_name, email_history, brain_context=None, meeting_request=False):
    try:
        client = get_gemini_client()
        prompt = f"""
You are Wayne Stevenson, owner of Keystone Possibilities.
You are drafting a reply to a message from a lead.

Lead Name: {lead_name}
Email History (latest at the bottom):
{email_history}
"""
        if brain_context:
            prompt += f"\nRelevant Building Code / Construction Details from your brain:\n{brain_context}\n"
        elif meeting_request:
            prompt += "\nThe lead wants to meet. Propose 2-3 specific time slots next week (e.g., next Tuesday at 10 AM, Wednesday at 2 PM, or Thursday at 11 AM) in a casual, professional way.\n"
            
        prompt += """
Write a casual, knowledgeable, professional reply. Mention Keystone Possibilities if natural. Sign off as Wayne Stevenson.
Do not output subject lines or anything else, just the email body content.
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error composing reply via LLM: {e}")
        return f"Hi {lead_name},\n\nThanks for reaching out. Let's arrange a time to speak next week. How does Tuesday morning work for you?\n\nBest,\nWayne Stevenson\nKeystone Possibilities"

def check_escalation_llm(email_body):
    try:
        client = get_gemini_client()
        prompt = f"""
Analyze the following email from a prospect or client. Determine if it meets any of the following escalation criteria:
1. Mentions financial disputes, budgets, or money amounts > $10,000.
2. Mentions contract violations, legal actions, or lawyers.
3. Contains strong complaints, angry language, or threats.

Email content:
\"\"\"
{email_body}
\"\"\"

Respond with a JSON object:
{{
  "escalate": true|false,
  "reason": "Brief reason if escalate is true, otherwise empty"
}}
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(response.text.strip())
        return data.get("escalate", False), data.get("reason", "")
    except Exception as e:
        logger.warning(f"Escalation check LLM failed: {e}. Falling back to simple regex checks.")
        has_large_money = bool(re.search(r'\$\s*\d{2,3}(?:,\d{3}){2,}', email_body))
        has_legal = any(word in email_body.lower() for word in ["legal", "contract", "lawyer", "attorney", "dispute", "court", "sue"])
        has_complaint = any(word in email_body.lower() for word in ["complain", "fail", "delay", "poor", "unacceptable", "terrible", "worst"])
        if has_large_money or has_legal or has_complaint:
            return True, f"Regex warning: money={has_large_money}, legal={has_legal}, complaint={has_complaint}"
        return False, ""

def check_building_code_question_llm(email_body):
    try:
        client = get_gemini_client()
        prompt = f"""
Analyze the following email from a prospect. Determine if they are asking a specific technical question about BC Building Code, STEP Code, zoning, permits, or local Squamish/Vancouver building requirements.

Email content:
\"\"\"
{email_body}
\"\"\"

Respond with a JSON object:
{{
  "is_building_code_question": true|false
}}
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        data = json.loads(response.text.strip())
        return data.get("is_building_code_question", False)
    except Exception as e:
        logger.warning(f"Building code question check LLM failed: {e}. Falling back to keyword checks.")
        keywords = ["step code", "building code", "zoning", "permit", "bcbc", "bylaw", "egress", "height", "setback"]
        return any(k in email_body.lower() for k in keywords)

# --------------------------------------------------------------------------
# MCP Client Context Manager
# --------------------------------------------------------------------------
class MCPSessionManager:
    def __init__(self, command, args, env=None):
        self.command = command
        self.args = args
        self.env = env
        self.read_stream = None
        self.write_stream = None
        self.session = None
        self._exit_stack = None

    async def __aenter__(self):
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        process_env = os.environ.copy()
        if self.env:
            process_env.update(self.env)
            
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=process_env
        )
        
        streams = await self._exit_stack.enter_async_context(stdio_client(server_params))
        self.read_stream, self.write_stream = streams
        self.session = await self._exit_stack.enter_async_context(ClientSession(self.read_stream, self.write_stream))
        await self.session.initialize()
        return self.session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.aclose()

# --------------------------------------------------------------------------
# Robust Message Body Extractor
# --------------------------------------------------------------------------
def extract_email_body(msg_data):
    if not msg_data:
        return ""
    if isinstance(msg_data, str):
        return msg_data
    if isinstance(msg_data, list):
        text_parts = []
        for part in msg_data:
            if hasattr(part, "text"):
                text_parts.append(part.text)
            elif isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
        return "\n".join(text_parts)
    if isinstance(msg_data, dict):
        if "body" in msg_data:
            return msg_data["body"]
        if "snippet" in msg_data:
            return msg_data["snippet"]
        if "content" in msg_data:
            return msg_data["content"]
        if "text" in msg_data:
            return msg_data["text"]
    return str(msg_data)

# --------------------------------------------------------------------------
# Core Outreach Workflows
# --------------------------------------------------------------------------
async def process_new_outreach(ws_session, digest_report):
    logger.info("Starting processing of new outreach leads...")
    db = load_leads()
    new_leads = [l for l in db["leads"] if l.get("status") == "new"]
    
    if not new_leads:
        logger.info("No new leads found to reach out to.")
        return
        
    for lead in new_leads:
        name = lead.get("name")
        company = lead.get("company")
        email = lead.get("email")
        notes = lead.get("notes", "")
        
        logger.info(f"Composing cold outreach for {name} ({company})...")
        subject, body = compose_outreach_email_llm(name, company, notes)
        
        try:
            logger.info(f"Creating Gmail draft for {email}...")
            draft_res = await ws_session.call_tool("createGmailDraft", {
                "account": WORKSPACE_ACCOUNT,
                "to": email,
                "subject": subject,
                "body": body
            })
            logger.info(f"Created draft successfully: {draft_res}")
            
            # Update lead in db
            lead["status"] = "contacted"
            lead["last_contact"] = datetime.now().isoformat()
            lead["follow_up_date"] = add_business_days(datetime.now(), 3).isoformat()
            
            # Record in history
            if "conversation_history" not in lead:
                lead["conversation_history"] = []
            lead["conversation_history"].append({
                "date": datetime.now().isoformat(),
                "sender": "Wayne Stevenson",
                "subject": subject,
                "body": body,
                "type": "outreach_draft"
            })
            
            digest_report["new_outreach_drafts"] += 1
            digest_report["details"].append(f"Created cold outreach draft for {name} ({company}) - {email}")
        except Exception as e:
            logger.error(f"Failed to create Gmail draft for {email}: {e}")
            
    save_leads(db)

async def check_incoming_replies(ws_session, brain_session, digest_report):
    logger.info("Checking for incoming replies from contacted leads...")
    db = load_leads()
    contacted_leads = [l for l in db["leads"] if l.get("status") == "contacted"]
    
    if not contacted_leads:
        logger.info("No contacted leads in database to check for replies.")
        return
        
    for lead in contacted_leads:
        email = lead.get("email")
        name = lead.get("name")
        last_contact_str = lead.get("last_contact")
        
        logger.info(f"Searching Gmail for messages from {email}...")
        try:
            search_res = await ws_session.call_tool("searchGmail", {
                "account": WORKSPACE_ACCOUNT,
                "query": f"from:{email}",
                "maxResults": 10
            })
            
            # searchGmail returns a list or text with message list
            # Let's inspect search_res.content or structure
            # Typically searchGmail lists message IDs
            messages_text = extract_email_body(search_res.content)
            
            # Workspace tool output format parser
            # Let's look for message IDs matching regex or json
            message_ids = []
            # Find all message IDs (normally 16-hex characters in Gmail)
            found_ids = re.findall(r"\b[0-9a-fA-F]{16}\b", messages_text)
            for m_id in found_ids:
                if m_id not in message_ids:
                    message_ids.append(m_id)
            
            if not message_ids:
                logger.info(f"No emails found from {email}.")
                continue
                
            last_contact_dt = datetime.fromisoformat(last_contact_str) if last_contact_str else datetime.now() - timedelta(days=30)
            
            new_replies_found = 0
            for m_id in message_ids:
                msg_detail = await ws_session.call_tool("readGmailMessage", {
                    "account": WORKSPACE_ACCOUNT,
                    "messageId": m_id,
                    "format": "full"
                })
                msg_body = extract_email_body(msg_detail.content)
                
                # Check message date from headers in body
                # Let's look for Date header or check metadata
                date_match = re.search(r"Date:\s*(.*)", msg_body, re.IGNORECASE)
                msg_date = None
                if date_match:
                    try:
                        # Simple parsed date fallback
                        # Gmail date formats: e.g., "Thu, 25 Jun 2026 13:00:00 -0700"
                        # We can try to parse or just check if it contains recent year
                        pass
                    except Exception:
                        pass
                
                # To be safe, we also check if this message ID is already in conversation_history
                if "conversation_history" not in lead:
                    lead["conversation_history"] = []
                    
                already_processed = any(h.get("gmail_id") == m_id for h in lead["conversation_history"])
                if already_processed:
                    continue
                    
                logger.info(f"Processing new email reply (ID: {m_id}) from {email}...")
                
                # 1. Escalation check
                escalate, reason = check_escalation_llm(msg_body)
                if escalate:
                    logger.warning(f"ESCALATION TRIGGERED for lead {name} ({email}): {reason}")
                    lead["status"] = "replied"
                    lead["escalated"] = True
                    lead["escalation_reason"] = reason
                    lead["conversation_history"].append({
                        "date": datetime.now().isoformat(),
                        "sender": name,
                        "gmail_id": m_id,
                        "body": msg_body,
                        "type": "incoming_reply_escalated"
                    })
                    digest_report["escalations"].append(f"ESCALATED Lead: {name} - Reason: {reason}")
                    new_replies_found += 1
                    continue
                    
                # 2. Building code question check
                is_building_code = check_building_code_question_llm(msg_body)
                brain_context = None
                if is_building_code and brain_session:
                    logger.info("Building code question detected. Searching master brain...")
                    search_res = await brain_session.call_tool("search_master_brain", {
                        "query": msg_body,
                        "namespace": "possibilities",
                        "limit": 3
                    })
                    brain_context = extract_email_body(search_res.content)
                    logger.info(f"Retrieved brain context: {brain_context[:200]}...")
                    
                # 3. Draft reply
                # Compile conversation history for LLM context
                history_summary = []
                for h in lead["conversation_history"][-5:]:
                    history_summary.append(f"{h.get('sender')}: {h.get('body')[:300]}")
                history_summary.append(f"{name} (Incoming): {msg_body[:1000]}")
                history_text = "\n\n".join(history_summary)
                
                meeting_request = "meet" in msg_body.lower() or "schedule" in msg_body.lower() or "call" in msg_body.lower()
                
                reply_body = compose_reply_email_llm(name, history_text, brain_context, meeting_request)
                
                # Create draft reply in Gmail
                subject_match = re.search(r"Subject:\s*(.*)", msg_body, re.IGNORECASE)
                subject = f"Re: {subject_match.group(1).strip()}" if subject_match else f"Re: Project Collaboration"
                
                try:
                    draft_res = await ws_session.call_tool("createGmailDraft", {
                        "account": WORKSPACE_ACCOUNT,
                        "to": email,
                        "subject": subject,
                        "body": reply_body,
                        "replyToMessageId": m_id
                    })
                    logger.info(f"Created draft reply successfully: {draft_res}")
                    
                    # Update lead db
                    lead["status"] = "replied"
                    lead["last_contact"] = datetime.now().isoformat()
                    lead["conversation_history"].append({
                        "date": datetime.now().isoformat(),
                        "sender": name,
                        "gmail_id": m_id,
                        "body": msg_body,
                        "type": "incoming_reply"
                    })
                    lead["conversation_history"].append({
                        "date": datetime.now().isoformat(),
                        "sender": "Wayne Stevenson",
                        "body": reply_body,
                        "type": "reply_draft",
                        "subject": subject
                    })
                    
                    digest_report["replies_received"] += 1
                    digest_report["details"].append(f"Received reply from {name} and created draft reply (threaded)")
                    new_replies_found += 1
                except Exception as e:
                    logger.error(f"Failed to create draft reply for {email}: {e}")
                    
            if new_replies_found > 0:
                save_leads(db)
        except Exception as e:
            logger.error(f"Failed to check replies for {email}: {e}")

async def process_followups(ws_session, digest_report):
    logger.info("Checking for leads needing follow-ups...")
    db = load_leads()
    contacted_leads = [l for l in db["leads"] if l.get("status") == "contacted"]
    
    if not contacted_leads:
        logger.info("No contacted leads to follow up on.")
        return
        
    for lead in contacted_leads:
        follow_up_date_str = lead.get("follow_up_date")
        last_contact_str = lead.get("last_contact")
        
        should_follow_up = False
        if follow_up_date_str:
            should_follow_up = datetime.now() >= datetime.fromisoformat(follow_up_date_str)
        elif last_contact_str:
            last_contact_dt = datetime.fromisoformat(last_contact_str)
            should_follow_up = get_business_days_diff(last_contact_dt, datetime.now()) >= 3
            
        if not should_follow_up:
            continue
            
        email = lead.get("email")
        name = lead.get("name")
        company = lead.get("company")
        
        logger.info(f"Generating follow-up draft for {name} ({company})...")
        
        # Pull history
        history_summary = []
        for h in lead.get("conversation_history", [])[-3:]:
            history_summary.append(f"{h.get('sender')}: {h.get('body')[:200]}")
        history_text = "\n\n".join(history_summary)
        
        try:
            client = get_gemini_client()
            prompt = f"""
You are Wayne Stevenson, owner of Keystone Possibilities.
You sent a B2B cold outreach email to a prospect 3 business days ago and haven't heard back. 
You want to send a brief, polite, casual follow-up check-in.

Prospect Details:
- Name: {name}
- Company: {company}
- Past Message History:
{history_text}

Tone:
- Casual, warm, confident, professional.
- Simple: "Just checking in to see if you had a chance to read my last email and if you have 5 minutes to connect."
- Signs off as Wayne Stevenson.

Do not output subject lines or anything else, just the email body content.
"""
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            body = response.text.strip()
            
            # Find subject from history
            subject = "Following up"
            for h in reversed(lead.get("conversation_history", [])):
                if h.get("subject"):
                    subject = h["subject"]
                    if not subject.lower().startswith("re:"):
                        subject = f"Re: {subject}"
                    break
                    
            logger.info(f"Creating follow-up Gmail draft for {email}...")
            draft_res = await ws_session.call_tool("createGmailDraft", {
                "account": WORKSPACE_ACCOUNT,
                "to": email,
                "subject": subject,
                "body": body
            })
            logger.info(f"Follow-up draft created: {draft_res}")
            
            # Update lead
            lead["last_contact"] = datetime.now().isoformat()
            lead["follow_up_date"] = add_business_days(datetime.now(), 3).isoformat()
            lead["conversation_history"].append({
                "date": datetime.now().isoformat(),
                "sender": "Wayne Stevenson",
                "body": body,
                "type": "follow_up_draft",
                "subject": subject
            })
            
            digest_report["followups_created"] += 1
            digest_report["details"].append(f"Created follow-up draft for {name} ({company}) - {email}")
        except Exception as e:
            logger.error(f"Failed to create follow-up draft for {email}: {e}")
            
    save_leads(db)

# --------------------------------------------------------------------------
# Daily Digest and Voice Outbox Compilation
# --------------------------------------------------------------------------
def compile_digest(digest_report):
    logger.info("Compiling daily digest...")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Conversational Summary for Voice Outbox (Wayne Stevenson's ear)
    outbox_text = f"Hey Wayne, here is your morning outreach digest for {datetime.now().strftime('%A, %B %d')}. "
    
    if digest_report["new_outreach_drafts"] > 0:
        outbox_text += f"We compiled and generated {digest_report['new_outreach_drafts']} new cold B2B outreach email drafts. "
    else:
        outbox_text += "No new cold outreach emails were drafted today. "
        
    if digest_report["replies_received"] > 0:
        outbox_text += f"We received {digest_report['replies_received']} replies from your leads. I have searched the master brain and pre-drafted threaded replies for you to review in Gmail. "
    else:
        outbox_text += "There are no new replies from leads. "
        
    if digest_report["followups_created"] > 0:
        outbox_text += f"I scheduled and created {digest_report['followups_created']} polite follow-up drafts for prospects who hadn't replied in three business days. "
        
    if digest_report["escalations"]:
        outbox_text += f"Important! We have {len(digest_report['escalations'])} escalated item requiring your direct attention. "
        for esc in digest_report["escalations"]:
            outbox_text += f"{esc}. "
    else:
        outbox_text += "There are no escalated complaints or high-value issues today. "
        
    outbox_text += "All messages are saved in your Gmail Drafts folder. Let me know if you want me to do anything else."
    
    # Write to Voice Outbox
    try:
        VOICE_OUTBOX.parent.mkdir(parents=True, exist_ok=True)
        VOICE_OUTBOX.write_text(outbox_text, encoding="utf-8")
        logger.info(f"Voice outbox compiled and written to: {VOICE_OUTBOX}")
    except Exception as e:
        logger.error(f"Failed to write to voice outbox: {e}")

# --------------------------------------------------------------------------
# Main Program Orchestrator
# --------------------------------------------------------------------------
async def run_pipeline(args):
    digest_report = {
        "new_outreach_drafts": 0,
        "replies_received": 0,
        "followups_created": 0,
        "escalations": [],
        "details": []
    }
    
    logger.info("Initializing Outreach Engine Pipeline...")
    
    # Start Google Workspace MCP
    logger.info("Connecting to google-workspace MCP...")
    async with MCPSessionManager("npx", ["-y", "google-workspace-mcp@latest", "serve"]) as ws_session:
        logger.info("google-workspace MCP initialized.")
        
        # Start Keystone Brain MCP
        logger.info("Connecting to keystone-brain MCP...")
        async with MCPSessionManager("python", ["C:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Engine/Qdrant_Brain/keystone_brain_v2_mcp.py"]) as brain_session:
            logger.info("keystone-brain MCP initialized.")
            
            # Execute steps based on arguments
            if args.outreach or args.run_all:
                await process_new_outreach(ws_session, digest_report)
                
            if args.replies or args.run_all:
                await check_incoming_replies(ws_session, brain_session, digest_report)
                
            if args.followups or args.run_all:
                await process_followups(ws_session, digest_report)
                
            if args.digest or args.run_all:
                compile_digest(digest_report)

    logger.info("Outreach Engine Pipeline completed.")
    return digest_report

# --------------------------------------------------------------------------
# CLI Entry Point
# --------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Keystone Possibilities Autonomous Client Outreach System")
    parser.add_argument("--run-all", action="store_true", help="Run all pipeline steps (Outreach, Replies, Follow-ups, and Digest)")
    parser.add_argument("--outreach", action="store_true", help="Draft new cold outreach emails")
    parser.add_argument("--replies", action="store_true", help="Check incoming email replies and draft responses")
    parser.add_argument("--followups", action="store_true", help="Check follow-up dates and draft check-ins")
    parser.add_argument("--digest", action="store_true", help="Compile digest and write to voice outbox")
    parser.add_argument("--daemon", action="store_true", help="Run in background daemon mode")
    parser.add_argument("--interval", type=int, default=3600, help="Daemon sleep interval in seconds (default: 3600)")
    
    args = parser.parse_args()
    
    # If no flags are set, run all by default
    if not (args.run_all or args.outreach or args.replies or args.followups or args.digest or args.daemon):
        args.run_all = True
        
    if args.daemon:
        logger.info(f"Running in DAEMON mode with interval {args.interval}s...")
        while True:
            try:
                # Force run_all for daemon ticks
                daemon_args = argparse.Namespace(run_all=True, outreach=False, replies=False, followups=False, digest=True, daemon=False)
                asyncio.run(run_pipeline(daemon_args))
            except Exception as e:
                logger.error(f"Daemon pipeline error: {e}")
            logger.info(f"Daemon sleeping for {args.interval} seconds...")
            import time
            time.sleep(args.interval)
    else:
        asyncio.run(run_pipeline(args))

if __name__ == "__main__":
    main()
