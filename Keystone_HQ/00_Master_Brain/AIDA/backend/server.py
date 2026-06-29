import os
import sys
import re
import shutil
import threading
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Ensure parent directory (AIDA root) and backend directory are in sys.path so imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import manager modules using try-except to support both PyInstaller frozen bundle and raw run
try:
    from backend.chat_manager import ChatManager
    from backend.system_monitor import SystemMonitor
    from backend.app_launcher import AppLauncher
    from backend.voice_bridge_api import VoiceBridgeAPI
except (ImportError, ModuleNotFoundError):
    from chat_manager import ChatManager
    from system_monitor import SystemMonitor
    from app_launcher import AppLauncher
    from voice_bridge_api import VoiceBridgeAPI

# --- Module-Level Constants (single source of truth) ---
PROJECT_MAP = {
    "chronos": "02ec213a-7c20-4ec1-8396-ea46c276b1b1",
    "recomposition": "649e6bdc-08b0-4778-92b9-14486c1d005f",
    "protocols": "a581830e-c700-4716-bde1-2908591bc4bf",
    "possibilities": "6ae51756-6b7f-408d-bba5-0ebb98a1c173",
    "webmaster": "84242fa1-1246-4e33-967d-f7a0f2e54a26",
    "site_super": "d52622c1-399e-499b-9349-5a7599b9e030",
    "wayne_health": "e7e5a7b6-df41-4770-985d-85fa715f2081",
    "tax_finance": "f3b6c701-4478-4ec8-b61e-fa0ebb715e21",
    "market_analyst": "ac6110f2-b715-4fa0-9289-4a921d7b1a20",
    "self_evolution": "b8e72c84-17c0-4ad9-bf95-9ebb24a1b072"
}

FOLDER_MAP = {
    "chronos": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.learnings\archive",
    "recomposition": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\06_Music_Recomposition\archive",
    "protocols": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\07_Health_Protocols\archive",
    "possibilities": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities\archive",
    "webmaster": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AIDA_V2\backend\archive",
    "wayne_health": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\07_Health_Protocols\wayne_stats\archive",
    "site_super": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\02_Keystone_Possibilities_Construction\archive",
    "tax_finance": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\03_Email_and_Advertising\tax_archive",
    "market_analyst": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.learnings\market_archive",
    "self_evolution": r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.learnings\evolution_archive"
}

MODULE_NAMES = {
    "chronos": "Chronos Master Brain",
    "recomposition": "Chronos Recomposition Music",
    "protocols": "Keystone Protocol Wellness",
    "possibilities": "Keystone Possibilities PM",
    "webmaster": "Keystone Webmaster SEO",
    "wayne_health": "Wayne Stevenson Health",
    "site_super": "Site Superintendent Work",
    "tax_finance": "Tax Strategist Finance",
    "market_analyst": "Market Analyst Wealth",
    "self_evolution": "Self Evolution Learning"
}

INFRA_SCRIPTS = frozenset([
    'app_entry.py', 'server.py', 'voice_bridge.py', 'git_wrapper.py'
])

# Instantiate managers
chat_manager = ChatManager()
system_monitor = SystemMonitor()
app_launcher = AppLauncher()
voice_bridge_api = VoiceBridgeAPI()

is_agent_working = False
is_python_working = False
active_agents_count = 0
active_python_count = 0

def monitor_agent_work_loop():
    """Lightweight agent/python work monitor. Polls every 5s, no object caching."""
    global is_agent_working, is_python_working, active_agents_count, active_python_count
    import time
    import psutil
    current_pid = os.getpid()
    while True:
        try:
            agents = 0
            py_tasks = 0
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    name = (proc.info.get('name') or '').lower()
                    pid = proc.info.get('pid')
                    if name == 'language_server.exe':
                        agents += 1
                    elif pid != current_pid and 'python' in name:
                        try:
                            # Only query cmdline for Python processes to prevent massive AccessDenied CPU overhead
                            cmdline = proc.cmdline() or []
                            for arg in cmdline:
                                if arg.endswith('.py'):
                                    base = os.path.basename(arg).lower()
                                    if base not in INFRA_SCRIPTS and not base.endswith(('_mcp.py', '_server.py')) and 'mcp' not in base:
                                        py_tasks += 1
                                    break
                        except (psutil.AccessDenied, psutil.ZombieProcess):
                            pass
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            # Subtract 1 from agents for the idle Antigravity language server
            active = max(0, agents - 1) if agents > 0 else 0
            is_agent_working = active > 0
            active_agents_count = active
            is_python_working = py_tasks > 0
            active_python_count = py_tasks
        except Exception:
            pass
        time.sleep(5.0)


@asynccontextmanager
async def lifespan(app):
    """Modern FastAPI lifespan handler — replaces deprecated on_event."""
    print("A.I.D.A. Server starting up...")
    monitor_thread = threading.Thread(target=monitor_agent_work_loop, daemon=True)
    monitor_thread.start()
    print("Started background agent work monitor thread (5s interval).")
    yield
    print("A.I.D.A. Server shutting down...")
    try:
        voice_bridge_api.stop_bridge()
    except Exception as e:
        print(f"Error in voice bridge shutdown: {e}")

app = FastAPI(title="A.I.D.A. Backend Server", version="1.0.0", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware for Cache Control of Static Assets ---
@app.middleware("http")
async def add_cache_control_header(request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path.startswith("/css") or path.startswith("/js") or path.startswith("/assets") or path == "/" or path.endswith(".html"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


# --- API Request Models ---
class SwitchChatRequest(BaseModel):
    chat_id: str

class RenameChatRequest(BaseModel):
    name: str

class NewChatRequest(BaseModel):
    model: str  # flash_lite | flash | pro

class ChangeModelRequest(BaseModel):
    model: str

class SendMessageRequest(BaseModel):
    message: str

class SpeakRequest(BaseModel):
    text: str

class SpeakFileRequest(BaseModel):
    path: str

class CommitLearningRequest(BaseModel):
    tried: str
    wrong_because: str
    fix: str
    category: str
    severity: str
    chat_id: Optional[str] = None

class OpenFolderRequest(BaseModel):
    path: str

# --- API Routes ---

# Projects
@app.get("/api/projects")
def get_projects():
    return chat_manager.get_projects()

@app.post("/api/projects")
def add_project(name: str = Form(...)):
    return chat_manager.add_project(name)

@app.delete("/api/projects/{project_id}")
def delete_project(project_id: str):
    success = chat_manager.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete project")
    return {"success": True}

@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: str):
    success = chat_manager.delete_chat(chat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete chat")
    return {"success": True}

# Chats
@app.get("/api/chats")
def get_chats(project_id: str = None, refresh: bool = False):
    all_chats = chat_manager.get_chats(force=refresh)
    if project_id:
        # Find the Chronos ID dynamically to use as default fallback for legacy chats
        chronos_id = "chronos"
        for p in chat_manager.get_projects():
            if "Chronos" in p.get("name", ""):
                chronos_id = p["id"]
                break
                
        return [c for c in all_chats if c.get("project_id", chronos_id) == project_id]
    return all_chats
@app.get("/api/chats/active")
def get_active_chat():
    import json
    import os
    cfg_path = chat_manager.voice_bridge_config_path
    
    # 1. Dynamically find the newest active conversation ID from db and brain files
    latest_id = None
    conv_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "conversations")
    try:
        candidates = []
        if os.path.exists(conv_dir):
            for f in os.listdir(conv_dir):
                if f.endswith(('.db', '.db-wal', '.db-shm')):
                    name = f.split('.')[0]
                    if len(name) == 36 and "-" in name:
                        full_path = os.path.join(conv_dir, f)
                        candidates.append((name, os.path.getmtime(full_path)))
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            latest_id = candidates[0][0]
    except Exception:
        pass

    if not latest_id:
        # Fallback to brain directory
        brain_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")
        try:
            candidates = []
            for d in os.listdir(brain_dir):
                full_path = os.path.join(brain_dir, d)
                if os.path.isdir(full_path) and len(d) == 36 and "-" in d:
                    key_files = [
                        os.path.join(full_path, ".system_generated", "logs", "transcript.jsonl"),
                        os.path.join(full_path, "task.md"),
                        os.path.join(full_path, "working_memory.md")
                    ]
                    max_mtime = 0
                    for kf in key_files:
                        if os.path.exists(kf):
                            try:
                                mtime = os.path.getmtime(kf)
                                if mtime > max_mtime:
                                    max_mtime = mtime
                            except Exception:
                                pass
                    if max_mtime == 0:
                        try:
                            max_mtime = os.path.getmtime(full_path)
                        except Exception:
                            pass
                    candidates.append((d, max_mtime))
            if candidates:
                candidates.sort(key=lambda x: x[1], reverse=True)
                latest_id = candidates[0][0]
        except Exception:
            pass

    active_chat_id = None
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                active_chat_id = config.get("conversation_id")
        except Exception:
            pass
            
    # Sync config if out of date
    if latest_id and active_chat_id != latest_id:
        active_chat_id = latest_id
        try:
            cfg = {}
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            cfg["conversation_id"] = latest_id
            os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2)
        except Exception:
            pass
            
    return {"active_chat_id": active_chat_id}


def get_bounce_back_context(module_id: str) -> str:
    target_project_id = PROJECT_MAP.get(module_id)
    if not target_project_id:
        return ""
    try:
        all_chats = chat_manager.get_chats(force=True)
        module_chats = [c for c in all_chats if c.get("project_id") == target_project_id]
        prev_chat = None
        for chat in module_chats:
            messages = chat_manager.get_messages(chat["id"])
            user_msgs = [m for m in messages if m.get("sender") == "user"]
            if user_msgs:
                prev_chat = chat
                break
        if not prev_chat:
            return "\n\n---\n## Previous Session Bounce-Back\nNo previous session history found for this module."
        messages = chat_manager.get_messages(prev_chat["id"])
        tail_msgs = []
        for msg in messages[-6:]:
            sender = "User" if msg.get("sender") == "user" else "Assistant"
            content = msg.get("content", "").strip()
            if content and not content.startswith("# ") and not content.startswith("[BOOTSTRAP"):
                if len(content) > 300:
                    content = content[:297] + "..."
                tail_msgs.append(f"**{sender}:** {content}")
        tail_str = "\n".join(tail_msgs)
        return f"\n\n---\n## Previous Session Bounce-Back\n* **Last Active Chat:** `{prev_chat.get('name', prev_chat['id'])}` (ID: `{prev_chat['id']}`)\n* **Where We Left Off:**\n{tail_str or 'No conversation content found.'}"
    except Exception as e:
        print(f"Error compiling bounce-back context: {e}")
        return ""

@app.get("/api/bootstrap/{module_id}")
def get_module_bootstrap(module_id: str):
    clean_id = "".join(c for c in module_id if c.isalnum() or c in ("_", "-"))
    prompt_path = os.path.join(chat_manager.aida_root, "backend", "bootstraps", f"{clean_id}.md")
    if clean_id == "chronos" and not os.path.exists(prompt_path):
        prompt_path = os.path.join(chat_manager.master_brain, "00_CHRONOS_MASTER_SYSTEM_PROMPT.md")
    if os.path.exists(prompt_path):
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                prompt_content = f.read()
            bounce_back = get_bounce_back_context(clean_id)
            return {"prompt": prompt_content + bounce_back}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read prompt: {e}")
    return {"prompt": f"[Bootstrap file for {clean_id} not found on server]"}

@app.get("/api/archive/files")
def get_archive_files(module_id: str, chat_id: Optional[str] = None):
    
    files = []
    
    clean_chat_name = ""
    if chat_id:
        chat_info = chat_manager.names_cache.get(chat_id, {})
        chat_name = chat_info.get("name", "")
        if chat_name:
            clean_chat_name = "".join(c for c in chat_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    
    # 1. Add general static archive files from the folder map
    target_dir = FOLDER_MAP.get(module_id)
    if target_dir and os.path.exists(target_dir):
        try:
            # Check target_dir directly
            for item in os.listdir(target_dir):
                full_path = os.path.join(target_dir, item)
                if os.path.isfile(full_path):
                    # Filter out other chats' synced active files or transcripts if chat_id is passed
                    include_file = True
                    if chat_id:
                        is_chat_transcript = item.startswith("chat_")
                        is_active_chat_sync = item.startswith("walkthrough_") or item.startswith("implementation_plan_") or item.startswith("Master_Prompt_") or item.startswith("task_")
                        
                        if is_chat_transcript:
                            if chat_id[:8] not in item:
                                include_file = False
                        elif is_active_chat_sync:
                            if not clean_chat_name or clean_chat_name not in item:
                                include_file = False
                                
                    if include_file:
                        files.append({
                            "name": item,
                            "path": full_path,
                            "type": "archive"
                        })
            
            # Check history subdirectory
            history_dir = os.path.join(target_dir, "history")
            if os.path.exists(history_dir) and os.path.isdir(history_dir):
                for item in os.listdir(history_dir):
                    full_path = os.path.join(history_dir, item)
                    if os.path.isfile(full_path):
                        # Filter out other chats' transcripts or synced files if chat_id is passed
                        include_file = True
                        if chat_id:
                            is_chat_transcript = item.startswith("chat_")
                            is_active_chat_sync = item.startswith("walkthrough_") or item.startswith("implementation_plan_") or item.startswith("Master_Prompt_") or item.startswith("task_")
                            
                            if is_chat_transcript:
                                if chat_id[:8] not in item:
                                    include_file = False
                            elif is_active_chat_sync:
                                if not clean_chat_name or clean_chat_name not in item:
                                    include_file = False
                                    
                        if include_file:
                            files.append({
                                "name": item,
                                "path": full_path,
                                "type": "archive"
                            })
        except Exception:
            pass
            
    # 2. Add dynamic chat artifacts from the requested chat, or fallback to all module chats
    target_project_id = PROJECT_MAP.get(module_id)
    if target_project_id:
        try:
            all_chats = chat_manager.get_chats(force=True)
            if chat_id:
                module_chats = [c for c in all_chats if c.get("id") == chat_id]
            else:
                module_chats = [c for c in all_chats if c.get("project_id") == target_project_id]
            
            root_whitelist = ["walkthrough.md", "implementation_plan.md", "self_evolution_update_ideas.md"]
            scratch_whitelist = ["check_voice_bridge.py", "test_server_port.py", "start_voice_bridge.py"]
            
            for c in module_chats:
                cid = c["id"]
                chat_info = chat_manager.names_cache.get(cid, {})
                chat_name = chat_info.get("name", f"Chat {cid[:8]}")
                
                chat_brain_dir = os.path.join(chat_manager.brain_dir, cid)
                if os.path.exists(chat_brain_dir) and os.path.isdir(chat_brain_dir):
                    # Skip folders marked as deleted
                    if os.path.exists(os.path.join(chat_brain_dir, ".deleted")):
                        continue
                    # Check root files
                    for item in os.listdir(chat_brain_dir):
                        full_path = os.path.join(chat_brain_dir, item)
                        if os.path.isfile(full_path):
                            if item in root_whitelist or item.endswith("Master_Prompt.md"):
                                files.append({
                                    "name": f"{item} ({chat_name})",
                                    "path": full_path,
                                    "type": "code"
                                })
                                # Sync to the OS archive folder so they show up on the OS and are up-to-date
                                if target_dir:
                                    import shutil
                                    try:
                                        clean_chat_name = "".join(c for c in chat_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
                                        base, ext = os.path.splitext(item)
                                        synced_filename = f"{base}_{clean_chat_name}{ext}"
                                        dest_path = os.path.join(target_dir, synced_filename)
                                        if not os.path.exists(dest_path) or os.path.getmtime(full_path) > os.path.getmtime(dest_path):
                                            os.makedirs(target_dir, exist_ok=True)
                                            shutil.copy2(full_path, dest_path)
                                            print(f"[Archive Sync] Synced {item} to {dest_path}")
                                    except Exception as e:
                                        print(f"[Archive Sync] Error: {e}")
                                
                    # Check scratch files
                    scratch_dir = os.path.join(chat_brain_dir, "scratch")
                    if os.path.exists(scratch_dir) and os.path.isdir(scratch_dir):
                        for item in os.listdir(scratch_dir):
                            full_path = os.path.join(scratch_dir, item)
                            if os.path.isfile(full_path) and item in scratch_whitelist:
                                files.append({
                                    "name": f"{item} ({chat_name})",
                                    "path": full_path,
                                    "type": "code"
                                })
        except Exception as e:
            print(f"Error scanning chat brain directories: {e}")
                
    return files

@app.get("/api/archive/file")
def get_archive_file_content(path: str):
    allowed_workspace = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ"
    allowed_home = os.path.join(os.path.expanduser("~"), ".gemini")
    
    normalized_path = os.path.abspath(path)
    is_allowed = normalized_path.lower().startswith(allowed_workspace.lower()) or normalized_path.lower().startswith(allowed_home.lower())
    
    if not is_allowed:
        raise HTTPException(status_code=403, detail="Access denied")
        
    if os.path.exists(normalized_path) and os.path.isfile(normalized_path):
        try:
            with open(normalized_path, "r", encoding="utf-8", errors="replace") as f:
                return {"content": f.read()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read file: {e}")
            
    raise HTTPException(status_code=404, detail="File not found")

@app.delete("/api/archive/file")
def delete_archive_file(path: str):
    allowed_workspace = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ"
    allowed_home = os.path.join(os.path.expanduser("~"), ".gemini")
    
    normalized_path = os.path.abspath(path)
    is_allowed = normalized_path.lower().startswith(allowed_workspace.lower()) or normalized_path.lower().startswith(allowed_home.lower())
    
    if not is_allowed:
        raise HTTPException(status_code=403, detail="Access denied")
        
    if os.path.exists(normalized_path) and os.path.isfile(normalized_path):
        try:
            os.remove(normalized_path)
            # Clear caches so the deleted file doesn't linger in directory lists
            chat_manager._chats_cache = None
            return {"success": True}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete file: {e}")
            
    raise HTTPException(status_code=404, detail="File not found")

@app.put("/api/chats/{chat_id}/name")
def rename_chat(chat_id: str, request: RenameChatRequest):
    success = chat_manager.rename_chat(chat_id, request.name)
    return {"success": success}

@app.post("/api/chats/{chat_id}/model")
def set_chat_model(chat_id: str, request: ChangeModelRequest):
    success = chat_manager.set_chat_model(chat_id, request.model)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to set model")
    try:
        voice_bridge_api.speak(f"Model updated to {request.model}")
    except Exception as e:
        print(f"Failed to speak model update: {e}")
    return {"success": True}

# /api/mcp/refresh route removed — was causing Antigravity window glitching

@app.post("/api/chats/switch")
def switch_chat(request: SwitchChatRequest):
    success = chat_manager.switch_chat(request.chat_id)
    return {"success": success}

@app.post("/api/open-folder")
def open_folder(request: OpenFolderRequest):
    print(f"[AIDA API] Request to open/toggle folder: {request.path}")
    try:
        normalized_path = os.path.normpath(request.path)
        print(f"[AIDA API] Normalized path: {normalized_path}")
        if os.path.exists(normalized_path):
            import subprocess
            if os.name == 'nt':
                import ctypes
                folder_title = os.path.basename(normalized_path.rstrip("\\/")).lower()
                full_path_lower = normalized_path.lower()
                hwnd = None
                
                # EnumWindows callback
                WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
                
                def get_window_text(h):
                    length = ctypes.windll.user32.GetWindowTextLengthW(h)
                    if length > 0:
                        buff = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(h, buff, length + 1)
                        return buff.value
                    return ""

                def get_class_name(h):
                    buff = ctypes.create_unicode_buffer(256)
                    ctypes.windll.user32.GetClassNameW(h, buff, 256)
                    return buff.value

                def enum_callback(h, lParam):
                    nonlocal hwnd
                    class_name = get_class_name(h)
                    if class_name == "CabinetWClass":
                        title = get_window_text(h).lower()
                        if (folder_title in title) or (full_path_lower in title):
                            hwnd = h
                            return False  # Stop enumeration
                    return True

                ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
                
                if hwnd:
                    is_minimized = ctypes.windll.user32.IsIconic(hwnd)
                    if is_minimized:
                        # Restore SW_RESTORE (9)
                        ctypes.windll.user32.ShowWindow(hwnd, 9)
                        ctypes.windll.user32.SetForegroundWindow(hwnd)
                        print(f"[AIDA API] Restored minimized window for {folder_title}")
                    else:
                        # Minimize SW_MINIMIZE (6)
                        ctypes.windll.user32.ShowWindow(hwnd, 6)
                        print(f"[AIDA API] Minimized active window for {folder_title}")
                else:
                    # Open new window
                    print(f"[AIDA API] Spawning explorer.exe for: {normalized_path}")
                    subprocess.Popen(["explorer.exe", normalized_path], close_fds=True)
            else:
                print(f"[AIDA API] Spawning xdg-open for: {normalized_path}")
                subprocess.run(['xdg-open', normalized_path])
            return {"success": True}
        else:
            print(f"[AIDA API] Path does not exist: {normalized_path}")
            raise HTTPException(status_code=404, detail=f"Path does not exist: {normalized_path}")
    except Exception as e:
        print(f"[AIDA API] Error opening folder {request.path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

def archive_chat_to_module(chat_id: str, module_id: str):
    from datetime import datetime
    target_dir = FOLDER_MAP.get(module_id)
    if not target_dir:
        print(f"[Archive] No archive directory mapped for module: {module_id}")
        return
        
    try:
        messages = chat_manager.get_messages(chat_id)
        if not messages:
            print(f"[Archive] Chat {chat_id} is empty. Skipping.")
            return
            
        chat_info = chat_manager.names_cache.get(chat_id, {})
        chat_name = chat_info.get("name", "Untitled Chat")
        
        md_content = f"# Chat Archive: {chat_name}\n"
        md_content += f"* **Chat ID:** `{chat_id}`\n"
        md_content += f"* **Module:** `{module_id}`\n"
        md_content += f"* **Archived At:** `{datetime.utcnow().isoformat()}Z`\n\n"
        md_content += "---\n\n"
        
        for msg in messages:
            sender = msg.get("sender", "unknown")
            content = msg.get("content", "").strip()
            timestamp = msg.get("timestamp", "")
            
            if sender == "user":
                sender_label = "**User**"
            elif sender == "assistant":
                sender_label = "**Assistant (AIDA)**"
            else:
                sender_label = f"**{sender.capitalize()}**"
                
            md_content += f"### {sender_label} *({timestamp})*\n\n{content}\n\n"
            
        history_dir = os.path.join(target_dir, "history")
        os.makedirs(history_dir, exist_ok=True)
        clean_name = "".join(c for c in chat_name if c.isalnum() or c in (" ", "_", "-")).strip()
        clean_name = clean_name.replace(" ", "_")
        filename = f"chat_{chat_id[:8]}_{clean_name}.md"
        file_path = os.path.join(history_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[Archive] Successfully archived chat {chat_id} to {file_path}")
        
    except Exception as e:
        print(f"[Archive] Failed to archive chat {chat_id}: {e}")

@app.post("/api/chats/new")
def new_chat(request: NewChatRequest, project_id: str = None, module_id: str = None):
    if not project_id:
        for p in chat_manager.get_projects():
            if "Chronos" in p.get("name", ""):
                project_id = p["id"]
                break
        if not project_id:
            project_id = "chronos"

    # 1. Fetch bootstrap prompt if module_id is provided
    initial_prompt = "Hello"
    if module_id:
        try:
            boot_data = get_module_bootstrap(module_id)
            if boot_data and boot_data.get("prompt"):
                initial_prompt = boot_data["prompt"]
                print(f"[AIDA Backend] Loaded dynamic bootstrap + bounce-back for module={module_id}")
        except Exception as e:
            print(f"[AIDA Backend] Error loading bootstrap for new chat: {e}")

    target_project_id = PROJECT_MAP.get(module_id, project_id) if module_id else project_id

    # Locate previous (old) chats before creating the new one
    old_chats = []
    if target_project_id:
        try:
            all_chats = chat_manager.get_chats(force=True)
            old_chats = [c for c in all_chats if c.get("project_id") == target_project_id]
        except Exception as e:
            print(f"[AIDA Backend] Error scanning for old chats: {e}")

    # 2. Initialize a new chat session
    chat_data = chat_manager.new_chat(request.model, project_id, initial_prompt)
    if not chat_data:
        raise HTTPException(status_code=500, detail="Failed to create new conversation")

    # 3. Automatically rename the new chat
    target_name = MODULE_NAMES.get(module_id, "New Chat")
    chat_manager.rename_chat(chat_data["id"], target_name)
    chat_data["name"] = target_name

    # 3. Start the project bootstrap process (done via initial_prompt parameter in new_chat)
    # Ensure state of the new chat is fully updated and categorised correctly (switched in config)
    chat_manager.switch_chat(chat_data["id"])

    # 4. Locate the previous (old) chat and archive it
    for chat in old_chats:
        # Prevent deleting the newly created chat ID by chance
        if chat["id"] == chat_data["id"]:
            continue
        try:
            msgs = chat_manager.get_messages(chat["id"])
            user_msgs = [m for m in msgs if m.get("sender") == "user"]
            if user_msgs:
                archive_chat_to_module(chat["id"], module_id or "chronos")
            chat_manager.delete_chat(chat["id"])
        except Exception as e:
            print(f"[AIDA Backend] Error archiving/deleting old chat {chat['id']}: {e}")

    # 5. Ensure the state of the new chat is fully updated and returned
    return chat_data

@app.post("/api/chats/{chat_id}/send")
def send_message(chat_id: str, request: SendMessageRequest):
    return chat_manager.send_message(chat_id, request.message)

@app.get("/api/chats/{chat_id}/messages")
def get_chat_messages(chat_id: str):
    return chat_manager.get_messages(chat_id)

# File Upload
@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...), 
    chat_id: Optional[str] = Form(None)
):
    try:
        filename = file.filename
        if not filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        # Determine target path
        if chat_id and chat_id != "undefined":
            # Save directly to the chat's brain directory
            target_dir = os.path.join(chat_manager.brain_dir, chat_id)
        else:
            # Save to staging/temp media directory
            target_dir = os.path.join(chat_manager.brain_dir, "tempmediaStorage")
            
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "success": True, 
            "filename": filename, 
            "path": file_path, 
            "message": f"Saved file to {target_dir}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Learning & Corrections
@app.get("/api/learn/extract")
def extract_learning(chat_id: str):
    if not chat_id:
        raise HTTPException(status_code=400, detail="chat_id is required")
    return chat_manager.extract_chat_correction(chat_id)

@app.post("/api/learn/commit")
def commit_learning(request: CommitLearningRequest):
    try:
        rule_id = chat_manager.commit_learning(
            tried=request.tried,
            wrong_because=request.wrong_because,
            fix=request.fix,
            category=request.category,
            severity=request.severity,
            chat_id=request.chat_id
        )
        # Speak the rule ID clearly by adding spaces between letters/numbers
        spaced_rule_id = " ".join(list(rule_id.replace("-", " ")))
        try:
            voice_bridge_api.speak(f"New learning committed as rule {spaced_rule_id}")
        except Exception as ve:
            print(f"Failed to speak rule confirmation: {ve}")
        return {"success": True, "rule_id": rule_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/learn/commit-auto")
def commit_learning_auto(chat_id: str):
    # 1. Extract the correction
    extracted = chat_manager.extract_chat_correction(chat_id)
    tried = extracted.get("tried", "")
    fix = extracted.get("fix", "")
    
    if not tried:
        tried = "Automated learning extraction from chat."
    if not fix:
        raise HTTPException(status_code=400, detail="Could not extract a fix/prevention rule from the chat message history.")

    wrong_because = "Action did not achieve the desired outcome or required adjustments."
    
    # 3. Infer the category and severity via keywords
    text_to_scan = (tried + " " + fix).lower()
    
    category = "general"
    if any(k in text_to_scan for k in ["ui", "design", "layout", "button", "css", "html", "react", "component", "frontend", "color"]):
        category = "frontend"
    elif any(k in text_to_scan for k in ["seo", "indexing", "google console", "backlink", "traffic", "ranking"]):
        category = "seo"
    elif any(k in text_to_scan for k in ["server", "api", "route", "port", "backend", "fastapi", "python"]):
        category = "backend"
    elif any(k in text_to_scan for k in ["youtube", "video", "upload", "channel", "media", "b-roll"]):
        category = "media"
    elif any(k in text_to_scan for k in ["music", "lyrics", "song", "spotify"]):
        category = "music"
    elif any(k in text_to_scan for k in ["tax", "finance", "money", "deduction"]):
        category = "tax"
    elif any(k in text_to_scan for k in ["legal", "compliance", "law", "contract"]):
        category = "legal"
    elif any(k in text_to_scan for k in ["construction", "superintendent", "site", "step code", "blueprint"]):
        category = "construction"
        
    severity = "medium"
    if any(k in text_to_scan for k in ["critical", "crash", "broken", "failed", "error", "breaking"]):
        severity = "critical"
    elif any(k in text_to_scan for k in ["warning", "important", "fix", "incorrect", "wrong"]):
        severity = "high"
        
    try:
        rule_id = chat_manager.commit_learning(
            tried=tried,
            wrong_because=wrong_because,
            fix=fix,
            category=category,
            severity=severity,
            chat_id=chat_id
        )
        
        # Speak confirmation
        spaced_rule_id = " ".join(list(rule_id.replace("-", " ")))
        try:
            voice_bridge_api.speak(f"Auto committed learning rule {spaced_rule_id}")
        except Exception as ve:
            print(f"Failed to speak rule confirmation: {ve}")
            
        return {"success": True, "rule_id": rule_id, "category": category, "severity": severity}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sync/drive")
def sync_brain_to_drive_api(background_tasks: BackgroundTasks):
    scripts_dir = os.path.join(chat_manager.master_brain, "scripts")
    sync_brain_script = os.path.join(scripts_dir, "sync_brain_to_drive.py")
    sync_docs_script = os.path.join(scripts_dir, "sync_to_google_docs.py")
    sync_notebook_script = os.path.join(scripts_dir, "notebooklm_rpc_sync.py")
    
    def run_sync_pipeline():
        try:
            import subprocess
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            print("[AIDA Sync] Starting sync_brain_to_drive...")
            try:
                voice_bridge_api.speak("Syncing brain to Google Drive started")
            except Exception:
                pass
            
            if os.path.exists(sync_brain_script):
                subprocess.run([sys.executable, sync_brain_script], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=creation_flags)
                print("[AIDA Sync] sync_brain_to_drive completed.")
            else:
                print(f"[AIDA Sync] SKIPPED: {sync_brain_script} not found.")
            
            if os.path.exists(sync_docs_script):
                print("[AIDA Sync] Starting sync_to_google_docs...")
                subprocess.run([sys.executable, sync_docs_script], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=creation_flags)
                print("[AIDA Sync] sync_to_google_docs completed.")
            else:
                print(f"[AIDA Sync] SKIPPED: {sync_docs_script} not found.")
            
            if os.path.exists(sync_notebook_script):
                print("[AIDA Sync] Starting NotebookLM sync...")
                subprocess.run([sys.executable, sync_notebook_script], check=True, capture_output=True, text=True, encoding="utf-8", errors="replace", creationflags=creation_flags)
                print("[AIDA Sync] NotebookLM sync completed.")
            else:
                print(f"[AIDA Sync] SKIPPED: NotebookLM sync script not found yet.")
            
            try:
                voice_bridge_api.speak("Google Drive and Notebook L M sync complete")
            except Exception:
                pass
        except Exception as e:
            print(f"[AIDA Sync] Error during sync: {e}")
            try:
                voice_bridge_api.speak("Google Drive sync failed")
            except Exception:
                pass
                
    background_tasks.add_task(run_sync_pipeline)
    return {"status": "success", "message": "Google Drive and NotebookLM sync started in the background."}

# System Stats
@app.get("/api/system")
def get_system_stats():
    return system_monitor.get_stats()

# Model Quota Limits Scraper
@app.get("/api/models/quota")
def get_model_quota():
    return chat_manager.get_model_limits()

# External App Launcher
@app.post("/api/launch/{app_name}")
def launch_app(app_name: str):
    res = app_launcher.launch(app_name)
    if not res.get("success"):
        raise HTTPException(status_code=500, detail=res.get("error"))
    return res

@app.post("/api/stop/{app_name}")
def stop_app(app_name: str):
    res = app_launcher.stop(app_name)
    if not res.get("success"):
        raise HTTPException(status_code=500, detail=res.get("error"))
    return res

@app.get("/api/status/{app_name}")
def get_app_status(app_name: str):
    is_running = app_launcher.is_running(app_name)
    return {"running": is_running}


# Voice Bridge Control
@app.get("/api/voice/status")
def get_voice_status():
    return voice_bridge_api.get_status_data()

@app.post("/api/voice/speak")
def voice_speak(request: SpeakRequest):
    success = voice_bridge_api.speak(request.text)
    return {"success": success}

@app.post("/api/voice/start")
def start_voice_bridge():
    success = voice_bridge_api.start_bridge()
    return {"success": success, "status": voice_bridge_api.get_status()}

@app.post("/api/voice/stop")
def stop_voice_bridge():
    success = voice_bridge_api.stop_bridge()
    return {"success": success, "status": voice_bridge_api.get_status()}

@app.post("/api/voice/press")
def voice_press():
    print("[API] /api/voice/press called by frontend!")
    success = voice_bridge_api.trigger_press()
    return {"success": success}

@app.post("/api/voice/release")
def voice_release():
    print("[API] /api/voice/release called by frontend!")
    success = voice_bridge_api.trigger_release()
    return {"success": success}

@app.get("/api/agent/status")
def get_agent_status():
    global is_agent_working, is_python_working, active_agents_count, active_python_count
    return {
        "working": is_agent_working,
        "active_agents": active_agents_count,
        "python_working": is_python_working,
        "active_python_tasks": active_python_count
    }

def clean_markdown_for_speech(text: str) -> str:
    """Strip markdown formatting for TTS output."""
    text = re.sub(r'```[a-zA-Z0-9]*', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\*\*([^*]+)\*\*|__([^_]+)__', r'\1\2', text)
    text = re.sub(r'\*([^*]+)\*|_([^_]+)_', r'\1\2', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

@app.post("/api/voice/speak-file")
def speak_file(request: SpeakFileRequest):
    allowed_workspace = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ"
    allowed_home = os.path.join(os.path.expanduser("~"), ".gemini")
    
    normalized_path = os.path.abspath(request.path)
    is_allowed = normalized_path.lower().startswith(allowed_workspace.lower()) or normalized_path.lower().startswith(allowed_home.lower())
    
    if not is_allowed:
        raise HTTPException(status_code=403, detail="Access denied")
        
    if os.path.exists(normalized_path) and os.path.isfile(normalized_path):
        try:
            with open(normalized_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            cleaned = clean_markdown_for_speech(content)
            success = voice_bridge_api.speak(cleaned)
            return {"success": success}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read file: {e}")
            
    raise HTTPException(status_code=404, detail="File not found")

@app.post("/api/voice/abort")
def voice_abort():
    success = voice_bridge_api.abort()
    return {"success": success}


class ClientErrorRequest(BaseModel):
    message: str
    source: str = None
    lineno: int = None
    colno: int = None
    error: str = None

@app.post("/api/log/error")
def log_client_error(request: ClientErrorRequest):
    print(f"[Client JS Error] {request.message} at {request.source}:{request.lineno}:{request.colno}")
    if request.error:
        print(f"Details: {request.error}")
    sys.stdout.flush()
    return {"status": "ok"}

# --- Serve Static Frontend Files ---
# Mount CSS, JS, Assets directories
frontend_dir = os.path.join(chat_manager.aida_root, "frontend")
dist_dir = os.path.join(frontend_dir, "dist")
dist_assets_dir = os.path.join(dist_dir, "assets")

css_dir = os.path.join(frontend_dir, "css")
js_dir = os.path.join(frontend_dir, "js")
assets_dir = os.path.join(frontend_dir, "assets")

os.makedirs(css_dir, exist_ok=True)
os.makedirs(js_dir, exist_ok=True)
os.makedirs(assets_dir, exist_ok=True)

app.mount("/css", StaticFiles(directory=css_dir), name="css")
app.mount("/js", StaticFiles(directory=js_dir), name="js")

if os.path.exists(dist_assets_dir):
    app.mount("/assets", StaticFiles(directory=dist_assets_dir), name="assets")
else:
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

# DaVinci Resolve Assembly Webhook Router
class AssembleRequest(BaseModel):
    script: str
    brand: str

class ComputerUseRequest(BaseModel):
    task: str

@app.post("/api/computer-use")
def run_computer_use_endpoint(request: ComputerUseRequest, background_tasks: BackgroundTasks):
    print(f"[AIDA API] Received Computer Use request: '{request.task}'")
    
    script_path = os.path.join(parent_dir, "scripts", "computer_use_demo.py")
    if not os.path.exists(script_path):
        script_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\computer_use_demo.py"
        
    def execute_loop():
        workspace_dir = os.path.dirname(parent_dir)
        log_path = os.path.join(workspace_dir, "scripts", "computer_use.log")
        try:
            import subprocess
            with open(log_path, "w", encoding="utf-8") as log_file:
                subprocess.run(
                    [sys.executable, "-u", script_path, request.task],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    check=True
                )
            print("[AIDA API] Computer Use task completed successfully.")
        except Exception as e:
            print(f"[AIDA API] Error during Computer Use task: {e}")
            
    background_tasks.add_task(execute_loop)
    return {"status": "success", "message": "Computer Use task started in the background."}

@app.post("/api/davinci/assemble")
def davinci_assemble(request: AssembleRequest, background_tasks: BackgroundTasks):
    print(f"[AIDA Webhook] Received DaVinci Assemble: brand={request.brand}, script_len={len(request.script)}")
    
    script_path = os.path.join(parent_dir, "scripts", "build_long_001_timeline.py")
    if not os.path.exists(script_path):
        script_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\scripts\build_long_001_timeline.py"
        
    def run_assembly():
        try:
            import subprocess
            creation_flags = subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            subprocess.run([sys.executable, script_path], check=True, creationflags=creation_flags)
            print("[AIDA Webhook] DaVinci Resolve Assembly completed successfully.")
        except Exception as e:
            print(f"[AIDA Webhook] Error during DaVinci Resolve Assembly: {e}")
            
    background_tasks.add_task(run_assembly)
    return {"status": "success", "message": "DaVinci Resolve timeline assembly started in the background."}

# Root index route
@app.get("/")
def get_index():
    dist_index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(dist_index_path):
        return FileResponse(dist_index_path)
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found in frontend or dist directory"}

# Catch-all SPA route
@app.get("/{file_path:path}")
def get_static_file(file_path: str):
    if file_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
        
    dist_file_path = os.path.join(dist_dir, file_path)
    if os.path.exists(dist_file_path) and os.path.isfile(dist_file_path):
        return FileResponse(dist_file_path)
        
    dist_index_path = os.path.join(dist_dir, "index.html")
    if os.path.exists(dist_index_path):
        return FileResponse(dist_index_path)
        
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8421, log_level="warning")

