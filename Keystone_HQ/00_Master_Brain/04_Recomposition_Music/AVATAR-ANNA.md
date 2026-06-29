# Visual Skill Metadata: AVATAR-ANNA
**ROLE:** International DJ & Producer // Keystone Recomposition
**STATUS:** Locked Character Seed // MediaClaw v3.0

## 1. Character Reference Ingredient
- **Actor ID:** `anna_dj_v3_premium`
- **Visual Profile:** 28-year-old female, voluminous jet-black hair, HAZEL eyes, olive complexion.
- **Wardrobe:** Crop-cut matte charcoal technical windbreaker with black studio headphones around neck.

## 2. Background Reference Ingredient
- **Environment Reference:** https://keystonerecomposition.com/assets/open_air_dj_stage.jpg
- **Scene:** Modern cedar DJ booth nested on a natural granite ledge in coastal BC.

## 3. Playback and Composition Matting Rules
- **Matting Source:** Local ONNX U2Net human segmentation (`transparent_matte.webm` VP9-with-alpha).
- **Rule A (Animate Wrapper):** Always animate parent wrapping `<div>` opacity. Do not apply GSAP opacity to raw `<video>` node.
- **Rule B (Simultaneous Mount):** Mount WebM and background assets at time zero (`data-start="0"`) and toggle parent `visibility` to hidden to prevent browser-seek frame lag.

---
📁 **See also:** ← Directory Index