# Keystone Background Loops & Daemons System Reference
> Created on 2026-06-25 for the Gemini 3.5 Pro Upgrade Cycle

This document registers and describes the two primary background loop architectures active in the Keystone Master Brain. When **Gemini 3.5 Pro** becomes active, it should use this reference to locate, audit, test, and upgrade these automation systems.

---

## 1. Loop 1: The Keystone OS Daemon (`keystone_os_daemon.py`)

### 📋 Specifications
* **Primary Script File**: [keystone_os_daemon.py](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/keystone_os_daemon.py)
* **Status Log**: [os_daemon.log](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/os_daemon.log)
* **Heartbeat Indicator**: [heartbeat.json](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/heartbeat.json)
* **Execution Context**: Runs 24/7 as an elevated background process (`pythonw.exe`).
* **Launcher/Restarter**: Desktop batch file `Restart_Keystone_Daemon.bat` (which self-elevates to Administrator via PowerShell UAC prompts).

### ⚙️ Periodic Task Intervals
1. **Heartbeat & RAM Check (Every 60s)**:
   - Updates `heartbeat.json` with the current UTC ISO timestamp.
   - Monitors RAM availability. Warns if available RAM drops below 4.0 GB.
2. **MCP Daemon Watchdog (Every 120s)**:
   - Enumerates system processes to verify all core MCP servers are running:
     - `keystone_brain_v2_mcp.py`
     - `youtube_mcp.py`
     - `content_engine_mcp.py`
     - `youtube_researcher_mcp.py`
     - `git_wrapper.py`
3. **Docker & Disk Check (Every 300s)**:
   - Checks state of required Docker containers: `keystone_qdrant_brain`, `keystone_qdrant_clone`, `neo4j-graph-memory`, `n8n-workflow-engine`, `n8n-postgres`, and `sanity-gravity-desktop`. Restarts any stopped containers.
   - Checks disk space for `C:\` and `G:\`. Warns if free space drops below 200 GB.
4. **Self-Healing & Learning Cycle (Every 600s / 10 Minutes)**:
   - Spawns the [chrome_self_learner.py](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/chrome_self_learner.py) process.
   - Queries Gemini-2.5-flash with the last 50 lines of `transcript.jsonl` and the `correction_journal.json` to extract new rules and auto-promote them to the foundation `SKILL.md`.
5. **Temp Cleaner (Every 6 hours)**:
   - Purges temp directory files and compiled research documents older than 7 days.

---

## 2. Loop 2: The Nightly Orchestrator (`nightly_orchestrator.py`)

### 📋 Specifications
* **Primary Script File**: [nightly_orchestrator.py](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/nightly_orchestrator.py)
* **Weekly Scheduler**: [nightly_research_scheduler.py](file:///c:/Users/Curtis/New%20folder/construction-website/Keystone_HQ/00_Master_Brain/scripts/nightly_research_scheduler.py)
* **Execution Context**: Scheduled via Windows Task Scheduler to run in the overnight window (typically 1:00 AM – 6:00 AM).
* **Run Log**: `last_nightly_run.json` saved in the learnings directory.

### ⚙️ Sequence Phases (Synchronous Pipeline)
1. **Phase 1: Brain Sync**: Runs `sync_brain_to_drive.py` to back up vector DBs and knowledge bases to Google Drive.
2. **Phase 2: Research Prompts**: Runs `nightly_research_scheduler.py` to generate the day's specific deep research prompts based on a weekly rotation topic (e.g. BC Building Codes, Local SEO, Property leads).
3. **Phase 3: Brain Redistribution**: Runs `redistribute_brain.py --execute` to consolidate vector indexes.
4. **Phase 4: Dream Consolidation**: Runs `dream_engine.py --dream` to perform memory decay calculations, applying Ebbinghaus forgetting curves to prune old/low-score ephemeral entries.
5. **Phase 5: Stale Data Check**: Runs `stale_data_pruner.py --safe`.
6. **Phase 6: Skill Evolution**: Runs `self_evolution.py --evolve` to merge daily digests and refine permanent agent skills.
7. **Phase 7: Health Check**: Runs `self_evolution.py --health` to assess the health score of the entire fleet.
8. **Chrome Deep Research Integration**: The generated `tonight_research_prompts.json` is read by the Antigravity `/schedule` command loop to execute 3-tab deep research sessions using the user's browser flat-rate subscription.

---

## 3. Gemini 3.5 Pro Upgrade Opportunities

When **Gemini 3.5 Pro** initializes, it should audit these systems and execute the following upgrades:

### 1. Robust Asynchronous Handling
* **Current Issue**: The daemon runs synchronous blocking `Popen` processes and relies on raw system shell calls.
* **Upgrade Target**: Rewrite using `asyncio` for non-blocking sub-process management, allowing concurrent monitoring and better exception safety.

### 2. Native Windows Service Wrapper
* **Current Issue**: Daemon runs as `pythonw.exe` in user space and requires manual restarts via the desktop batch file if terminated.
* **Upgrade Target**: Package `keystone_os_daemon.py` using `pywin32` or a `NSSM` wrapper as a native Windows System Service that automatically restarts on system boot.

### 3. Integrated Dynamic Rate Limiting
* **Current Issue**: High-frequency API calls during self-learning risk hitting rate limit blocks if the chat log increases in size.
* **Upgrade Target**: Implement a cost-aware sliding window that dynamically scales the lookback size of the transcript based on remaining free quota tokens.

### 4. Telemetry and Dashboard Reporting
* **Current Issue**: Monitoring the daemon requires manually viewing log files or heartbeats.
* **Upgrade Target**: Generate a simple web dashboard or an MCP endpoint that allows other agents to query daemon health directly in real-time.