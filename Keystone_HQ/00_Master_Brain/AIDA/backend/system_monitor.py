import os
import re
import time
import psutil
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.brain_dir = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "brain")
        self.dream_logs_dir = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\AIDA\..\.learnings\dream_logs"
        # Fallback path if the above relative one resolves incorrectly
        self.dream_logs_dir_abs = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.learnings\dream_logs"
        
        # Track last network usage for rate calculation
        self.last_net_bytes = None
        self.last_net_time = None

    def get_vram_stats(self) -> dict:
        try:
            import subprocess
            cmd = ["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"]
            output = subprocess.check_output(cmd, text=True, timeout=1.5, creationflags=subprocess.CREATE_NO_WINDOW)
            parts = output.strip().split(",")
            if len(parts) == 2:
                used = float(parts[0].strip())
                total = float(parts[1].strip())
                if total > 0:
                    return {
                        "percent": round((used / total) * 100, 1),
                        "used_gb": round(used / 1024, 1),
                        "total_gb": round(total / 1024, 1)
                    }
        except Exception:
            pass
        return {"percent": 0.0, "used_gb": 0.0, "total_gb": 0.0}

    def get_stats(self) -> dict:
        # VRAM stats
        vram_stats = self.get_vram_stats()
        vram_percent = vram_stats["percent"]
        vram_used_gb = vram_stats["used_gb"]
        vram_total_gb = vram_stats["total_gb"]

        # RAM stats
        try:
            vm = psutil.virtual_memory()
            ram_percent = vm.percent
            ram_used_gb = round(vm.used / (1024 ** 3), 1)
            ram_total_gb = round(vm.total / (1024 ** 3), 1)
        except Exception:
            ram_percent = 0.0
            ram_used_gb = 0.0
            ram_total_gb = 0.0


        # CPU stats
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
        except Exception:
            cpu_percent = 0.0

        # Net stats
        net_percent = 0
        try:
            net_io = psutil.net_io_counters()
            now = time.time()
            current_bytes = net_io.bytes_sent + net_io.bytes_recv
            if self.last_net_bytes is not None and self.last_net_time is not None:
                elapsed = now - self.last_net_time
                if elapsed > 0:
                    bytes_per_sec = (current_bytes - self.last_net_bytes) / elapsed
                    # Convert to percentage where 1 MB/s (1024 KB/s) is 100%
                    kb_per_sec = bytes_per_sec / 1024
                    net_percent = min(100, int((kb_per_sec / 1024) * 100))
            self.last_net_bytes = current_bytes
            self.last_net_time = now
        except Exception:
            pass

        # Active agents (language_server.exe processes)
        active_agents = 0
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'] and proc.info['name'].lower() == 'language_server.exe':
                        active_agents += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            print(f"Error counting language server processes: {e}")
            active_agents = 1 # fallback default since we are running

        # Brain episodes (number of UUID directories in brain_dir)
        brain_episodes = 0
        if os.path.exists(self.brain_dir):
            try:
                for item in os.listdir(self.brain_dir):
                    if os.path.isdir(os.path.join(self.brain_dir, item)):
                        if re.match(r"^[0-9a-fA-F\-]{36}$", item):
                            brain_episodes += 1
            except Exception as e:
                print(f"Error counting brain episodes: {e}")

        # Brain last decay (newest dream report date)
        brain_last_decay = "N/A"
        target_dir = self.dream_logs_dir_abs if os.path.exists(self.dream_logs_dir_abs) else self.dream_logs_dir
        if os.path.exists(target_dir):
            try:
                files = os.listdir(target_dir)
                dream_files = [f for f in files if f.endswith("-dream-report.md")]
                if dream_files:
                    # Sort files alphabetically since they start with ISO date YYYY-MM-DD
                    dream_files.sort(reverse=True)
                    newest_file = dream_files[0]
                    # Extract date YYYY-MM-DD
                    match = re.match(r"^(\d{4}-\d{2}-\d{2})", newest_file)
                    if match:
                        brain_last_decay = match.group(1)
            except Exception as e:
                print(f"Error finding last decay: {e}")

        return {
            "ram_percent": ram_percent,
            "ram_used_gb": ram_used_gb,
            "ram_total_gb": ram_total_gb,
            "cpu_percent": cpu_percent,
            "vram_percent": vram_percent,
            "vram_used_gb": vram_used_gb,
            "vram_total_gb": vram_total_gb,
            "net_percent": net_percent,
            "active_agents": active_agents,
            "brain_episodes": brain_episodes,
            "brain_last_decay": brain_last_decay
        }

