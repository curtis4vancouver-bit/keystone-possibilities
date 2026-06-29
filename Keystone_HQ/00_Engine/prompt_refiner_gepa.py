import os
import sys
import json
import datetime
import math
from typing import List, Dict, Any, Tuple
from google import genai

# Force UTF-8 output on Windows to handle emojis in logs and print statements
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Set the service account credentials path for Vertex AI authentication
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
key_path = os.path.join(PROJECT_ROOT, "scratch", "gcs_key.json")
if os.path.exists(key_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# Initialize Google GenAI client configured for Vertex AI
try:
    client = genai.Client(vertexai=True, project="semiotic-ion-458504-e9", location="us-central1")
except Exception as e:
    client = None
    print(f"[GEPA] Warning: Failed to initialize Google GenAI Client: {e}")

LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
CORRECTION_JOURNAL = os.path.join(LEARNINGS_DIR, "correction_journal.json")
SYSTEM_PROMPT_PATH = os.path.join(PROJECT_ROOT, "00_CHRONOS_MASTER_SYSTEM_PROMPT.md")
EVOLVED_PROMPT_OUTPUT = os.path.join(LEARNINGS_DIR, "evolved_system_prompts.json")

def load_journal() -> List[Dict[str, Any]]:
    if not os.path.exists(CORRECTION_JOURNAL):
        return []
    try:
        with open(CORRECTION_JOURNAL, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("entries", [])
    except Exception:
        return []

def load_system_prompt() -> str:
    if not os.path.exists(SYSTEM_PROMPT_PATH):
        return ""
    try:
        with open(SYSTEM_PROMPT_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

def save_system_prompt(content: str):
    try:
        with open(SYSTEM_PROMPT_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[GEPA] Evolved system prompt written to {SYSTEM_PROMPT_PATH}")
    except Exception as e:
        print(f"[GEPA] Failed to write system prompt: {e}")

def get_failed_traces(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Filter entries that represent errors (success=False or has failed outcomes)
    return [e for e in entries if not e.get("success", False)]

def propose_mutations(base_prompt: str, failed_traces: List[Dict[str, Any]]) -> List[str]:
    """Uses Gemini to reflect on failures and propose mutated system prompts."""
    if client is None:
        print("[GEPA] Client offline. Cannot propose mutations.")
        return []
    
    traces_str = ""
    for idx, trace in enumerate(failed_traces[:5]):
        traces_str += f"--- Failure {idx+1} ---\n"
        traces_str += f"Error Type: {trace.get('error_type')}\n"
        traces_str += f"Context: {trace.get('original_context')}\n"
        traces_str += f"Fix Applied: {trace.get('fix_description')}\n\n"

    prompt = f"""
You are the GEPA (Generalized Prompt Evolution) engine for a sovereign AI fleet.
Your task is to review the current base system prompt and a set of failed execution traces,
and propose 3 distinct mutated versions of the system prompt to prevent these failures.

The mutated versions should try to achieve different points of optimization:
1. Candidate 1 (Detailed & Rule-Oriented): Focuses on adding explicit prevention rules for the failures.
2. Candidate 2 (Brevity & Focus-Oriented): Focuses on condensing the prompt to save token count while preserving instructions.
3. Candidate 3 (Hybrid & Multi-Tenant): Focuses on optimizing the multi-brand partitioning and safety.

Current Base Prompt:
\"\"\"
{base_prompt}
\"\"\"

Failed Traces:
{traces_str}

Format your output exactly as a JSON object with a 'candidates' list:
{{
  "candidates": [
     "candidate 1 prompt text...",
     "candidate 2 prompt text...",
     "candidate 3 prompt text..."
  ]
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        data = json.loads(text)
        return data.get("candidates", [])
    except Exception as e:
        print(f"[GEPA] Error proposing mutations: {e}")
        return []

def evaluate_candidate(candidate: str, failed_traces: List[Dict[str, Any]], base_prompt: str) -> Tuple[float, int]:
    """Evaluates candidate prompt for accuracy (preventing traces) and token count (brevity)."""
    length = len(candidate)
    
    if not candidate or client is None:
        return 0.0, 999999
    
    traces_str = ""
    for idx, trace in enumerate(failed_traces[:5]):
        traces_str += f"--- Failure {idx+1} ---\n"
        traces_str += f"Error Type: {trace.get('error_type')}\n"
        traces_str += f"Context: {trace.get('original_context')}\n"
        traces_str += f"Fix Applied: {trace.get('fix_description')}\n\n"
        
    prompt = f"""
You are an accuracy critic evaluating a proposed system prompt mutation against historical failure traces.
Review the proposed prompt and determine how many of the historical failures it would successfully prevent.

Proposed Prompt:
\"\"\"
{candidate}
\"\"\"

Failure Traces:
{traces_str}

Evaluate each of the failure traces. Output a score from 0.0 to 1.0 (where 1.0 means it prevents all 5 failures, 0.0 means none).

Return your response strictly in JSON:
{{
  "prevented_count": 3,
  "accuracy_score": 0.6
}}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        res = json.loads(text)
        return float(res.get("accuracy_score", 0.5)), length
    except Exception:
        return 0.5, length

def pareto_frontier(candidates_scores: List[Tuple[str, float, int]]) -> List[Tuple[str, float, int]]:
    """Calculates the Pareto frontier: non-dominated candidates."""
    frontier = []
    for c, acc, length in candidates_scores:
        dominated = False
        for other_c, other_acc, other_length in candidates_scores:
            if other_c == c:
                continue
            if (other_acc >= acc and other_length <= length) and (other_acc > acc or other_length < length):
                dominated = True
                break
        if not dominated:
            frontier.append((c, acc, length))
    return frontier

def run_gepa_evolution():
    print("[GEPA] Starting Prompt Evolution Cycle...")
    journal = load_journal()
    failed_traces = get_failed_traces(journal)
    
    if not failed_traces:
        print("[GEPA] No failed traces found in journal. Prompt is currently optimal.")
        return
        
    base_prompt = load_system_prompt()
    if not base_prompt:
        print("[GEPA] Base system prompt not found at path.")
        return
        
    print(f"[GEPA] Found {len(failed_traces)} failure traces. Proposing mutations...")
    candidates = propose_mutations(base_prompt, failed_traces)
    
    if not candidates:
        print("[GEPA] No mutation candidates generated.")
        return
        
    # Include base prompt in evaluation pool
    pool = [(base_prompt, "base")] + [(c, f"candidate_{idx+1}") for idx, c in enumerate(candidates)]
    
    scored_pool = []
    for prompt_text, name in pool:
        print(f"[GEPA] Evaluating {name}...")
        acc, length = evaluate_candidate(prompt_text, failed_traces, base_prompt)
        scored_pool.append((prompt_text, acc, length, name))
        print(f"  - Accuracy: {acc:.2f} | Length: {length} chars")
        
    # Calculate Pareto frontier
    frontier = pareto_frontier([(pt, acc, length) for pt, acc, length, name in scored_pool])
    print(f"\n[GEPA] Pareto Frontier contains {len(frontier)} non-dominated candidate(s):")
    
    best_prompt = None
    best_acc = -1.0
    best_len = 9999999
    
    for pt, acc, length in frontier:
        print(f"  - Accuracy: {acc:.2f} | Length: {length} chars")
        if acc > best_acc or (acc == best_acc and length < best_len):
            best_prompt = pt
            best_acc = acc
            best_len = length
            
    base_acc, base_len = scored_pool[0][1], scored_pool[0][2]
    print(f"\n[GEPA] Base Accuracy: {base_acc:.2f} (len: {base_len}) | Best Frontier Accuracy: {best_acc:.2f} (len: {best_len})")
    
    if best_prompt and (best_acc > base_acc or (best_acc == base_acc and best_len < base_len)):
        print("[GEPA] Found an improved evolved prompt! Saving...")
        save_system_prompt(best_prompt)
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "previous_length": base_len,
            "new_length": best_len,
            "previous_accuracy": base_acc,
            "new_accuracy": best_acc,
            "evolved": True
        }
        with open(EVOLVED_PROMPT_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
    else:
        print("[GEPA] Base prompt remains on the Pareto frontier. No mutation applied.")

if __name__ == "__main__":
    run_gepa_evolution()
