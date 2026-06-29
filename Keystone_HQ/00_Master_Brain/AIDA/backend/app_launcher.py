import os
import subprocess

class AppLauncher:
    def __init__(self):
        # Define paths to executables
        self.app_paths = {
            "antigravity": [
                os.path.join(os.path.expanduser("~"), r"AppData\Local\Programs\Antigravity\Antigravity.exe")
            ],
            "davinci": [
                r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe"
            ],
            "docker": [
                r"C:\Program Files\Docker\Docker\Docker Desktop.exe"
            ],
            "obsidian": [
                os.path.join(os.path.expanduser("~"), r"AppData\Local\Programs\Obsidian\Obsidian.exe")
            ],
            "vpn": [
                r"C:\Program Files\Proton\VPN\ProtonVPN.Launcher.exe"
            ]
        }

    def launch(self, app_name: str) -> dict:
        app_name = app_name.lower().strip()
        
        if app_name == "facebook":
            try:
                subprocess.Popen(
                    ["explorer.exe", "shell:AppsFolder\\FACEBOOK.FACEBOOK_8xx8rvfyw5nnt!App"],
                    close_fds=True
                )
                return {"success": True, "message": "Launched Facebook App"}
            except Exception as e:
                return {"success": False, "error": f"Failed to launch Facebook App: {e}"}
                
        # Desktop applications
        if app_name in self.app_paths:
            paths_to_try = self.app_paths[app_name]
            launched = False
            error_msgs = []
            
            for path in paths_to_try:
                if os.path.exists(path):
                    try:
                        args = [path]
                        if app_name == "obsidian":
                            args.append(r"C:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
                            
                        # Use subprocess.Popen to launch without blocking the server
                        # start_new_session=True runs the process in a new session (independent of python)
                        # On Windows, we use creationflags=subprocess.DETACHED_PROCESS to launch independently
                        subprocess.Popen(
                            args, 
                            creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0,
                            close_fds=True
                        )
                        launched = True
                        break
                    except Exception as e:
                        error_msgs.append(f"Path {path} failed: {e}")
                else:
                    error_msgs.append(f"Path {path} does not exist")
                    
            if launched:
                return {"success": True, "message": f"Launched {app_name}"}
            else:
                return {"success": False, "error": f"Failed to launch {app_name}. Errors: {'; '.join(error_msgs)}"}
                
        return {"success": False, "error": f"Unknown app_name: {app_name}"}

    def stop(self, app_name: str) -> dict:
        # Note: Renamed internally to handle Window Toggling (minimize/restore) instead of killing the process
        app_name = app_name.lower().strip()
        
        process_names = {
            "antigravity": "Antigravity.exe",
            "davinci": "Resolve.exe",
            "docker": "Docker Desktop.exe",
            "obsidian": "Obsidian.exe",
            "vpn": "ProtonVPN.exe"
        }
        
        if app_name in process_names:
            proc_name = process_names[app_name].lower()
            import psutil
            target_pids = []
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] and proc.info['name'].lower() == proc_name:
                        target_pids.append(proc.info['pid'])
            except Exception:
                pass
                
            if not target_pids:
                return {"success": True, "message": f"{app_name} was not running"}
                
            try:
                import ctypes
                hwnd = None
                
                WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
                
                def enum_callback(h, lParam):
                    nonlocal hwnd
                    pid = ctypes.c_ulong()
                    ctypes.windll.user32.GetWindowThreadProcessId(h, ctypes.byref(pid))
                    if pid.value in target_pids:
                        # Ensure it's a visible main window
                        if ctypes.windll.user32.IsWindowVisible(h):
                            length = ctypes.windll.user32.GetWindowTextLengthW(h)
                            if length > 0:  # Has a title
                                hwnd = h
                                return False # Stop enumeration
                    return True
                    
                ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
                
                if hwnd:
                    is_minimized = ctypes.windll.user32.IsIconic(hwnd)
                    fg_hwnd = ctypes.windll.user32.GetForegroundWindow()
                    
                    if is_minimized or fg_hwnd != hwnd:
                        # Restore and bring to front (SW_RESTORE = 9)
                        ctypes.windll.user32.ShowWindow(hwnd, 9)
                        ctypes.windll.user32.SetForegroundWindow(hwnd)
                        return {"success": True, "message": f"Restored {app_name} window"}
                    else:
                        # Minimize (SW_MINIMIZE = 6)
                        ctypes.windll.user32.ShowWindow(hwnd, 6)
                        return {"success": True, "message": f"Minimized {app_name} window"}
                else:
                    return {"success": False, "error": f"Could not find a visible window for {app_name}. It may be in the system tray."}
                    
            except Exception as e:
                return {"success": False, "error": f"Failed to toggle {app_name}: {e}"}
                
        return {"success": False, "error": f"Unknown app_name: {app_name}"}

    def is_running(self, app_name: str) -> bool:
        app_name = app_name.lower().strip()
        process_names = {
            "antigravity": "Antigravity.exe",
            "davinci": "Resolve.exe",
            "docker": "Docker Desktop.exe",
            "obsidian": "Obsidian.exe",
            "vpn": "ProtonVPN.exe"
        }
        if app_name in process_names:
            proc_name = process_names[app_name].lower()
            import psutil
            try:
                for proc in psutil.process_iter(['name']):
                    if proc.info['name'] and proc.info['name'].lower() == proc_name:
                        return True
            except Exception:
                pass
        return False

