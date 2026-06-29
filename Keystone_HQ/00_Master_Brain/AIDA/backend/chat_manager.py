import os
import json
import re
import subprocess
from datetime import datetime

class ChatManager:
    def __init__(self):
        self.master_brain = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
        self.aida_root = os.path.join(self.master_brain, "AIDA")
        self.brain_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")
        self.voice_bridge_config_path = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json")
        self.agentapi_exe = os.path.join(
            os.path.expanduser("~"), "AppData", "Local", "Programs",
            "Antigravity", "resources", "bin", "language_server.exe"
        )
        self.cache_path = os.path.join(self.aida_root, "backend", "chat_names.json")
        self.projects_path = os.path.join(self.aida_root, "backend", "projects.json")
        
        # Ensure backend directory exists
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        
        # Load names cache
        self.names_cache = {}
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    self.names_cache = json.load(f)
            except Exception as e:
                print(f"Error loading chat names cache: {e}")
                self.names_cache = {}
        
        self._cached_limits = None
        self._last_limits_scrape_time = 0
                
        self.ag_projects_dir = os.path.join(os.path.expanduser("~"), ".gemini", "config", "projects")
        
        # Initialize default projects if empty
        self.projects = []
        self._load_projects_from_ag()
        
        # Caching for get_chats to eliminate 230+ folder stats lag
        self._chats_cache = None
        self._chats_cache_time = 0.0
        self._messages_cache = {} # {chat_id: (mtime, messages)}

    def _load_projects_from_ag(self):
        projects = []
        if os.path.exists(self.ag_projects_dir):
            for file in os.listdir(self.ag_projects_dir):
                if file.endswith(".json"):
                    path = os.path.join(self.ag_projects_dir, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            projects.append({
                                "id": data.get("id"),
                                "name": data.get("name")
                            })
                    except Exception as e:
                        print(f"Error loading project {file}: {e}")
        
        # Sort or add Chronos if missing
        has_chronos = any(p["name"] == "⏳ Chronos" for p in projects)
        if not has_chronos:
            projects.append({"id": "chronos", "name": "Project Chronos"})
            
        self.projects = projects

    def _save_projects(self):
        # We don't overwrite antigravity project files directly for now, 
        # let antigravity handle it, or we could. For now, pass.
        pass

    def get_projects(self) -> list:
        self._load_projects_from_ag()
        self.projects.sort(key=lambda x: x.get("name", "").lower())
        return self.projects

    def get_chronos_project_id(self) -> str:
        for p in self.get_projects():
            if "Chronos" in p.get("name", ""):
                return p["id"]
        return "chronos"

    def add_project(self, name: str) -> dict:
        project_id = name.lower().replace(" ", "_").replace("-", "_")
        # Ensure unique ID
        base_id = project_id
        counter = 1
        while any(p["id"] == project_id for p in self.projects):
            project_id = f"{base_id}_{counter}"
            counter += 1
            
        new_project = {"id": project_id, "name": name}
        self.projects.append(new_project)
        self._save_projects()
        return new_project

    def delete_project(self, project_id: str) -> bool:
        if project_id == "chronos":
            return False # Prevent deleting default
        initial_len = len(self.projects)
        self.projects = [p for p in self.projects if p["id"] != project_id]
        if len(self.projects) < initial_len:
            self._save_projects()
            return True
        return False

    def _save_names_cache(self):
        try:
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self.names_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving chat names cache: {e}")

    def _clean_text(self, text: str) -> str:
        # Strip XML/HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        # Remove markdown symbols and punctuation
        text = re.sub(r"[#*_`~[\]()\-+={}\.!,;?:\r\n]", " ", text)
        # Normalize whitespace
        text = " ".join(text.split())
        return text

    def _generate_name_from_text(self, text: str) -> str:
        cleaned = self._clean_text(text)
        words = cleaned.split()
        
        # Stopwords list
        stopwords = {
            "the", "a", "an", "to", "for", "of", "and", "or", "in", "on", "is", "are", 
            "was", "were", "be", "been", "with", "by", "at", "from", "as", "it", "this", 
            "that", "these", "those", "i", "you", "he", "she", "they", "we", "my", "your", 
            "his", "her", "their", "our", "me", "him", "them", "us", "get", "set", "up", 
            "once", "about", "what", "how", "why", "where", "when", "who", "which", "will", 
            "would", "should", "can", "could", "do", "does", "did", "doing", "go", "has",
            "have", "had", "just", "like", "more", "some", "any", "no", "yes"
        }
        
        filtered = [w for w in words if w.lower() not in stopwords]
        
        if len(filtered) >= 2:
            # Capitalize and join the first 3-4 significant words
            name = " ".join(w.capitalize() for w in filtered[:4])
        elif len(words) >= 1:
            name = " ".join(w.capitalize() for w in words[:4])
        else:
            name = "Unnamed Chat"
            
        # Truncate if too long
        if len(name) > 30:
            name = name[:27] + "..."
        return name

    def get_chats(self, force: bool = False) -> list:
        import time
        now = time.time()
        if force:
            if os.path.exists(self.cache_path):
                try:
                    with open(self.cache_path, "r", encoding="utf-8") as f:
                        self.names_cache = json.load(f)
                except Exception as e:
                    print(f"Error reloading chat names cache: {e}")

        # Load active chat ID
        active_chat_id = None
        if os.path.exists(self.voice_bridge_config_path):
            try:
                with open(self.voice_bridge_config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    active_chat_id = config.get("conversation_id")
            except Exception as e:
                print(f"Error reading voice bridge config: {e}")

        if not force and self._chats_cache is not None and (now - self._chats_cache_time) < 30.0:
            # Quick status update for active state
            for c in self._chats_cache:
                c["is_active"] = (c["id"] == active_chat_id)
                c["status"] = "online" if (c["id"] == active_chat_id) else "idle"
            return self._chats_cache

        chats = []
        cache_dirty = False

        # Get dynamic Chronos ID
        chronos_id = "chronos"
        for p in self.get_projects():
            if "Chronos" in p.get("name", ""):
                chronos_id = p["id"]
                break

        if not os.path.exists(self.brain_dir):
            return []

        # Phase 1: Collect all conversation folders with their mtimes (cheap stat calls)
        candidates = []
        for folder in os.listdir(self.brain_dir):
            folder_path = os.path.join(self.brain_dir, folder)
            if not os.path.isdir(folder_path):
                continue
                
            # Expect folder to be UUID
            if not re.match(r"^[0-9a-fA-F\-]{36}$", folder):
                continue

            # Skip folders marked as deleted
            if os.path.exists(os.path.join(folder_path, ".deleted")):
                continue

            transcript_path = os.path.join(folder_path, ".system_generated", "logs", "transcript_full.jsonl")
            if not os.path.exists(transcript_path):
                transcript_path = os.path.join(folder_path, ".system_generated", "logs", "transcript.jsonl")
            if not os.path.exists(transcript_path):
                continue

            try:
                mtime = os.path.getmtime(transcript_path)
            except Exception:
                mtime = 0

            candidates.append((folder, transcript_path, mtime))

        # Phase 2: Sort by newest first, only process top 25 to keep things fast
        candidates.sort(key=lambda x: x[2], reverse=True)
        candidates = candidates[:25]

        for folder, transcript_path, mtime in candidates:
            mtime_str = datetime.fromtimestamp(mtime).isoformat() if mtime else ""

            chat_id = folder
            chat_name = None
            created_at = None
            project_id = chronos_id # Default
            chat_model = "Gemini 3.5 Flash (High)" # Default

            # Get data from cache if available
            if chat_id in self.names_cache:
                chat_name = self.names_cache[chat_id].get("name")
                created_at = self.names_cache[chat_id].get("created_at")
                project_id = self.names_cache[chat_id].get("project_id", chronos_id)
                chat_model = self.names_cache[chat_id].get("model", "Gemini 3.5 Flash (High)")

            # Parse transcript to extract created_at and name if not cached
            first_user_content = ""
            last_message_preview = ""
            
            try:
                with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    
                if lines:
                    # Parse first line for created_at and starting prompt
                    try:
                        first_step = json.loads(lines[0])
                        if not created_at:
                            created_at = first_step.get("created_at")
                        if not chat_name:
                            first_user_content = first_step.get("content", "")
                    except Exception:
                        pass
                        
                    # Find last meaningful message for preview
                    # Scan backwards to find the last step with content or thinking
                    for line in reversed(lines):
                        try:
                            step = json.loads(line)
                            step_type = step.get("type", "")
                            
                            # Check content/thinking fields
                            content = step.get("content", "")
                            thinking = step.get("thinking", "")
                            
                            if content:
                                # Clean up formatting
                                content_clean = self._clean_text(content)
                                if content_clean:
                                    last_message_preview = content_clean[:80] + ("..." if len(content_clean) > 80 else "")
                                    break
                            elif thinking:
                                thinking_clean = self._clean_text(thinking)
                                if thinking_clean:
                                    last_message_preview = f"Thinking: {thinking_clean[:70]}" + ("..." if len(thinking_clean) > 70 else "")
                                    break
                            elif step_type == "CONVERSATION_HISTORY":
                                last_message_preview = "Conversation history loaded"
                                break
                        except Exception:
                            continue
            except Exception as e:
                print(f"Error reading transcript for {chat_id}: {e}")

            if not created_at:
                created_at = mtime_str

            if not chat_name:
                if first_user_content:
                    chat_name = self._generate_name_from_text(first_user_content)
                else:
                    chat_name = f"Chat {chat_id[:8]}"
                
                # Save to cache
                self.names_cache[chat_id] = {
                    "name": chat_name,
                    "created_at": created_at,
                    "project_id": project_id,
                    "model": chat_model
                }
                cache_dirty = True

            chats.append({
                "id": chat_id,
                "name": chat_name,
                "created_at": created_at,
                "modified_at": mtime_str,
                "mtime": mtime,
                "project_id": project_id,
                "is_active": (chat_id == active_chat_id),
                "status": "online" if (chat_id == active_chat_id) else "idle",
                "has_unread": False,
                "last_message_preview": last_message_preview or "No messages yet",
                "model": chat_model
            })

        if cache_dirty:
            self._save_names_cache()

        # Sort by mtime descending (newest activity first)
        chats.sort(key=lambda x: x["mtime"], reverse=True)

        # Save to cache
        self._chats_cache = chats
        self._chats_cache_time = now

        return chats

    def rename_chat(self, chat_id: str, new_name: str) -> bool:
        if chat_id in self.names_cache:
            self.names_cache[chat_id]["name"] = new_name
        else:
            # Try to fetch created_at from file
            created_at = None
            transcript_path = os.path.join(self.brain_dir, chat_id, ".system_generated", "logs", "transcript.jsonl")
            if os.path.exists(transcript_path):
                try:
                    with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                        first_line = f.readline()
                        if first_line:
                            first_step = json.loads(first_line)
                            created_at = first_step.get("created_at")
                except Exception:
                    pass
            
            if not created_at:
                created_at = datetime.utcnow().isoformat() + "Z"
                
            self.names_cache[chat_id] = {
                "name": new_name,
                "created_at": created_at,
                "project_id": self.get_chronos_project_id()
            }
            
        self._save_names_cache()
        self._chats_cache = None

        # Also write/update the .pbtxt annotation file for the IDE
        annotations_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "annotations")
        os.makedirs(annotations_dir, exist_ok=True)
        pbtxt_path = os.path.join(annotations_dir, f"{chat_id}.pbtxt")
        try:
            import time
            now_seconds = int(time.time())
            content = f'title:"{new_name}"  last_user_view_time:{{seconds:{now_seconds}  nanos:0}}'
            with open(pbtxt_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[ChatManager] Wrote title annotation '{new_name}' to {pbtxt_path}")
        except Exception as e:
            print(f"[ChatManager] Error writing annotation during rename: {e}")

        return True

    def delete_chat(self, chat_id: str) -> bool:
        import shutil
        
        # 1. Trigger the Electron UI archiving first to let the client handle it natively
        try:
            self._archive_electron_chat(chat_id)
        except Exception as e:
            print(f"[ChatManager] Error archiving chat in Electron UI: {e}")
            
        folder_path = os.path.join(self.brain_dir, chat_id)
        success = False
        
        # Delete the chat directory
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                success = True
            except Exception as e:
                print(f"Error deleting chat folder: {e}")
                # Write a sentinel file to mark it as deleted if locked on Windows
                try:
                    sentinel_path = os.path.join(folder_path, ".deleted")
                    with open(sentinel_path, "w", encoding="utf-8") as sf:
                        sf.write("deleted")
                except Exception as se:
                    print(f"Error writing deleted sentinel: {se}")
                
        # Delete SQLite database file
        db_path = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "conversations", f"{chat_id}.db")
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                success = True
            except Exception as e:
                print(f"Error deleting sqlite db file: {e}")
                
            # Clean up SQLite WAL and SHM files if they exist
            for ext in ["-wal", "-shm"]:
                ext_path = db_path + ext
                if os.path.exists(ext_path):
                    try:
                        os.remove(ext_path)
                    except Exception:
                        pass
                
        # Delete annotation pbtxt file
        pbtxt_path = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "annotations", f"{chat_id}.pbtxt")
        if os.path.exists(pbtxt_path):
            try:
                os.remove(pbtxt_path)
                success = True
            except Exception as e:
                print(f"Error deleting annotation file: {e}")
                
        # Remove from names cache
        if chat_id in self.names_cache:
            del self.names_cache[chat_id]
            self._save_names_cache()
            success = True
        self._chats_cache = None
            
        # If the deleted chat was the active targeted conversation, redirect to another
        active_chat_id = None
        if os.path.exists(self.voice_bridge_config_path):
            try:
                with open(self.voice_bridge_config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    active_chat_id = config.get("conversation_id")
            except Exception:
                pass
                
        if active_chat_id == chat_id:
            remaining_chats = []
            if os.path.exists(self.brain_dir):
                for folder in os.listdir(self.brain_dir):
                    f_path = os.path.join(self.brain_dir, folder)
                    if os.path.isdir(f_path) and re.match(r"^[0-9a-fA-F\-]{36}$", folder) and folder != chat_id:
                        remaining_chats.append(folder)
            
            if remaining_chats:
                self.switch_chat(remaining_chats[0])
            else:
                self.switch_chat("")
                
        return success

    def switch_chat(self, chat_id: str) -> bool:
        if not os.path.exists(self.voice_bridge_config_path):
            # Create a basic config file if it doesn't exist
            default_config = {
                "conversation_id": chat_id,
                "ls_address": "127.0.0.1:58852",
                "csrf_token": "",
                "project_id": ""
            }
            try:
                os.makedirs(os.path.dirname(self.voice_bridge_config_path), exist_ok=True)
                with open(self.voice_bridge_config_path, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2)
                self._switch_electron_chat(chat_id)
                return True
            except Exception as e:
                print(f"Error creating voice bridge config: {e}")
                return False

        try:
            with open(self.voice_bridge_config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            config["conversation_id"] = chat_id
            
            with open(self.voice_bridge_config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
                
            self._switch_electron_chat(chat_id)
            return True
        except Exception as e:
            print(f"Error updating voice bridge config: {e}")
            return False

    def _switch_electron_chat(self, chat_id: str) -> bool:
        try:
            import os
            import json
            import urllib.request
            from websocket import create_connection
            
            chat_info = self.names_cache.get(chat_id, {})
            chat_name = chat_info.get("name", "")
            
            appdata = os.environ.get("APPDATA", "")
            path = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
            if not os.path.exists(path):
                print(f"[ChatManager] DevToolsActivePort not found at {path}. Antigravity UI might not be running.")
                return False
                
            with open(path, "r") as f:
                content = f.read().splitlines()
                if not content:
                    return False
                port = content[0]
                
            url = f"http://127.0.0.1:{port}/json/list"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1.5) as response:
                targets = json.loads(response.read().decode())
                
            page_target = None
            for t in targets:
                if t.get('type') == 'page' and 'devtools' in t.get('webSocketDebuggerUrl', ''):
                    page_target = t
                    break
                    
            if not page_target:
                print("[ChatManager] No page target found in Electron DevTools.")
                return False
                
            ws_url = page_target['webSocketDebuggerUrl'].replace("localhost", "127.0.0.1")
            
            # JS to locate and click the chat link/item in Electron DOM
            js_switch_chat = r"""
            (() => {
                const chatId = "{chat_id}";
                const chatName = "{chat_name}";
                const sectionId = "02ec213a-7c20-4ec1-8396-ea46c276b1b1";
                
                // 1. Try to find link with chat ID in href
                const link = document.querySelector(`a[href*="${chatId}"]`);
                if (link) {
                    link.click();
                    return { success: true, method: "href_click" };
                }
                
                // 2. Try attribute matching
                const item = document.querySelector(`[data-chat-id="${chatId}"]`) || 
                             document.querySelector(`[data-testid="chat-item-${chatId}"]`);
                if (item) {
                    item.click();
                    return { success: true, method: "attribute_click" };
                }
                
                // 3. Search by text content of the chat name
                if (chatName) {
                    const elements = Array.from(document.querySelectorAll('button, a, div, span'));
                    const targetEl = elements.find(el => {
                        const text = (el.innerText || el.textContent || '').trim().replace(/\r?\n/g, ' ');
                        return text === chatName || text.includes(chatName);
                    });
                    if (targetEl) {
                        targetEl.click();
                        return { success: true, method: "text_click" };
                    }
                }
                
                // 4. Fallback disabled to prevent Electron reload loops and crashing
                return { success: false, error: "Chat tab not visible in DOM, skipping navigation fallback." };
            })()
            """.replace("{chat_id}", chat_id).replace("{chat_name}", chat_name)
            
            ws = create_connection(ws_url, suppress_origin=True, timeout=2.0)
            try:
                payload = {
                    "id": 45,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": js_switch_chat,
                        "awaitPromise": True,
                        "returnByValue": True
                    }
                }
                ws.send(json.dumps(payload))
                result = ws.recv()
                res_data = json.loads(result)
                val = res_data.get('result', {}).get('result', {}).get('value', {})
                print(f"[ChatManager] Electron chat switch result: {val}")
                return val.get('success', False)
            finally:
                ws.close()
        except Exception as e:
            import traceback
            print(traceback.format_exc(), flush=True)
            print(f"[ChatManager] Failed to switch Electron chat: {e}", flush=True)
            return False

    def _archive_electron_chat(self, chat_id: str) -> bool:
        try:
            import os
            import json
            import urllib.request
            from websocket import create_connection
            
            appdata = os.environ.get("APPDATA", "")
            path = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
            if not os.path.exists(path):
                print(f"[ChatManager] DevToolsActivePort not found at {path}. Antigravity UI might not be running.")
                return False
                
            with open(path, "r") as f:
                content = f.read().splitlines()
                if not content:
                    return False
                port = content[0]
                
            url = f"http://127.0.0.1:{port}/json/list"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1.5) as response:
                targets = json.loads(response.read().decode())
                
            page_target = None
            for t in targets:
                if t.get('type') == 'page' and 'devtools' in t.get('webSocketDebuggerUrl', ''):
                    page_target = t
                    break
                    
            if not page_target:
                print("[ChatManager] No page target found in Electron DevTools.")
                return False
                
            ws_url = page_target['webSocketDebuggerUrl'].replace("localhost", "127.0.0.1")
            
            js_archive = r"""
            (async () => {
                const pill = document.querySelector(`[data-testid="convo-pill-{chat_id}"]`);
                if (!pill) return { error: "Pill not found in DOM" };
                
                const lvl3 = pill.parentElement.parentElement.parentElement;
                const shrink0 = lvl3.children[1];
                if (!shrink0) return { error: "shrink0 container not found" };
                
                const buttons = Array.from(shrink0.querySelectorAll('button'));
                if (buttons.length < 3) return { error: "Archive button not found" };
                
                buttons[2].click();
                
                await new Promise(resolve => setTimeout(resolve, 300));
                
                const modalButtons = Array.from(document.querySelectorAll('button, div'));
                const confirmBtn = modalButtons.find(el => {
                    const text = (el.innerText || el.textContent || '').trim().toLowerCase();
                    return text === 'confirm' || text === 'archive' || text === 'yes';
                });
                
                if (confirmBtn) {
                    confirmBtn.click();
                    return { success: true, message: "Clicked confirm button" };
                }
                
                return { success: true, message: "Archived" };
            })()
            """.replace("{chat_id}", chat_id)
            
            ws = create_connection(ws_url, suppress_origin=True, timeout=2.0)
            try:
                payload = {
                    "id": 145,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": js_archive,
                        "awaitPromise": True,
                        "returnByValue": True
                    }
                }
                ws.send(json.dumps(payload))
                result = ws.recv()
                res_data = json.loads(result)
                val = res_data.get('result', {}).get('result', {}).get('value', {})
                print(f"[ChatManager] Electron UI archiving result for {chat_id}: {val}")
                return val.get('success', False)
            finally:
                ws.close()
        except Exception as e:
            print(f"[ChatManager] Failed to archive Electron chat {chat_id}: {e}", flush=True)
            return False

    def _switch_electron_model(self, target_model: str) -> bool:
        try:
            import os
            import json
            import urllib.request
            from websocket import create_connection
            
            appdata = os.environ.get("APPDATA", "")
            path = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
            if not os.path.exists(path):
                print(f"[ChatManager] DevToolsActivePort not found at {path}. Antigravity UI might not be running.")
                return False
                
            with open(path, "r") as f:
                content = f.read().splitlines()
                if not content:
                    return False
                port = content[0]
                
            url = f"http://127.0.0.1:{port}/json/list"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1.5) as response:
                targets = json.loads(response.read().decode())
                
            page_target = None
            for t in targets:
                if t.get('type') == 'page' and 'devtools' in t.get('webSocketDebuggerUrl', ''):
                    page_target = t
                    break
                    
            if not page_target:
                print("[ChatManager] No page target found in Electron DevTools.")
                return False
                
            ws_url = page_target['webSocketDebuggerUrl'].replace("localhost", "127.0.0.1")
            
            # JS to open dropdown, select model, and close dropdown
            js_switch = r"""
            (() => {
                const btn = document.querySelector('button[aria-label^="Select model"]');
                if (!btn) return Promise.resolve({ error: "Dropdown button not found" });
                
                btn.click();
                
                return new Promise((resolve) => {
                    setTimeout(() => {
                        const options = Array.from(document.querySelectorAll('button'));
                        const targetOpt = options.find(opt => {
                            const text = (opt.innerText || opt.textContent || '').trim().replace(/\r?\n/g, ' ');
                            return text.includes("{target_model}");
                        });
                        
                        if (targetOpt) {
                            targetOpt.click();
                            resolve({ success: true, model: "{target_model}" });
                        } else {
                            const event = new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, code: 'Escape', bubbles: true });
                            document.dispatchEvent(event);
                            resolve({ error: "Option '{target_model}' not found in dropdown" });
                        }
                    }, 150);
                });
            })()
            """.replace("{target_model}", target_model)
            
            ws = create_connection(ws_url, suppress_origin=True, timeout=2.0)
            try:
                payload = {
                    "id": 42,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": js_switch,
                        "awaitPromise": True,
                        "returnByValue": True
                    }
                }
                ws.send(json.dumps(payload))
                result = ws.recv()
                res_data = json.loads(result)
                val = res_data.get('result', {}).get('result', {}).get('value', {})
                print(f"[ChatManager] Electron model switch result: {val}")
                return val.get('success', False)
            finally:
                ws.close()
        except Exception as e:
            import traceback
            print(traceback.format_exc(), flush=True)
            print(f"[ChatManager] Failed to switch Electron model: {e}", flush=True)
            return False

    def refresh_mcp_servers(self) -> bool:
        try:
            import os
            import json
            import urllib.request
            import time
            from websocket import create_connection
            
            appdata = os.environ.get("APPDATA", "")
            path = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
            if not os.path.exists(path):
                print("[ChatManager] DevToolsActivePort not found. Antigravity UI might not be running.", flush=True)
                return False
                
            with open(path, "r") as f:
                content = f.read().splitlines()
                if not content:
                    return False
                port = content[0]
                
            url = f"http://127.0.0.1:{port}/json/list"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1.5) as response:
                targets = json.loads(response.read().decode())
                
            page_target = None
            for t in targets:
                if t.get('type') == 'page' and 'devtools' in t.get('webSocketDebuggerUrl', ''):
                    page_target = t
                    break
                    
            if not page_target:
                print("[ChatManager] No page target found in Electron DevTools.", flush=True)
                return False
                
            ws_url = page_target['webSocketDebuggerUrl'].replace("localhost", "127.0.0.1")
            
            js_refresh = r"""
            (() => {
                const customizationsTabOpen = document.querySelector('[data-testid="settings-nav-item-Customizations"]');
                if (customizationsTabOpen) {
                    customizationsTabOpen.click();
                    return new Promise((resolve) => {
                        setTimeout(() => {
                            const buttons = Array.from(document.querySelectorAll('button'));
                            const refreshBtn = buttons.find(btn => {
                                const text = (btn.innerText || btn.textContent || '').trim();
                                const title = btn.getAttribute('title') || '';
                                return text === 'Refresh' && !title.includes('quota') && !title.includes('credits');
                            });
                            if (!refreshBtn) {
                                resolve({ error: "MCP Refresh button not found" });
                                return;
                            }
                            refreshBtn.click();
                            resolve({ success: true, alreadyOpen: true });
                        }, 800);
                    });
                }

                const settingsBtn = document.querySelector('[data-testid="settings-button"]');
                if (!settingsBtn) {
                    return Promise.resolve({ error: "Settings button not found" });
                }
                settingsBtn.click();
                
                return new Promise((resolve) => {
                    setTimeout(() => {
                        const customizationsTab = document.querySelector('[data-testid="settings-nav-item-Customizations"]');
                        if (!customizationsTab) {
                            resolve({ error: "Customizations tab button not found" });
                            return;
                        }
                        customizationsTab.click();
                        
                        setTimeout(() => {
                            const buttons = Array.from(document.querySelectorAll('button'));
                            const refreshBtn = buttons.find(btn => {
                                const text = (btn.innerText || btn.textContent || '').trim();
                                const title = btn.getAttribute('title') || '';
                                return text === 'Refresh' && !title.includes('quota') && !title.includes('credits');
                            });
                            
                            if (!refreshBtn) {
                                resolve({ error: "MCP Refresh button not found" });
                                return;
                            }
                            
                            refreshBtn.click();
                            resolve({ success: true, alreadyOpen: false });
                        }, 800);
                    }, 800);
                });
            })()
            """
            
            ws = create_connection(ws_url, suppress_origin=True, timeout=3.0)
            try:
                payload = {
                    "id": 43,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": js_refresh,
                        "awaitPromise": True,
                        "returnByValue": True
                    }
                }
                ws.send(json.dumps(payload))
                result = ws.recv()
                res_data = json.loads(result)
                val = res_data.get('result', {}).get('result', {}).get('value', {})
                print(f"[ChatManager] MCP refresh trigger result: {val}", flush=True)
                
                # Only close settings if we were the ones who opened it
                if val.get('success') and not val.get('alreadyOpen', False):
                    # Wait 1 second before closing settings to let the click execute/render
                    time.sleep(1.0)
                    
                    close_payload = {
                        "id": 44,
                        "method": "Runtime.evaluate",
                        "params": {
                            "expression": r"""
                            (() => {
                                const closeBtn = document.querySelector('[data-testid="close-settings-button"]') || 
                                                 document.querySelector('[aria-label="Close"]') || 
                                                 document.querySelector('button[title="Close"]');
                                if (closeBtn) {
                                    closeBtn.click();
                                    return { success: true, method: "click" };
                                }
                                const event = new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, code: 'Escape', bubbles: true });
                                document.dispatchEvent(event);
                                return { success: true, method: "escape" };
                            })()
                            """,
                            "returnByValue": True
                        }
                    }
                    ws.send(json.dumps(close_payload))
                    ws.recv()
                
                return val.get('success', False) or 'success' in val
            finally:
                ws.close()
        except Exception as e:
            import traceback
            print(traceback.format_exc(), flush=True)
            print(f"[ChatManager] Failed to trigger MCP refresh: {e}", flush=True)
            return False

    def set_chat_model(self, chat_id: str, model: str) -> bool:
        if chat_id in self.names_cache:
            self.names_cache[chat_id]["model"] = model
        else:
            created_at = datetime.utcnow().isoformat() + "Z"
            self.names_cache[chat_id] = {
                "name": f"Chat {chat_id[:8]}",
                "created_at": created_at,
                "project_id": self.get_chronos_project_id(),
                "model": model
            }
        self._save_names_cache()
        self._chats_cache = None
        
        # SQLite hack: dynamically change the model in the active conversation DB
        db_path = os.path.join(self.brain_dir, "conversations", f"{chat_id}.db")
        if os.path.exists(db_path):
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("SELECT data FROM executor_metadata")
                row = cur.fetchone()
                if row and row[0]:
                    data = bytearray(row[0])
                    # Common model strings used by Antigravity under the hood
                    known_models = [
                        b'gemini-3.1-pro-low',
                        b'gemini-pro-agent',
                        b'gemini-3.5-flash',
                        b'gemini-2.0-flash-exp'
                    ]
                    
                    # Target model string based on AIDA selection
                    target = b'gemini-3.5-flash'
                    model_lower = model.lower()
                    if "pro" in model_lower or "sonnet" in model_lower or "opus" in model_lower or "gpt" in model_lower:
                        target = b'gemini-pro-agent'
                    elif "lite" in model_lower or "haiku" in model_lower or "mini" in model_lower:
                        target = b'gemini-3.1-pro-low'
                        
                    for km in known_models:
                        idx = data.find(km)
                        if idx > 0:
                            # Verify length prefix byte matches the string length
                            if data[idx-1] == len(km):
                                new_data = data[:idx-1] + bytes([len(target)]) + target + data[idx+len(km):]
                                cur.execute("UPDATE executor_metadata SET data=?", (new_data,))
                                conn.commit()
                                break
                conn.close()
            except Exception as e:
                print(f"Error updating SQLite model for {chat_id}: {e}")

        # Programmatically sync the active model to the running Electron UI window via CDP!
        self._switch_electron_model(model)

        return True

    def get_model_limits(self) -> dict:
        default_limits = {
            "credit_overage": True,
            "gemini_weekly": 86,
            "gemini_weekly_text": "You have used some of your weekly limit, it will fully refresh in 3 days, 2 hours.",
            "gemini_5hour": 91,
            "gemini_5hour_text": "You have used some of your 5-hour limit, it will fully refresh in 4 hours, 32 minutes.",
            "claude_weekly": 14,
            "claude_weekly_text": "You have used some of your weekly limit, it will fully refresh in 13 hours, 20 minutes.",
            "claude_5hour": 100,
            "claude_5hour_text": "You have not used any of your 5-hour limit."
        }
        
        # Caching logic to prevent constant settings window popping up
        import time
        now = time.time()
        # Cache for 1 hour (3600 seconds)
        if hasattr(self, '_cached_limits') and self._cached_limits and (now - getattr(self, '_last_limits_scrape_time', 0) < 3600):
            return self._cached_limits

        try:
            import os
            import json
            import urllib.request
            from websocket import create_connection
            
            appdata = os.environ.get("APPDATA", "")
            path = os.path.join(appdata, "Antigravity", "DevToolsActivePort")
            if not os.path.exists(path):
                return default_limits
                
            with open(path, "r") as f:
                content = f.read().splitlines()
                if not content:
                    return default_limits
                port = content[0]
                
            url = f"http://127.0.0.1:{port}/json/list"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1.5) as response:
                targets = json.loads(response.read().decode())
                
            page_target = None
            for t in targets:
                if t.get('type') == 'page' and 'devtools' in t.get('webSocketDebuggerUrl', ''):
                    page_target = t
                    break
                    
            if not page_target:
                return default_limits
                
            ws_url = page_target['webSocketDebuggerUrl'].replace("localhost", "127.0.0.1")
            
            js_scrape = r"""
            (() => {
                return new Promise((resolve) => {
                    function openModelsTab(callback) {
                        const activeTab = document.querySelector('[data-testid="settings-nav-item-Models"][class*="active"]') ||
                                          document.querySelector('[data-testid="settings-nav-item-Models"][class*="bg-select-item-background"]');
                        if (activeTab) {
                            callback();
                            return;
                        }
                        
                        const settingsBtn = document.querySelector('[data-testid="settings-button"]');
                        if (!settingsBtn) {
                            const modelsTab = document.querySelector('[data-testid="settings-nav-item-Models"]');
                            if (modelsTab) {
                                modelsTab.click();
                                setTimeout(callback, 500);
                            } else {
                                resolve({ error: "Settings button not found" });
                            }
                            return;
                        }
                        
                        settingsBtn.click();
                        setTimeout(() => {
                            const modelsTab = document.querySelector('[data-testid="settings-nav-item-Models"]');
                            if (!modelsTab) {
                                resolve({ error: "Models tab not found" });
                                return;
                            }
                            modelsTab.click();
                            
                            let attempts = 0;
                            const checkInterval = setInterval(() => {
                                const hasPercentages = Array.from(document.querySelectorAll('span, div')).some(el => /^\d+%$/.test((el.innerText || '').trim()) && el.children.length === 0);
                                attempts++;
                                if (hasPercentages || attempts > 10) {
                                    clearInterval(checkInterval);
                                    callback();
                                }
                            }, 100);
                        }, 500);
                    }

                    openModelsTab(() => {
                        try {
                            const results = {
                                credit_overage: true,
                                gemini_weekly: 86,
                                gemini_weekly_text: "You have used some of your weekly limit, it will fully refresh in 3 days, 2 hours.",
                                gemini_5hour: 91,
                                gemini_5hour_text: "You have used some of your 5-hour limit, it will fully refresh in 4 hours, 32 minutes.",
                                claude_weekly: 14,
                                claude_weekly_text: "You have used some of your weekly limit, it will fully refresh in 13 hours, 20 minutes.",
                                claude_5hour: 100,
                                claude_5hour_text: "You have not used any of your 5-hour limit."
                            };
                            
                            const toggle = document.querySelector('[role="switch"]') || document.querySelector('input[type="checkbox"]');
                            if (toggle) {
                                results.credit_overage = toggle.getAttribute('aria-checked') === 'true' || toggle.checked || false;
                            }
                            
                            const pctSpans = Array.from(document.querySelectorAll('span')).filter(el => {
                                const txt = el.innerText.trim();
                                return /^\d+%$/.test(txt) && el.className.includes('text-right');
                            });
                            
                            if (pctSpans.length >= 1) {
                                const el = pctSpans[0];
                                results.gemini_weekly = parseInt(el.innerText);
                                const row = el.parentElement.parentElement;
                                const texts = Array.from(row.querySelectorAll('span, div, p'))
                                    .map(e => e.innerText.trim())
                                    .filter(t => t && !t.includes('%') && t !== 'Weekly Limit' && t !== 'Five Hour Limit');
                                if (texts.length > 0) results.gemini_weekly_text = texts[0];
                            }
                            if (pctSpans.length >= 2) {
                                const el = pctSpans[1];
                                results.gemini_5hour = parseInt(el.innerText);
                                const row = el.parentElement.parentElement;
                                const texts = Array.from(row.querySelectorAll('span, div, p'))
                                    .map(e => e.innerText.trim())
                                    .filter(t => t && !t.includes('%') && t !== 'Weekly Limit' && t !== 'Five Hour Limit');
                                if (texts.length > 0) results.gemini_5hour_text = texts[0];
                            }
                            if (pctSpans.length >= 3) {
                                const el = pctSpans[2];
                                results.claude_weekly = parseInt(el.innerText);
                                const row = el.parentElement.parentElement;
                                const texts = Array.from(row.querySelectorAll('span, div, p'))
                                    .map(e => e.innerText.trim())
                                    .filter(t => t && !t.includes('%') && t !== 'Weekly Limit' && t !== 'Five Hour Limit');
                                if (texts.length > 0) results.claude_weekly_text = texts[0];
                            }
                            if (pctSpans.length >= 4) {
                                const el = pctSpans[3];
                                results.claude_5hour = parseInt(el.innerText);
                                const row = el.parentElement.parentElement;
                                const texts = Array.from(row.querySelectorAll('span, div, p'))
                                    .map(e => e.innerText.trim())
                                    .filter(t => t && !t.includes('%') && t !== 'Weekly Limit' && t !== 'Five Hour Limit');
                                if (texts.length > 0) results.claude_5hour_text = texts[0];
                            }
                            
                            const closeBtn = document.querySelector('[data-testid="settings-close-button"]') || document.querySelector('button[aria-label="Close"]');
                            if (closeBtn) {
                                closeBtn.click();
                            } else {
                                const event = new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27, code: 'Escape', bubbles: true });
                                document.dispatchEvent(event);
                            }
                            
                            resolve(results);
                        } catch (e) {
                            resolve({ error: e.toString() });
                        }
                    });
                });
            })()
            """
            
            ws = create_connection(ws_url, suppress_origin=True, timeout=5.0)
            try:
                payload = {
                    "id": 45,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": js_scrape,
                        "awaitPromise": True,
                        "returnByValue": True
                    }
                }
                ws.send(json.dumps(payload))
                result = ws.recv()
                res_data = json.loads(result)
                val = res_data.get('result', {}).get('result', {}).get('value', {})
                if isinstance(val, dict) and "error" not in val:
                    # Clean up description texts by stripping label prefixes
                    for key in ["gemini_weekly_text", "gemini_5hour_text", "claude_weekly_text", "claude_5hour_text"]:
                        if key in val and val[key]:
                            t = val[key]
                            t = t.replace("Weekly Limit\n", "").replace("Weekly Limit", "")
                            t = t.replace("Five Hour Limit\n", "").replace("Five Hour Limit", "")
                            t = t.strip()
                            val[key] = t
                    self._cached_limits = val
                    self._last_limits_scrape_time = now
                    return val
                
                self._cached_limits = default_limits
                self._last_limits_scrape_time = now - 3600 + 60 # Retry in 60s
                return default_limits
            finally:
                ws.close()
        except Exception as e:
            print(f"[ChatManager] Failed to get model limits: {e}")
            self._cached_limits = default_limits
            self._last_limits_scrape_time = now - 3600 + 60 # Retry in 60s
            return default_limits

    def commit_learning(self, tried: str, wrong_because: str, fix: str, category: str, severity: str, chat_id: str = None) -> str:
        import uuid
        import sys
        
        # 1. Add to correction journal (.learnings/correction_journal.json)
        # We write directly to ensure both "wrong_because" and "error" are populated
        journal_path = os.path.join(self.master_brain, ".learnings", "correction_journal.json")
        try:
            if os.path.exists(journal_path):
                with open(journal_path, "r", encoding="utf-8") as f:
                    journal = json.load(f)
            else:
                journal = []
        except Exception:
            journal = []
            
        rule_uuid = uuid.uuid4().hex[:8]
        entry_id = f"CJ-{rule_uuid}"
        
        entry = {
            "id": entry_id,
            "tried": tried,
            "wrong_because": wrong_because,
            "error": f"[{category}] {wrong_because}",
            "fix": fix,
            "prevention": fix,
            "prevention_rule": fix,
            "category": category,
            "severity": severity,
            "agent": "master",
            "timestamp": datetime.now().isoformat(),
            "resolved": True,
            "skill_updated": False
        }
        journal.append(entry)
        
        # Save journal
        try:
            with open(journal_path, "w", encoding="utf-8") as f:
                json.dump(journal, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving correction journal: {e}")
            
        # 2. Trigger evolve() from scripts/self_evolution.py
        try:
            scripts_path = os.path.join(self.master_brain, "scripts")
            if self.master_brain not in sys.path:
                sys.path.insert(0, self.master_brain)
            if scripts_path not in sys.path:
                sys.path.insert(0, scripts_path)
            from scripts.self_evolution import evolve
            evolve()
        except Exception as e:
            print(f"Error calling evolve: {e}")

        # 3. Read target skill file based on active chat's project_id
        # Scan foundation skill to get highest rule number across the system
        foundation_dir = os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills", "00_keystone_foundation")
        foundation_path = os.path.join(foundation_dir, "SKILL.md")
        
        highest_rule_num = 38
        if os.path.exists(foundation_path):
            try:
                with open(foundation_path, "r", encoding="utf-8") as f:
                    found_content = f.read()
                rule_nums = [int(num) for num in re.findall(r"\[PR-(\d+)\]", found_content)]
                if rule_nums:
                    highest_rule_num = max(rule_nums)
            except Exception:
                pass
                
        next_num = highest_rule_num + 1
        rule_id = f"PR-{next_num:03d}"
        
        # Determine target skill directory based on active chat's project_id
        target_skill_dir = "00_keystone_foundation"
        if chat_id and chat_id in self.names_cache:
            p_id = self.names_cache[chat_id].get("project_id")
            if p_id == "6ae51756-6b7f-408d-bba5-0ebb98a1c173":
                target_skill_dir = "02_possibilities_brand"
            elif p_id == "a581830e-c700-4716-bde1-2908591bc4bf":
                target_skill_dir = "05_protocol_script_studio"
            elif p_id == "649e6bdc-08b0-4778-92b9-14486c1d005f":
                target_skill_dir = "08_music_brand"
                
        target_dir = os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills", target_skill_dir)
        target_path = os.path.join(target_dir, "SKILL.md")
        
        if os.path.exists(target_path):
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Format category to snake_case
                clean_category = category.lower().replace(" ", "_").replace("-", "_")
                
                # Format new rule line
                new_rule_line = f"- **[{rule_id}]** (!! {severity.upper()}) `{clean_category}`: {fix}"
                
                # Insert rule and update timestamp
                lines = content.splitlines()
                
                # Find if Learned Prevention Rules section exists
                rules_section_idx = -1
                for idx, line in enumerate(lines):
                    if "Learned Prevention Rules" in line:
                        rules_section_idx = idx
                        break
                        
                if rules_section_idx == -1:
                    # Append rules section to the end of the file
                    lines.append("")
                    lines.append("## Learned Prevention Rules")
                    lines.append("")
                    lines.append("> These rules were automatically extracted from the correction journal.")
                    lines.append("> They encode hard-won operational lessons. DO NOT remove them.")
                    lines.append("")
                    lines.append(new_rule_line)
                    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                    lines.append("")
                    lines.append(f"_Last updated: {now_str}_")
                else:
                    # Find where the last updated timestamp is
                    last_updated_idx = -1
                    for idx in range(rules_section_idx + 1, len(lines)):
                        if "_Last updated:" in lines[idx]:
                            last_updated_idx = idx
                            break
                            
                    if last_updated_idx != -1:
                        # Insert right before the last updated timestamp
                        inserted_lines = [new_rule_line]
                        lines[last_updated_idx:last_updated_idx] = inserted_lines
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                        new_last_updated_idx = last_updated_idx + 1
                        lines[new_last_updated_idx] = f"_Last updated: {now_str}_"
                    else:
                        lines.append(new_rule_line)
                        now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                        lines.append(f"_Last updated: {now_str}_")
                
                new_content = "\n".join(lines)
                with open(target_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                    
            except Exception as e:
                print(f"Error updating target SKILL.md: {e}")
                
        # 4. Save detailed Markdown file under .learnings/insights/
        today_date = datetime.now().strftime("%Y-%m-%d")
        summary_slug = tried[:30].lower().replace(" ", "_").replace("-", "_")
        summary_slug = re.sub(r'[^a-z0-9_]', '', summary_slug)
        insight_filename = f"insight_{today_date}_{rule_id.lower()}_{summary_slug}.md"
        insight_dir = os.path.join(self.master_brain, ".learnings", "insights")
        os.makedirs(insight_dir, exist_ok=True)
        insight_path = os.path.join(insight_dir, insight_filename)
        
        insight_content = f"""# Insight: Rule {rule_id} ({category.capitalize()})

**Date:** {today_date}  
**Domain:** {category}  
**Severity:** {severity.upper()}  
**Rule ID:** {rule_id}  
**Chat Context ID:** {chat_id or "N/A"}  

## Tried / Scenario
{tried}

## Wrong Because / Issue
{wrong_because}

## Fix / Prevention Rule
{fix}
"""
        try:
            with open(insight_path, "w", encoding="utf-8") as f:
                f.write(insight_content)
        except Exception as e:
            print(f"Error saving insight markdown file: {e}")
            
        return rule_id

    def extract_chat_correction(self, chat_id: str) -> dict:
        messages = self.get_messages(chat_id)
        if not messages:
            return {"tried": "", "wrong_because": "", "fix": ""}
            
        last_user = ""
        last_assistant = ""
        prev_user = ""
        prev_assistant = ""
        
        for msg in reversed(messages):
            sender = msg.get("sender")
            content = msg.get("content", "").strip()
            if sender == "user":
                if not last_user:
                    last_user = content
                elif not prev_user:
                    prev_user = content
            elif sender == "assistant":
                if msg.get("is_thinking"):
                    continue
                if not last_assistant:
                    last_assistant = content
                elif not prev_assistant:
                    prev_assistant = content
                    
        tried = ""
        fix = ""
        
        if messages and messages[-1].get("sender") == "user":
            fix = messages[-1].get("content", "")
            for m in reversed(messages[:-1]):
                if m.get("sender") == "assistant" and not m.get("is_thinking"):
                    tried = m.get("content", "")
                    break
        else:
            if last_user:
                fix = last_user
            if prev_assistant:
                tried = prev_assistant
            elif last_assistant:
                tried = last_assistant
                
        if len(tried) > 500:
            tried = tried[:497] + "..."
        if len(fix) > 300:
            fix = fix[:297] + "..."
            
        return {
            "tried": tried,
            "wrong_because": "",
            "fix": fix
        }
    def _patch_conversation_project(self, chat_id: str, specific_project_id: str, target_project_id: str, project_name: str):
        # 1. Update the SQLite database
        db_path = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "conversations", f"{chat_id}.db")
        if os.path.exists(db_path):
            try:
                import sqlite3
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = [r[0] for r in cursor.fetchall()]
                
                # Dynamically discover the actual project ID stored in trajectory_meta
                actual_project_id = None
                if "trajectory_meta" in tables:
                    cursor.execute("SELECT * FROM trajectory_meta")
                    meta_row = cursor.fetchone()
                    if meta_row:
                        actual_project_id = meta_row[0]
                
                # Fallback to specific_project_id if table is missing or empty
                project_to_replace = actual_project_id or specific_project_id
                
                print(f"[ChatManager] Database {chat_id}.db: Replacing project ID '{project_to_replace}' with '{target_project_id}'")
                
                specific_uuid = project_to_replace.encode('utf-8')
                target_uuid = target_project_id.encode('utf-8')
                
                for t in tables:
                    cursor.execute(f"PRAGMA table_info({t});")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    cursor.execute(f"SELECT rowid, * FROM {t};")
                    rows = cursor.fetchall()
                    
                    for row in rows:
                        rowid = row[0]
                        vals = row[1:]
                        updates = {}
                        for col_idx, val in enumerate(vals):
                            col_name = columns[col_idx]
                            if isinstance(val, bytes):
                                if specific_uuid in val:
                                    updates[col_name] = val.replace(specific_uuid, target_uuid)
                            elif isinstance(val, str):
                                if project_to_replace in val:
                                    updates[col_name] = val.replace(project_to_replace, target_project_id)
                                    
                        if updates:
                            set_clause = ", ".join([f"{col} = ?" for col in updates.keys()])
                            sql = f"UPDATE {t} SET {set_clause} WHERE rowid = ?;"
                            params = list(updates.values()) + [rowid]
                            cursor.execute(sql, params)
                            
                conn.commit()
                conn.close()
                print(f"[ChatManager] Patched SQLite project ID from {specific_project_id} to {target_project_id}")
            except Exception as e:
                print(f"[ChatManager] Error patching SQLite: {e}")

        # 2. Write the .pbtxt annotation file
        annotations_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "annotations")
        os.makedirs(annotations_dir, exist_ok=True)
        pbtxt_path = os.path.join(annotations_dir, f"{chat_id}.pbtxt")
        try:
            import time
            now_seconds = int(time.time())
            content = f'title:"{project_name}"  last_user_view_time:{{seconds:{now_seconds}  nanos:0}}'
            with open(pbtxt_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[ChatManager] Wrote title annotation '{project_name}' to {pbtxt_path}")
        except Exception as e:
            print(f"[ChatManager] Error writing annotation: {e}")

    def new_chat(self, model: str, project_id: str = "chronos", initial_prompt: str = "Hello") -> dict:
        if project_id == "chronos":
            project_id = self.get_chronos_project_id()
        # 1. Discover live credentials
        creds = self._discover_ls_credentials()
        env = {
            **os.environ,
            "ANTIGRAVITY_AGENT": "1",
            "ANTIGRAVITY_LS_ADDRESS": creds.get("ls_address", "127.0.0.1:65235"),
            "ANTIGRAVITY_CSRF_TOKEN": creds.get("csrf_token", ""),
        }
        
        # 2. Map user-friendly model name to backend model code (flash_lite | flash | pro)
        mapped_model = "flash"
        model_lower = model.lower()
        if "pro" in model_lower or "sonnet" in model_lower or "opus" in model_lower or "gpt" in model_lower:
            mapped_model = "pro"
        elif "lite" in model_lower or "low" in model_lower:
            mapped_model = "flash_lite"
            
        print(f"[ChatManager] Creating new chat with model={mapped_model} (mapped from {model})...")
        
        try:
            # 3. Create conversation using language server agentapi
            cmd = [self.agentapi_exe, "agentapi", "new-conversation", f"--model={mapped_model}", initial_prompt]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True, encoding="utf-8", errors="replace",
                env=env, creationflags=subprocess.CREATE_NO_WINDOW
            )
            output = json.loads(result.stdout)
            conv_id = output.get("response", {}).get("newConversation", {}).get("conversationId")
            if not conv_id:
                raise Exception("No conversation ID returned by agentapi new-conversation")
                
            created_at = datetime.utcnow().isoformat() + "Z"
            
            # Write default conversation starter to transcript.jsonl if not created
            folder_path = os.path.join(self.brain_dir, conv_id)
            log_dir = os.path.join(folder_path, ".system_generated", "logs")
            os.makedirs(log_dir, exist_ok=True)
            transcript_path = os.path.join(log_dir, "transcript.jsonl")
            
            if not os.path.exists(transcript_path):
                starter = {
                    "step_index": 0,
                    "source": "SYSTEM",
                    "type": "CONVERSATION_HISTORY",
                    "content": "Conversation started.",
                    "created_at": created_at
                }
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(json.dumps(starter) + "\n")
                    
            # 4. Save metadata to cache
            project_name = "New Chat"
            for p in self.get_projects():
                if p["id"] == project_id:
                    project_name = p["name"]
                    break
            clean_project_name = project_name.replace("⏳", "").replace("🎵", "").strip()

            # Patch SQLite project ID to Chronos so it is visible in the desktop app sidebar,
            # but keep AIDA's internal mapping to the target project_id in cache.
            self._patch_conversation_project(conv_id, project_id, self.get_chronos_project_id(), clean_project_name)

            self.names_cache[conv_id] = {
                "name": clean_project_name,
                "created_at": created_at,
                "project_id": project_id,
                "model": model
            }
            self._save_names_cache()
            self._chats_cache = None
            
            # Switch config to target this new conversation
            self.switch_chat(conv_id)
            
            return {
                "id": conv_id,
                "name": self.names_cache[conv_id]["name"],
                "created_at": self.names_cache[conv_id]["created_at"],
                "project_id": project_id,
                "model": model,
                "is_active": True,
                "status": "online",
                "has_unread": False,
                "last_message_preview": "No messages yet"
            }
            
        except Exception as e:
            print(f"[ChatManager] Failed to create new conversation via agentapi: {e}. Falling back to manual.")
            import uuid
            conv_id = str(uuid.uuid4())
            
            # Create folder structure manually on disk
            folder_path = os.path.join(self.brain_dir, conv_id)
            log_dir = os.path.join(folder_path, ".system_generated", "logs")
            os.makedirs(log_dir, exist_ok=True)
            transcript_path = os.path.join(log_dir, "transcript.jsonl")
            created_at = datetime.utcnow().isoformat() + "Z"
            
            starter = {
                "step_index": 0,
                "source": "SYSTEM",
                "type": "CONVERSATION_HISTORY",
                "content": "Conversation started.",
                "created_at": created_at
            }
            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(starter) + "\n")
                
            project_name = "New Chat"
            for p in self.get_projects():
                if p["id"] == project_id:
                    project_name = p["name"]
                    break
            clean_project_name = project_name.replace("⏳", "").replace("🎵", "").strip()

            self.names_cache[conv_id] = {
                "name": clean_project_name,
                "created_at": created_at,
                "project_id": project_id,
                "model": model
            }
            self._save_names_cache()
            self._chats_cache = None
            self.switch_chat(conv_id)
            
            return {
                "id": conv_id,
                "name": self.names_cache[conv_id]["name"],
                "created_at": self.names_cache[conv_id]["created_at"],
                "project_id": project_id,
                "model": model,
                "is_active": True,
                "status": "online",
                "has_unread": False,
                "last_message_preview": "No messages yet"
            }

    def _discover_ls_credentials(self) -> dict:
        """Dynamically discover live LS address and CSRF token from the running language_server.exe process."""
        import re
        try:
            import psutil
            for p in psutil.process_iter(['name', 'pid', 'cmdline']):
                try:
                    if p.info['name'] and p.info['name'].lower() == 'language_server.exe':
                        pid = p.info['pid']
                        cmdline = p.info['cmdline'] or []
                        
                        # Extract --csrf_token
                        csrf = None
                        for i, arg in enumerate(cmdline):
                            if arg == '--csrf_token' and i + 1 < len(cmdline):
                                csrf = cmdline[i + 1]
                                break
                        
                        # Extract HTTP port from log
                        import os
                        log_path = os.path.join(
                            os.environ.get("APPDATA", ""),
                            "Antigravity", "logs", "language_server.log"
                        )
                        port = None
                        if csrf and os.path.exists(log_path):
                            port_pattern = re.compile(r"Language server listening on random port at (\d+) for HTTP")
                            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = f.readlines()
                            for line in reversed(lines):
                                if str(pid) in line:
                                    match = port_pattern.search(line)
                                    if match:
                                        port = match.group(1)
                                        break
                            if not port:
                                for line in reversed(lines):
                                    match = port_pattern.search(line)
                                    if match:
                                        port = match.group(1)
                                        break
                        
                        if csrf and port:
                            return {"ls_address": f"127.0.0.1:{port}", "csrf_token": csrf}
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"[ChatManager] Discovery error: {e}")
        
        # Fallback: read from config file
        try:
            if os.path.exists(self.voice_bridge_config_path):
                with open(self.voice_bridge_config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                return {"ls_address": cfg.get("ls_address", ""), "csrf_token": cfg.get("csrf_token", "")}
        except Exception:
            pass
        return {"ls_address": "", "csrf_token": ""}

    def send_message(self, chat_id: str, message: str) -> dict:
        # Run agentapi send-message with dynamically discovered credentials
        # Command syntax: language_server.exe agentapi send-message <recipient_id> <content>
        try:
            creds = self._discover_ls_credentials()
            env = {
                **os.environ,
                "ANTIGRAVITY_AGENT": "1",
                "ANTIGRAVITY_LS_ADDRESS": creds["ls_address"],
                "ANTIGRAVITY_CSRF_TOKEN": creds["csrf_token"],
            }
            cmd = [self.agentapi_exe, "agentapi", "send-message", chat_id, message]
            subprocess.Popen(
                cmd, env=env, creationflags=subprocess.CREATE_NO_WINDOW
            )
            return {
                "success": True,
                "recipient_id": chat_id,
                "content": message
            }
        except Exception as e:
            print(f"Error sending message: {e}")
            return {"success": False, "error": str(e)}

    def extract_file_changes_from_step(self, step) -> list:
        tool_calls = step.get("tool_calls", [])
        if not tool_calls:
            return []
            
        def clean_arg_val(val):
            if isinstance(val, str):
                val = val.strip()
                if val.startswith('"') and val.endswith('"'):
                    try:
                        return json.loads(val)
                    except Exception:
                        return val[1:-1]
            return val

        file_changes_map = {}
        
        for tc in tool_calls:
            name = tc.get("name", "")
            # Remove any api prefix
            if ":" in name:
                name = name.split(":")[-1]
                
            if name not in ("write_to_file", "replace_file_content", "multi_replace_file_content"):
                continue
                
            args = tc.get("args", {})
            if not args:
                continue
                
            target_file = clean_arg_val(args.get("TargetFile"))
            if not target_file:
                continue
                
            # Normalize path
            target_file = os.path.abspath(target_file).replace("\\", "/")
            
            # Skip voice_outbox
            if target_file.endswith("voice_outbox.txt"):
                continue
                
            # Get/initialize file entry
            if target_file not in file_changes_map:
                file_changes_map[target_file] = {
                    "path": target_file,
                    "name": os.path.basename(target_file),
                    "additions": 0,
                    "deletions": 0
                }
                
            entry = file_changes_map[target_file]
            
            if name == "write_to_file":
                code_content = clean_arg_val(args.get("CodeContent")) or ""
                lines_count = len(code_content.splitlines())
                entry["additions"] += lines_count
                
            elif name == "replace_file_content":
                replacement = clean_arg_val(args.get("ReplacementContent")) or ""
                target = clean_arg_val(args.get("TargetContent")) or ""
                entry["additions"] += len(replacement.splitlines())
                entry["deletions"] += len(target.splitlines())
                
            elif name == "multi_replace_file_content":
                chunks = clean_arg_val(args.get("ReplacementChunks")) or []
                if isinstance(chunks, str):
                    try:
                        chunks = json.loads(chunks)
                    except Exception:
                        chunks = []
                for chunk in chunks:
                    replacement = chunk.get("ReplacementContent", "")
                    target = chunk.get("TargetContent", "")
                    entry["additions"] += len(replacement.splitlines())
                    entry["deletions"] += len(target.splitlines())
                    
        return list(file_changes_map.values())

    def get_messages(self, chat_id: str) -> list:
        transcript_path = os.path.join(self.brain_dir, chat_id, ".system_generated", "logs", "transcript_full.jsonl")
        if not os.path.exists(transcript_path):
            transcript_path = os.path.join(self.brain_dir, chat_id, ".system_generated", "logs", "transcript.jsonl")
        if not os.path.exists(transcript_path):
            return []

        try:
            mtime = os.path.getmtime(transcript_path)
            cached = self._messages_cache.get(chat_id)
            if cached and cached[0] == mtime:
                return cached[1]
        except Exception:
            mtime = 0.0

        messages = []
        try:
            with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                
            for idx, line in enumerate(lines):
                try:
                    step = json.loads(line)
                    step_type = step.get("type", "")
                    source = step.get("source", "")
                    content = step.get("content", "")
                    thinking = step.get("thinking", "")
                    created_at = step.get("created_at", "")
                    
                    # 1. Parse User Messages
                    if step_type == "USER_INPUT" or (source == "USER_EXPLICIT" and step_type != "EPHEMERAL_MESSAGE"):
                        if content:
                            # Extract content inside <USER_REQUEST> tags if present
                            req_match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                            clean_content = req_match.group(1).strip() if req_match else content.strip()
                            
                            # Clean up structured intent blocks injected by voice bridge/tools
                            if "[STRUCTURED INTENT]" in clean_content:
                                clean_content = clean_content.split("[STRUCTURED INTENT]")[0].strip()

                            # Skip if empty
                            if not clean_content:
                                continue
                                
                            messages.append({
                                "sender": "user",
                                "content": clean_content,
                                "timestamp": created_at
                            })
                            
                    elif step_type == "SYSTEM_MESSAGE" and source == "SYSTEM":
                        if content and "[VOICE COMMAND" in content and "content=" in content:
                            try:
                                # Extract everything after "content=" up to the closing tag
                                msg_part = content.split("content=", 1)[1]
                                clean_content = msg_part.split("</SYSTEM_MESSAGE>")[0].strip()
                                # Clean up the "VOICE COMMAND from Wayne" prefix if present
                                clean_content = clean_content.replace("[VOICE COMMAND from Wayne]:", "").strip()
                                
                                # Clean up structured intent blocks injected by voice bridge/tools
                                if "[STRUCTURED INTENT]" in clean_content:
                                    clean_content = clean_content.split("[STRUCTURED INTENT]")[0].strip()
                                    
                                if clean_content:
                                    messages.append({
                                        "sender": "user",
                                        "content": clean_content,
                                        "timestamp": created_at
                                    })
                            except Exception:
                                pass
                            
                    # 2. Parse Assistant Messages
                    elif step_type == "PLANNER_RESPONSE":
                        file_changes = self.extract_file_changes_from_step(step)
                        if content or file_changes:
                            messages.append({
                                "sender": "assistant",
                                "content": content or "",
                                "timestamp": created_at,
                                "file_changes": file_changes
                            })
                        elif thinking and idx == len(lines) - 1:
                            # Only show thinking if it's the active, last step in the transcript
                            messages.append({
                                "sender": "assistant",
                                "content": "Thinking...",
                                "timestamp": created_at,
                                "is_thinking": True
                            })
                except Exception:
                    continue
        except Exception as e:
            print(f"Error reading messages for {chat_id}: {e}")
            
        self._messages_cache[chat_id] = (mtime, messages)
        return messages

