# SOP: Audiobook Production & Micro-Commerce Integration

**PROJECT:** Builder's Health & Recomposition  
**SYSTEM TARGET:** $70 High-Ticket Hybrid Digital Asset  
**STANDARDS:** ACX (Audible Compliance) & Shopify Starter Automation  

---

## Phase 1: Voice Synthesis & Script Formatting (ElevenLabs)

### 1. Script Pre-Processing & Normalization
TTS engines struggle with abbreviations, units, and symbols. Before importing the manuscript of *Builder's Health & Recomposition* into ElevenLabs, the text must undergo complete orthographic normalization:

| Raw Format | Spoken Form | Purpose |
| :--- | :--- | :--- |
| **1.6g/kg** | "one point six grams per kilogram" | Metric normalization for nutritional guides |
| **450 kcal** | "four hundred fifty kilocalories" | Expansion of energetic values |
| **1RM** | "one-rep maximum" | Conversion of specialized lifting acronyms |
| **RPE 9** | "rate of perceived exertion of nine" | Translation of subjective intensity scales |
| **Type II fibers** | "type two fibers" | Correct reading of roman numerals |
| **NEAT** | "n. e. a. t." (or "neat") | Explicit phonetic handling for acronyms |
| **$5/month** | "five dollars per month" | Expansion of financial values |
| **GLP-1** | "G L P one" | Sarcopenia/peptide tracking |
| **semaglutide** | "sema-gloo-tide" | Phonetic spelling override |

### 2. Custom Pronunciation Lexicons (.PLS)
For complex anatomical and physiological terminology, compile and upload a custom Pronunciation Lexicon Specification (`.pls`) file. Enforce correct syllable stress using explicit phonetic CMU Arpabet tagging:
```xml
<!-- Example: Correct stress on hypertrophy -->
<lexeme>
  <grapheme>hypertrophy</grapheme>
  <phoneme alphabet="cmu-arpabet" ph="hh ay - p er1 - t r aY - f i"/>
</lexeme>
```

### 3. ElevenLabs Voice Clone Configuration
Narrator settings inside ElevenLabs Voice Settings must match the following guidelines:
*   **Stability (0.60 to 0.70):** Prevents robotic monotony while avoiding emotional drift or erratic pacing.
*   **Style Exaggeration (0.00 to 0.15):** Keeps inflections authoritative and academic. Prevents dramatic whispering or breathing anomalies.
*   **Clarity / Similarity Optimization (0.75 to 0.85):** Adheres closely to the acoustic profile of Wayne's reference recordings.
*   **Pacing Settings (1.00):** Maintain default speed to preserve natural breath gaps. Dip to **0.95** only if technical sections require slower comprehension.
*   **Timeline Manipulation:** Insert `<break time="1.2s" />` tags between major concepts or paragraph transitions to simulate natural pausing.

---

## Phase 2: Mastering & ACX Compliance (Audacity Workflow)

Every exported audio file must adhere to standard audiobook technical specifications:

| Technical Variable | Required Specification Limit | Intent and Purpose |
| :--- | :--- | :--- |
| **File Format** | MP3, Constant Bit Rate (CBR) | Guarantees error-free encoding across playback devices |
| **Bit Rate** | 192 kbps or higher | Minimizes compression artifacts |
| **Sample Rate** | 44.1 kHz (44,100 Hz) | Standard high-resolution audio sampling rate |
| **Loudness (RMS)** | -23 dB to -18 dB RMS | Establishes uniform volume, eliminating listener adjustment |
| **Peak Amplitude** | Under -3.0 dBFS | Provides headroom to prevent clipping and distortion |
| **Noise Floor** | Under -60 dBFS | Eliminates hums, hisses, or fans |
| **Channel Count** | Uniform Mono or Stereo | Mono is preferred to keep download sizes small |

### Mastering Step-by-Step Chain (Audacity)

```text
[Raw WAV Export] 
       │
       ▼
[Filter Curve EQ] ────► Roll-off below 80 Hz (Microphone rumble) & above 16 kHz (Hiss)
       │
       ▼
[Loudness Normal] ───► Target precisely -20 dB RMS
       │
       ▼
[Soft Limiter] ──────► Limit at -3.5 dBFS with 10ms hold time (Prevents MP3 peaks clipping)
       │
       ▼
[Noise Reduction] ───► Apply "Noise of the Beast" (6 / 6 / 6) on silent room tone if required
       │
       ▼
[MP3 CBR Export] ────► 192 kbps, Mono
```

1.  **High-Pass & Low-Pass Filtering:**
    Apply a steep high-pass filter at **80 Hz** (EQ & Filters > Filter Curve) to eliminate low-frequency rumble. Concurrently, apply a low-pass filter rolling off above **16,000 Hz** to eliminate electronic hiss.
2.  **Audiobook Mastering Macro:**
    Import the official `498B. Audiobook-Mastering-Macro.txt` and run it via **Tools > Macro Manager** to automate:
    *   Primary sub-80 Hz roll-off.
    *   Loudness Normalization targeting exactly **-20.0 dB RMS**.
    *   Soft Limiter set to **-3.5 dBFS** (leaves a 0.5 dB buffer for MP3 compression expansion).
3.  **Noise Floor Adjustment (The "Noise of the Beast"):**
    If noise check reports values above -60 dBFS:
    *   Select 3-5 seconds of silent room tone -> Effect -> Noise Reduction -> Click **Get Noise Profile**.
    *   Select the entire track -> Apply Noise Reduction: **6 dB / 6 Sensitivity / 6 Frequency Smoothing**.
4.  **Structural Spacing Specs:**
    *   **Beginning:** 0.5 to 1.0 seconds of clean room tone before the voice starts.
    *   **Ending:** 1.0 to 2.0 seconds of clean room tone at the end.
    *   Opening credits, closing credits, and a 1–5 minute retail promotional sample must be saved as **separate files**.

---

## Phase 3: Storefront Deployment (Shopify Starter)

1.  **Plan Selection:** Activate the **Shopify Starter Plan at $5/month** (Settings > Plan).
2.  **Integrated Gateway:** Navigate to Settings > Payments. Configure **Shopify Payments** to capture Credit Cards, Apple Pay, and Google Pay.
3.  **Preferences & Access:** Go to Online Store > Preferences. Disable the password protection to make the checkout system live.
4.  **Spotlight Theme Styling:** Upload your luxury cover art, brand font, and a premium, high-converting product description.
5.  **Linkpop Setup:** Log in to `Linkpop.com` with your store credentials. Create `linkpop.com/builders_health`. Add the shoppable checkout card to bypass standard storefront browsing.

---

## Phase 4: Automated Delivery Integration

1.  **App Setup:** Install the official, free **Shopify Digital Downloads App** from the admin app store.
2.  **Product Creation:**
    *   Add product: "Builder's Health & Recomposition: The Complete Audiobook".
    *   **Shipping Bypass:** Uncheck "Physical product / Requires shipping" to prevent checkout friction.
    *   **Inventory Bypass:** Set inventory tracking to **"Not tracked"**.
3.  **File Packaging & Association:**
    *   Package your chapters, credits, and PDF checklists into a single, high-fidelity **`.zip` file** (limit: 5 GB).
    *   Upload the `.zip` file to the product in the Digital Downloads app.
4.  **Automation & Constraints:**
    *   Set fulfillment type to **"Sent automatically"** to deliver access links instantly upon transaction confirmation.
    *   Set download limit to **3 or 5** to prevent link sharing.
    *   Enable checkout downloads by dragging the Digital Downloads block into the Shopify Checkout Editor's Thank-You page.

---

## Phase 5: Testing & Auditing

1.  **Simulate Checkout:** Create a **100% discount code** in your Shopify dashboard. Go to your Linkpop page, add the product, apply the discount code, and finish checkout.
2.  **Audit the Confirmation Page:** Confirm that a styled "Download Now" button appears immediately on the Thank-You screen.
3.  **Audit the Email:** Verify that your "Downloads Ready" email arrives within 60 seconds with personal checkout variables.
4.  **Audit the Payload:** Download the `.zip`, unzip it, verify all chapters are present, and run Audacity's "ACX Check" on the MP3s to guarantee spectral compliance.