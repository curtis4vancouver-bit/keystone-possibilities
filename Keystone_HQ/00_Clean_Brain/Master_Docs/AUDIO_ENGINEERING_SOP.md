---
id: doc-audioengineeringsop
title: Audio Engineering Sop
type: document
summary: 'PROJECT: Keystone Recomposition Media Engine'
entities:
- DaVinci
- DaVinci Resolve
- ElevenLabs
- Keystone Recomposition
created: '2026-05-23T18:19:59.206473'
updated: '2026-06-14T19:57:35.971668'
---
# SOP: Electroacoustic Audio Engineering & Mastering
**PROJECT:** Keystone Recomposition Media Engine  
**SYSTEM TARGET:** Intelligible Synthetic Narration & Ambient Focus Beds  
**METHODOLOGY:** Spectral Carving, Dynamic Sidechaining, and Continuous Room Tone Synthesis  

---

<!-- CONTEXT: Audio Engineering Sop / 1. Psychoacoustics & The Realism Paradox -->
## 1. Psychoacoustics & The Realism Paradox

Synthetic text-to-speech (TTS) engines generate vocal signals in absolute, sterile digital silence ($-\infty$ dBFS) during narrative pauses. Layering this dry vocal track directly over ambient [[music|music]] beds creates the **realism paradox**: the voice sounds artificially detached, sits awkwardly "on top" of the mix, or becomes completely drowned out by overlapping frequencies. 

To bridge this gap, we implement a highly calibrated electroacoustic mastering chain that addresses:
1.  **Spectral Masking:** Overlapping frequencies in critical auditory bandwidths.
2.  **Dynamic Amplitude Separation:** Volume changes triggered relative to dialogue activity.
3.  **Acoustic Continuity:** Continuous synthetic room tone to mask silent gaps.

---

<!-- CONTEXT: Audio Engineering Sop / 2. Electroacoustic Principles: Corrective EQ & Spectral Carving -->
## 2. Electroacoustic Principles: Corrective EQ & Spectral Carving

The human ear canal is naturally tuned to amplify frequencies in the **1 kHz to 4 kHz** range. ThisPresence Zone is the critical threshold for phoneme recognition, sibilant definition, and consonantal clarity. 

```text
       [ Ambient Music Track ]                  [ Synthetic Vocal Track ]
                 │                                         │
                 ▼                                         ▼
   [ Parametric EQ (Q≈1.0) ]                     [ High-Pass Filter (HPF) ]
   Wide Cut: -3 dB to -6 dB                      Steep roll-off at 80 Hz - 100 Hz
   Center: 2 kHz to 2.5 kHz                                │
                 │                                         ▼
                 │                               [ Surgical Notch (High Q) ]
                 │                               Notch boxiness: 250 Hz - 500 Hz
                 │                                         │
                 ▼                                         ▼
    ┌───────────────────────┐                  ┌───────────────────────┐
    │  Frequency carved out │ ◄────────────────┤ Dynamic presence area │
    │  dedicated vocal pocket│                  │  intelligible & pristine│
    └───────────────────────┘                  └───────────────────────┘
```

<!-- CONTEXT: Audio Engineering Sop / 1. Corrective EQ on Voice (Pre-Compression) -->
### 1. Corrective EQ on Voice (Pre-Compression)
Always clean up muddy and harsh frequencies *before* sending the vocal track to dynamics processors, or the compressor will react to unwanted low-end and boxy buildups.
*   **High-Pass Filtering (HPF):** Sweep upward from 80 Hz to 120 Hz (18 to 24 dB/octave slope) until the chest tone begins to thin out, then back it off slightly. This completely removes room rumble and digital low-frequency HVAC noise.
*   **Problematic Resonances (High-Q Surgical Cuts):**
    *   *Boxiness / Mud:* Apply a surgical cut (Q $\ge$ 2.5) between **250 Hz and 500 Hz** to clean up the low-mids.
    *   *Nasal Harshness:* Attenuate narrow spikes between **2.5 kHz and 3.5 kHz**.
    *   *Sibilance:* Surgical notch sweeps between **6 kHz and 8 kHz**.

<!-- CONTEXT: Audio Engineering Sop / 2. Spectral Carving on Music Bed -->
### 2. Spectral Carving on Music Bed
Do not increase vocal track gain to compete with background music. Instead, carve out a frequency pocket in the music track:
*   **Static Carve:** Apply a wide parametric cut of **$-2$ dB to $-6$ dB** to the ambient music track strictly between **1 kHz and 4 kHz** (Q $\approx$ 1.0).
*   **Dynamic Carve (Pro-Q 3 / SPACE):** Route the voice track as an external sidechain trigger to a dynamic EQ band on the music track centered at 2.5 kHz. The frequency dips $-4$ dB only when the narrator speaks, allowing the music to bloom back to full fidelity during narrative pauses.
*   **Mid-Side (M/S) Carving:** Apply the sidechain-triggered dynamic carve exclusively to the **Mid channel** of the music track. Gently boost the **Side channels** by **$+1.5$ dB above 8 kHz**. This flings lush ambient textures out to the absolute edges of the stereo field while keeping the center open and pristine for the mono synthetic voice.

---

<!-- CONTEXT: Audio Engineering Sop / 3. Dynamic Sidechain Compression (Volume Ducking) -->
## 3. Dynamic Sidechain Compression (Volume Ducking)

To prevent the instrumental track's overall amplitude peaks from masking the vocal, configure a transparent sidechain compressor on the music track keyed off the voice:

| Parameter | Standard Target | Justification |
| :--- | :--- | :--- |
| **Threshold** | $-15$ dB to $-25$ dB | Low enough to catch quiet consonant endings; prevents premature music volume surges. |
| **Ratio** | 2:1 to 4:1 | Soft, natural gain reduction. Ratios $> 5:1$ behave like limiters and cause pumping. |
| **Attack** | 20 ms to 100 ms | Prevents popping at dialogue starts. Allows vocal transients to cut through smoothly. |
| **Release** | 150 ms to 300 ms | Sweets spot. Too fast ($< 100$ ms) causes syllable pumping; too slow ($> 500$ ms) leaves dead holes. |

<!-- CONTEXT: Audio Engineering Sop / DAW Workflows -->
### DAW Workflows

#### 1. Cockos Reaper (ReaComp Routing)
1.  Insert **ReaComp** onto Track 1 (Music). Set Track Channels to **4** in the I/O menu.
2.  Drag routing send from Track 2 (Voice) directly onto the ReaComp interface. Change destination to **Auxiliary Audio 3/4**.
3.  Set ReaComp Detector Input to **Auxiliary Input (L/R) (3/4)**.
4.  Configure Ratio to **4:1**, Attack to **30 ms**, Release to **200 ms**, and lower Threshold to achieve a subtle ducking range of **$-4$ dB to $-6$ dB**.

#### 2. Adobe Audition (Essential Sound Auto-Ducking)
1.  Tag all vocal clips in the ESP as **Dialogue**.
2.  Tag background music clips in the ESP as **Music**.
3.  Check **Ducking** in the Music panel -> Set to "Duck against Dialogue clips".
4.  **Specialist Calibration:** Reduce the default Fade Speed from 800 ms down to a sweet spot of **400 ms to 500 ms** to prevent music from bleeding into the beginning of words.

#### 3. Audacity (Auto Duck Destructive Offline Render)
1.  Position the music track at the very top of the timeline stack. Mix down all dialogue clips into a single mono track and drag it directly underneath the music track.
2.  Select the music track (leave voice track below unselected).
3.  Go to Effect -> Volume & Compression -> **Auto Duck**.
4.  Adjust: Threshold **$-35$ dB**, Duck Amount **$-8$ dB**, Fade Down/Up **0.5s**, Max Pause **1.0s** (keeps ducking locked during brief vocal gaps). Click OK to render the envelope.

---

<!-- CONTEXT: Audio Engineering Sop / 4. Environmental Acoustics & Continuous Room Tone -->
## 4. Environmental Acoustics & Continuous Room Tone

Absolute silence ($-\infty$ dB) between vocal sentences triggers immediate alarm in the human brain, highlighting the artificiality of a synthetic voice. 

<!-- CONTEXT: Audio Engineering Sop / 1. Pink Noise Room Tone Matching -->
### 1. Pink Noise Room Tone Matching
Synthesize a continuous ambient noise floor by combining sound generation with spectral mapping:
1.  **Generate Pink Noise:** Pink noise exhibits energy distribution ($1/f$) that matches natural room acoustics.
2.  **Parametric EQ Match:** Put a parametric EQ on the pink noise track. Sweep a narrow boost around **60 Hz / 120 Hz** to mimic low-end HVAC rumble, and apply a high-frequency roll-off above **8 kHz** to match standard acoustic absorption.
3.  **Mix Level:** Run the room tone track continuously at a very low level (between **$-45$ dBFS and $-60$ dBFS**) just under the dialogue. **Never gate or duck this track.**

<!-- CONTEXT: Audio Engineering Sop / 2. AI-Based Room Tone Modeling (Fairlight / Neural Engine) -->
### 2. AI-Based Room Tone Modeling (Fairlight / Neural Engine)
In DaVinci Resolve Studio (Fairlight):
1.  Apply the DaVinci Neural Engine's **Dialogue Separator** to pull the ambient room texture from your physical video stems.
2.  Use the **Dialogue Matcher** to extract the acoustic characteristics (reveberant field and room tone) and apply it directly to the dry synthetic ElevenLabs voiceover track.

---

<!-- CONTEXT: Audio Engineering Sop / 5. Standardized Post-Production Workflow Sequence -->
## 5. Standardized Post-Production Workflow Sequence

Execute these steps in sequence to guarantee a world-class, commercial [[master|master]]:

```text
[ Step 1: Clean Voice ] ──────► Corrective HPF at 80-100Hz -> Notch boxy low-mids (250-400Hz)
             │
             ▼
[ Step 2: Layer Room Tone ] ──► Inject shaped continuous Pink Noise at -50 dBFS (Never ducked)
             │
             ▼
[ Step 3: Carve Instrumental ] ► Dynamic EQ bell at 2.5kHz on Music (Sidechain keyed to Voice)
             │
             ▼
[ Step 4: Duck Music ] ───────► Transparent sidechain compressor on Music (30ms Attack / 200ms Release)
             │
             ▼
[ Step 5: Master Bus Glue ] ──► Glue compressor (100ms Attack / 100ms Release / 1.5 dB reduction)
             │
             ▼
[ Step 6: Limiter Peak ] ─────► Limiter ceiling set to -1.0 dBFS (Prevents web streaming inter-sample clips)
```


---
📁 **See also:** [[Master_Docs/INDEX|← Directory Index]]
