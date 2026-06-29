import os
import sys
import glob
import json
import urllib.request
import datetime
import argparse

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma2"

def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    """Queries local Ollama instance."""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data.get("response", "")
    except Exception as e:
        print(f"Error querying Ollama: {e}", file=sys.stderr)
        return ""

def distill_logs(log_contents: str) -> dict:
    """Distills raw log contents into lessons, priorities, and decisions using local Ollama."""
    prompt = f"""You are the Keystone Sovereign Memory Heartbeat. Distill these raw chronological agent logs into:
1. Active Priorities (under 5 items)
2. Recent Lessons Learned (brief, actionable statements)
3. Key Decisions Made (concrete choices)

Raw Logs:
---
{log_contents}
---

Output your distillation in valid JSON format ONLY with this schema:
{{
  "priorities": ["priority 1", "priority 2"],
  "lessons": ["lesson 1", "lesson 2"],
  "decisions": ["decision 1", "decision 2"]
}}
Do NOT output any markdown blocks or conversational text, only the JSON object.
"""
    response_text = query_ollama(prompt)
    if not response_text:
        return {}
    
    try:
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"Failed to parse JSON response from Ollama: {e}", file=sys.stderr)
        print(f"Response was: {response_text}", file=sys.stderr)
        return {}

def update_state_file(state_path: str, distilled: dict, max_chars: int = 10000):
    """Updates STATE.md with new distilled insights while respecting the character ceiling."""
    if not os.path.exists(state_path):
        current_content = "# Active State\n\n## Current Priorities\n- [ ] None\n\n## Recent Lessons\n- None\n"
    else:
        with open(state_path, "r", encoding="utf-8") as f:
            current_content = f.read()

    new_priorities = distilled.get("priorities", [])
    new_lessons = distilled.get("lessons", [])
    
    now_str = datetime.datetime.utcnow().isoformat() + "Z"
    
    priorities_list = ""
    for p in new_priorities:
        priorities_list += f"- [ ] {p}\n"
        
    lessons_list = ""
    for l in new_lessons:
        lessons_list += f"- {l}\n"
        
    updated_content = f"""# Active State (Auto-managed by heartbeat — last updated: {now_str})

## Current Priorities
{priorities_list if priorities_list else "- [ ] Configure Meta System User tokens\n- [ ] Test Graphthulhu vault traversal\n"}
## Recent Lessons
{lessons_list if lessons_list else "- No new lessons recorded\n"}
"""
    if len(updated_content) > max_chars:
        updated_content = updated_content[:max_chars]
        
    with open(state_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print(f"Updated STATE.md (size: {len(updated_content)} chars)")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run a test compaction with mock logs")
    args = parser.parse_args()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    memory_dir = os.path.join(base_dir, "memory")
    state_path = os.path.join(base_dir, "STATE.md")
    
    os.makedirs(memory_dir, exist_ok=True)
    
    if args.test:
        print("Running test memory compaction...")
        mock_log = """
[2026-06-14T03:05:00] INFO: Successfully deployed n8n Docker containers inside WSL2.
[2026-06-14T03:10:00] ERROR: Facebook posting failed because Meta access token was expired. Need system user never-expire token.
[2026-06-14T03:15:00] INFO: Tested Graphthulhu command-line tool, works with read-only /vault mount.
"""
        test_file = os.path.join(memory_dir, "test_log.md")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(mock_log)
            
    log_files = glob.glob(os.path.join(memory_dir, "*.md"))
    if not log_files:
        print("No log files found in memory/ directory.")
        return
        
    combined_logs = ""
    for lf in log_files:
        if os.path.basename(lf) == "archive":
            continue
        with open(lf, "r", encoding="utf-8") as f:
            combined_logs += f"\nFile: {os.path.basename(lf)}\n" + f.read() + "\n"
            
    print(f"Found {len(log_files)} log files. Distilling...")
    
    distilled = distill_logs(combined_logs)
    if not distilled:
        print("Ollama distillation returned empty, using fallback heuristic parser...")
        priorities = []
        lessons = []
        for line in combined_logs.split("\n"):
            if "ERROR" in line or "failed" in line.lower():
                lessons.append(line.strip())
            elif "priorit" in line.lower() or "todo" in line.lower():
                priorities.append(line.strip())
        distilled = {
            "priorities": priorities[:3],
            "lessons": lessons[:3]
        }
        
    update_state_file(state_path, distilled)
    
    archive_dir = os.path.join(memory_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)
    for lf in log_files:
        dest = os.path.join(archive_dir, os.path.basename(lf))
        if os.path.exists(dest):
            os.remove(dest)
        os.rename(lf, dest)
        
    print("Memory compaction completed successfully.")

if __name__ == "__main__":
    main()
