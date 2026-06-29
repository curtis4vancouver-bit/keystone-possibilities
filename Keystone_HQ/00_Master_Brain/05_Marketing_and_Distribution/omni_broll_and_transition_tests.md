# OMNI GOOGLE FLOW: B-ROLL VOICEOVER & TRANSITION LOOK-OFF TESTS

*Objective:* Premium 10-second stress-test prompts designed to verify visual-audio hand-offs, the "Look-Off" transition hack, and clean cloned-voice voiceovers over B-roll.

---

### 📋 TEST 1: THE TALKING-HEAD "LOOK-OFF" TRANSITION
*Purpose: Tests natural talking-head hand-offs. Wayne looks away to the construction site at second 8, creating a seamless visual bridge to the next clip.*

```text
THIS IS THE SCRIPT:
Wayne says: To prevent sarcopenia and optimize hypertrophy, we analyze tir-zepa-tide, ret-a-troo-tide, and sema-gloo-tide.

THIS IS THE VIDEO PROMPT:
A premium, highly desaturated 8k cinematic shot of Wayne, a rugged 43-year-old Canadian builder, looking stoic facing the camera on a Squamish wellness retreat construction site. The camera executes a steady slow dolly-in. Wayne's lips are synchronized flawlessly to the script. At 0:08, Wayne naturally turns his head to look off-camera toward the active construction horizon. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into a cinematic motion blur to transition away. --no watermark --no warped face --no floating limbs --no text artifacts --no subtitles
```

---

### 📋 TEST 2: THE VOICEOVER B-ROLL (VOICE ONLY, NO FACE)
*Purpose: Verifies the engine's ability to render a cloned voiceover cleanly over scenic B-roll while keeping Wayne completely off-camera.*

```text
THIS IS THE SCRIPT:
Wayne's voiceover says: On these rugged Squamish cliffs, our geotechnical framing must support massive timber and panoramic glass.

THIS IS THE VIDEO PROMPT:
A premium, highly desaturated 8k cinematic drone shot sweeping over a steep cliffside wellness retreat construction site in Squamish. Dramatic morning light glinting off panoramic glass and massive exposed Douglas fir timber framing. Wayne is completely off-camera. The video is clean visual B-roll of the construction layout, with Wayne's voiceover playing clearly over the scene. --no humans --no watermark --no text artifacts --no subtitles
```

---

### 📋 TEST 3: THE HIGH-DIFFICULTY B-ROLL VOICEOVER (CLINICAL & CONSTRUCTION JARGON)
*Purpose: Verifies system capability to articulate complex medical/structural terms over pure visual B-roll.*

```text
THIS IS THE SCRIPT:
Wayne's voiceover says: We combine bio-philic design, geo-technical shot-crete, G-H-K copper, and ipa-more-ellin protocols.

THIS IS THE VIDEO PROMPT:
A premium, highly desaturated 8k cinematic shot of a heavy excavator preparing a rocky granite foundation on a Squamish cliffside. Bright morning sun beams breaking through Douglas fir trees. Wayne is completely off-camera. No humans or faces are in the frame. The video is pure visual construction B-roll, with Wayne's cloned voiceover playing cleanly over the scene. --no humans --no faces --no watermark --no text artifacts --no subtitles
```

---

### 🔍 PROMPT ARCHITECTURE RULES FOR 5-MINUTE VIDEOS

1. **The 14-Word Pace Rule:** Every 10-second segment must strictly cap the script dialogue at **14-15 words**. This enforces Wayne’s signature slow, high-end, stoic builder cadence.
2. **Dialogue Triggering Syntax:** 
   - Use `Wayne says:` to trigger talking-head rendering.
   - Use `Wayne's voiceover says:` for off-camera narration overlay.
   - *Do not use standard quotation marks inside the script blocks.*
3. **The Look-Off Transition:** Command the character to look away from the camera or down at blueprints during the final 1-2 seconds of talking-head shots, paired with a whip-pan, to eliminate jump cuts.
4. **Visual Quality Lock:** Every visual prompt must end with this identical negative prompt block to ensure rendering fidelity:
   `--no watermark --no warped face --no floating limbs --no text artifacts --no subtitles`