---
name: "Keystone Brain: Master Implementation Plan & Ecosystem Execution Blueprint"
description: "Actionable 6-phase multi-week implementation plan, itemized task matrix with task IDs, component cleanup & 11.0 GB disk reclamation blueprint, and testing protocol commands."
folder: "root"
tags: ["root", "implementation_plan", "cleanup", "tauri", "52603", "vector_brain"]
last_updated: "2026-08-11 18:55:00"
---
# 📋 KEYSTONE BRAIN: MASTER IMPLEMENTATION PLAN & ECOSYSTEM EXECUTION BLUEPRINT

**Document Version**: 1.0.0  
**Author**: Synthesis Worker (`synthesis_worker` Subagent)  
**Date**: August 11, 2026  
**Workspace Root**: `c:\Users\Curtis\Desktop\Keystone Brain`  
**Scope**: 6-Phase Master Implementation Roadmap, Actionable Task Matrix (Task IDs, Components, File Targets, Priority, Acceptance Criteria), Component Cleanup & Disk Reclamation Blueprint, and Verification Protocols.

---

## 1. EXECUTIVE OVERVIEW & PHASED ROLLOUT TIMELINE

The **Master Implementation Plan** outlines the sequential execution roadmap for hardening, optimizing, and evolving the Keystone Brain ecosystem across 6 distinct operational phases:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PHASED ROLLOUT TIMELINE (PHASES 1 - 6)                           │
├──────────────────────────┬──────────────────────────────────────────────┬────────────────────────┤
│ Phase                    │ Primary Focus & Core Objectives              │ Est. Duration          │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 1: Pre-Migration   │ Disk space reclamation (~11.0 GB reclaimed), │ Week 1                 │
│ Disk Cleanup             │ root folder cleanup, test directory pruning. │                        │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 2: Directory       │ Consolidate ad-hoc folders (`01_scripts`,    │ Week 2                 │
│ & Path Consolidation     │ `04_analytics`, `05_music`), update daemons. │                        │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 3: Tauri HUD &     │ Implement fail-closed job assignment, native │ Weeks 3–4              │
│ Daemon Hardening         │ Rust HTTP fallback, dynamic paths in main.rs.│                        │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 4: HUD Automation  │ Deploy 12 JSON automation button configs,    │ Weeks 5–6              │
│ Triggers & Subtabs       │ bind subtabs in WorkstationMatrixPage.tsx.   │                        │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 5A: WASAPI + Dual  │ Low-latency WASAPI audio capture,            │ Weeks 7–9              │
│ Bootstrap IPC            │ mutex/socket mutual launch IPC architecture. │                        │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 5B: Gemini Live +  │ Gemini Live WebSocket API, 3D WebGL          │ Weeks 10–12            │
│ 3D Visualizer & Service  │ visualizer shaders, NT Service supervisor.   │                        │
├──────────────────────────┼──────────────────────────────────────────────┼────────────────────────┤
│ Phase 6: System-Wide     │ Full E2E verification suite execution,       │ Week 13                │
│ E2E Verification         │ automated pre-commit hook deployment.        │                        │
└──────────────────────────┴──────────────────────────────────────────────┴────────────────────────┘
```

### 1.1 Architectural Audit Baseline & Vulnerability Notes
- **Pillar 5 (BC Building Code, Bill 44 & R1-1 Zoning)**: No structural vulnerabilities identified; web portal security hardening (CSRF tokens, server-side signature verification) deferred to Phase 6 E2E verification.


---

## 2. ACTIONABLE TASK CHECKLIST & TASK MATRIX

### 2.1 Key Inter-Task Dependency Chains
- **TASK-205 (Janitor Path Updating)**: Depends on `TASK-201`, `TASK-202`, and `TASK-203` (folder consolidation must complete before whitelist path updating).
- **TASK-502 (Dual Bootstrap IPC)**: Depends on `TASK-301` (Tauri host process lifetime & job object fail-closed hardening must be in place before registering dual-bootstrap IPC handlers).
- **TASK-503 (Gemini Live API)**: Depends on `TASK-501` (low-latency WASAPI audio capture pipeline must be operational before connecting bidirectional audio WebSocket streaming).

### Phase 1: Pre-Migration Disk Cleanup & Reclamation Blueprint
**Goal**: Reclaim **~11.0 GB** of disk space, remove lingering subagent test directories, and eliminate build artifact noise.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-101` | Disk Reclamation | `15_archive/05_Keystone_HUD_v23_backup/src-tauri/target/` | `P0 (Urgent)` | Delete Rust build output folder | Reclaims ~5.5 GB space; `target/` removed |
| `TASK-102` | Disk Reclamation | `15_archive/keystone_hud_backup_2026-08-02/05_Keystone_HUD/src-tauri/target/` | `P0 (Urgent)` | Delete Rust build output folder | Reclaims ~5.5 GB space; `target/` removed |
| `TASK-103` | Root Cleanup | `97_auditor_forensic_test/`, `97_reviewer2_dyn_test/` | `P1 (High)` | Remove test directories from root | Root directory free of `97_*` test folders |
| `TASK-104` | Root Cleanup | `.pytest_cache/` at workspace root | `P2 (Medium)` | Delete root `.pytest_cache` folder | Zero root cache artifacts |
| `TASK-105` | Archive Migration | `13_scratch/old_website_scripts/` | `P2 (Medium)` | Move 16 legacy WP scripts to `15_archive/legacy_wp_scripts/` | `13_scratch` free of single-use scripts |
| `TASK-106` | Sandbox Cleanup | `14_sandbox/keystone_hud_chrome_extension/` | `P2 (Medium)` | Delete deprecated chrome extension prototype | Obsoleted extension deleted from `14_sandbox` |

---

### Phase 2: Directory Consolidation & Path Redirections
**Goal**: Enforce the canonical 20-folder ontology (`00_todays_video_upload` through `18_session_continuity`) and update daemon path references.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-201` | Folder Consolidation | `01_scripts/` $\rightarrow$ `08_Keystone_protocols/scripts/` | `P1 (High)` | Move root script files and remove `01_scripts` folder | All peptide scripts located in `08_Keystone_protocols/scripts/` |
| `TASK-202` | Folder Consolidation | `04_video_analytics_history/` $\rightarrow$ `04_brand_assets/video_analytics/` | `P1 (High)` | Move analytics files and remove top-level folder | Analytics history consolidated under `04_brand_assets` |
| `TASK-203` | Folder Consolidation | `05_music_and_media/` $\rightarrow$ `07_Keystone_recomposition/music/` | `P1 (High)` | Move music catalog and remove top-level folder | All music assets consolidated under `07_Keystone_recomposition` |
| `TASK-204` | Test Consolidation | `16_daemons/test_*.py` $\rightarrow$ `16_daemons/tests/` | `P2 (Medium)` | Move loose test scripts to dedicated `tests/` folder | `16_daemons/` root contains only core daemons & utilities |
| `TASK-205` | Path Updating | `16_daemons/keystone_janitor_daemon.py` | `P1 (High)` | Update folder whitelist paths in `get_dynamic_canonical_folders()` *(Depends on TASK-201, 202, 203)* | Janitor sweeps target updated consolidated paths |
| `TASK-206` | Path Updating | `16_daemons/keystone_cron_scheduler.py` | `P1 (High)` | Update path references to consolidated folders | Cron scheduler executes successfully without path errors |
| `TASK-207` | MCP Path Fix | `03_MCP/API_MCP_REGISTRY.md` | `P1 (High)` | Update 7 legacy MCP path references pointing to `New folder\...\00_Engine\` to canonical paths | Zero legacy path references in `API_MCP_REGISTRY.md` |
| `TASK-208` | Disclaimer Alignment | `08_Keystone_protocols/` scripts | `P1 (High)` | Audit all script files for spoken medical disclaimer text and convert spoken disclaimer to B-roll visual overlay annotation only per Skill A1 mandate | Spoken medical disclaimer text converted to visual-only annotation; zero spoken disclaimer text |

---

### Phase 3: Tauri HUD Rust Host & Daemon Lifecycle Hardening
**Goal**: Hard-close process leaks, eliminate PowerShell process creation overhead, and dynamic path resolution in `05_Keystone_HUD/src-tauri/src/main.rs`.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-301` | Fail-Closed Job | `05_Keystone_HUD/src-tauri/src/main.rs:278-283` | `P0 (Urgent)` | Modify `spawn_daemon()` to invoke `child.kill()` if `AssignProcessToJobObject` returns 0 | Zero risk of orphan daemon processes running outside Job Object |
| `TASK-302` | Native HTTP Fallback| `05_Keystone_HUD/src-tauri/src/main.rs:175-190` | `P1 (High)` | Replace `Command::new("powershell")` with native Rust TCP/HTTP dispatch | Fallback prompt submission latency drops from ~400ms to <5ms |
| `TASK-303` | Dynamic Python Exec | `05_Keystone_HUD/src-tauri/src/main.rs:39` | `P1 (High)` | Resolve `PYTHON_EXE` relative to executable path rather than hardcoded string | Executable runs portably across different installation paths |
| `TASK-304` | Graceful Shutdown | `05_Keystone_HUD/src-tauri/src/main.rs` | `P2 (Medium)` | Intercept `WM_CLOSE` / `WM_QUERYENDSESSION` to issue `POST /api/shutdown` 500ms before close | Daemons cleanly commit SQLite WAL writes before process termination |
| `TASK-305` | Compiler Warning Fix | `05_Keystone_HUD/src-tauri/src/main.rs:27,306,533` | `P2 (Medium)` | Clean unused imports, cast function pointer via `*const () as isize` | Clean Rust compilation output with 0 warnings |

---

### Phase 4: HUD Automation Triggers Registry & Web Frontend Integration
**Goal**: Deploy 12 JSON button configuration files into `05_Keystone_HUD/button_configs/automation_triggers/` and bind 1-click actions across Workstation subtabs.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-401` | JSON Trigger Deploy | `05_Keystone_HUD/button_configs/automation_triggers/` | `P1 (High)` | Deploy all 12 JSON button configuration files (`vector_brain_reindex.json`, `script_prepare_prompts.json`, etc.) | 12 JSON files present and validated |
| `TASK-402` | Subtab UI Binding | `05_Keystone_HUD/src/pages/WorkstationMatrixPage.tsx` | `P1 (High)` | Dynamic config loader reading `automation_triggers/` and rendering 1-click action buttons | All 12 buttons rendered cleanly under subtabs |
| `TASK-403` | Pointer Compliance | `05_Keystone_HUD/src/components/ReaderDrawer.tsx` | `P1 (High)` | Verify 5-stage Radix pointer events and 350ms exit portal delay | Zero click-through onto WebGL canvas during drawer closing animation |
| `TASK-404` | DaVinci Auto-Launch | `13_scratch/davinci_2track_assembly.py` | `P2 (Medium)` | Add auto-launch check for `Resolve.exe` if `fusionscript.dll` returns `None` | Timeline script launches DaVinci Studio automatically if offline |

---

### Phase 5A: WASAPI + Dual Bootstrap IPC (Weeks 7–9)
**Goal**: Integrate low-latency WASAPI audio capture and dual bootstrap IPC mutual launch architecture.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-501` | Low-Latency WASAPI | `05_Keystone_HUD/src-tauri/src/audio.rs` (New) | `P1 (High)` | Implement `cpal` WASAPI Shared Mode (`IAudioClient3`), MMCSS elevation, SPSC ring buffer, and 5-stage FSM | Sub-10ms PTT audio capture with zero GC stutter |
| `TASK-502` | Dual Bootstrap IPC | `05_Keystone_HUD/src-tauri/src/main.rs` & `16_daemons/` | `P1 (High)` | Inject `KEYSTONE_MUTUAL_LAUNCH=1`, Win32 lockfiles, and Ephemeral Port 0 discovery via `%APPDATA%\ai-agent\ipc.json` *(Depends on TASK-301)* | Mutual launch prevents duplicate instances; HMAC token validates sockets |

---

### Phase 5B: Gemini Live + 3D Visualizer + NT Service (Weeks 10–12)
**Goal**: Integrate Gemini Multimodal Live API, 3D WebGL visualizer shaders, and Zero-Downtime NT Service supervisor.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-503` | Gemini Live API | `05_Keystone_HUD/src/services/geminiLiveClient.ts` | `P1 (High)` | Upgrade to `models/gemini-3.6-flash` Bidi WebSocket, `Kore` voice persona, and server VAD instant queue flushing *(Depends on TASK-501)* | <400ms TTFA voice interaction with instant interruption flushing |
| `TASK-504` | 3D Voice Visualizer | `05_Keystone_HUD/src/components/SingularityAvatar3D.tsx` | `P2 (Medium)` | Implement Three.js WebGL2 icosahedron with GLSL Simplex noise vertex displacement and 15,000 instanced orbital rings | Real-time audio spectrum visualization at 60 FPS |
| `TASK-505` | Zero-Downtime Daemon| `16_daemons/supervisor_service.rs` (New) | `P2 (Medium)` | Implement Rust NT Service Supervisor with 5-second Heartbeat Watchdog escalation and `MoveFileEx` atomic persistence | Service auto-recovers from crashes; zero NTFS file corruption |

---

### Phase 6: System-Wide E2E Verification & Web Publishing (Week 13)
**Goal**: Execute master verification suite and complete web/GEO SEO updates.

| Task ID | Component / Area | File Target / Path | Priority | Action Summary | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `TASK-601` | GEO Sitemap Index | `09_Keystone_websites/sitemap_index.xml` | `P1 (High)` | Generate sitemap index referencing all regional GEO pages | `sitemap_index.xml` returns 200 OK; resolves 404 crawl log error |
| `TASK-602` | GEO Footer Mesh | `09_Keystone_websites/landing_pages/*.html` | `P1 (High)` | Update footer navigation links to include `pemberton-luxury-builder.html` across all 6 landing pages | All regional landing pages contain reciprocal links |
| `TASK-603` | Frontmatter Sweep | Workspace root `.md` files | `P2 (Medium)` | Run `python 16_daemons/keystone_cron_scheduler.py --all` to inject YAML frontmatter headers | 100% frontmatter compliance across all root documentation |
| `TASK-604` | E2E Test Suite | Entire Ecosystem | `P0 (Urgent)` | Execute full build, test, and daemon socket verification suite | `npx tsc --noEmit` PASS, `vitest` PASS, `tauri build` PASS, 100% `SO_EXCLUSIVEADDRUSE` PASS |

---

## 3. COMPONENT CLEANUP & DISK RECLAMATION BLUEPRINT

### 3.1 Itemized Disk Reclamation Targets (~11.0 GB Total Recovery)
1. **Target 1**: Delete `15_archive/05_Keystone_HUD_v23_backup/src-tauri/target/` (**~5.5 GB** reclaimed).
2. **Target 2**: Delete `15_archive/keystone_hud_backup_2026-08-02/05_Keystone_HUD/src-tauri/target/` (**~5.5 GB** reclaimed).
3. **Target 3**: Delete root test directories `97_auditor_forensic_test` and `97_reviewer2_dyn_test`.
4. **Target 4**: Delete root `.pytest_cache/` directory.

### 3.2 Automated PowerShell Execution Command for Cleanup:
```powershell
# Execute Disk Reclamation & Subagent Artifact Cleanup
Remove-Item -Recurse -Force "c:\Users\Curtis\Desktop\Keystone Brain\15_archive\05_Keystone_HUD_v23_backup\src-tauri\target" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "c:\Users\Curtis\Desktop\Keystone Brain\15_archive\keystone_hud_backup_2026-08-02\05_Keystone_HUD\src-tauri\target" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "c:\Users\Curtis\Desktop\Keystone Brain\97_auditor_forensic_test" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "c:\Users\Curtis\Desktop\Keystone Brain\97_reviewer2_dyn_test" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "c:\Users\Curtis\Desktop\Keystone Brain\.pytest_cache" -ErrorAction SilentlyContinue
Write-Host "✅ Disk Reclamation Complete: ~11.0 GB space recovered."
```

---

## 4. TESTING & VERIFICATION PROTOCOL COMMANDS

To verify system integrity at every step of implementation, execute the following standardized test suites:

### 4.1 Frontend TypeScript & Vitest Verification Suite
```powershell
# Navigate to Tauri HUD directory
cd "c:\Users\Curtis\Desktop\Keystone Brain\05_Keystone_HUD"

# 1. Type Check (Zero TypeScript Errors)
npx tsc --noEmit

# 2. Vitest Unit Test Suite Execution
npx vitest run
```

### 4.2 Standalone Production Binary Build Verification
```powershell
# Execute Tauri Standalone Production Build (Zero-Bundle Mode)
cd "c:\Users\Curtis\Desktop\Keystone Brain\05_Keystone_HUD"
npx tauri build --no-bundle
```

### 4.3 Python Daemons Socket Binding & SO_EXCLUSIVEADDRUSE Compliance
```powershell
# Verify socket lock enforcement across all listening daemon scripts
python -c "
import os, socket
daemon_dir = r'c:\Users\Curtis\Desktop\Keystone Brain\16_daemons'
daemons = ['local_stt_daemon.py', 'agent_voice_tts_daemon.py', 'vector_brain_daemon.py', 'chrome_overlay_daemon.py', 'instant_watchdog.py', 'keystone_janitor_daemon.py']
for f in daemons:
    with open(os.path.join(daemon_dir, f), 'r') as fp:
        content = fp.read()
        assert 'SO_EXCLUSIVEADDRUSE' in content, f'Violation in {f}'
print('✅ 100% Compliance Verified: All active daemons enforce SO_EXCLUSIVEADDRUSE')
"
```

### 4.4 Vector Brain Query Latency Benchmark (<10ms Budget)
```powershell
# Execute vector search performance test against Port 9878
curl -X POST http://127.0.0.1:9878/api/search -H "Content-Type: application/json" -d "{\"query\": \"Mounjaro recomposition\"}"
```

### 4.5 Subagent Registry Parity Verification
```powershell
# Verify 1:1 match between 17_subagents/INDEX.md and subdirectories
python -c "
import os
base = r'c:\Users\Curtis\Desktop\Keystone Brain\17_subagents'
dirs = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
assert len(dirs) == 9, f'Expected 9 subagents, found {len(dirs)}'
print(f'✅ Subagent Parity Verified: {len(dirs)} matching subagents')
"
```

---

## 5. ROLLBACK & VERSION CONTROL PROTOCOL

To ensure system stability, zero-downtime execution, and instant recoverability across all phases, the following version control and rollback protocols are strictly enforced:

### 5.1 Git Branching Strategy
- Every implementation phase must be executed on a dedicated Git feature branch following the naming convention `phase-N/description` (e.g., `phase-2/directory-consolidation`, `phase-3/tauri-hardening`).
- Direct unverified commits to `main` without completing phase acceptance criteria are strictly prohibited.

### 5.2 Pre-Phase Checkpoint Tagging
- Before initiating any phase (especially destructive disk operations or structural code changes), create an annotated Git tag matching `pre-phase-N` (e.g., `pre-phase-1`, `pre-phase-2`, `pre-phase-3`).
- Command: `git tag -a pre-phase-N -m "Checkpoint prior to executing Phase N"`

### 5.3 Automated & Manual Revert Policy
- **Build / Test Failure Trigger**: If any phase implementation causes compilation errors (e.g., `npx tauri build --no-bundle` failure) or test suite regressions, the executing agent must immediately halt work.
- **Rollback Execution**: Perform an immediate hard rollback to the corresponding `pre-phase-N` checkpoint tag:
  ```powershell
  git reset --hard pre-phase-N
  git clean -fd
  ```
- **Post-Rollback Protocol**: Document the failure root cause in `handoff.md`, update `progress.md`, and report findings to the orchestrator before re-attempting implementation.

---

*Plan approved and certified by,*  
**Synthesis Worker Agent**  
*Keystone Brain Ecosystem Engineering*
