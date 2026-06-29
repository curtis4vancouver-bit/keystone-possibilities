import os
import sys
import time
import json
import shutil
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

# Force UTF-8 encoding on Windows to prevent print errors
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("ERROR: watchdog library is not installed.")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("ERROR: psutil library is not installed.")
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────────────────────
MASTER_BRAIN_ROOT = Path("C:/Users/Curtis/New folder/construction-website/Keystone_HQ/00_Master_Brain")
SCRIPTS_DIR = MASTER_BRAIN_ROOT / "scripts"
LOG_FILE = SCRIPTS_DIR / "os_daemon.log"
HEARTBEAT_FILE = SCRIPTS_DIR / "heartbeat.json"

VOICE_OUTBOX_PATH = Path("C:/Users/Curtis/.gemini/antigravity/voice_outbox.txt")
CORRECTION_JOURNAL_PATH = MASTER_BRAIN_ROOT / ".learnings" / "correction_journal.json"
AGENT_FLEET_DIR = MASTER_BRAIN_ROOT / "Agent_Fleet"

# ── Logging Setup ──────────────────────────────────────────────────────────
logger = logging.getLogger("KeystoneOSDaemon")
logger.setLevel(logging.INFO)

# Rotating File Handler: 5 MB max, 3 backups, UTF-8 encoding
file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ── Helper Functions ───────────────────────────────────────────────────────
def parse_iso_timestamp(ts_str):
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'
    return datetime.fromisoformat(ts_str)

def run_task_async(task_name):
    if task_name == "self_learning_cycle":
        script_path = SCRIPTS_DIR / "auto_learning_scheduler.py"
        logger.info(f"Running self_learning_cycle task: {script_path} --run")
        try:
            subprocess.Popen([sys.executable, str(script_path), "--run"])
        except Exception as e:
            logger.error(f"Failed to launch self_learning_cycle: {e}")
    elif task_name == "email_check":
        script_path = SCRIPTS_DIR / "email_check.py"
        logger.info(f"Running email_check task: {script_path}")
        if script_path.exists():
            try:
                subprocess.Popen([sys.executable, str(script_path)])
            except Exception as e:
                logger.error(f"Failed to launch email_check: {e}")
        else:
            logger.warning(f"email_check task triggered but {script_path} does not exist. Simulating successful check.")
    elif task_name == "self_healing_cycle":
        script_path = SCRIPTS_DIR / "chrome_self_learner.py"
        logger.info(f"Running self_healing_cycle task: {script_path}")
        try:
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as e:
            logger.error(f"Failed to launch self_healing_cycle: {e}")

# ── Watchdog Handler ───────────────────────────────────────────────────────
class DaemonFileSystemHandler(FileSystemEventHandler):
    def handle_event(self, event):
        if event.is_directory:
            return
        
        path = os.path.abspath(event.src_path).replace('\\', '/')
        
        # Check voice_outbox.txt
        if path.lower().endswith("/.gemini/antigravity/voice_outbox.txt"):
            logger.info(f"Watchdog: voice_outbox.txt modified (event: {event.event_type})")
            
        # Check correction_journal.json
        elif path.lower().endswith("/00_master_brain/.learnings/correction_journal.json"):
            logger.info(f"Watchdog: correction_journal.json modified (event: {event.event_type})")
            
        # Check Agent_Fleet/*/INBOX.json
        elif "/agent_fleet/" in path.lower() and path.lower().endswith("/inbox.json"):
            parts = path.split('/')
            if len(parts) >= 3 and parts[-1].lower() == "inbox.json" and parts[-3].lower() == "agent_fleet":
                agent_name = parts[-2]
                logger.info(f"Watchdog: Inbox for agent '{agent_name}' modified (event: {event.event_type})")

    def on_modified(self, event):
        self.handle_event(event)

    def on_created(self, event):
        self.handle_event(event)

# ── Health Check Routines ──────────────────────────────────────────────────
def check_ram():
    try:
        virtual_mem = psutil.virtual_memory()
        available_gb = virtual_mem.available / (1024 ** 3)
        if available_gb < 4.0:
            logger.warning(f"RAM check: Available RAM is LOW: {available_gb:.2f} GB (threshold: 4.00 GB)")
        else:
            logger.info(f"RAM check: Available RAM is healthy: {available_gb:.2f} GB")
    except Exception as e:
        logger.error(f"Error checking RAM: {e}")

def check_disk_space():
    drives = ["C:\\", "G:\\"]
    for drive in drives:
        try:
            if not os.path.exists(drive):
                logger.warning(f"Disk check: Drive {drive} is not mounted or accessible.")
                continue
            usage = shutil.disk_usage(drive)
            free_gb = usage.free / (1024 ** 3)
            if free_gb < 200.0:
                logger.warning(f"Disk check: Drive {drive} free space is LOW: {free_gb:.2f} GB (threshold: 200.00 GB)")
            else:
                logger.info(f"Disk check: Drive {drive} free space is healthy: {free_gb:.2f} GB")
        except Exception as e:
            logger.error(f"Error checking disk space for {drive}: {e}")

def check_docker_containers():
    required_containers = [
        "keystone_qdrant_brain",
        "keystone_qdrant_clone",
        "neo4j-graph-memory",
        "n8n-workflow-engine",
        "n8n-postgres",
        "sanity-gravity-desktop"
    ]
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.State}}"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split("\n")
        container_states = {}
        for line in lines:
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                container_states[parts[0].strip()] = parts[1].strip()

        for container in required_containers:
            state = container_states.get(container)
            if state is None:
                logger.warning(f"Docker check: Container '{container}' is missing from the system.")
            elif state != "running":
                logger.warning(f"Docker check: Container '{container}' is not running (state: '{state}'). Restarting...")
                try:
                    subprocess.run(["docker", "start", container], check=True, capture_output=True)
                    logger.info(f"Docker check: Container '{container}' started successfully.")
                except subprocess.CalledProcessError as err:
                    err_msg = err.stderr.strip() if err.stderr else str(err)
                    logger.error(f"Docker check: Failed to start container '{container}': {err_msg}")
            else:
                logger.info(f"Docker check: Container '{container}' is running.")
    except Exception as e:
        logger.error(f"Docker check: Failed to run Docker check: {e}")

def check_mcp_processes():
    mcp_scripts = [
        "keystone_brain_v2_mcp.py",
        "youtube_mcp.py",
        "content_engine_mcp.py",
        "youtube_researcher_mcp.py",
        "git_wrapper.py"
    ]
    
    running_cmdlines = []
    try:
        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline')
                if cmdline:
                    running_cmdlines.append(cmdline)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
    except Exception as e:
        logger.error(f"MCP watchdog: Error enumerating processes: {e}")
        return

    for script in mcp_scripts:
        is_running = False
        for cmdline in running_cmdlines:
            for arg in cmdline:
                normalized_arg = arg.replace('\\', '/')
                if normalized_arg.endswith('/' + script) or normalized_arg == script or os.path.basename(normalized_arg) == script:
                    is_running = True
                    break
            if is_running:
                break
        
        if not is_running:
            logger.warning(f"MCP watchdog: Process is missing: {script}")
        else:
            logger.info(f"MCP watchdog: Process is running: {script}")

# ── Clean Routines ─────────────────────────────────────────────────────────
def purge_old_files(directory, days=7):
    if not directory or not os.path.exists(directory):
        logger.info(f"Cleaner: Directory '{directory}' does not exist, skipping.")
        return
        
    cutoff_time = time.time() - (days * 24 * 3600)
    logger.info(f"Cleaner: Purging files older than {days} days from: {directory}")
    
    files_deleted = 0
    errors = 0
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                if mtime < cutoff_time:
                    os.remove(file_path)
                    files_deleted += 1
            except Exception:
                errors += 1
                
    logger.info(f"Cleaner: Purged '{directory}'. Deleted {files_deleted} files. Errors/locked files: {errors}")

def clean_temp_files():
    temp_dir = os.environ.get("TEMP")
    compiled_sources_dir = MASTER_BRAIN_ROOT / "Deep_Research_Results" / "Compiled_Sources"
    
    purge_old_files(temp_dir, days=7)
    purge_old_files(str(compiled_sources_dir), days=7)

# ── Heartbeat and Catch-up ─────────────────────────────────────────────────
def write_heartbeat():
    try:
        data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "running"
        }
        with open(HEARTBEAT_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logger.info("Heartbeat written to heartbeat.json")
    except Exception as e:
        logger.error(f"Failed to write heartbeat: {e}")

def run_catchup():
    if not HEARTBEAT_FILE.exists():
        logger.info("No heartbeat.json found. Skipping catch-up.")
        return

    try:
        with open(HEARTBEAT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        last_heartbeat_str = data.get("timestamp")
        if not last_heartbeat_str:
            logger.warning("Heartbeat file lacks timestamp. Skipping catch-up.")
            return

        last_time = parse_iso_timestamp(last_heartbeat_str)
        current_time = datetime.now(timezone.utc)
        gap = (current_time - last_time).total_seconds()
        logger.info(f"Startup catch-up check: last heartbeat was {last_heartbeat_str}, gap is {gap:.1f} seconds.")

        # self_learning_cycle: disabled automatically to prevent behavioral drift. Run manually when needed.
        pass

        # email_check: interval 1 hour (3600s), expiration 12 hours (43200s)
        email_interval = 3600
        email_expiry = 43200
        if gap >= email_expiry:
            logger.warning(f"email_check catch-up EXPIRED (gap {gap:.1f}s >= threshold {email_expiry}s). Task skipped.")
        elif gap >= email_interval:
            logger.info(f"email_check task was missed (gap {gap:.1f}s >= interval {email_interval}s). Running catch-up now...")
            run_task_async("email_check")

    except Exception as e:
        logger.error(f"Error during catch-up execution: {e}")

# ── Main Loop ──────────────────────────────────────────────────────────────
def main():
    logger.info("============================================================")
    logger.info("Keystone OS Optimization Daemon starting...")
    logger.info(f"Root: {MASTER_BRAIN_ROOT}")
    logger.info("============================================================")

    # 1. Run catch-up first on startup
    run_catchup()

    # 2. Write initial heartbeat
    write_heartbeat()

    # 3. Setup watchdog observer
    handler = DaemonFileSystemHandler()
    observer = Observer()

    # Watch C:\Users\Curtis\antigravity folder for voice_outbox.txt
    voice_dir = VOICE_OUTBOX_PATH.parent
    if voice_dir.exists():
        observer.schedule(handler, str(voice_dir), recursive=False)
        logger.info(f"Watching voice outbox directory: {voice_dir}")
    else:
        logger.warning(f"Voice outbox directory does not exist: {voice_dir}")

    # Watch learnings folder for correction_journal.json
    learnings_dir = CORRECTION_JOURNAL_PATH.parent
    if learnings_dir.exists():
        observer.schedule(handler, str(learnings_dir), recursive=False)
        logger.info(f"Watching learnings directory: {learnings_dir}")
    else:
        logger.warning(f"Learnings directory does not exist: {learnings_dir}")

    # Watch Agent_Fleet folder recursively for INBOX.json files
    if AGENT_FLEET_DIR.exists():
        observer.schedule(handler, str(AGENT_FLEET_DIR), recursive=True)
        logger.info(f"Watching Agent Fleet directory recursively: {AGENT_FLEET_DIR}")
    else:
        logger.warning(f"Agent Fleet directory does not exist: {AGENT_FLEET_DIR}")

    observer.start()
    logger.info("Watchdog observer active.")

    # 4. Tick scheduler loop variables (track last executed timestamp)
    last_ram_check = 0
    last_heartbeat = 0
    last_mcp_check = 0
    last_docker_check = 0
    last_disk_check = 0
    last_temp_clean = 0
    last_self_healing = 0

    try:
        while True:
            now = time.time()

            # RAM Check every 60s
            if now - last_ram_check >= 60:
                check_ram()
                last_ram_check = now

            # Heartbeat write every 60s
            if now - last_heartbeat >= 60:
                write_heartbeat()
                last_heartbeat = now

            # MCP Watchdog every 120s (2 minutes)
            if now - last_mcp_check >= 120:
                check_mcp_processes()
                last_mcp_check = now

            # Docker Healthcheck every 300s (5 minutes)
            if now - last_docker_check >= 300:
                check_docker_containers()
                last_docker_check = now

            # Disk Space Check every 300s (5 minutes)
            if now - last_disk_check >= 300:
                check_disk_space()
                last_disk_check = now

            # Temp File Cleaner every 21600s (6 hours)
            if now - last_temp_clean >= 21600:
                clean_temp_files()
                last_temp_clean = now

            # Self-healing check: disabled automatically to prevent behavioral drift. Run manually when needed.
            if now - last_self_healing >= 600:
                # logger.info("Self-healing check interval reached. Auto-run skipped to prevent behavioral drift.")
                last_self_healing = now

            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down daemon...")
    finally:
        observer.stop()
        observer.join()
        logger.info("Daemon successfully stopped.")

if __name__ == "__main__":
    main()
