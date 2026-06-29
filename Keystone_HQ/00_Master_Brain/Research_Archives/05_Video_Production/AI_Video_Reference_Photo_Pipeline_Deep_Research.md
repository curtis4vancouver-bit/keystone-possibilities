# AI Video Reference Photo Pipeline — Deep Research Report
## Identity Consistency, Production Workflows & Legal Frameworks (2026)
### Source: Gemini Deep Research — May 12, 2026

---

## CRITICAL FINDING: THE EXACT TOOL STACK

### Tool-by-Tool Comparison

| Spec | Veo 3.1 | Kling 3.0 | Runway Gen-4.5 | Hailuo 3.0 | Seedance 2.0 |
|---|---|---|---|---|---|
| **Best For** | Realism + native audio | Cinematic motion + multi-shot | Pro control + post-edit | Extended 4K duration | Dynamic transitions |
| **Max Clip** | 8s (extendable) | 15s (6 connected shots) | 16s | 20s | 15s |
| **Native Audio** | ✅ Dialogue + SFX | ✅ Multilingual | ❌ Needs ElevenLabs | ✅ | ✅ |
| **Character Lock** | "Ingredients to Video" refs | Character ID (3-5 photos) | Single ref + Act-Two mocap | Advanced character ref | Pre-gen character sheets |
| **Max Resolution** | 4K native | 4K native | 4K | 4K | 1080p |
| **ELO Ranking** | — | #1 (1,243) | — | — | — |

### Which Tool for Which Scene

| Scene | Challenge | Use This Tool | Why |
|---|---|---|---|
| **Construction site** | PPE geometry, hard hats, scaffolding | Runway Gen-4.5 or Kling 3.0 | Object permanence keeps hard hat stable |
| **Gym/fitness** | Muscle deformation, weight physics | Kling 3.0 | Best human kinematics, foot placement |
| **Kitchen/cooking** | Fluid dynamics, particles | Runway Gen-4.5 | Superior liquid/surface simulation |
| **Beach/outdoors** | Light, wind, sand interaction | Veo 3.1 | Unmatched lighting physics |

---

## THE EXACT WORKFLOW (Step by Step)

### Phase 1: Character Sheet Creation
1. Take 15-30 high-quality reference photos (neutral background, soft lighting)
2. Use **Nano Banana Pro** to generate a **4-column character sheet**:
   - Front view | Left profile | Right profile | Back view
   - Full body on top, close-up portrait below each
3. This "Consistency Core" prevents identity drift across all video clips

### Phase 2: Pre-Generation (Keyframe Staging)
1. Use Nano Banana Pro to generate a **static 4K image** of yourself in the target environment
   - Example: You on a construction site in a hard hat and hi-vis vest
2. Adjust lighting, color mood, and depth of field to commercial quality
3. This keyframe image becomes the input for video generation (NOT text-to-video)

### Phase 3: Video Generation
1. Feed the staged keyframe + character sheet into the appropriate tool
2. **Construction ads:** Runway Gen-4.5 or Kling 3.0
3. **Health/beach content:** Veo 3.1
4. **Gym B-roll:** Kling 3.0
5. Use precise prompt architecture:
   > ❌ "Me on a construction site"
   > ✅ "wearing a mathematically symmetrical, high-visibility yellow ANSI Class 2 safety vest and a flawless, rigid white polycarbonate hard hat. Standing dynamically on a reinforced concrete foundation, examining blueprints. Background features heavy earth-moving machinery in sharp focus."

### Phase 4: DaVinci Resolve 20 Post-Production
1. **AI Motion Deblur** → removes synthetic motion artifacts
2. **AI UltraSharpen** → fixes focal softness on face
3. **Generative Extend** → stretches clips to fill timeline gaps (needs 12-24GB VRAM)
4. **AI Voice Isolation** → cleans ElevenLabs audio artifacts
5. **IntelliCut** → maps ElevenLabs audio to lip movements (ADR cues)
6. **Ducker Track FX** → auto-ducks music under dialogue

### Phase 5: Export for YouTube
| Resolution | FPS | Standard Bitrate | AI Video Optimal |
|---|---|---|---|
| 1080p | 30 | 8 Mbps | **12-15 Mbps** |
| 1080p | 60 | 12 Mbps | **15-18 Mbps** |
| 4K | 30 | 35-45 Mbps | **45-55 Mbps** |
| 4K | 60 | 53-68 Mbps | **68-85 Mbps** |

> **Critical:** Upload at HIGHER bitrate than standard to prevent YouTube's encoder from crushing AI texture details into visible macro-blocking.

---

## BODY TRANSFORMATION TRACKING (LoRA Workflow)

For documenting GLP-1 / peptide body transformation over months:

1. **Dataset:** Curate 15-30 photos of new physique [[STATE|state]] every 2-4 weeks
2. **Physique LoRA (0.6 weight):** Trains on new body shape WITHOUT overwriting face
3. **PuLID Adapter (0.8 weight):** Aggressively locks original facial identity
4. **ControlNet (OpenPose):** Forces correct posture and skeleton alignment
5. **AnimateDiff motion LoRAs:** Creates smooth temporal transitions for transformation videos

> ⚠️ NEVER just add "muscular body" to a text prompt — this causes identity drift and anatomical severing

---

## LEGAL FRAMEWORK

### Copyright Reality
- **Raw AI video output = NOT copyrightable** (no human authorship)
- **Post-produced video in DaVinci Resolve = copyrightable** (human creative decisions)
- Must demonstrate: timeline editing, compositing, color grading, sound design
- Use **C2PA / SynthID watermarks** for provenance tracking

### Protecting Your Likeness
- **Right of Publicity** protects your face, voice, name from unauthorized AI use
- **NO FAKES Act** (federal) provides civil remedies against unauthorized deepfakes
- If competitor uses your photos to train a LoRA → you can sue for:
  - Privacy violation
  - False endorsement
  - Defamation

### Trademark Strategy (Advanced)
- File a **federal trademark on your digital likeness** and visual brand aesthetic
- Provides nationwide takedown power against unauthorized AI clones
- Shifts legal burden from proving publicity rights to enforcing trademark infringement
- Precedent: celebrities successfully trademarked personas to combat AI cloning in 2024

---

## KEYSTONE-SPECIFIC APPLICATION

### Keystone Possibilities (Construction Ads)
- Use Runway Gen-4.5 for construction site B-roll with your face
- Generate: hard hat + hi-vis vest walking job sites, reviewing blueprints
- Post-produce in DaVinci Resolve → export at 12-15 Mbps 1080p for Google Ads

### Keystone Protocols (Health Videos)
- Use Veo 3.1 for beach/outdoor establishing shots
- Use Kling 3.0 for gym B-roll with muscle/weight physics
- Track body transformation with LoRA updates every 4-6 weeks
- Monthly face-on-camera provides E-E-A-T shield

### Keystone Recomposition (Music Videos)
- Use Veo 3.1 or Hailuo 3.0 for cinematic ambient visuals
- Generate: you DJing, studio shots, beach sunset scenes
- Hailuo 3.0's 20-second clips ideal for music video sequences


---
📁 **See also:** ← Directory Index
