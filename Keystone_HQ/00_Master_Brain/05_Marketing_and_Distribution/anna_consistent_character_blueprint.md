# 👩‍🎤 ANNA: CONSISTENT MUSIC VIDEO CHARACTER BLUEPRINT

*Objective:* Fully define, render, and lock in our primary female star, **Anna**, as a consistent character across all music videos. Integrates step-by-step setup guides, visual prompts, and seamless 10-second transition blocks.

---

## 🎨 CHARACTER DESIGN & VISUAL SPECS

*Anna is engineered to be an incredibly magnetic, ultra-premium, and highly professional international DJ and music producer. Her look perfectly blends modern high-fashion tech-wear with the biophilic, raw, organic coastal forest aesthetic.*

*   **Name (Dialogue Tag):** `Anna` (Always use `Anna says:` or `Anna's voiceover says:` to lock in her voice).
*   **Visual Profile:** 28-year-old female, long voluminous jet-black hair, high-contrast striking hazel eyes, elegant cheekbones, warm olive complexion, raw magnetic presence.
*   **Outfit (Style Lock):** Modern minimalist matte-charcoal cropped technical windbreaker, sleek minimalist silver accent jewelry, and high-end matte-black studio headphones resting around her neck.

---

## 📸 HOW TO LOCK IN ANNA'S CHARACTER IN GOOGLE FLOW

To keep Anna looking mathematically identical across every single video clip, follow this step-by-step pipeline using the Google Labs ecosystem:

### Step 1: Generate & Save the Reference Seed (Google Whisk)
1. Go to **Google Whisk** (the character-building module inside Google Labs).
2. Copy and paste the **Master Character Prompt** (found below) to generate a clean, clear portrait.
3. Once generated, save this high-resolution image to your computer. It is your **Character Reference Sheet**.

### Step 2: Set the "Character Reference" Ingredient in Flow
1. Open **Google Flow** and start your project.
2. In the left panel, navigate to the **Asset Management / Ingredients** section.
3. Click "Add Ingredient" and upload the saved portrait of Anna.
4. Set the tag type of this asset to **Character Reference** (or Actor Seed) and label it `Anna`.

### Step 3: Scenebuilder Character Retention
1. When generating clips, use the **Scenebuilder** timeline.
2. For each shot containing Anna, toggle on the **Anna Character Reference** ingredient.
3. In your visual prompts, refer to her strictly as **"the female subject, Anna"** and describe her clothing and black hair to reinforce the model's weights.
4. Keep the **enhancePrompt** setting turned **OFF** to prevent Flow from changing her facial structure or outfit.

---

## 🎙️ VOICE RECOMMENDATION FOR ANNA
In Google Flow, when you assign dialogue using the `Anna says:` syntax, Flow will prompt you to select or configure a vocal track. 
*   **Vocal Profile Target:** Select a **"Warm, Melodic, Confident, slightly deep, and clear female voice"** (e.g., the "Melodic Female" or "Warm Alto" presets).
*   **Consistency rule:** Do not change her name tag! Using `Anna says:` consistently across all scenes keeps her vocal footprint locked.

---

## 🎬 MASTER CHARACTER PROMPTS

### 1. THE REFERENCE GENERATION PROMPT (Use in Whisk / Imagen 3)
```text
A high-fidelity character reference sheet and cinematic portrait of Anna, a stunning 28-year-old international DJ and producer. She has long, sleek, voluminous jet-black hair, striking hazel eyes, elegant high cheekbones, a warm olive complexion, and a cool, magnetic presence. She is wearing a modern, minimalist matte charcoal cropped tech-jacket and high-end matte-black studio headphones loosely around her neck. Desaturated, premium color grade. Cinematic studio lighting on a neutral charcoal background, showing a clear, consistent view of her face and features. 8k, photorealistic.
```

---

## 🎵 THE 10-SECOND MODULAR SCENE TEMPLATES (STARRING ANNA)

*Use these templates to sequence Anna seamlessly inside your music videos. Notice the look-away and whip-pan transition tags that allow easy visual chaining.*

### 🎥 SCENE A: ANNA PERFORMING (TALKING & LOOK-AWAY HACK)
*   **Audio (Script):**  
    `Anna says: This track is calibrated to match the natural biophilic frequencies of the Squamish valley.`
*   **Video Prompt:**  
    `A premium, highly desaturated 8k cinematic shot of Anna, a stunning 28-year-old female DJ with voluminous jet-black hair and striking hazel eyes, wearing a matte-charcoal tech-jacket. She is standing behind natural cedar DJ decks on an oceanfront wellness deck. The camera slow dollies in as she speaks, lips perfectly synchronized to the script. At 0:08, Anna naturally turns her head to look off-camera to the left. At 0:09, the camera executes a rapid 1-second whip-pan to the left, dissolving into motion blur. --no watermark --no warped face --no subtitles`

### 🎥 SCENE B: ANNA MIXING (PURE MUSIC PERFORMANCE - NO DIALOGUE)
*   **Audio (Script):**  
    `[Techno beat drops heavily and synchronizes with her hand movement]`
*   **Video Prompt:**  
    `The video starts with a rapid camera tilt-down from the sky, emerging from light. A gorgeous close-up of Anna with long jet-black hair, wearing sleek studio headphones, actively tweaking a rotary dial on custom wooden mixer decks. Modern neon-accented lighting. Her expression is focused, confident, and magnetic. At 0:08, she looks directly up at the camera with a brilliant smile. At 0:09, the camera executes a rapid 1-second whip-pan to the right, dissolving into motion blur. --no watermark --no text artifacts --no subtitles`