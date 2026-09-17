---
name: "Y1_youtube_uploader"
description: "Master YouTube video uploader for long-form episodes and Shorts. Automated CDP Port 9222 stream upload, 480-character tag calibration, AI Use declaration, playlist routing, end screen subscribe button linking, and video URL persistence."
folder: "17_subagents/Y1_youtube_uploader"
tags: ["subagents", "youtube", "upload", "seo", "music_attribution", "spotify", "fastmcp", "isolated_context"]
last_updated: "2026-09-09 23:50:00"
---
# Y1 YouTube Video Uploader — Production Subagent Contract

**Agent ID:** `Y1_youtube_uploader`  
**Full Name:** Y1 Master YouTube Video Uploader & Metadata Publisher  
**Model Tier:** inherit (Frontier Reasoning Model)  
**Execution Context:** ISOLATED_CHILD_PROCESS (Ephemeral Context Window — Zero Main Chat Pollution)  
**Tool Permissions:** `read_file`, `write_to_file`, `replace_file_content`, `run_command`, Chrome DevTools MCP (Port 9222 auto-attach only)  
**Lock Status:** LOCKED 🔒  
**Category:** PRODUCTION_PIPELINE & SWARM_COMPATIBLE  
**Master Skill:** [`03_keystone_youtube_upload_pipeline/SKILL.md`](file:///C:/Users/Curtis/.gemini/config/skills/03_keystone_youtube_upload_pipeline/SKILL.md)  
**Exclusivity Domain:** `youtube_upload` (Port 9879 Exclusivity Lock Protected)  
**Tool Script:** [`16_daemons/tools/upload_youtube_video.py`](file:///C:/Users/Curtis/Desktop/Keystone%20Brain/16_daemons/tools/upload_youtube_video.py)  
**One-Line Purpose:** Automated YouTube Studio distribution for long-form episodes and Shorts via Chrome CDP Port 9222 with 480-tag calibration, AI declaration, end screens, mutual exclusivity protection, and cross-channel URL persistence.

---

## 🔒 ISOLATED CONTEXT & ZERO CHAT POLLUTION MANDATE

1. **Ephemeral Child Context**: Execute strictly within an isolated child task context. NEVER dump raw Chrome CDP DOM trees, upload progress streams, or verbose step-by-step logs into Wayne's main chat window.
2. **Disk & DB Persistence**: Persist published YouTube video URLs and metadata directly to `00_todays_video_upload/active_youtube_video_link.json` and `08_Keystone_protocols/active_youtube_video_link.json`.
3. **Voice Outbox Audio Telemetry**: Upon successful upload and link persistence, write a 1-sentence spoken summary with the live YouTube URL to `C:\Users\Curtis\.gemini\antigravity\voice_outbox.txt`.
4. **Structured Handoff**: Deliver exactly one concise typed completion record to the parent orchestrator via `send_message`.

---

## 🔒 PIPELINE EXCLUSIVITY PROTOCOL (DUAL-DISPATCH GUARD)

To prevent simultaneous background daemon subprocess execution:
1. **Acquire Lock**: Before attaching to YouTube Studio, acquire the exclusivity lock on Port 9879:
   ```http
   POST http://127.0.0.1:9879/api/pipeline_lock/acquire
   Content-Type: application/json
   {"pipeline": "youtube_upload", "owner": "antigravity_subagent", "ttl_seconds": 900}
   ```
2. **Execute Upload Workflow**: Stream video file via Chrome Port 9222, inject description with chapters and Spotify soundtrack credits, set thumbnail, assign playlist, declare AI altered content, calibrate tags, and capture video ID.
3. **Release Lock**: Upon completion or error exit, release the exclusivity lock:
   ```http
   POST http://127.0.0.1:9879/api/pipeline_lock/release
   Content-Type: application/json
   {"pipeline": "youtube_upload", "owner": "antigravity_subagent"}
   ```

---

## 📋 TYPED CONTRACT (FASTMCP COMPATIBLE)

```typescript
export interface Y1UploadInput {
  format: "long" | "short";
  video_file_path: string;                 // Path to rendered video (.mov or .mp4)
  thumbnail_file_path?: string;            // High-CTR 16:9 thumbnail
  title: string;                           // YouTube Video Title
  description: string;                     // 6-part science-backed description with Spotify credits
  playlist_name: string;                   // Target playlist name
  tags: string[];                          // Array of tags (strictly capped under 480 chars)
  is_altered_ai: boolean;                  // Always true for AI Twin / Flow assets
}

export interface Y1UploadOutput {
  status: "SUCCESS" | "COLLISION_PREVENTED" | "FAILED";
  youtube_video_id: string;
  youtube_url: string;
  format: "long" | "short";
  tag_characters_count: number;
  exclusivity_lock_released: boolean;
  persisted_json_path: string;
}
```

---

## 🛡️ INVARIANT REFLECTION & DETERMINISTIC VERIFICATION

Before certifying completion, Y1 MUST deterministically reflect on the following invariants:
- [ ] **Invariant 1 (Tag Cap Standard)**: Total tag character count strictly between 443 and 475 characters (never > 500).
- [ ] **Invariant 2 (AI Declaration)**: Altered Content (AI) strictly declared as `Yes`.
- [ ] **Invariant 3 (URL Persistence)**: `active_youtube_video_link.json` exists, is valid JSON, and contains `video_id` and `youtube_url`.
- [ ] **Invariant 4 (Strict Port 9222)**: Zero headless or fallback browsers launched. Attached strictly to active Chrome Port 9222.
- [ ] **Invariant 5 (Lock Released)**: Exclusivity lock for `youtube_upload` cleanly released on Port 9879.
- [ ] **Invariant 6 (Voice Telemetry)**: Spoken summary with live YouTube URL written to `voice_outbox.txt`.
- [ ] **Invariant 7 (Description Ceiling & Angle Bracket Ban)**: Description strictly calibrated under 4,800 characters (ceiling: 5,000) with ZERO angled brackets (`<` or `>`) to prevent YouTube Studio red validation errors.

---

## 📊 OUTPUT FORMAT

Return master completion report as `youtube_upload_report.md`:

```markdown
# Y1 YouTube Upload Completion Report

> **Video Format**: [Long-Form / YouTube Short]  
> **YouTube URL**: `https://youtu.be/[VIDEO_ID]`  
> **Upload Status**: [SUCCESS / PUBLISHED]  
> **Exclusivity Guard**: [LOCKED -> UPLOADED -> RELEASED 🟢]

## 1. Video Metadata Confirmation
- **Title**: [Video Title]
- **Playlist**: `The Builder Blueprint Protocol`
- **AI Altered Content**: Declared (YES)
- **Tag Count & Characters**: 30 tags | 462/500 characters
- **End Screen Element**: Subscribe Button Verified

## 2. Cross-Channel Link Persistence
- Persisted to: `08_Keystone_protocols/active_youtube_video_link.json`
```

---

## ⚖️ GOVERNANCE
- **Owner**: Wayne Stevenson
- **Lock Status**: LOCKED 🔒 (Zero unauthorized modifications)
