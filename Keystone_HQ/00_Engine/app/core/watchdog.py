import asyncio
import os
import sys
import psutil
import datetime
from typing import Set, Dict, Any, List

class WatchdogDaemon:
    def __init__(self, workspace_root: str = None, ws_broadcast_callback = None):
        """
        Background System Watchdog & Telemetry Controller.
        Polices RAM envelopes, schedules transcript log compaction sweeps,
        and dynamically catches incoming Chrome Deep Research scraped documents.
        """
        if workspace_root is None:
            # app/core/watchdog.py -> root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            workspace_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
            
        self.workspace_root = workspace_root
        self.ws_broadcast_callback = ws_broadcast_callback
        
        # Directories to poll for new document events
        self.polling_paths = [
            os.path.join(self.workspace_root, "Master_Docs"),
            os.path.join(self.workspace_root, "Research_Archives")
        ]
        
        # In-memory index of loaded documents to catch new arrivals
        self.known_files: Set[str] = set()
        self.running = False
        self.loop_task: Optional[asyncio.Task] = None
        
        self.initialize_file_index()

    def initialize_file_index(self):
        """Builds the initial baseline index of all local documents."""
        for path in self.polling_paths:
            if os.path.exists(path):
                for f in os.listdir(path):
                    f_abs = os.path.join(path, f)
                    if os.path.isfile(f_abs):
                        self.known_files.add(f_abs)

    async def start(self):
        """Launches the non-blocking background loops."""
        self.running = True
        self.loop_task = asyncio.create_task(self._daemon_loop())
        print(f"[Watchdog] Chronos Watchdog Daemon Active. Polling {len(self.polling_paths)} folders.")

    async def stop(self):
        """Stops the daemon background loops gracefully."""
        self.running = False
        if self.loop_task:
            self.loop_task.cancel()
            try:
                await self.loop_task
            except asyncio.CancelledError:
                pass

    async def _daemon_loop(self):
        """Central scheduling loop checking telemetry and directories."""
        compaction_interval_sec = 3600  # Compile & compact transcripts hourly
        last_compaction = datetime.datetime.now()
        
        while self.running:
            try:
                # 1. Evaluate memory envelope (Zero-VRAM CPU backpressure manager)
                process = psutil.Process(os.getpid())
                mem_info = process.memory_info()
                ram_mb = mem_info.rss / (1024 * 1024)
                
                if ram_mb > 500:
                    print(f"[Watchdog] ⚠️ RAM high: {ram_mb:.1f}MB. Triggering active garbage collection sweep.", file=sys.stderr)
                    import gc
                    gc.collect()
                
                # 2. Check for newly arriving Chrome Deep Research documents
                await self._check_for_new_documents()
                
                # 3. Schedule hourly log compaction
                if (datetime.datetime.now() - last_compaction).total_seconds() > compaction_interval_sec:
                    await self._execute_log_compaction()
                    last_compaction = datetime.datetime.now()
                    
            except Exception as e:
                print(f"[Watchdog] Error in daemon execution loop: {str(e)}", file=sys.stderr)
                
            await asyncio.sleep(5.0)  # Polling throttle limit

    async def _check_for_new_documents(self):
        """Scans directories for new documents written by Chrome Deep Research automation."""
        newly_ingested: List[Dict[str, Any]] = []
        
        for path in self.polling_paths:
            if not os.path.exists(path):
                continue
                
            for f in os.listdir(path):
                f_abs = os.path.join(path, f)
                if os.path.isfile(f_abs) and f_abs not in self.known_files:
                    self.known_files.add(f_abs)
                    size = os.path.getsize(f_abs)
                    
                    doc_event = {
                        "filename": f,
                        "size_bytes": size,
                        "folder": os.path.basename(path),
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    newly_ingested.append(doc_event)
                    print(f"[Watchdog] 💎 Caught new Chrome Deep Research Document: {f} ({size} bytes)")
        
        # Broadcast caught documents immediately to dual-screens over WebSockets
        if newly_ingested and self.ws_broadcast_callback:
            for doc in newly_ingested:
                await self.ws_broadcast_callback({
                    "event_type": "document_ingested",
                    "data": doc
                })

    async def _execute_log_compaction(self):
        """Runs the self_evolution.py log compaction to prevent token bloat."""
        print("[Watchdog] Triggering scheduled transcript log compaction sweep...")
        
        try:
            # We run in a non-blocking thread pool to avoid blocking GIL socket schedules
            await asyncio.to_thread(self._run_compaction_script)
        except Exception as e:
            print(f"[Watchdog] Compaction sweep failed: {e}", file=sys.stderr)

    def _run_compaction_script(self):
        """Executes compaction directly using the self_evolution import."""
        sys.path.insert(0, self.workspace_root)
        try:
            from self_evolution import SovereignSelfEvolution
            evolver = SovereignSelfEvolution()
            report = evolver.run_weekly_compaction()
            print(f"[Watchdog] Compaction sweep finalized: Compacted {report.get('files_compacted_and_pruned', 0)} files, reclaimed {report.get('context_freed_bytes', 0)} bytes.")
            
            # Broadcast the report to the UI console drawer
            if self.ws_broadcast_callback:
                asyncio.run(self.ws_broadcast_callback({
                    "event_type": "compaction_completed",
                    "data": report
                }))
        except Exception as e:
            print(f"[Watchdog] Error executing self_evolution weekly compaction: {e}", file=sys.stderr)
