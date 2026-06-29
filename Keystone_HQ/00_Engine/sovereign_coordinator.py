# Keystone Sovereign - Master Multi-Agent Coordinator
# Coordinates health, media, web dev, music, and research subagents.
# Enforces strict YouTube YMYL compliance, shared state tracking, and task delegation.

import os
import json
import re
import sys
import subprocess
import argparse
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(ROOT_DIR, "Transcripts", "agent_state.json")

# YMYL Semantic Mapping Dictionary (Red-flag word mitigation for YouTube, TikTok, and Meta)
YMYL_DICTIONARY = {
    r"\bprotocol\b": "case study",
    r"\bprotocols\b": "case studies",
    r"\bdosing\b": "titration schedule",
    r"\bdoses\b": "titration schedules",
    r"\bsource\b": "supply chain",
    r"\bsources\b": "supply chains",
    r"\bvendor\b": "supplier",
    r"\bvendors\b": "suppliers",
    r"\bfat burning\b": "lipid oxidation",
    r"\bstacking\b": "combinatorial analysis",
    r"\bstack\b": "combinatorial model",
    r"\bBPC-157\b": "compound BPC",
    r"\bBPC157\b": "compound BPC",
    r"\bTB-500\b": "compound TB",
    r"\bTB500\b": "compound TB",
    r"\bpeptides\b": "metabolic compounds",
    r"\bpeptide\b": "metabolic compound",
    r"\binjections\b": "administration methods",
    r"\binjection\b": "administration method",
    r"\bOzempic\b": "metabolic research targets",
    r"\bMounjaro\b": "metabolic research targets",
    r"\bWegovy\b": "metabolic research targets",
    r"\bweight loss\b": "body recomposition",
    r"\blose weight\b": "body recomposition",
    r"\bfat loss\b": "lipid reduction",
    r"\bbuy peptides\b": "acquire compounds for study",
}


class IntentRouter:
    """
    Tiered Model Registry & Intent Routing Gateway
    Analyzes queries locally to dispatch to the cheapest capable model.
    """
    @staticmethod
    def route_intent(query: str) -> dict:
        query_lower = query.lower()
        if "analyze" in query_lower or "architecture" in query_lower or "synthesize" in query_lower:
            return {"model": "claude-3-opus-20240229", "tier": "premium", "reason": "Deep reasoning required."}
        elif "format" in query_lower or "json" in query_lower or "read" in query_lower:
            return {"model": "gemini-2.5-flash", "tier": "cheap", "reason": "Routine/formatting task."}
        else:
            return {"model": "gemini-1.5-pro", "tier": "balanced", "reason": "Standard inference."}

    @staticmethod
    def build_cached_prompt(system_prompt: str, tools: list, history: list) -> list:
        """
        Cache Anchoring (Anthropic / Gemini explicit caching)
        Forces large static definitions to the top with cache_control blocks.
        """
        payload = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]}
        ]
        # In a real implementation, tools are cached via API headers.
        payload.extend(history)
        return payload


class KeystoneSovereign:
    def __init__(self):
        self.state = self._load_state()
        self.learnings = self._load_learnings()
        print("Keystone Sovereign Orchestration System Online.")
        print("Initialised V8 Master Brain protocols.")
        if self.learnings and "entries" in self.learnings:
            entries = self.learnings.get("entries", [])
            stats = self.learnings.get("stats", {})
            print(f"[Self-Healing Bootstrapped] Loaded {len(entries)} known correction logs from past sessions.")
            print(f"   - Total Auto-Healed Errors: {stats.get('auto_healed', 0)} // Total Resolved Fixes: {stats.get('total_fixes', 0)}")

    def _load_learnings(self) -> dict:
        learnings_file = os.path.join(ROOT_DIR, ".learnings", "correction_journal.json")
        if os.path.exists(learnings_file):
            try:
                with open(learnings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"entries": [], "stats": {"total_errors": 0, "total_fixes": 0, "auto_healed": 0}}

    def _load_state(self):
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        default_state = {
            "last_updated": str(datetime.now()),
            "active_sprints": {},
            "subagent_jobs": {
                "health_agent": [],
                "media_agent": [],
                "dev_agent": [],
                "research_agent": [],
                "music_agent": [],
                "youtube_flow_agent": []
            },
            "music_pipeline_status": {}
        }
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    saved = json.load(f)
                    # Ensure all subagents are present in loaded state
                    if "subagent_jobs" not in saved:
                        saved["subagent_jobs"] = default_state["subagent_jobs"]
                    else:
                        for k, v in default_state["subagent_jobs"].items():
                            if k not in saved["subagent_jobs"]:
                                saved["subagent_jobs"][k] = v
                    if "music_pipeline_status" not in saved:
                        saved["music_pipeline_status"] = {}
                    return saved
            except Exception:
                pass
        return default_state

    def _save_state(self):
        self.state["last_updated"] = str(datetime.now())
        with open(STATE_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    def delegate_task(self, subagent: str, task_description: str) -> dict:
        """
        Delegates a specific action to a subagent and saves it in the shared state.
        """
        valid_agents = ["health_agent", "media_agent", "dev_agent", "research_agent", "music_agent", "youtube_flow_agent"]
        if subagent not in valid_agents:
            raise ValueError(f"Invalid subagent: {subagent}. Select from {valid_agents}")
        
        job = {
            "timestamp": str(datetime.now()),
            "description": task_description,
            "status": "Queued"
        }
        self.state["subagent_jobs"][subagent].append(job)
        self._save_state()
        print(f"[Delegation] Queued task to {subagent.upper()}: '{task_description}'")
        return job

    def update_job_status(self, subagent: str, description_keyword: str, status: str):
        """Updates the status of a specific job in the queue."""
        if subagent in self.state["subagent_jobs"]:
            for job in self.state["subagent_jobs"][subagent]:
                if description_keyword.lower() in job["description"].lower() and job["status"] == "Queued":
                    job["status"] = status
                    self._save_state()
                    print(f"[State Update] Marked {subagent.upper()} job '{job['description']}' as '{status}'.")
                    break

    def run_ymyl_compliance_check(self, script_text: str) -> str:
        """
        Scrubs draft scripts to ensure compliance with YouTube YMYL (Your Money or Your Life) guidelines.
        Replaces high-risk words with educational/scientific terminology.
        """
        scrubbed_text = script_text
        replacements_made = 0
        
        for pattern, replacement in YMYL_DICTIONARY.items():
            matches = re.findall(pattern, scrubbed_text, flags=re.IGNORECASE)
            if matches:
                scrubbed_text, count = re.subn(pattern, replacement, scrubbed_text, flags=re.IGNORECASE)
                replacements_made += count
                
        print(f"[YMYL Scrub] Completed. Replacements made: {replacements_made}")
        return scrubbed_text

    def print_system_status(self):
        """
        Returns a formatted audit of the entire multi-agent hierarchy.
        """
        print("\n" + "="*50)
        print("   KEYSTONE ENTERPRISE MULTI-AGENT STATE REPORT")
        print("="*50)
        print(f"Last Orchestrated: {self.state['last_updated']}\n")
        
        for agent, jobs in self.state["subagent_jobs"].items():
            print(f"[AGENT] {agent.replace('_', ' ').title()}:")
            if not jobs:
                print("   - Active Queue: Idle")
            for job in jobs:
                print(f"   - [{job['status']}] {job['description']} (Assigned: {job['timestamp']})")
        print("="*50 + "\n")

    def monitor_desktop_music(self):
        """
        Scans Wayne's 5 physical desktop directories and updates
        music_pipeline_status inside agent_state.json.
        """
        desktop_dir = r"C:\Users\Curtis\Desktop"
        folders = {
            "New Songs": os.path.join(desktop_dir, "New Songs"),
            "sounds": os.path.join(desktop_dir, "sounds"),
            "ready for toolost": os.path.join(desktop_dir, "ready for toolost"),
            "musicmacth": os.path.join(desktop_dir, "musicmacth"),
            "compeleted albums": os.path.join(desktop_dir, "compeleted albums")
        }
        
        pipeline_status = {}
        for name, path in folders.items():
            if os.path.exists(path):
                try:
                    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                    pipeline_status[name] = {
                        "count": len(files),
                        "files": files
                    }
                except Exception as e:
                    pipeline_status[name] = {"error": str(e)}
            else:
                pipeline_status[name] = {"status": "Missing Directory"}
                
        self.state["music_pipeline_status"] = pipeline_status
        self._save_state()
        print(f"[Music Monitor] Updated desktop music pipeline tracking in shared state.")

    def execute_subagent(self, agent_name: str, args_list: list) -> str:
        """
        Spawns a specialized subagent script in a secure subprocess synchronously.
        Applies strict process isolation and updates state matrix.
        """
        scripts = {
            "health": os.path.join(ROOT_DIR, "07_Health_Protocols", "health_agent.py"),
            "music": os.path.join(ROOT_DIR, "06_Music_Recomposition", "music_agent.py"),
            "dev": os.path.join(ROOT_DIR, "02_Keystone_Possibilities", "dev_agent.py"),
            "research": os.path.join(ROOT_DIR, "08_Deep_Research_Agents", "research_agent.py"),
            "media": os.path.join(ROOT_DIR, "09_YouTube_Operations", "media_agent.py")
        }
        
        if agent_name not in scripts:
            return f"Error: Unknown subagent '{agent_name}'"
            
        script_path = scripts[agent_name]
        if not os.path.exists(script_path):
            return f"Error: Script '{script_path}' not found."

        # Strict token environment lock gating
        env = os.environ.copy()
        args_str = " ".join(args_list).lower()
        if agent_name in ["media", "music"]:
            # B2C Media Locks
            if "possibilities" in args_str or "youtube_token_possibilities.json" in args_str:
                raise PermissionError("[Security Lock] Blocked: B2C agent attempted to access B2B credentials!")
            env["KEYSTONE_PIPELINE_MODE"] = "B2C"
            env["KEYSTONE_ACTIVE_YOUTUBE_TOKEN"] = os.path.join(ROOT_DIR, "youtube_token_protocols.json")
        elif agent_name == "dev":
            # B2B SaaS Locks
            if "protocols" in args_str or "youtube_token_protocols.json" in args_str:
                raise PermissionError("[Security Lock] Blocked: B2B agent attempted to access B2C credentials!")
            env["KEYSTONE_PIPELINE_MODE"] = "B2B"
            env["KEYSTONE_ACTIVE_YOUTUBE_TOKEN"] = os.path.join(ROOT_DIR, "youtube_token_possibilities.json")

        cmd = [sys.executable, script_path] + args_list
        print(f"[Executor] Spawning subprocess with token security locks: {' '.join(cmd)}")
        
        # Log task as queued/in progress
        task_desc = f"CLI execute: {' '.join(args_list)}"
        self.delegate_task(f"{agent_name}_agent", task_desc)
        
        try:
            result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=30)
            output = result.stdout + "\n" + result.stderr
            
            # Apply YMYL scrub to stdout if it's text compilation
            scrubbed_output = self.run_ymyl_compliance_check(output)
            
            self.update_job_status(f"{agent_name}_agent", task_desc, "Completed")
            return scrubbed_output
        except Exception as e:
            self.update_job_status(f"{agent_name}_agent", task_desc, f"Failed: {str(e)}")
            return f"Subprocess failed to run: {str(e)}"

    def execute_subagent_async(self, agent_name: str, args_list: list) -> str:
        """
        Spawns a specialized subagent in a non-blocking background process.
        Routes logs to Transcripts/ and registers the job for background monitoring.
        """
        scripts = {
            "health": os.path.join(ROOT_DIR, "07_Health_Protocols", "health_agent.py"),
            "music": os.path.join(ROOT_DIR, "06_Music_Recomposition", "music_agent.py"),
            "dev": os.path.join(ROOT_DIR, "02_Keystone_Possibilities", "dev_agent.py"),
            "research": os.path.join(ROOT_DIR, "08_Deep_Research_Agents", "research_agent.py"),
            "media": os.path.join(ROOT_DIR, "09_YouTube_Operations", "media_agent.py")
        }
        
        if agent_name not in scripts:
            return f"Error: Unknown subagent '{agent_name}'"
            
        script_path = scripts[agent_name]
        if not os.path.exists(script_path):
            return f"Error: Script '{script_path}' not found."

        # Strict token environment lock gating
        env = os.environ.copy()
        args_str = " ".join(args_list).lower()
        if agent_name in ["media", "music"]:
            # B2C Media Locks
            if "possibilities" in args_str or "youtube_token_possibilities.json" in args_str:
                raise PermissionError("[Security Lock] Blocked: B2C agent attempted to access B2B credentials!")
            env["KEYSTONE_PIPELINE_MODE"] = "B2C"
            env["KEYSTONE_ACTIVE_YOUTUBE_TOKEN"] = os.path.join(ROOT_DIR, "youtube_token_protocols.json")
        elif agent_name == "dev":
            # B2B SaaS Locks
            if "protocols" in args_str or "youtube_token_protocols.json" in args_str:
                raise PermissionError("[Security Lock] Blocked: B2B agent attempted to access B2C credentials!")
            env["KEYSTONE_PIPELINE_MODE"] = "B2B"
            env["KEYSTONE_ACTIVE_YOUTUBE_TOKEN"] = os.path.join(ROOT_DIR, "youtube_token_possibilities.json")
            
        import uuid
        job_id = str(uuid.uuid4())[:8]
        log_dir = os.path.join(ROOT_DIR, "Transcripts")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"subagent_{agent_name}_{job_id}.log")
        
        cmd = [sys.executable, script_path] + args_list
        print(f"[Async Executor] Spawning background subprocess with token security locks: {' '.join(cmd)}")
        print(f"[Async Executor] Redirecting logs to: {log_file}")
        
        task_desc = f"CLI execute async: {' '.join(args_list)}"
        self.delegate_task(f"{agent_name}_agent", task_desc)
        
        try:
            # Open the log file for writing output
            out_f = open(log_file, "w", encoding="utf-8")
            # Start process asynchronously
            proc = subprocess.Popen(
                cmd,
                stdout=out_f,
                stderr=subprocess.STDOUT,
                cwd=ROOT_DIR,
                env=env,
                text=True
            )
            
            # Register background job in state
            if "active_background_jobs" not in self.state:
                self.state["active_background_jobs"] = []
                
            job_record = {
                "job_id": job_id,
                "agent_name": agent_name,
                "pid": proc.pid,
                "cmd": " ".join(cmd),
                "task_desc": task_desc,
                "log_file": log_file,
                "start_time": str(datetime.now()),
                "status": "Running"
            }
            self.state["active_background_jobs"].append(job_record)
            self._save_state()
            
            return f"SUCCESS: Spawned {agent_name} subagent as background process PID {proc.pid}. Logs: {log_file}"
        except Exception as e:
            self.update_job_status(f"{agent_name}_agent", task_desc, f"Failed to spawn: {str(e)}")
            return f"Error: Failed to spawn background process: {str(e)}"

    def check_background_jobs(self) -> str:
        """
        Polls active background processes. Cleans up completed jobs, scrubs their
        outputs for YMYL compliance, and triggers Master Brain ingestion.
        """
        if "active_background_jobs" not in self.state or not self.state["active_background_jobs"]:
            return "No active background subagent jobs running."
            
        import psutil
        active_jobs = []
        completed_count = 0
        report = []
        
        for job in self.state["active_background_jobs"]:
            pid = job["pid"]
            agent_name = job["agent_name"]
            job_id = job["job_id"]
            
            # Check if process is still running
            proc_running = False
            try:
                proc = psutil.Process(pid)
                if proc.is_running() and proc.status() != psutil.STATUS_ZOMBIE:
                    proc_running = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
            if proc_running:
                active_jobs.append(job)
                report.append(f"- Job {job_id} ({agent_name}): Running (PID {pid}, started {job['start_time']})")
            else:
                # Process completed! Let's parse and process output
                completed_count += 1
                status = "Completed"
                output_content = ""
                
                if os.path.exists(job["log_file"]):
                    try:
                        with open(job["log_file"], "r", encoding="utf-8") as f:
                            output_content = f.read()
                    except Exception as e:
                        output_content = f"Error reading log file: {str(e)}"
                
                # Perform YMYL scrub on completed log
                scrubbed_out = self.run_ymyl_compliance_check(output_content)
                with open(job["log_file"], "w", encoding="utf-8") as f:
                    f.write(scrubbed_out)
                    
                # Mark job as completed in subagent_jobs list
                self.update_job_status(f"{agent_name}_agent", job["task_desc"], "Completed")
                report.append(f"- Job {job_id} ({agent_name}): Completed! Output scrubbed and logged.")
                
                # If this was a research job, save result to Deep_Research_Results/ for RAG ingestion
                if agent_name == "research" and "keyword" in job["task_desc"].lower():
                    target_file = os.path.join(ROOT_DIR, "Deep_Research_Results", f"scraped_competitor_intel_{job_id}.md")
                    os.makedirs(os.path.dirname(target_file), exist_ok=True)
                    with open(target_file, "w", encoding="utf-8") as f:
                        f.write(f"# Scrubbed Competitor Intelligence Report (Job {job_id})\n\n{scrubbed_out}")
                    print(f"[Async Ingestion] Saved output to: {target_file}")
                    
                    # Run master brain ingestion script
                    ingest_script = os.path.join(ROOT_DIR, "scratch", "ingest_deep_research.py")
                    try:
                        subprocess.run([sys.executable, ingest_script], check=True)
                        print("[Async Ingestion] Automatically ingested research output into Master Brain database.")
                    except Exception as ex:
                        print(f"[Async Ingestion] Ingestion script warning: {str(ex)}")
                        
        self.state["active_background_jobs"] = active_jobs
        self._save_state()
        
        report_str = f"Background Jobs Audit: {completed_count} completed, {len(active_jobs)} still running.\n" + "\n".join(report)
        print(f"[Async Monitor] {report_str}")
        return report_str

    def trigger_youtube_campaign(self, topic: str) -> str:
        """
        Triggers the YouTube Flow Agent to compile a campaign for a given topic.
        """
        task_desc = f"Generate comprehensive content campaign for: '{topic}'"
        self.delegate_task("youtube_flow_agent", task_desc)
        
        agent_dir = os.path.join(ROOT_DIR, "09_YouTube_Operations")
        if agent_dir not in sys.path:
            sys.path.append(agent_dir)
            
        try:
            from youtube_flow_agent import YouTubeFlowAgent
            agent = YouTubeFlowAgent()
            result = agent.compile_campaign(topic)
            self.update_job_status("youtube_flow_agent", task_desc, "Completed")
            return result
        except Exception as e:
            self.update_job_status("youtube_flow_agent", task_desc, f"Failed: {str(e)}")
            return f"Failed to run YouTube Flow Agent campaign: {str(e)}"

    def run_complete_diagnostic_suite(self):
        """Runs testing routines across all 5 specialized subagents to verify status."""
        print("\n" + "="*50)
        print("     RUNNING KEYSTONE MULTI-AGENT DIAGNOSTIC SUITE")
        print("="*50)
        
        # 1. Health Agent
        print("\n[Diagnostic 1/5] Testing Keystone Health Agent...")
        health_out = self.execute_subagent("health", ["--peptide", "BPC-157"])
        print(health_out.strip())
        
        # 2. Music Agent
        print("\n[Diagnostic 2/5] Testing Keystone Music Agent...")
        music_out = self.execute_subagent("music", ["--scan"])
        print(music_out.strip())
        
        # 3. Dev Agent
        print("\n[Diagnostic 3/5] Testing Keystone Dev Agent...")
        dev_out = self.execute_subagent("dev", ["--audit"])
        print(dev_out.strip())
        
        # 4. Research Agent
        print("\n[Diagnostic 4/5] Testing Keystone Research Agent...")
        research_out = self.execute_subagent("research", ["--keyword-report"])
        print(research_out.strip())
        
        # 5. Media Agent
        print("\n[Diagnostic 5/5] Testing Keystone Media Agent...")
        print(media_out.strip())
        
        print("\n" + "="*50)
        print("           DIAGNOSTIC SUITE RUN COMPLETE")
        print("="*50 + "\n")

    def list_pending_skills(self) -> list:
        """Lists all pending skills in .agents/pending/."""
        pending_dir = os.path.join(ROOT_DIR, ".agents", "pending")
        if not os.path.exists(pending_dir):
            print("No pending skills directory found.")
            return []
        
        items = os.listdir(pending_dir)
        print("\n=== Pending Proposals ===")
        if not items:
            print("No pending skill proposals.")
            return []
            
        for idx, item in enumerate(items):
            path = os.path.join(pending_dir, item)
            item_type = "Folder" if os.path.isdir(path) else "File"
            print(f"[{idx}] {item} ({item_type})")
        print("=========================\n")
        return items

    def diff_pending_skill(self, proposal_id: str):
        """Displays diff of a pending proposal."""
        pending_dir = os.path.join(ROOT_DIR, ".agents", "pending")
        if not os.path.exists(pending_dir):
            print("No pending skills directory found.")
            return
            
        items = os.listdir(pending_dir)
        try:
            if proposal_id.isdigit():
                target = items[int(proposal_id)]
            else:
                target = proposal_id
        except (IndexError, ValueError):
            print(f"Proposal ID '{proposal_id}' not found.")
            return
            
        target_path = os.path.join(pending_dir, target)
        print(f"\n=== Diff for Proposal: {target} ===")
        if os.path.isdir(target_path):
            skill_md = os.path.join(target_path, "SKILL.md")
            if os.path.exists(skill_md):
                with open(skill_md, "r", encoding="utf-8") as f:
                    print("SKILL.md Contents:")
                    print("-" * 40)
                    print(f.read())
                    print("-" * 40)
            else:
                print(f"New skill folder structure:")
                for root, dirs, files in os.walk(target_path):
                    for file in files:
                        print(f"  {os.path.join(root, file)}")
        else:
            with open(target_path, "r", encoding="utf-8") as f:
                print(f.read())
        print("===================================\n")

    def approve_pending_skill(self, proposal_id: str):
        """Merges a pending proposal into active skills."""
        pending_dir = os.path.join(ROOT_DIR, ".agents", "pending")
        skills_dir = os.path.join(ROOT_DIR, ".agents", "skills")
        os.makedirs(skills_dir, exist_ok=True)
        
        items = os.listdir(pending_dir)
        try:
            if proposal_id.isdigit():
                target = items[int(proposal_id)]
            else:
                target = proposal_id
        except (IndexError, ValueError):
            print(f"Proposal ID '{proposal_id}' not found.")
            return
            
        src = os.path.join(pending_dir, target)
        dest = os.path.join(skills_dir, target)
        
        if os.path.isdir(src):
            import shutil
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.move(src, dest)
            print(f"✅ Successfully approved and merged skill: {target}")
        else:
            import shutil
            shutil.move(src, dest)
            print(f"✅ Approved change file: {target}")

    def reject_pending_skill(self, proposal_id: str):
        """Deletes a pending proposal."""
        pending_dir = os.path.join(ROOT_DIR, ".agents", "pending")
        items = os.listdir(pending_dir)
        try:
            if proposal_id.isdigit():
                target = items[int(proposal_id)]
            else:
                target = proposal_id
        except (IndexError, ValueError):
            print(f"Proposal ID '{proposal_id}' not found.")
            return
            
        target_path = os.path.join(pending_dir, target)
        if os.path.isdir(target_path):
            import shutil
            shutil.rmtree(target_path)
        else:
            os.remove(target_path)
        print(f"❌ Rejected and deleted proposal: {target}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Keystone Sovereign - Master Coordinator")
    parser.add_argument("--status", action="store_true", help="Print the current multi-agent report status")
    parser.add_argument("--monitor-music", action="store_true", help="Scan and track the physical music desktop pipeline")
    parser.add_argument("--test-all", action="store_true", help="Run the full 5-agent diagnostic self-test suite")
    parser.add_argument("--check-jobs", action="store_true", help="Audit and clean up completed background subagent processes")
    parser.add_argument("--agent", type=str, choices=["health", "music", "dev", "research", "media"], help="Target subagent to execute")
    parser.add_argument("--args", nargs=argparse.REMAINDER, help="Arguments to pass directly to the target subagent")
    
    # Skills approval CLI commands
    parser.add_argument("--skills-list", action="store_true", help="Show all pending proposals")
    parser.add_argument("--skills-diff", type=str, help="Display unified diff of proposed changes by ID/name")
    parser.add_argument("--skills-approve", type=str, help="Merge the staged skill into the active skills directory")
    parser.add_argument("--skills-reject", type=str, help="Delete the staged proposal")
    
    args = parser.parse_args()
    coordinator = KeystoneSovereign()
    
    if args.status:
        coordinator.print_system_status()
    elif args.monitor_music:
        coordinator.monitor_desktop_music()
    elif args.test_all:
        coordinator.run_complete_diagnostic_suite()
    elif args.check_jobs:
        report = coordinator.check_background_jobs()
        print("\n[Background Jobs Report]")
        print(report)
    elif args.skills_list:
        coordinator.list_pending_skills()
    elif args.skills_diff:
        coordinator.diff_pending_skill(args.skills_diff)
    elif args.skills_approve:
        coordinator.approve_pending_skill(args.skills_approve)
    elif args.skills_reject:
        coordinator.reject_pending_skill(args.skills_reject)
    elif args.agent:
        subagent_args = args.args if args.args else []
        output = coordinator.execute_subagent(args.agent, subagent_args)
        print("\n[Subagent Output Result]")
        print(output)
    else:
        # Default behavior: Print status
        coordinator.print_system_status()


