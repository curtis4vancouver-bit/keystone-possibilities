---
name: "Project: Keystone Brain Ecosystem \u2014 Dual-Layer Tauri HUD Command Center & CDP Chrome Overlay Architecture"
description: "The Keystone Brain Ecosystem implementation builds out the complete Dual-Layer Command Center & CDP Automation Pipeline:"
folder: "18_session_continuity"
tags: ["session_continuity", "vector_brain"]
last_updated: "2026-08-11 16:39:49"
---
# Project: Keystone Brain Ecosystem — Dual-Layer Tauri HUD Command Center & CDP Chrome Overlay Architecture

## Architecture
The Keystone Brain Ecosystem implementation builds out the complete Dual-Layer Command Center & CDP Automation Pipeline:
1. **Subagent Brain Repository (`17_subagents/`)**: Specialized subagent definitions (`scriptwriter_agent.md`, `cdp_injector_agent.md`, `seo_publisher_agent.md`) equipped with strict frontmatter metadata, domain rules, and MCP/skill tool bindings.
2. **Tauri HUD React GUI (`05_Keystone_HUD/src/`)**: 5-port live telemetry LEDs (9876, 9877, 9878, 9879, 9891), 2-Step Execution Approval Modal (`ApprovalModal.tsx`), and Visual Button Manager (`ButtonBuilder.tsx`).
3. **Chrome CDP Overlay Registry (`05_Keystone_HUD/button_configs/`)**: Consolidated `_overlay_registry.json` and `overlay.js` for Google Flow (`labs.google/fx/tools/flow`) and YouTube Studio automation on Port 9222.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Subagent Prompt Repository | Populate `17_subagents/video-pipeline/scriptwriter_agent.md` with Builder-Translator peptide & zoning rules | R1 | R1 |
| 2 | CDP Injector Agent Prompt | Populate `17_subagents/button-builder/cdp_injector_agent.md` with Slate.js React Fiber AST & 80ms asset loops | R1 | R1 |
| 3 | SEO Publisher Agent Prompt | Populate `17_subagents/website-builder/seo_publisher_agent.md` with Rank Math & 500-char YT tag resolution | R1 | R1 |
| 4 | Header Telemetry LEDs | Live green/red status LEDs for ports 9876, 9877, 9878, 9879, 9891 in `Header.tsx` | R2 | R2 |
| 5 | 2-Step Approval Modal | `ApprovalModal.tsx` showing Distilled Execution Summary with Approve/Edit action buttons | R2 | R2 |
| 6 | Visual Button Manager | `ButtonBuilder.tsx` component allowing dynamic inspection, adding, and editing of button configs | R2 | R2 |
| 7 | Tauri HUD Build Verification | Clean compilation of Tauri HUD (`npm run build` / `cargo check`) | R2 | R2 |
| 8 | Overlay Registry Consolidation | Verify and update `05_Keystone_HUD/button_configs/_overlay_registry.json` for Flow & YT Studio | R3 | R3 |
| 9 | Chrome Overlay JS Injection | Verify `overlay.js` for 1-click prompt execution and Slate.js AST injection on Port 9222 | R3 | R3 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| R1 | Subagent Brain Repository Setup | Specialized prompts under `17_subagents/` (scriptwriter, cdp_injector, seo_publisher) | None | DONE |
| R2 | Tauri HUD Interface Upgrade | Telemetry LEDs, ApprovalModal.tsx, ButtonBuilder.tsx, TypeScript build | R1 | DONE |
| R3 | Chrome CDP Overlay & Integration | `_overlay_registry.json`, `overlay.js`, Google Flow & YT Studio integration | R2 | DONE |

## Code Layout & Deliverables
- Prompts: `17_subagents/video-pipeline/scriptwriter_agent.md`, `17_subagents/button-builder/cdp_injector_agent.md`, `17_subagents/website-builder/seo_publisher_agent.md`
- React Components: `05_Keystone_HUD/src/components/Header.tsx`, `05_Keystone_HUD/src/components/ApprovalModal.tsx`, `05_Keystone_HUD/src/components/ButtonBuilder.tsx`
- Overlay Configs: `05_Keystone_HUD/button_configs/_overlay_registry.json`, `05_Keystone_HUD/button_configs/overlay.js`
