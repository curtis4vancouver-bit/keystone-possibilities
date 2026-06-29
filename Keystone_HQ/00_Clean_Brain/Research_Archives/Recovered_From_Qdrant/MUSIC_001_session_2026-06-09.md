# Recovered from Qdrant Vector Database
# Original source_id: MUSIC_001_session_2026-06-09
# Chunks recovered: 4
# Recovery date: 2026-06-14

---

# MUSIC_001 Production Workflow — Proven Batch Pipeline

## Batch Download + Programmatic Rename (Phase 2B)
Proven on MUSIC_001 session (24 clips, 2026-06-09). This is 3x faster than renaming in Flow.

### The Pattern
1. Generate ALL clips in Google Flow using batch prompting (5-6 at a time)
2. Download ALL clips at 1080p WITHOUT renaming them in Flow
3. Run a Python script that matches each downloaded file to its correct clip number
4. The script uses prompt keyword matching + os.path.getmtime sorting for duplicates

### Why It Works
- Flow names downloaded files with the first few words of the prompt + timestamp
- Example: Ana_behind_DJ_controller_202606082338.mp4
- Each prompt has unique starting words that can be matched via glob patterns
- When two prompts start identically, sort by file modification time (oldest = first generated)
- Windows adds (1) suffix for duplicate filenames — glob handles this

### Batch Prompting Optimization
- Queue 5-6 clips at a time in Flow, don't wait

ile modification time (oldest = first generated)
- Windows adds (1) suffix for duplicate filenames — glob handles this

### Batch Prompting Optimization
- Queue 5-6 clips at a time in Flow, don't wait between submissions
- Flow generates clips while you're still prompting the next batch
- Character/avatar must be re-attached for EVERY SINGLE clip via +Create then Characters then Add to Prompt
- Monitor queue — max 6 pending before Flow backs up

### [[music|Music]] Video Assembly (DaVinci Resolve)
- Use media_pool.ImportMedia() for batch imports (more reliable than AddItemsToMediaPool)
- Sort clips numerically with regex: re.search(r'A(\d+)', name)
- Pass raw MediaPoolItem list to AppendToTimeline (preserves linked audio)
- MUTE Track A1 (Flow ambient noise is garbage)
- Create Track A2 for background music
- No B-roll overlay for music videos — continuous performance footage

### Characters
- Ana Stevenson: DJ character, NEVER speaks, Recomposition Music only
- Victoria: Interviewer, Protocol +

nd music
- No B-roll overlay for music videos — continuous performance footage

### Characters
- Ana Stevenson: DJ character, NEVER speaks, Recomposition Music only
- Victoria: Interviewer, Protocol + [[possibilities|Possibilities]]
- Wayne: Expert/Host, Protocol + Possibilities
- Characters are saved in Google Flow project — delete old assets but KEEP characters between productions

### Energy Arc for Music Videos
Intro (slow reveal) then Warm-up (finding groove) then Build (energy rising) then Peak (maximum intensity) then Groove (riding energy) then Outro (fade to black)

### DaVinci Resolve Scripting Paths (Windows)
- Primary: C:\Program Files\Blackmagic Design\DaVinci Resolve\Developer\Scripting\Modules
- Fallback: C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules
- Always try both if import fails

### [[davinci-resolve-mcp/docs/SKILL|Skill]] Location
All of this is documented in: keystone_short_production_pipeline/[[davinci-resolve-mcp/docs/SKILL|SKILL]].md (Phase 2B + Phase 3M sections)

lways try both if import fails

### [[davinci-resolve-mcp/docs/SKILL|Skill]] Location
All of this is documented in: keystone_short_production_pipeline/[[davinci-resolve-mcp/docs/SKILL|SKILL]].md (Phase 2B + Phase 3M sections)

---
📁 **See also:** [[Research_Archives/Recovered_From_Qdrant/INDEX|← Directory Index]]

**Related:** [[insight_2026-06-15_music_conductor]] · [[MUSIC_PROVEN_FLOW_PROMPTS_2026-06-09]] · [[deep_research_ai_music_video_production_2026]]
