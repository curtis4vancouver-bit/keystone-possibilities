---
name: keystone-google-flow-script-format
description: "Enforces proper Google Flow video script formatting rules: max ~22 words per clip for 10-second delivery, natural conversation patterns, phonetic drug names, and the THIS IS THE SCRIPT / THIS IS THE VIDEO PROMPT format. ACTIVATE whenever writing or editing scripts for Google Flow video production."
---

# Google Flow Script Formatting Rules

> **CRITICAL**: These rules are non-negotiable. Every script for Google Flow video production MUST follow them exactly. Failure causes wasted credits and re-work.

---

## Rule 1: Word Count Per Clip — MAX 22 WORDS

Google Flow generates 10-second video clips. The AI voice CANNOT speak more than ~22 words in 10 seconds. If the script line is too long, the AI runs out of time and cuts off mid-sentence.

**Hard limit: 22 words maximum per script line.**

Count every word. Hyphenated phonetic terms (e.g., `tir-zep-a-tide`) count as ONE word.

### Examples

✅ GOOD (20 words):
```
Wayne says: I am Wayne Stevenson. Licensed BC contractor. Twenty-six weeks on tir-zep-a-tide. Today we break down ret-a-tru-tide.
```

❌ BAD (36 words — WILL GET CUT OFF):
```
Wayne says: My name is Wayne Stevenson. I am a licensed BC general contractor and I have been documenting my own body recomposition on tir-zep-a-tide for over six months. Today we are breaking down ret-a-tru-tide.
```

### How to Trim
- Remove filler: "I am going to" → just state it
- Remove "And" at sentence starts
- Remove "that is" / "it is" where possible
- Remove "the" where meaning is preserved
- Remove "really" / "actually" / "basically" / "essentially"
- Combine short sentences: "I have been on it. For twenty-six weeks." → "Twenty-six weeks on tir-zep-a-tide."
- Use periods for pacing instead of conjunctions

---

## Rule 2: Script Format — THIS IS THE SCRIPT / THIS IS THE VIDEO PROMPT

Every clip MUST use this exact format inside a code block:

```text
THIS IS THE SCRIPT:
[Speaker] says: [dialogue — max 22 words]

THIS IS THE VIDEO PROMPT:
[Visual direction — camera, framing, background, expression. Always end with "No subtitles."]
```

### Speaker Format
- Wayne clips: `Wayne says:`
- Victoria clips: `Victoria says:`

### Video Prompt Rules (5-Layer Cinematic Framework)
- ALWAYS start with: `Standing against pure black background`
- **1. Camera & Lens:** Include lens (e.g., `35mm lens`, `Shallow depth of field at f/2.8`)
- **2. Framing:** Include shot size (`Medium close-up` / `Close-up on face` / `Low-angle shot`)
- **3. Camera Motion:** Force dynamic movement: `Slow dolly-in`, `Lateral tracking shot`, `Orbital sweep`. Avoid static shots.
- **4. Lighting & Mood:** `Warm rim lighting`, `Harsh cinematic shadows`, `Pale neon glow`
- **5. Subject Action:** `Slight furrowed brow`, `Nodding empathetically`, `Teaching mode`
- ALWAYS end with: `No subtitles.`

---

## Rule 3: Natural Conversation Flow

The script must feel like a real podcast conversation, NOT a robotic alternating pattern.

### Opus-Level Cadence & Burstiness
- **Burstiness:** Natural speech mixes short, punchy statements (3-5 words) with longer explanatory sentences (15-20 words). Never use uniform sentence lengths.
- **Pacing Controls:** Use ellipses (`...`) to force rhythmic, thoughtful pauses. Use em-dashes (`—`) for sudden tangents.
- **The Filler Ban:** NEVER use words like "furthermore," "moreover," and "essentially." Enforce contractions ("don't", "gonna") and mid-sentence breathers.

### Natural Transitions & Pattern Interrupts
- VARY the pattern: 2 Wayne → 1 Victoria → 2 Victoria → 1 Wayne → etc.
- NEVER do strict 1-for-1 alternation for more than 3 exchanges. Force a pattern interrupt every 3-4 clips.
- Wayne reacting: "Right." / "Exactly." / "And honestly..." / "But here is the thing."
- Victoria pushing back: "Wait, so directly..." / "Hold on." / "OK but..." / "OK here is what confuses me."
- Victoria bridging: "So let me ask you..." / "Which brings us to..."
- Wayne pivoting: "Now..." / "But starting from scratch?" / "Same thing any builder does."

### Character Traits

**Wayne Stevenson:**
- Licensed BC general contractor — uses construction analogies naturally
- Personal experience on tirzepatide — speaks from first-hand knowledge
- Direct, no-BS delivery — does not hedge or over-qualify
- Builder vocabulary: "shoring", "load-bearing", "demolition", "rebar", "framing crew", "finishing trade"
- Passionate about protecting people from bad decisions
- Says "I am not a doctor" — educational case study framing

**Victoria (Co-Host):**
- Data-driven — quotes studies, trial names, percentages
- Asks smart questions that the audience is thinking
- Plays devil's advocate — challenges Wayne constructively
- Professional but warm — not robotic
- Flags scientific caveats (preclinical data, disclaimers)
- Reacts naturally: surprise, concern, curiosity

---

## Rule 4: Phonetic Drug Names

ALL drug/compound names MUST be hyphenated phonetically so the AI voice pronounces them correctly:

| Written | In Script |
|---------|-----------|
| tirzepatide | tir-zep-a-tide |
| retatrutide | ret-a-tru-tide |
| semaglutide | sem-a-glu-tide |
| fibroblasts | fi-bro-blasts |
| lyophilized | ly-oph-i-lized |
| sarcopenia | sar-co-pe-ni-a |
| angiogenesis | an-gi-o-gen-e-sis |

Acronyms spelled out with hyphens: `G-L-P`, `G-I-P`, `B-P-C`, `T-B`, `G-H-K`, `C-O-A`, `H-P-L-C`, `B-M-I`, `B-S-C-G`

---

## Rule 5: Google Flow Production Workflow (MCP)

### How to Generate Each Clip (ONE AT A TIME)
1. **Take snapshot** (`take_snapshot`) to get element UIDs
2. **Click "+ Create"** button to open character selection
3. **Select Avatar tab** (for Wayne) or **Characters tab** (for Victoria)
4. **Click "Add to Prompt"** on the correct character
5. **Click the text input box** (the prompt bar)
6. **Type the FULL prompt** (script + video prompt combined) using `type_text`
7. **Click "Create"** (the arrow button) to submit
8. **Wait for generation** — take screenshot to verify completion
9. **Repeat** from step 1 for next clip — CHARACTER DOES NOT PERSIST

### Critical Rules
- You MUST re-attach the character/avatar for EVERY clip
- You CANNOT batch-submit via scripts — one at a time through the UI
- You CANNOT use `fill` on the prompt box — use `type_text` after clicking
- Always verify the settings show: `Omni Flash · 10s · 16:9`
- For B-roll images: switch to Image mode, NO avatar needed
- **NATIVE VISION ACTIVATED**: You are authorized to use `take_screenshot` and process the raw image to VISUALLY VERIFY that the generated clip or avatar looks correct. Do not just rely on the DOM snapshot. Use your native multimodal eyes to look at the screen.

### Settings Changes
- Video duration: Click the settings button → select `10s` tab
- Aspect ratio: Click the ratio button → select `16:9`
- Model: Should show `Omni Flash` in the prompt bar

---

## Rule 6: Clip Header Format

```markdown
### 📋 CLIP [ID] — [SPEAKER] ([Brief Topic])
```

Examples:
- `### 📋 CLIP A1 — WAYNE (Cold Open Hook)`
- `### 📋 CLIP A15 — VICTORIA (Appetite Paradox)`

Clips separated by `---` horizontal rules.

---

## Rule 7: B-Roll Image Prompts

- One B-roll image per video clip (same count)
- NO avatar/character attached
- Use Image mode: 🍌 Nano Banana Pro → 16:9 → 1x
- Every prompt starts with `Photorealistic`
- Every prompt ends with `16:9.`
- Include lighting direction and mood
- Always reference `pure black background` or `dark surface` for brand consistency

---

## Checklist Before Submitting Any Script

- [ ] Every script line is ≤22 words
- [ ] All drug names use phonetic hyphens
- [ ] Speaker pattern varies naturally (not strict alternation)
- [ ] Wayne uses construction analogies
- [ ] Victoria asks questions and cites data
- [ ] Natural transitions between speakers
- [ ] Video prompts all start with "Standing against pure black background"
- [ ] Video prompts all end with "No subtitles."
- [ ] Format is `THIS IS THE SCRIPT:` / `THIS IS THE VIDEO PROMPT:`
- [ ] B-roll count matches clip count
