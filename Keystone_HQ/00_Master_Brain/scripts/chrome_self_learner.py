import os
import sys
import json
import re
from datetime import datetime
import subprocess
from pathlib import Path
import dotenv
from google import genai
from google.genai import types

# Ensure sys.stdout handles UTF-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Setup paths
WORKSPACE_ROOT = Path(r"C:\Users\Curtis\New folder\construction-website")
MASTER_BRAIN = WORKSPACE_ROOT / "Keystone_HQ" / "00_Master_Brain"
LEARNINGS = MASTER_BRAIN / ".learnings"
CORRECTION_JOURNAL = LEARNINGS / "correction_journal.json"
PENDING_PROPOSALS = LEARNINGS / "pending_proposals.json"
SKILLS_DIR = Path(r"C:\Users\Curtis\.gemini\config\skills")
FOUNDATION_SKILL_PATH = SKILLS_DIR / "00_keystone_foundation" / "SKILL.md"

# Load environment variables
dotenv.load_dotenv(MASTER_BRAIN / ".env")
API_KEY = os.getenv("GEMINI_API_KEY")

# Log file setup
LOG_FILE = MASTER_BRAIN / "scripts" / "self_learner.log"

def log_message(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a", encoding="utf-8") as lf:
        lf.write(formatted + "\n")

def get_transcript_path():
    config_path = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
    )
    conv_id = None
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            conv_id = config.get("conversation_id")
        except Exception:
            pass

    if not conv_id:
        conv_id = "b352331d-7ad0-45d8-9daa-058939da47d3"

    path = os.path.join(
        os.path.expanduser("~"), ".gemini", "antigravity", "brain", conv_id, ".system_generated", "logs", "transcript.jsonl"
    )
    return path

def read_last_transcript_lines(path, limit=50):
    if not os.path.exists(path):
        log_message(f"[Warning] Transcript file not found at {path}")
        return ""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
        log_message(f"Read {len(lines)} lines from transcript.jsonl.")
        return "".join(lines[-limit:])
    except Exception as e:
        log_message(f"[Error] Failed to read transcript: {e}")
        return ""

def load_correction_journal():
    if not CORRECTION_JOURNAL.exists():
        log_message(f"[Warning] Correction journal not found at {CORRECTION_JOURNAL}")
        return []
    try:
        with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
            data = json.load(f)
        log_message(f"Loaded {len(data)} entries from correction journal.")
        return data
    except Exception as e:
        log_message(f"[Error] Failed to load correction journal: {e}")
        return []

def load_pending_proposals():
    if not PENDING_PROPOSALS.exists():
        return []
    try:
        with open(PENDING_PROPOSALS, "r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            if "hits" not in item:
                item["hits"] = 1
        return data
    except Exception as e:
        log_message(f"[Error] Failed to load pending proposals: {e}")
        return []

def save_pending_proposals(data):
    try:
        os.makedirs(PENDING_PROPOSALS.parent, exist_ok=True)
        with open(PENDING_PROPOSALS, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        log_message(f"Saved {len(data)} pending proposals.")
    except Exception as e:
        log_message(f"[Error] Failed to save pending proposals: {e}")

def run_git_cmd(args, cwd):
    try:
        res = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            log_message(f"[Git Error] Command failed: {' '.join(args)} - Stderr: {res.stderr}")
        return res.returncode == 0
    except Exception as e:
        log_message(f"[Git Error] Failed to execute {' '.join(args)}: {e}")
        return False

def promote_to_foundation_skills(rule):
    log_message(f"PROMOTING RULE: {rule['proposed_fix']}")
    
    # 1. Commit pre-edit changes in config repo if dirty
    run_git_cmd(["git", "add", "."], SKILLS_DIR.parent)
    run_git_cmd(["git", "commit", "-m", f"SELF-LEARN: Pre-promotion baseline for {rule['skill']}"], SKILLS_DIR.parent)
    
    if not FOUNDATION_SKILL_PATH.exists():
        log_message(f"[Error] Foundation SKILL.md not found at {FOUNDATION_SKILL_PATH}")
        return False
        
    try:
        with open(FOUNDATION_SKILL_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse existing rule IDs to find the next PR-XXX
        rule_ids = re.findall(r"\[PR-(\d+)\]", content)
        next_num = 1
        if rule_ids:
            next_num = max(int(rid) for rid in rule_ids) + 1
            
        pr_id = f"PR-{next_num:03d}"
        severity_upper = rule.get("severity", "MEDIUM").upper()
        category = rule.get("category", "general")
        rule_str = f"- **[{pr_id}]** (!! {severity_upper}) `{category}`: {rule['proposed_fix']}"
        
        log_message(f"Generated new rule: {rule_str}")
        
        # Locate the Learned Prevention Rules section and insert the rule right before '_Last updated:'
        # or at the end of the bulleted list under the header
        lines = content.splitlines()
        insert_idx = -1
        in_section = False
        
        for idx, line in enumerate(lines):
            if "## Learned Prevention Rules" in line:
                in_section = True
                continue
            if in_section:
                if "_Last updated:" in line:
                    insert_idx = idx
                    break
                    
        if insert_idx == -1:
            # Fallback to appending at the end of the file
            lines.append(rule_str)
            lines.append(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_")
        else:
            # Find the blank line or insertion spot before '_Last updated'
            # Look backwards from insert_idx to find the last rule line
            search_idx = insert_idx
            while search_idx > 0 and lines[search_idx - 1].strip() == "":
                search_idx -= 1
            lines.insert(search_idx, rule_str)
            
            # Update the last updated line
            for idx, line in enumerate(lines):
                if "_Last updated:" in line:
                    lines[idx] = f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_"
                    break

        # Write back updated skill content
        with open(FOUNDATION_SKILL_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
            
        log_message(f"Promoted rule {pr_id} to foundation SKILL.md successfully.")
        
        # 2. Run git commit for the skill edit
        run_git_cmd(["git", "add", "."], SKILLS_DIR.parent)
        run_git_cmd(["git", "commit", "-m", f"SELF-LEARN: {pr_id} - {rule['proposed_fix'][:50]}"], SKILLS_DIR.parent)
        return True
    except Exception as e:
        log_message(f"[Error] Failed to promote rule to foundation SKILL.md: {e}")
        return False

def query_gemini_learner(journal_entries, transcript_segment, pending_proposals):
    if not API_KEY:
        log_message("[Error] GEMINI_API_KEY is not configured.")
        return None
        
    client = genai.Client(api_key=API_KEY)
    
    # Format current pending proposals list for Gemini
    pending_formatted = []
    for idx, item in enumerate(pending_proposals):
        pending_formatted.append({
            "index": idx,
            "skill": item.get("skill"),
            "error": item.get("error"),
            "proposed_fix": item.get("proposed_fix"),
            "hits": item.get("hits", 1)
        })

    prompt = f"""You are the Keystone Sovereign Agent Fleet Self-Learning Daemon.
Your goal is to analyze the agent's recent correction journal and chat transcript to detect patterns of errors or corrections, and formulate new "Learned Prevention Rules" (format: [PR-XXX]) or identify "hits" (repeating occurrences) for existing pending proposals.

Here is the recent correction journal entries:
{json.dumps(journal_entries[-10:], indent=2)}

Here is the last 50 lines of the chat transcript log:
{transcript_segment}

And here is the current list of pending proposals:
{json.dumps(pending_formatted, indent=2)}

Please perform the analysis:
1. Examine the transcript and journal to find errors or manual corrections that occurred.
2. Formulate clear, actionable, and specific prevention rules (e.g., "ALWAYS bring DaVinci Resolve to the foreground...", "NEVER use angled brackets in YouTube descriptions...").
3. For each prevention rule, check if it matches (or is highly similar to) an existing proposal in the pending proposals list.
   - If yes, identify its index in the pending proposals list so we can increment its hits.
   - If no, list it as a new proposal. Specify the target skill folder (e.g. '00_keystone_foundation', 'keystone_davinci_timeline_assembly', etc.), category (e.g., 'orchestration', 'metadata', 'automation'), and severity ('low', 'medium', 'high', 'critical').

Your output must be a single, raw JSON object matching this schema:
{{
  "new_proposals": [
    {{
      "skill": "skill_folder_name",
      "error": "Description of the error",
      "proposed_fix": "Text of the proposed rule",
      "severity": "low|medium|high|critical",
      "category": "category_name"
    }}
  ],
  "matching_proposal_indices": [
    {{
      "index": 0,
      "error": "New instance of this error observed in transcript or journal"
    }}
  ]
}}

Return ONLY the raw JSON object. Do not wrap it in ```json ... ``` or include any explanation outside the JSON.
"""

    try:
        log_message("Querying Gemini-2.5-flash for learning insights...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )
        text = response.text.strip()
        
        # Clean up code blocks if present
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n", "", text)
            text = re.sub(r"\n```$", "", text)
            text = text.strip()
            
        return json.loads(text)
    except Exception as e:
        log_message(f"[Error] Gemini querying/parsing failed: {e}")
        return None

def main():
    log_message("=== STARTING SELF-LEARNING CYCLE ===")
    
    # Load inputs
    journal = load_correction_journal()
    transcript_path = get_transcript_path()
    transcript_segment = read_last_transcript_lines(transcript_path, 50)
    pending_proposals = load_pending_proposals()
    
    if not journal and not transcript_segment:
        log_message("[Error] No correction journal or transcript available to learn from.")
        return
        
    # Query Gemini
    result = query_gemini_learner(journal, transcript_segment, pending_proposals)
    if not result:
        log_message("[Error] Failed to get valid learning results from Gemini.")
        return
        
    log_message(f"Gemini response parsed successfully.")
    log_message(f"New proposals identified: {len(result.get('new_proposals', []))}")
    log_message(f"Matching existing proposal hits: {len(result.get('matching_proposal_indices', []))}")
    
    promoted_any = False
    
    # 1. Update hits for matching proposals
    for match in result.get("matching_proposal_indices", []):
        idx = match.get("index")
        if idx is not None and 0 <= idx < len(pending_proposals):
            prop = pending_proposals[idx]
            prop["hits"] = prop.get("hits", 1) + 1
            prop["last_hit_timestamp"] = datetime.utcnow().isoformat() + "Z"
            log_message(f"Hit incremented for proposal at index {idx}: '{prop['proposed_fix']}' -> hits: {prop['hits']}")
            
            # Check if promotion threshold (3 hits) is met
            if prop["hits"] >= 3 and prop.get("status") == "pending_review":
                success = promote_to_foundation_skills(prop)
                if success:
                    prop["status"] = "promoted"
                    promoted_any = True
                    
    # 2. Add new proposals
    for new_p in result.get("new_proposals", []):
        # Avoid duplicate additions to pending
        duplicate = False
        for existing in pending_proposals:
            if existing.get("proposed_fix").lower().strip() == new_p.get("proposed_fix").lower().strip():
                duplicate = True
                existing["hits"] = existing.get("hits", 1) + 1
                log_message(f"Duplicate proposal found. Incremented hits: '{new_p['proposed_fix']}' -> hits: {existing['hits']}")
                if existing["hits"] >= 3 and existing.get("status") == "pending_review":
                    success = promote_to_foundation_skills(existing)
                    if success:
                        existing["status"] = "promoted"
                        promoted_any = True
                break
                
        if not duplicate:
            new_p["hits"] = 1
            new_p["timestamp"] = datetime.utcnow().isoformat() + "Z"
            new_p["status"] = "pending_review"
            pending_proposals.append(new_p)
            log_message(f"Added new pending proposal: '{new_p['proposed_fix']}'")
            
    # Save the updated pending proposals
    save_pending_proposals(pending_proposals)
    log_message("=== SELF-LEARNING CYCLE COMPLETE ===")

if __name__ == "__main__":
    main()
