"""
Evolved Dynamic Skill: youtube_script_compiler
Description: High-fidelity script and SEO packet compiler for custom YouTube scripts
"""

def compile_voice_notes_to_cinematic_script(raw_voice_notes: str, topic_key: str, duration_type: str = "short") -> dict:
    import re
    import json
    import datetime

    # 1. YMYL substitution dictionary
    ymyl_dict = {
        r"\bpeptides\b": "metabolic compounds",
        r"\bpeptide\b": "metabolic compound",
        r"\bprotocol\b": "case study",
        r"\bprotocols\b": "case studies",
        r"\bdosing\b": "titration schedule",
        r"\bdoses\b": "titration schedules",
        r"\bsource\b": "supply chain",
        r"\bsources\b": "supply chains",
        r"\bvendor\b": "supplier",
        r"\bvendors\b": "suppliers",
        r"\bfat burning\b": "lipid oxidation",
        r"\bstacking\b": "combinatorial analysis",
        r"\bstack\b": "combinatorial model",
        r"\binjections\b": "administration methods",
        r"\binjection\b": "administration method",
        r"\bOzempic\b": "metabolic research targets",
        r"\bMounjaro\b": "metabolic research targets",
        r"\bWegovy\b": "metabolic research targets",
        r"\bweight loss\b": "body recomposition",
        r"\blose weight\b": "body recomposition",
        r"\bfat loss\b": "lipid reduction",
        r"\bbuy peptides\b": "acquire compounds for study",
        r"\bpeptide supplier\b": "academic research supplier",
        r"\bpeptide supply\b": "research supply chain"
    }

    # 2. ElevenLabs phonetic dictionary
    phonetic_dict = {
        r"\bRetatrutide\b": "Retta true tide",
        r"\bTirzepatide\b": "Teer zeppa tide",
        r"\bSemaglutide\b": "Semma glue tide",
        r"\bBPC-157\b": "B P C one fifty seven",
        r"\bBPC157\b": "B P C one fifty seven",
        r"\bTB-500\b": "T B five hundred",
        r"\bTB500\b": "T B five hundred",
        r"\bGHK-Cu\b": "G H K copper",
        r"\bGLP-1\b": "G L P one",
        r"\bSarcopenia\b": "Sar ko peen ee ah",
        r"\bBiophilic\b": "By-o-fill-ic",
    }

    # Helper function to clean raw text and apply substitutions
    def scrub_ymyl(text: str) -> str:
        scrubbed = text
        for pattern, replacement in ymyl_dict.items():
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        return scrubbed

    def apply_phonetics(text: str) -> str:
        phonetic = text
        for pattern, replacement in phonetic_dict.items():
            phonetic = re.sub(pattern, replacement, phonetic, flags=re.IGNORECASE)
        return phonetic

    # 3. Clean raw voice notes and split into sentences
    cleaned_input = re.sub(r"\s+", " ", raw_voice_notes.strip())
    # Split by sentence end markers
    sentence_matches = re.split(r"(?<=[.!?])\s+", cleaned_input)
    sentences = [s.strip() for s in sentence_matches if s.strip()]

    if not sentences:
        sentences = ["No transcript data provided. We must engineer the foundation first."]

    # 4. Group sentences into segments of ~10 seconds each (1-2 sentences)
    # A standard speaker talks at about 130-150 words per minute (~2.5 words per second).
    # 10 seconds is about 25 words.
    segments = []
    current_chunk = []
    current_word_count = 0

    for s in sentences:
        words_in_s = len(s.split())
        if current_word_count + words_in_s > 25 and current_chunk:
            segments.append(" ".join(current_chunk))
            current_chunk = [s]
            current_word_count = words_in_s
        else:
            current_chunk.append(s)
            current_word_count += words_in_s
    if current_chunk:
        segments.append(" ".join(current_chunk))

    # Limits segments to 6 for standard 60-second Short, or allows more if long-form
    if duration_type == "short":
        segments = segments[:6]
        # Pad if not enough segments
        while len(segments) < 6:
            segments.append("We build with precision—protect the load-bearing joints, and finish the job.")

    # 5. Mapping visual cues based on segment text content
    formatted_blocks = []
    for idx, text in enumerate(segments):
        start_sec = idx * 10
        end_sec = (idx + 1) * 10
        timecode = f"0:{start_sec:02d} - 0:{end_sec:02d}"

        # Detect B-Roll theme
        lower_text = text.lower()
        if "sleep" in lower_text or "emf" in lower_text or "bedroom" in lower_text or "shield" in lower_text:
            visual = "B-Roll (EMF Shielding & Conduit Installation)"
            prompt = "Shot on ARRI Alexa Mini, Zeiss Master Prime 50mm lens. Low-key warm side-lighting on a rigid aluminum conduit running along a raw solid cedar beam. Clean, modern, organic timber texture, film grain."
        elif "peptide" in lower_text or "bpc" in lower_text or "tb-500" in lower_text or "joint" in lower_text or "tendon" in lower_text or "repair" in lower_text or "wolverine" in lower_text:
            visual = "B-Roll (Molecular Tissue Repair Animation)"
            prompt = "Shot on ARRI Alexa Mini, Zeiss Master Prime 35mm lens. Cinematic macro close-up of dark charcoal steel reinforcement rebars being structurally welded on site. Spark reflections on metallic surfaces, raw texture."
        elif "sauna" in lower_text or "plunge" in lower_text or "contrast" in lower_text or "recovery" in lower_text:
            visual = "B-Roll (Cantilevered Cliff Sauna & Contrast Therapy)"
            prompt = "Shot on ARRI Alexa Mini, anamorphic 35mm lens. A slow forward push on a cantilevered raw timber sauna overlooking misty Squamish fjord waters at dusk. Rising steam wisps, steel grey water, moody Pacific Northwest atmosphere."
        elif "excavator" in lower_text or "granite" in lower_text or "grade" in lower_text or "dirt" in lower_text or "foundation" in lower_text:
            visual = "B-Roll (Site Grading & Concrete Foundation)"
            prompt = "Shot on ARRI Alexa, 35mm. Slow dolly-in on a heavy steel excavator scoop clearing wet Squamish granite. Overcast morning, misty fog, sharp dark rocks, high physical grit."
        elif "protein" in lower_text or "diet" in lower_text or "eat" in lower_text or "nutri" in lower_text:
            visual = "B-Roll (Stoic Athlete Nutrition Prep)"
            prompt = "Shot on ARRI Alexa, 50mm lens. Minimalist macro shot of raw organic steaks and clean spring water on a rustic timber countertop. Diffuse natural window light, warm shadows, ultra-tactile food texture."
        else:
            # Default alternating visual cues
            if idx == 0:
                visual = "Stoic Cold Open (Wayne on Camera)"
                prompt = "Shot on ARRI Alexa Mini, Zeiss Master Prime 35mm lens. High-fidelity macro close-up of a rugged 43-year-old Canadian custom builder on site. S2M slow forward push, wind catching his shirt, natural skin texture, sharp details."
            elif idx == len(segments) - 1:
                visual = "Outro CTA (Wayne back on Camera)"
                prompt = "Shot on ARRI Alexa Mini, Zeiss Master Prime 35mm lens. High-fidelity macro close-up of Wayne Stevenson on camera speaking directly, warm side-lighting, organic pine forest background out of focus."
            else:
                visual = f"B-Roll (Custom Timber Framing Segment {idx})"
                prompt = f"Shot on ARRI Alexa Mini, Zeiss Master Prime 35mm f/1.4 lens. Slow cinematic pan showing massive hand-peeled cedar logs being structurally secured into a custom frame. Sawdust drifting in golden hour sunlight."

        formatted_blocks.append({
            "timecode": timecode,
            "visual": visual,
            "broll_prompt": prompt,
            "original": text,
            "scrubbed": scrub_ymyl(text),
            "phonetic": apply_phonetics(scrub_ymyl(text))
        })

    # 6. Compute Premium Title & Meta Tags
    title_suffix = topic_key.replace("_", " ").title()
    computed_title = f"The Stoic Builder's Guide: {title_suffix}"
    
    # Render Parts of the script
    part1_blocks = []
    part2_blocks = []
    part3_blocks = []

    for b in formatted_blocks:
        part1_blocks.append(f"#### [{b['timecode']}] {b['visual']}\n*   **B-Roll Camera Cue:** \"{b['broll_prompt']}\"\n*   **Audio (Original):** \"{b['original']}\"")
        part2_blocks.append(f"#### [{b['timecode']}] {b['visual']}\n*   **Audio (Scrubbed YMYL):** \"{b['scrubbed']}\"")
        part3_blocks.append(f"#### [{b['timecode']}] {b['visual']}\n*   **Audio (ElevenLabs Phonetic Ready):**\n    <immersive>\n    {b['phonetic']}\n    </immersive>")

    merged_markdown = f"""# 🎬 PRODUCTION SCRIPT: {computed_title}
*Generated on: {datetime.datetime.now().strftime("%Y-%m-%d")}*
*Ecosystem Strategy:* Keystone Possibilities & Keystone Recomposition

---

## 🏛️ PART 1: RAW DRAFT (Original Concept)
{"\n\n".join(part1_blocks)}

---

## 🔒 PART 2: COMPLIANT SCRUBBED DRAFT (YMYL Algorithms Safe)
{"\n\n".join(part2_blocks)}

---

## 🎧 PART 3: PHONETIC AUDIO DRAFT (ElevenLabs Optimization)
{"\n\n".join(part3_blocks)}
"""

    seo_tags = f"keystone possibilities,wayne stevenson,squamish custom homes,whistler custom contracting,{topic_key.replace('_', ' ')},wellness retreat build,stoic builder athlete,elevenlabs voice,omi digital integration,keystone protocols,keystone recomposition"
    hashtags = f"#{title_suffix.replace(' ', '')} #KeystonePossibilities #KeystoneRecomposition #SquamishBuilder #StoicAthlete #OmiMusic"

    metadata = {
        "title": computed_title,
        "category": "Education (27)",
        "hashtags": hashtags,
        "tags_string": seo_tags,
        "structured_description": f"""In this technical architectural case study, we examine our systematic design approach for high-performance structural systems.

 Lying down is easy. Rebuilding the structural framework of your body and your home is the real engineering challenge.

TIMESTAMPS:
0:00 — Stoic Cold Thesis
0:10 — The Structural Degradation Threat
0:20 — Physical Infrastructure Optimization
0:30 — Environmental Control Arrays
0:40 — High-End Finished Biophilic Showcase
0:50 — Outro: Spotify Recovery & Client Blueprints

━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 SONIC IDENTITY:
All background music in this case study is sourced from the Official Artist Channel 'Keystone Recomposition'.
Stream the full catalog on Spotify: https://open.spotify.com/artist/keystone-recomposition
Subscribe to the OAC on YouTube: @KeystoneRecomposition

🏗️ THE BLUEPRINT:
Need luxury custom home project management or civil construction services in Squamish, Whistler, or Vancouver?
Let's build together: https://keystonepossibilities.ca

⚠️ SCIENTIFIC DISCLAIMER:
CONSTRUCTION & BIOCHEMISTRY CASE STUDY ONLY. NOT MEDICAL ADVICE. CONSULT A LICENSED PROFESSIONAL.
━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    }

    return {
        "status": "success",
        "title": computed_title,
        "script_md": merged_markdown,
        "metadata": metadata,
        "blocks": formatted_blocks
    }
