# Mastering Artificial Intelligence Filmmaking: A Comprehensive Guide to Prompt Engineering in Google Labs Flow

Google Labs Flow is powered by the Veo 3.1 video generation model and the Nano Banana Pro image model. Professional workflows require a systematic approach to structured syntax, cinematic film grammar, spatial parameter manipulation, and multi-modal asset integration.

## The Foundational Mechanics of the Prompt Architecture

An optimized text prompt for video generation must serve as a comprehensive directorial blueprint using five core components:

1. **Subject Definition:** Establish the primary entity with intense specificity (demographics, attire, emotional state, physical characteristics).
   * *Example:* "A sophisticated elderly woman wearing a vintage Chanel-style suit with a stoic, unreadable expression."
2. **Kinetic Action:** Dictate physical movement and temporal energy using precise action verbs to engage the physics engine.
   * *Example:* "Strides confidently through the center, her footwork fast and intricate, creating a sense of relentless momentum."
3. **Context & Environment:** Define spatial parameters, lighting, background architecture, and secondary physical consequences (e.g., wind).
   * *Example:* "A dimly lit underground chamber, dust particles floating in the shafts of light from her headlamp."
4. **Stylistic Identity:** Instruct the model on color grading, film grain, and overall aesthetic texture.
   * *Example:* "Cyberpunk aesthetic, neon glow lighting, shot on medium-format analog film with pronounced grain."
5. **Technical Camera:** Direct the virtual lens, framing, focal depth, and dynamic movement.
   * *Example:* "Medium close-up shot, smooth lateral tracking movement from left to right, shallow depth of field."

---

## Advanced Strategies for Syntactical Precision

### The Contextual Framework (Persona-Task-Format-Context)
* **Persona:** "Act as an award-winning cinematographer"
* **Task:** "Generate a continuous 8-second sequence"
* **Format:** "16:9 aspect ratio, hyper-realistic style"
* **Context:** "Handheld camera work during the frantic chase sequence... movement reflecting the character's panic"

### Gemini Integration (Meta-Prompting)
Utilize Gemini 3.1 Pro as a "meta-prompter" by feeding it a base idea and instructing it to output a "meticulously crafted, narrative-style text-to-video prompt."

### The Physics of Action Verbs
* **Weighted Movement (Trudge, Lumber, Stomp):** Simulates heavy mass and slow velocity.
* **Fluid/Frictionless (Glide, Flow, Drift):** Creates smooth, continuous motion.
* **Aggressive/Rapid (Sprint, Gallop, Spin, Leap):** Triggers high-velocity calculations and motion blur.

---

## The Lexicon of Virtual Cinematography: Camera Syntax Engineering

### Defining the Frame
* **Wide Shot / Establishing Shot:** Defines location and scale.
* **Medium Shot:** Shows body language and interactions.
* **Close-Up / Extreme Close-Up:** Renders high-frequency details (pores, eye reflections).
* **Low-Angle / High-Angle:** Encodes power/intimidation or vulnerability.

### Dynamic Camera Movements
* **Z-Axis (Depth):** Dolly In / Push-In, Dolly Out / Pull-Out, Crash Zoom, Dolly Zoom (Vertigo Effect).
* **X/Y-Axes (Lateral/Vertical):** Pan Left/Right, Whip Pan, Tilt Up/Down, Tracking / Lateral Movement, Crane Up/Down.
* **Rotational:** Orbit 180 / Half-Orbit, 360-Degree Full Orbit.

### Lens Dynamics and Lighting
* **Lighting Syntax:** "three-point softbox setup," "Chiaroscuro lighting," "Golden hour backlighting," "rim light."
* **Focal Control:** "35mm cinematic lens," "gentle rack focus shifting from the person's eyes to their hands," "shallow depth of field."

---

## Omission Protocols: The Mechanics of Negative Prompting

Avoid conversational negations like "no walls" in the main prompt (which increases the probability of generating walls). Use a comma-separated list of nouns and adjectives in the negative prompt UI or appended syntax.

* **Universal Quality Control Tokens:** `text overlays, watermarks, captions, subtitles, words on screen, cartoon, illustration, painting, low resolution artifacts, compression noise, bad lip sync, artificial lighting, deformed hands, extra limbs, unnatural movements, camera shake`

---

## Acoustic Engineering: Prompting for Native Audio in Veo 3

The text prompt must contain explicit acoustic descriptors:
* **Ambient Sound (Room Tone):** "quiet room tone in the background," "the soft hum of the refrigerator."
* **Sound Effects (SFX):** "SFX of heavy rain and distant thunder."
* **Dialogue Generation:** Format strictly as `Character Name: "Exact dialogue text."` (e.g., `The character says: "I'm ready to try again tomorrow."`).
* **CRITICAL:** Always include `subtitles, captions` in the negative prompt to prevent visual text hallucination during dialogue.

---

## Pre-Production and Asset Generation: Leveraging Nano Banana Pro

* **Edit, Don't Re-roll:** If an image is 80% correct, use conversational editing (e.g., "Change the lighting to sunset and make the text neon blue") instead of generating a new asset.
* **Text Rendering:** Enclose exact text in double quotation marks. Keep under 25 characters. Define font style and placement.
* **Identity Locking:** Generate a character reference sheet displaying multiple angles. Use these references in subsequent prompts ("Keep the person's facial features and proportions exactly the same as Image 1").

---

## Multi-Modal Synthesis: Ingredients to Video and Scenebuilder

* **The '@' Operator:** Use `@` to query the asset library and inject specific images (Character/Subject, Background/Setting, Style/Texture) directly into the text prompt box. The textual instructions must complement the visual inputs.
* **Scenebuilder Mechanics:**
  * **Extend:** Used for continuous action. The prompt must describe what happens next in the unbroken timeline. Avoid drastic prompt changes.
  * **Jump To:** A direct editorial cut (spatial teleportation). The prompt acts as a hard reset for the environment while preserving the subject's physical appearance.

---

## API Batch Processing and Parameters

When using API endpoints (`/v1/video:batchAsyncGenerateVideoText`) or automation extensions:
* **Seed Control:** Fixing the seed allows for tweaking a single word and observing its isolated effect.
* **Concurrent Prompts:** Limit to 2-3 maximum to prevent server overload.
* **Prompt Delay:** ~30 seconds to allow API rate limits to reset.
* **Formatting:** Each discrete prompt in a batch file must be separated by a hard blank line.

---

## UI Keyboard Shortcuts for Rapid Workflow

* `Shift + V` : Isolate Video
* `Shift + I` : Isolate Image
* `Shift + U` : Isolate Uploads
* `/` or `Ctrl + F` : Focus Search Bar
* `Esc` : Unfocus Search Bar
* `Ctrl + U` : Upload Asset
* `Shift + →` / `Shift + ←` : Frame-by-Frame playback in Video Edit View
* `Ctrl + G` : Group into Collection