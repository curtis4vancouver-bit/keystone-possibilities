---
id: doc-googleflowpromptingguide
title: Google Flow Prompting Guide
type: document
summary: The evolution of generative video has rapidly transitioned from an era of
  experimental, highly unpredictable clip generation into a discipline of d...
entities:
- DaVinci
- DaVinci Resolve
- GHK-Cu
- Squamish
created: '2026-05-10T21:17:12.589671'
updated: '2026-06-14T19:57:36.012107'
---
# Advanced Prompt Engineering and Physics Control in Google Labs Flow: Mastering the Veo 3.1 [[ARCHITECTURE|Architecture]]

The evolution of generative video has rapidly transitioned from an era of experimental, highly unpredictable clip generation into a discipline of deterministic, professional-grade visual production. At the vanguard of this paradigm shift is Google Labs Flow, an integrated artificial intelligence creative studio powered by the [[STATE|state]]-of-the-art Veo 3.1 architecture. While the Veo 3.1 model demonstrates unprecedented capabilities in rendering photorealistic, cinematic sequences natively in both 720p and 1080p resolutions across multiple aspect ratios including 16:9 and 9:16, achieving strict temporal consistency and physical accuracy remains a highly technical endeavor.

<!-- CONTEXT: Google Flow Prompting Guide / Deconstructing Latent Space Hallucinations in Mechanical Interactions -->
## Deconstructing Latent Space Hallucinations in Mechanical Interactions

The most persistent and visually disruptive artifact in generative video is the unintentional "melting" or morphing of entities, which occurs most frequently during complex physical interactions. When a text prompt is ambiguous or overly broad, the model's cross-attention mechanism fails to draw a hard semantic boundary between the hand and the tool. Consequently, the denoising process results in the amalgamation of both entities, creating the dreaded melting effect.

To prevent anatomical corruption and ensure the correct usage of tools, prompts must be meticulously engineered to explicitly define the interaction surface, the physical [[STATE|state]] of the objects, and the precise mechanical grip involved in the action.

The Veo 3.1 model utilizes a sophisticated text encoder that assigns greater mathematical weight to the early words in a prompt; therefore, the most critical physical constraints and subject definitions must be front-loaded. A fundamental architectural rule for ensuring realistic tool interaction is the strict enforcement of a single, highly detailed physical action per generated scene.

**Incorrect Prompt**: "a construction worker drilling a hole in a wall"
**Correct Prompt**: "A close-up shot of a worker's calloused, gloved hand gripping the ergonomic handle of a yellow power drill firmly. The drill bit rotates rapidly, maintaining a strict perpendicular angle as it presses into the rigid concrete block, sending a fine mist of gray dust outward."

<!-- CONTEXT: Google Flow Prompting Guide / Architectural Prompting for Rigid and Soft Body Physics -->
## Architectural Prompting for Rigid and Soft Body Physics

When dealing with rigid body physics, prompts must explicitly describe the transfer of kinetic energy. The model must be told how objects react upon impact to prevent them from simply passing through one another. Example: "Two solid billiard balls collide with accurate momentum transfer; the hard impact creates realistic recoil and sound as they separate at sharp angles based on rigid body principles".

Conversely, when simulating soft body physics, the prompting vocabulary must shift to emphasize fluid resistance, gravity, and material tension. Example: "A lightweight silk scarf falls slowly through the air, its delicate fabric billowing naturally against air resistance, landing softly on a wooden table with realistic draping and complex fold patterns".

Particle systems require defining environmental forces: "Thick smoke rises from the campfire in realistic wisps, the particles dispersing naturally with gentle cross-wind currents..."

<!-- CONTEXT: Google Flow Prompting Guide / Eradicating Artifacts: Advanced Prompt Hygiene and Negative Constraints -->
## Eradicating Artifacts: Advanced Prompt Hygiene and Negative Constraints

A significant breakthrough in stabilizing Veo 3.1 outputs involves the complete removal of poetic, flowery, or abstract language. Generative AI systems respond much more predictably to highly structured, hierarchical formats (JSON or strict shot-list formats).

A standard, highly effective negative string includes: `--no watermark --no warped face --no floating limbs --no text artifacts`. In specialized workflows requiring extreme anatomical precision, such as dental imagery generation, add negative prompts specifically targeting "teeth artifacts".

When a generation is near perfect, employ "seed bracketing" (altering the seed by a tiny increment, e.g., 10) to navigate local minima and refine the geometry without altering the overall composition.

<!-- CONTEXT: Google Flow Prompting Guide / The "Motion-Only" Paradigm: Mastering Image-to-Video Transitions -->
## The "Motion-Only" Paradigm: Mastering Image-to-Video Transitions

The absolute, non-negotiable rule for successful Image-to-Video generation is: **Prompt for motion only.**

Because the uploaded image already defines the subject's [[Brand_Constitution/protocol/IDENTITY|identity]], environmental setting, shot composition, and artistic style, the prompt must focus entirely on the action occurring, camera movement, and audio design. Use [[general|general]] reference terms like "the subject" or "the object" to refer to entities in the source image. Prompts must be kept to a maximum length of 1 to 3 sentences.

**Incorrect Image-to-Video Prompt**: "A joyful baker with a white hat kneading dough in a rustic kitchen as the camera pans."
**Correct Image-to-Video Prompt**: "The subject firmly kneads the dough. The camera executes a slow dolly-in. SFX: rhythmic thumping of dough on a wooden table."

<!-- CONTEXT: Google Flow Prompting Guide / Deterministic Transitions: First and Last Frame Interpolation -->
## Deterministic Transitions: First and Last Frame Interpolation

For complex transitions where spatial logic cannot be compromised, use the "First and Last Frame" feature. This creates a trajectory with a mathematically fixed start and end point. When executing this workflow in professional environments, ensure the `enhancePrompt` parameter is set to false to prevent unwanted creative interpretations.

<!-- CONTEXT: Google Flow Prompting Guide / Narrative Continuity: Temporal Engineering in Scenebuilder -->
## Narrative Continuity: Temporal Engineering in Scenebuilder

1. **Extend Protocol**: Lengthening continuous mechanical action without regenerating base assets. Preserves physical states and material properties without rerolling the seed.
2. **Jump To Mechanic**: Analyzes a subject and "teleports" them into a newly prompted context. Flawlessly preserves character [[Brand_Constitution/protocol/IDENTITY|identity]] for narrative jump cuts.
3. **Ingredients to Video**: Embeds reference images as locked variables to ensure the specific geometric shape of complex mechanical tools or specific facial features remain mathematically identical.

<!-- CONTEXT: Google Flow Prompting Guide / Multi-Sensory Physics: Fusing Native Audio with Visual Impact -->
## Multi-Sensory Physics: Fusing Native Audio with Visual Impact

Fusing visuals with intricate sound design dramatically enhances realism. Explicitly prompting for the exact sound effect forces the model to mathematically synchronize the visual impact of the tool with the waveform of the sound. Use markers like `SFX:` for sound effects.

Dialogue can be prompted explicitly using colons: `A woman says: We have to leave right now.` Avoid standard quotation marks as they can confuse the parser and trigger baked-in text subtitles. Enforce the negative prompt `(no subtitles)` or `No subtitles!`.

<!-- CONTEXT: Google Flow Prompting Guide / Directing the Virtual Camera -->
## Directing the Virtual Camera

Use precise terminology: "Dolly-in", "Tracking shot", "Arc shot", "whip pan". Appending "handheld camera" or "shaky cam" introduces organic movements that disguise the artificially smooth "AI look." By heavily prioritizing a "static" environment in the text prompt while focusing action solely on a localized area, the user effectively simulates a motion brush.

---

<!-- CONTEXT: Google Flow Prompting Guide / 🎬 THE KEYSTONE MODULAR PRODUCTION ENGINE (10-SECOND SCENES & B-ROLL PIPELINE) -->
### 🎬 THE KEYSTONE MODULAR PRODUCTION ENGINE (10-SECOND SCENES & B-ROLL PIPELINE)

To compile high-end, visual-consistent videos (Shorts and long-form vlogs), we operate on a strictly modular **10-second scene pacing architecture**. This protocol ensures flawless audio delivery, cinematic coherence, and seamless transitions between clips.

*   **The 22-to-25 Word Masterclass Cadence Rule:** For future long-form masterclass videos, target **22 to 25 words per 10-second block** (approximately 2.2 to 2.5 words per second). This ensures a faster, punchier, and highly engaging delivery that prevents drawn-out speaking patterns, while keeping the avatar's lips fully synchronized and the pacing sharp.
*   Dialogue Prefix Syntax: Dialogue must be declared explicitly using colons (e.g., `Wayne says: [dialogue]` for talking head shots, and `Wayne's voiceover says: [dialogue]` for pure B-roll voiceovers).
*   Subtitles Negative Filter: Never use standard quotation marks around the dialogue, and always append `--no subtitles` to prevent the engine from generating burned-in text.

<!-- CONTEXT: Google Flow Prompting Guide / 2. The Decoupled Reference Image Strategy (Perfect for Shorts) -->
### 2. The Decoupled Reference Image Strategy (Perfect for Shorts)
To generate highly consistent visual aesthetics without body warping or background morphing, always decouple your scene composition:
*   **Background Reference Image:** Use a high-quality static photo of the environment (e.g., Squamish ocean bluff, modern cedar beach house).
*   **Clothing/Likeness Reference Image:** Use a high-quality portrait photo of the clothes you want the avatar to wear.
*   **Decoupled Prompts:** When writing video scene prompts in Google Labs Flow, describe *only* action, camera views, and movement. Reference the visual inputs explicitly at the bottom: `"Reference the two pictures for clothes and background."`

<!-- CONTEXT: Google Flow Prompting Guide / 3. The "Studio Black" & Ken Burns Picture B-Roll Pipeline (Perfect for Long-Form) -->
### 3. The "Studio Black" & Ken Burns Picture B-Roll Pipeline (Perfect for Long-Form)
When producing longer videos, lining up continuous AI avatar footage directly causes noticeable frame shifts and jarring jump-cuts. We solve this with the **Studio Black B-Roll Pipeline**:
*   **Studio Black Backdrop:** Generate all long-form avatar talking-head clips against a **solid matte black-box studio background** (Picture 1 reference: `A premium 8k cinematic photo of a professional dark black-box filming studio...`). This completely eliminates background rendering artifacts and channels 100% of the AI's rendering power into flawless facial clarity and lip-syncing.
*   **Midjourney Ken Burns Hack:** Instead of rendering heavy B-roll video, generate ultra-high-resolution 4K/8K landscape images for free in Midjourney Pro. In DaVinci Resolve, place these high-end images directly over the transition boundaries between your 10-second avatar clips.
*   **The Zoom/Pan Motion:** Apply a subtle **Ken Burns effect** (slow panning or zooming) to the high-res Midjourney B-roll images in post-production. This completely masks the avatar's transition jump-cuts, keeps the editing workflow incredibly fast, and creates a highly professional, clinical masterclass aesthetic.

<!-- CONTEXT: Google Flow Prompting Guide / 4. Phonetic Spelling Guide for Peptide & Construction Terms -->
### 4. Phonetic Spelling Guide for Peptide & Construction Terms
When the text engine encounters complex clinical or construction terms, write the script phonetically inside the dialogue box using simple, hyphenated syllables to prevent slurring:
*   **Tirzepatide** $\rightarrow$ `tir-zepa-tide`
*   **Retatrutide** $\rightarrow$ `ret-a-troo-tide`
*   **Semaglutide** $\rightarrow$ `sema-gloo-tide`
*   **Tesamorelin** $\rightarrow$ `tesa-more-ellin`
*   **Ipamorelin** $\rightarrow$ `ipa-more-ellin`
*   **CJC-1295** $\rightarrow$ `C-J-C twelve ninety-five`
*   **GHK-Cu** $\rightarrow$ `G-H-K copper`
*   **AOD-9604** $\rightarrow$ `A-O-D ninety-six zero-four`
*   **Geotechnical** $\rightarrow$ `geo-technical`
*   **Shotcrete** $\rightarrow$ `shot-crete`
*   **Biophilic** $\rightarrow$ `bio-philic`


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]

**Related:** [[20260610_YOUTUBE_SCRIPTS_research_the_elevenlabs_and_google_flow_voice_generation_bes]] · [[20260610_VIDEO_PROD_deep_research_into_google_flow_batch_processing_and_automati]] · [[POSS_001_GOOGLE_FLOW_SEGMENTS]]
