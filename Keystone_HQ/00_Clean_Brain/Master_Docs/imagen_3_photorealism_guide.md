---
id: doc-imagen3photorealismguide
title: Imagen 3 Photorealism Guide
type: document
summary: The generation of photorealistic imagery via text-to-image models has undergone
  a paradigm shift, transitioning from a reliance on algorithmic inte...
entities: []
created: '2026-05-10T21:17:57.561182'
updated: '2026-06-14T19:57:36.021844'
---
# Advanced Prompt [[ARCHITECTURE|Architecture]] for Photorealistic Image Generation in Google Labs Flow

The generation of photorealistic imagery via text-to-image models has undergone a paradigm shift, transitioning from a reliance on algorithmic interpolation to the direct emulation of physical photographic mechanics. Within the Google Labs Flow environment, the underlying architectural models driving this platform—specifically the Imagen 3 family and the specialized Nano Banana variants—possess an unprecedented capacity to interpret natural language. Yet, their default outputs frequently veer toward a hyper-polished, synthetic aesthetic commonly referred to as the "AI look."

The primary challenge in modern prompt engineering is no longer achieving high resolution or coherent anatomy, but rather suppressing the generative model's inherent bias toward idealized perfection.

<!-- CONTEXT: Imagen 3 Photorealism Guide / The Google Labs Flow Ecosystem and Model Architecture -->
## The Google Labs Flow Ecosystem and Model Architecture

The Flow environment relies on two primary model families:

1.  **Imagen 3 Fast:** Latent Diffusion model optimized for Low Latency (~8 seconds). Moderate photorealistic fidelity, basic typographic rendering. Ideal for rapid prototyping and bulk generation.
2.  **Imagen 3 (Standard):** Latent Diffusion model optimized for Compositional Complexity. High fidelity, good typography. Ideal for complex photographic scene composition.
3.  **Nano Banana 2:** [[GEMINI|Gemini]] 2.5 Flash Image model. Default platform generation. Moderate to High fidelity, good typography. Ideal for rapid iteration.
4.  **Nano Banana Pro:** Gemini 3 Pro Image model. Precision Control. Ultra-High fidelity, Excellent typography. Ideal for studio-quality photorealism, exact camera emulation, embedded text mockups.

<!-- CONTEXT: Imagen 3 Photorealism Guide / The Fallacy of Aesthetic Intent and the "Aggressive Realism" Framework -->
## The Fallacy of Aesthetic Intent and the "Aggressive Realism" Framework

The most pervasive error in contemporary prompt engineering is the reliance on aesthetic buzzwords (e.g., "realistic," "cinematic," "studio lighting," "8k," "masterpiece"). These terms signal the AI to generate a sterile, lifeless image characterized by an unnatural level of sharpness and an exaggerated rendering of light and shadow.

**The "Aggressive Realism" Methodology:** Abandons stylistic descriptors entirely, replacing them with terminology that dictates the physical conditions of a photograph's capture. Real photographs are mechanically messy. 

*   Instead of "a beautiful portrait," specify "a rushed smartphone snapshot in a cramped room" or "a candid mirror selfie."
*   Prompt for "harsh fluorescent lighting," "weak winter sunlight," or "uneven light sources where parts of the image lose detail."
*   Subjects should never be described as "posing"; descriptions must focus on natural body shapes and fabric behavior reacting to gravity and posture.

**The De-Cliché Method:** Build style from foundational photography basics rather than relying on famous artist names. Define exact materiality (e.g., matte ceramic versus polished metal) and restrict the color palette to a tight 2-3 color scheme.

<!-- CONTEXT: Imagen 3 Photorealism Guide / The Universal Prompt Architecture for Optical Emulation -->
## The Universal Prompt Architecture for Optical Emulation

A professional-grade text-to-image prompt should sequentially address:

1.  **Subject and Demographic Specificity:** Define exact age, body type, hair texture, posture, and micro-expressions. Example: "A 30-year-old Caucasian woman with a slim build, wearing a fitted brown off-the-shoulder crop top... loose beachy waves."
2.  **Environmental Context and Spatial Grounding:** Ground the background to specific, mundane locales. Define lighting by its source, direction, and quality. Example: "a small, aesthetic city café by a rainy window on a cloudy afternoon... natural light illuminating the scene, casting soft shadows."
3.  **Hardware Emulation (Translating Camera Physics):** 
    *   **Aperture (f-stop):** e.g., f/1.4 for a shallow depth of field (bokeh/portraits), f/11 for sharp focus everywhere (architecture).
    *   **Shutter Speed:** e.g., 1/15 sec for natural motion blur.
    *   **Focal Length:** e.g., 24mm for wide angle, 35mm for standard field of view, 85mm for high-end close-up portraits, 100mm Macro for extreme product details.
    *   Example: "Environmental portrait of a man, shot on Sony A7R IV, 35mm f/1.8, natural soft diffusion."
4.  **Materiality, Texture, and Imperfection:** Deliberately integrate "Visual Noise" (film grain, dust particles, chromatic aberration). Utilize terminology like "raw photo," "unedited," or specific raw file extensions like "IMG_9854.CR2". Referencing analog mediums ("shot on Kodak Portra 400", "35mm film scan") strips away the digital sheen.

<!-- CONTEXT: Imagen 3 Photorealism Guide / Mastering Epidermal Realism and Anatomical Truth -->
## Mastering Epidermal Realism and Anatomical Truth

To combat algorithmic smoothing ("wax," "plastic," or "doll skin"):

1.  **Demand Texture:** Use terms like "detailed skin texture," "visible pores," "pore-level detail," "micro-texture," and "skin grain."
2.  **Sub-surface Lighting:** Use the term "subsurface scattering" so light penetrates and diffuses beneath the skin surface. Prompt for "peach fuzz softly catching the light."
3.  **Imperfection Anchoring:** Request flaws such as "light freckles," "subtle under-eye detail," "rosacea," "chapped lips," "sunburst capillaries," or "uneven skin tone." Add "slightly asymmetrical facial features" to break the AI symmetry.

<!-- CONTEXT: Imagen 3 Photorealism Guide / Constraint Engineering via Negative Prompting -->
## Constraint Engineering via Negative Prompting

Negative prompting acts as creative subtraction. Utilize clear negation phrases (`--no [element]`) or explicitly instruct the model to `avoid`, `without`, or `no`. Focus on the top 10 to 15 specific artifacts.

*   **Quality & Technical:** `blurry, pixelated, low resolution, grainy, distorted, noise, compression artifacts, jpeg artifacts, glitches.`
*   **Structural & Geometric:** `warped edges, floating objects, inconsistent shadows, curved walls, impossible geometry, distorted perspective, repeating patterns.`
*   **Synthetic & Artistic Bias:** `--no illustration, painting, drawing, 3d render, computer generated, cartoon, anime, sketch, CGI, vector art, oversaturated, artificial lighting, glossy surfaces.`
*   **Biological & Anatomical:** `--no plastic skin, waxy skin, airbrushed, zero smoothing, doll, unnatural skin, asymmetric face, poorly drawn face, extra limbs, deformed hands, extra fingers.`
*   **Dataset Watermark:** `watermark, text, logo, signature, copyright, blurry text.`

<!-- CONTEXT: Imagen 3 Photorealism Guide / Text Rendering and Typographic Integration -->
## Text Rendering and Typographic Integration

Nano Banana Pro excels at accurate text rendering. Distinctly separate the structural environment from the precise typographic instructions by wrapping the desired text in quotation marks and specifying its placement, color, and medium. 
*   Example: `Add a title to the center of the cookbook cover that reads, "Everyday Recipes" in orange block letters.`

<!-- CONTEXT: Imagen 3 Photorealism Guide / Advanced Studio Mechanics: Iterative Refinement -->
## Advanced Studio Mechanics: Iterative Refinement

*   **Seed Constancy:** Regenerate near-perfect images by manually inputting the original numerical seed (e.g., `-1010538901`) to make the starting point deterministic while altering stylistic keywords or appending negative prompts.
*   **Reference Image Weighting:** Adjust the slider to dictate how aggressively the AI should favor the visual data over the text description.
*   **Inpainting (Lasso Tool):** Highlight a corrupted region and prompt to "remove the object." Using a low denoising strength forces adherence to surrounding textures.
*   **Prompting by Doodling:** Draw rough shapes or annotate directly onto a generated image to indicate where a new element should be placed.

<!-- CONTEXT: Imagen 3 Photorealism Guide / Manual Post-Processing for Residual Synthetics -->
## Manual Post-Processing for Residual Synthetics

To break up residual synthetic smoothness on human skin in software like Photoshop:
1.  Create a new blank layer filled with 50% gray and set to 'Overlay'.
2.  Apply a 1% to 2% monochromatic noise filter.
This artificial grain convincingly substitutes for human skin pores and film grain. Frequency Separation can also smooth erratic AI lighting without destroying high-frequency skin textures.


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
