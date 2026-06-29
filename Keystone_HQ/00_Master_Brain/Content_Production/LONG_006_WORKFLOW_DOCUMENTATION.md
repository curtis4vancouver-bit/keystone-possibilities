# 🎬 LONG_006 Production Workflow — Complete Step-by-Step Documentation

> **Production**: LONG_006 — "The Triple Threat: Retatrutide, Tirzepatide, and the FDA"
> **Date**: June 2026
> **Status**: ✅ Successfully produced (with lessons learned)

---

## ✅ STEP 1: Script Writing

1. Research the topic thoroughly (used Research_Archives for peptide science, FDA regulatory data, compounding law)
2. Write the full script using the **Google Flow Script Format** (see `keystone-google-flow-script-format` skill):
   - `THIS IS THE SCRIPT:` / `THIS IS THE VIDEO PROMPT:` code block format
   - Max **22 words per clip** for 10-second delivery
   - Phonetic drug names: `ret-a-tru-tide`, `tir-zep-a-tide`, `sem-a-glu-tide`
   - Natural conversation flow — NOT strict 1-for-1 alternation
   - Wayne = construction analogies, personal experience
   - Victoria = data-driven, asks smart questions
3. Write matching B-roll image prompts (1 per clip), all starting with `Photorealistic` and ending with `16:9.`
4. Save script to `Content_Production/LONG_006_THE_TRIPLE_THREAT_FINAL_FLOW.md`

**Script file**: `Content_Production/LONG_006_THE_TRIPLE_THREAT_FINAL_FLOW.md`

---

## ✅ STEP 2: Google Flow Video Generation

### Settings
- **Video mode** → Omni Flash → 10 seconds → 16:9 → 1x
- **Image mode** (for B-rolls) → 🍌 Nano Banana Pro → 16:9 → 1x

### Per-Clip Workflow (ONE AT A TIME)
1. Click **"+ Create"** to open character selection
2. For Wayne clips: Select **Avatar tab** → click Wayne avatar ("me") → **"Add to Prompt"**
3. For Victoria clips: Select **Characters tab** → click Victoria → **"Add to Prompt"**
4. Click the **text input box** (prompt bar)
5. **Type the FULL prompt** (script + video prompt combined)
6. Click **"Create"** (arrow button) to submit
7. Wait for generation to complete
8. **REPEAT from step 1** — character does NOT persist between clips

### B-Roll Generation
1. Switch to **Image mode**
2. NO avatar needed
3. Paste the B-roll image prompt
4. Generate

---

## ✅ STEP 3: Download & Organize

1. Download all video clips from Google Flow
2. Download all B-roll images from Google Flow
3. Rename videos numerically: `1.mp4`, `2.mp4`, `3.mp4`, ... `50.mp4`
4. Rename B-rolls with prefix: `B1_description.jpg`, `B2_description.jpg`, etc.
5. Organize into folder structure:
   ```
   Desktop/it/
   ├── video/      (all numbered .mp4 files)
   └── b roll/     (all B-roll .jpg files)
   ```

---

## ✅ STEP 4: DaVinci Resolve Timeline Assembly (Automated)

1. Open DaVinci Resolve with a project loaded
2. Run the assembly script: `python scratch/assemble_timeline.py`
3. Script automatically:
   - Creates a media bin folder
   - Imports all videos and B-roll images
   - Sorts everything numerically
   - Creates a new timeline
   - Appends all videos back-to-back on **V1/A1**
   - Places B-roll images on **V2** centered at each video transition point
   - B-rolls are set to **3 seconds** (configured in DaVinci Preferences > User > Editing > Standard Still Duration)

### DaVinci Prerequisites
- **Preferences > System > General**: External Scripting Using = **Local**
- **Preferences > User > Editing**: Standard Still Duration = **3.0 seconds**

---

## ⚠️ KNOWN ISSUES & FIXES

### Issue 1: B-Roll Images Show "Media Offline"
**Cause**: Google Flow saves images as JPEG internally but names them `.png`. DaVinci Resolve sees the wrong extension and fails to decode.
**Fix**: Rename all `.png` files to `.jpg` before importing:
```powershell
Get-ChildItem -Path "path\to\b roll\*.png" | Rename-Item -NewName { $_.Name -replace '\.png$','.jpg' }
```

### Issue 2: B-Roll Duration Wrong (e.g. 5 seconds instead of 3)
**Cause**: DaVinci Resolve's "Standard Still Duration" preference was not set to 3 seconds.
**Fix**: Go to **Preferences > User > Editing** → set Standard Still Duration to **3.0 seconds** → Save → re-run the script.

### Issue 3: Characters Say Their Own Names at End of Clips ⚠️ CRITICAL
**Cause**: The script format uses `Wayne says:` and `Victoria says:` in the `THIS IS THE SCRIPT:` section. Google Flow's AI interprets the full text prompt including the speaker attribution, and sometimes the AI avatar **speaks the name out loud** at the tail end of the clip (e.g., "...Wayne" or "...Victoria").
**Fix**: **REMOVE the `[Speaker] says:` prefix from the script lines going forward.** The speaker is already identified in the video prompt section. Change from:
```text
THIS IS THE SCRIPT:
Wayne says: The most powerful weight loss drug ever tested just finished its Phase Three trial.
```
To:
```text
THIS IS THE SCRIPT:
The most powerful weight loss drug ever tested just finished its Phase Three trial.
```
The video prompt already specifies which character (Wayne or Victoria) to use, so the name in the script line is redundant and causes the AI to speak it.

---

## 📋 COMPLETE FILE INVENTORY

| Asset | Location |
|-------|----------|
| Final Script | `Content_Production/LONG_006_THE_TRIPLE_THREAT_FINAL_FLOW.md` |
| Video Clips (50) | `Desktop/it/video/1.mp4` through `50.mp4` |
| B-Roll Images (50) | `Desktop/it/b roll/B1_*.jpg` through `B50_*.jpg` |
| Assembly Script | `scratch/assemble_timeline.py` |
| Google Flow Script Formatting Rules | `skills/google-flow-script-format/SKILL.md` |
| DaVinci Assembly Skill | `skills/keystone_davinci_timeline_assembly/SKILL.md` |
| Short Production Pipeline Skill | `skills/keystone_short_production_pipeline/SKILL.md` |

---

*Documented by the Master Brain — June 18, 2026*
