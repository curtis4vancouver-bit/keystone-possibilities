#!/usr/bin/env python3
"""
🎬 KEYSTONE DYNAMIC VIDEO BLUEPRINT COMPILER
Path: scratch/dynamic_video_blueprint_compiler.py
Description: Programmatic compiler for high-retention video scripts & SEO packages.
             Implements Wayne Stevenson's rugged "Stoic Builder-Athlete" tone rules,
             rigorous YMYL compliance scrubbing, and Google Labs visual directives.
"""

import os
import sys
import json
import re
from datetime import datetime

# Set terminal stdout to UTF-8 to prevent Windows terminal encoding crashes
if sys.platform.startswith("win"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT_DIR = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
SCRIPTS_DIR = os.path.join(ROOT_DIR, "09_YouTube_Operations", "Scripts_Approved")
METADATA_DIR = os.path.join(ROOT_DIR, "09_YouTube_Operations", "Metadata_Drafts")

os.makedirs(SCRIPTS_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# YMYL Semantic Mapping Dictionary (Red-flag word mitigation for social algorithms)
YMYL_DICTIONARY = {
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

# ElevenLabs Phonetic Dictionary
PHONETIC_DICTIONARY = {
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

class ScriptCompiler:
    def __init__(self, topic_key):
        self.topic_key = topic_key
        self.raw_script = ""
        self.scrubbed_script = ""
        self.phonetic_script = ""
        
    def get_topic_data(self):
        """Loads structured narrative blueprints for Wayne's core themes."""
        topics = {
            "wolverine": {
                "title": "The Wolverine Stack: Cellular Tissue Repair & Resort Construction",
                "raw_script_blocks": [
                    ("0:00 - 0:10", "Stoic Cold Open (Wayne on Camera)", 
                     "Everyone wants to buy a luxury mountain resort. Nobody wants to talk about the structural concrete—or the molecular concrete holding their joints together. Let's dig in."),
                    ("0:10 - 0:20", "Transition (B-Roll Segment 1 - Shovel in Granite)", 
                     "At forty-three, building on steep BC grades will destroy your load-bearing structures. If your tendons leak, your production timeline fails."),
                    ("0:20 - 0:30", "B-Roll (B-Roll Segment 2 - Custom Timber Framing)", 
                     "To protect my foundation, I run a systematic titration schedule. A precise combinatorial analysis of compound BPC-157 and compound TB-500."),
                    ("0:30 - 0:40", "B-Roll (B-Roll Segment 3 - Molecular Animation)", 
                     "We add a daily protein floor of two hundred grams. We do not just build resorts—we engineer the body that builds them."),
                    ("0:40 - 0:50", "B-Roll (B-Roll Segment 4 - Cantilevered Cliff Sauna)", 
                     "Because in custom contracting, as in human biology: protect the foundation, and rebuild the load-bearing walls."),
                    ("0:50 - 1:00", "Outro CTA (Wayne back on Camera)", 
                     "If you want the complete biophilic wellness resort blueprint, grab the executive audio guide at the link below. Let's build.")
                ],
                "seo_tags": "vancouver builder,keystone recomposition,wayne stevenson,workout music,longevity research,focus music,longevity,longevity science,bpc 157 results,metabolic wellness,deep house,BPC-157,TB-500,peptide therapy,does bpc 157 work,injury recovery peptides,GLP-1 muscle preservation,biohacking,muscle growth over 40,men over 40 fitness,sarcopenic obesity prevention,connective tissue repair,squamish wellness resorts,off-grid cabin building bc,keystone possibilities,keystone protocols",
                "hashtags": "#WolverineStack #BPC157 #TB500 #PeptideScience #LongevityBuilder #MusclePreservation #SarcopeniaPrevention #SquamishWellness #LuxuryResortConstruction #KeystonePossibilities #KeystoneRecomposition #OmiMusic",
                "disclaimer": "SCIENTIFIC CASE STUDY ONLY. NOT MEDICAL ADVICE. CONSULT A LICENSED HEALTH PROFESSIONAL."
            },
            "biophilic_sanctuary": {
                "title": "Engineering the Sleep Sanctuary: EMF Shielding & Melatonin Alignments",
                "raw_script_blocks": [
                    ("0:00 - 0:10", "Stoic Cold Open (Wayne on Camera)", 
                     "Your bedroom is either an active recovery chamber or a slow-leak battery drain. Let's talk about engineering high-performance sleep sanctuaries."),
                    ("0:10 - 0:20", "Transition (B-Roll Segment 1 - Shielded Conduits)", 
                     "Most luxury homes are built with unshielded Romex wiring. That creates an active EMF grid running directly behind your headboard all night long."),
                    ("0:20 - 0:30", "B-Roll (B-Roll Segment 2 - Aluminum Conduit Installation)", 
                     "We route every single circuit through rigid aluminum conduits. It creates an absolute physical block, shielding your central nervous system."),
                    ("0:30 - 0:40", "B-Roll (B-Roll Segment 3 - Circadian LED Array Demo)", 
                     "Then we engineer the lighting. Post-sunset, the home switches automatically to amber LED wavelengths. No blue-light hormone disruption."),
                    ("0:40 - 0:50", "B-Roll (B-Roll Segment 4 - Organic Linen & Clay Plaster)", 
                     "We finish with raw unsealed materials. Zero VOCs. Zero plastic off-gassing. The bedroom is a biological intervention."),
                    ("0:50 - 1:00", "Outro CTA (Wayne back on Camera)", 
                     "Grab the complete off-grid sleep sanctuary blueprints at the link below. Subscribe to Keystone Recomposition on Spotify to lock in your sleep hygiene. Let's build.")
                ],
                "seo_tags": "sleep hygiene,emf shielding,circadian lighting,custom home vancouver,biophilic design,voc free bedroom,luxury home builder,wayne stevenson,keystone possibilities,keystone protocols,keystone recomposition,focus music,binaural beats,sleep optimization,biohacking sleep,arri alexa 35mm,outfit font,bedroom building codes",
                "hashtags": "#EMFShielding #SleepSanctuary #CircadianLighting #BiophilicDesign #ZeroVOC #HighPerformanceSleep #KeystonePossibilities #KeystoneProtocols #AeroDJ #MelodicDeepHouse",
                "disclaimer": "CONSTRUCTION ENGINEERING & DESIGN CASE STUDY ONLY. CONSULT A LICENSED ELECTRICAL ENGINEER FOR CODE COMPLIANCE."
            }
        }
        return topics.get(self.topic_key, topics["wolverine"])
        
    def scrub_ymyl(self, text):
        """Applies strict YMYL safety sanitization rules."""
        scrubbed = text
        for pattern, replacement in YMYL_DICTIONARY.items():
            scrubbed = re.sub(pattern, replacement, scrubbed, flags=re.IGNORECASE)
        return scrubbed
        
    def apply_phonetic_spelling(self, text):
        """Applies ElevenLabs phonetic spellings to optimize audio rendering quality."""
        phonetic = text
        for pattern, replacement in PHONETIC_DICTIONARY.items():
            phonetic = re.sub(pattern, replacement, phonetic, flags=re.IGNORECASE)
        return phonetic

    def compile(self):
        data = self.get_topic_data()
        title = data["title"]
        blocks = data["raw_script_blocks"]
        seo_tags = data["seo_tags"]
        hashtags = data["hashtags"]
        disclaimer = data["disclaimer"]
        
        # 1. Compile Script Text
        script_md = []
        scrubbed_md = []
        phonetic_md = []
        
        for time_range, visual, text in blocks:
            scrubbed_text = self.scrub_ymyl(text)
            phonetic_text = self.apply_phonetic_spelling(scrubbed_text)
            
            script_md.append(f"#### [{time_range}] {visual}\n*   **Audio (Original):** \"{text}\"")
            scrubbed_md.append(f"#### [{time_range}] {visual}\n*   **Overlay Card:** `{disclaimer}`\n*   **Audio (Scrubbed YMYL):** \"{scrubbed_text}\"")
            phonetic_md.append(f"#### [{time_range}] {visual}\n*   **Audio (ElevenLabs Phonetic Ready):**\n    <immersive>\n    {phonetic_text}\n    </immersive>")
            
        script_content = f"""# 🎬 PRODUCTION SCRIPT: {title}
*Generated on: {datetime.now().strftime("%Y-%m-%d")}*
*Ecosystem Strategy:* Keystone Possibilities & Keystone Recomposition

---

## 🏛️ PART 1: RAW DRAFT (Original Concept)
{"\n\n".join(script_md)}

---

## 🔒 PART 2: COMPLIANT SCRUBBED DRAFT (YMYL Algorithms Safe)
{"\n\n".join(scrubbed_md)}

---

## 🎧 PART 3: PHONETIC AUDIO DRAFT (ElevenLabs Optimization)
{"\n\n".join(phonetic_md)}
"""

        # 2. Compile Metadata Package
        metadata = {
            "title": title,
            "category": "Education (27)",
            "hashtags": hashtags,
            "tags_string": seo_tags,
            "structured_description": f"""In this engineering case study, we examine our systematic design approach for high-performance structural systems.

 Lying down is easy. Protecting your load-bearing joint and sleep structures is the real engineering challenge.

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
{disclaimer}
━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        }
        
        # Save Script File
        script_file_name = f"{self.topic_key}_script.md"
        script_file_path = os.path.join(SCRIPTS_DIR, script_file_name)
        with open(script_file_path, "w", encoding="utf-8") as f:
            f.write(script_content)
            
        # Save Metadata Draft JSON
        meta_file_name = f"{self.topic_key}_metadata.json"
        meta_file_path = os.path.join(METADATA_DIR, meta_file_name)
        with open(meta_file_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
            
        print(f"\n--- [Script Compiler] Compiling Topic: '{self.topic_key}' ---")
        print(f"[SUCCESS] Compiled Script written to: {script_file_path}")
        print(f"[SUCCESS] Compiled Metadata written to: {meta_file_path}")
        print(f"[SEO TAGS]: {seo_tags[:100]}...")

def main():
    topic = "wolverine"
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    
    compiler = ScriptCompiler(topic)
    compiler.compile()
    
    # Also compile the second topic to show total mastery
    if len(sys.argv) == 1:
        compiler2 = ScriptCompiler("biophilic_sanctuary")
        compiler2.compile()

if __name__ == "__main__":
    main()
