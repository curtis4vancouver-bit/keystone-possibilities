# Advanced Prompt Architecture for Photorealistic Image Generation in Google Labs Flow

The default output of modern text-to-image models often defaults to a hyper-polished, synthetic "AI look." Overcoming this bias requires suppressing the model's tendency toward perfection by emulating physical photographic mechanics, environmental imperfections, and camera physics.

## Google Labs Flow Model Architecture

*   **Imagen 3 Fast:** Latent Diffusion model optimized for low latency (~8 seconds). Moderate photorealistic fidelity, basic typographic rendering. Best for rapid prototyping.
*   **Imagen 3 (Standard):** Latent Diffusion model optimized for compositional complexity. High fidelity, reliable typography. Best for complex scene composition.
*   **Nano Banana 2:** Gemini 2.5 Flash Image model. Moderate to high fidelity, reliable typography. Best for rapid iteration.
*   **Nano Banana Pro:** Gemini 3 Pro Image model. Ultra-high fidelity, excellent typography. Best for studio-quality photorealism, exact camera emulation, and embedded text mockups.

---

## The "Aggressive Realism" Prompting Methodology

To prevent sterile, plastic outputs, replace aesthetic buzzwords (e.g., "photorealistic," "hyperrealistic," "8k," "masterpiece") with descriptions of physical conditions, mechanical limits, and natural imperfections.

*   **De-Cliché Method:** Define specific materiality (e.g., matte ceramic, brushed aluminum) and restrict color schemes to a tight 2-3 color palette instead of naming famous artists or using generic style terms.
*   **Situational Framing:** Contrast clean setups with messy real-world scenarios. Use phrases like "a rushed smartphone snapshot in a cramped hallway," "a candid mirror selfie," or "an unposed moment capturing natural body weight and fabric fold reactions."
*   **Imperfection-Driven Lighting:** Avoid balanced studio arrays. Specify "harsh overhead fluorescent lighting," "weak afternoon winter sunlight through dusty blinds," or "uneven light source casting heavy, unrefined shadows."

---

## Universal Prompt Architecture for Optical Emulation

Construct prompts sequentially using the following four-tier structure:

### 1. Subject and Demographic Specificity
Define exact age, body type, hair texture, posture, and micro-expressions.
*   *Example:* "A 30-year-old Caucasian woman with a slim build, wearing a fitted brown off-the-shoulder crop top, loose beachy waves."

### 2. Environmental Context and Spatial Grounding
Ground the background to specific, mundane locales and define light sources explicitly.
*   *Example:* "A small, aesthetic city café by a rainy window on a cloudy afternoon, natural light illuminating the scene, casting soft shadows."

### 3. Hardware Emulation (Camera Physics)
Emulate real camera hardware to dictate depth of field, field of view, and motion.
*   **Aperture (f-stop):** Use `f/1.4` to `f/2.2` for shallow depth of field (bokeh/portraits); use `f/8` to `f/11` for deep focus (landscapes/architecture).
*   **Focal Length:** 
    *   `24mm` for wide-angle distortion/environmental scale.
    *   `35mm` or `50mm` for standard, natural human field of view.
    *   `85mm` to `135mm` for compressed, flattering close-up portraits.
    *   `100mm Macro` for extreme close-up product/texture details.
*   **Shutter Speed:** Use `1/15 sec` to introduce intentional motion blur, or `1/1000 sec` to freeze fast action.
*   *Example:* "Environmental portrait, shot on Sony A7R IV, 35mm f/1.8, natural soft diffusion."

### 4. Materiality, Texture, and Imperfection
Introduce digital or analog visual noise to strip away the synthetic sheen. Use file indicators like "raw photo," "unedited," or specific RAW file extensions (`IMG_9854.CR2`). Referencing analog mediums ("shot on Kodak Portra 400", "35mm film scan") introduces realistic grain and color shifts.

---

## Epidermal Realism and Anatomical Truth

To eliminate "wax," "plastic," or "doll-like" skin:

1.  **Direct Texture Requests:** Command details with terms like "detailed skin texture," "visible pores," "pore-level detail," "micro-texture," and "fine skin grain."
2.  **Subsurface Lighting:** Request "subsurface scattering" so light realistically penetrates and diffuses beneath the skin surface, and specify "peach fuzz softly catching the backlight."
3.  **Imperfection Anchoring:** Explicitly request human flaws to break unnatural symmetry: "light freckles," "subtle under-eye bags," "rosacea," "chapped lips," "sunburst capillaries," or "slightly asymmetrical facial features."

---

## Constraint Engineering (Negative Prompting)

Use negative prompts (`--no [element]`) or explicit direct commands to suppress unwanted artifacts:

*   **Quality & Technical:** `blurry, pixelated, low resolution, grainy, distorted, noise, compression artifacts, jpeg artifacts, glitches.`
*   **Structural & Geometric:** `warped edges, floating objects, inconsistent shadows, curved walls, impossible geometry, distorted perspective, repeating patterns.`
*   **Synthetic & Artistic Bias:** `--no illustration, painting, drawing, 3d render, computer generated, cartoon, anime, sketch, CGI, vector art, oversaturated, artificial lighting, glossy surfaces.`
*   **Biological & Anatomical:** `--no plastic skin, waxy skin, airbrushed, zero smoothing, doll, unnatural skin, asymmetric face, poorly drawn face, extra limbs, deformed hands, extra fingers.`
*   **Dataset Watermark:** `watermark, text, logo, signature, copyright, blurry text.`

---

## Text Rendering and Typographic Integration

When using **Nano Banana Pro** for text integration, isolate the copy clearly from the rest of the prompt:
*   **Rule:** Wrap the exact text in double quotation marks and explicitly detail its placement, color, material, and font style.
*   *Example:* `A rustic wooden cookbook cover on a kitchen counter. Add a title centered on the front cover that reads, "Everyday Recipes" in orange block letters.`

---

## Iterative Refinement and Studio Mechanics

*   **Seed Constancy:** Lock the numerical seed (e.g., `-1010538901`) to maintain the exact structural composition while iteratively testing fine-tuned style descriptors or negative prompts.
*   **Reference Image Weighting:** Adjust the image weight slider to control the balance between the reference image's visual framework and the text prompt's instructions.
*   **Inpainting (Lasso Tool):** Isolate a flawed or synthetic region and describe the replacement target (e.g., "remove the object," "add realistic hand with five fingers"). Keep denoising strength low to preserve surrounding light and textures.
*   **Prompting by Doodling:** Draw rough sketches directly onto canvas selections to guide the spatial placement of newly generated elements.

---

## Manual Post-Processing for Residual Synthetics

To destroy remaining procedural smoothing on skin textures in software like Adobe Photoshop:

1.  Create a new blank layer above the image. Fill it with **50% Gray** and set the blend mode to **Overlay**.
2.  Go to `Filter > Noise > Add Noise`. Add **1% to 2% Monochromatic Noise** (Gaussian). This replaces missing pore-level detail with believable film grain.
3.  Use **Frequency Separation** to isolate and smooth out blotchy AI color transitions on the low-frequency layer without flattening the texture on the high-frequency layer.