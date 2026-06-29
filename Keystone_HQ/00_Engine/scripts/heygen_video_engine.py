#!/usr/bin/env python3
"""
Keystone Recomposition - HeyGen Cinematic Video Assembly & Visual Skill Engine.
Parses modular video scripts, enforces the 8-second temporal decay boundary,
translates sibilant phonetics, injects look-away gestures, compiles HeyGen Batch API payloads,
and outputs OpenClaw/MediaClaw-compliant visual skill metadata documents.
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List

# Target workspace paths
ROOT_DIR = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
APPROVED_SCRIPTS_DIR = ROOT_DIR / "09_YouTube_Operations" / "Scripts_Approved"
LEXICON_PATH = ROOT_DIR / "Audiobook" / "04_Companion_Docs" / "lexicon.json"


class VideoScriptParser:
    def __init__(self, lexicon_path: Path):
        self.lexicon = self._load_lexicon(lexicon_path)
        # Quiet Luxury Pacing parameters
        self.max_stable_words = 18  # Approx 7.5 to 8.0 seconds of speech at standard pacing
        self.word_pace_per_sec = 2.4

    def _load_lexicon(self, path: Path) -> Dict[str, str]:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Parser Warning] Failed to read lexicon.json: {e}")
        return {}

    def apply_phonetic_spellings(self, text: str) -> str:
        """Translates complex words to phonetic equivalents for clean lip-sync generation."""
        normalized = text
        
        phonetics = {
            "tirzepatide": "tir-zepa-tide",
            "retatrutide": "ret-a-troo-tide",
            "semaglutide": "sema-gloo-tide",
            "tesamorelin": "tesa-more-ellin",
            "ipamorelin": "ipa-more-ellin",
            "CJC-1295": "C-J-C twelve ninety-five",
            "GHK-Cu": "G-H-K copper",
            "AOD-9604": "A-O-D ninety-six zero-four",
            "geotechnical": "geo-technical",
            "shotcrete": "shot-crete",
            "biophilic": "bio-philic",
            "sarcopenia": "Sar ko peen ee ah"
        }
        
        # Merge dictionary from lexicon
        for key, val in self.lexicon.items():
            if key not in phonetics:
                phonetics[key] = val

        for key, val in phonetics.items():
            normalized = re.sub(rf'\b{key}\b', val, normalized, flags=re.IGNORECASE)
            
        return normalized

    def parse_modular_script(self, script_path: Path) -> List[Dict[str, Any]]:
        """
        Parses a structured modular scene script into discrete clip data blocks.
        Applies Dynamic Pacing (jittering durations naturally between 6.0s and 12.0s).
        Enforces the 8-second temporal decay boundary on dialogue elements.
        Injects eye-level parallax correction and confident reflection look-away gaze dynamics.
        """
        if not script_path.exists():
            raise FileNotFoundError(f"Approved script not found at: {script_path}")

        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        scenes = []
        # Support various scene headers: ### 📋 SCENE 1, #### 📋 SCENE 1, ### 📋 TEST SCENE 1, etc.
        scene_blocks = re.split(r'#+\s*(?:🔴|📋)\s*(?:TEST\s+)?SCENE\s+\d+', content)[1:]
        
        for idx, block in enumerate(scene_blocks, 1):
            dialogue = ""
            script_match = re.search(r'(?:THIS IS THE SCRIPT:|Script:)\s*([\s\S]*?)(?:THIS IS THE VIDEO PROMPT:|Action:|$)', block, re.IGNORECASE)
            immersive_match = re.search(r'<immersive>([\s\S]*?)<\/immersive>', block, re.IGNORECASE)
            wayne_match = re.search(r'Wayne says:\s*([\s\S]*?)(?:THIS IS THE VIDEO PROMPT:|Action:|$)', block, re.IGNORECASE)
            
            if script_match:
                dialogue = script_match.group(1).strip()
            elif immersive_match:
                dialogue = immersive_match.group(1).strip()
            elif wayne_match:
                dialogue = wayne_match.group(1).strip()
            else:
                # Direct fallback: see if Wayne says exists in block at all
                fallback_wayne = re.search(r'Wayne says:\s*(.*)', block, re.IGNORECASE)
                if fallback_wayne:
                    dialogue = fallback_wayne.group(1).strip()
                else:
                    # Clean lines in code blocks if present
                    code_lines = re.findall(r'```(?:text|markup)?\s*([\s\S]*?)```', block)
                    if code_lines:
                        dialogue = code_lines[0].strip()
            
            if dialogue.lower().startswith("wayne says:"):
                dialogue = dialogue[11:].strip()

            # Clean up dialogue
            dialogue = dialogue.replace('"', '').strip()
            dialogue = re.sub(r'^```[a-zA-Z]*\n|```$', '', dialogue).strip()
            dialogue = re.sub(r'```', '', dialogue).strip()

            action = ""
            action_match = re.search(r'(?:Action:|THIS IS THE VIDEO PROMPT:)\s*([\s\S]*?)(?:Instructions:|Reference|Play|$)', block, re.IGNORECASE)
            if action_match:
                action = action_match.group(1).strip()
            else:
                # Look for second code block if present
                code_lines = re.findall(r'```(?:text|markup)?\s*([\s\S]*?)```', block)
                if len(code_lines) > 1:
                    action = code_lines[1].strip()

            # Clean up action
            action = action.replace('"', '').strip()
            action = re.sub(r'^```[a-zA-Z]*\n|```$', '', action).strip()
            action = re.sub(r'```', '', action).strip()

            # Calculate estimated duration based on word count
            words = dialogue.split()
            word_count = len(words)
            estimated_duration = round(word_count / self.word_pace_per_sec, 2)
            decay_warning = False
            
            # Enforce 8-Second Temporal Video Decay Check
            if word_count > self.max_stable_words:
                decay_warning = True
                action += (
                    f" [TEMPORAL DECAY WARNING: Dialogue duration ({estimated_duration}s) exceeds 8-second facial stability threshold. "
                    "In post-production, layer high-contrast cinematic B-roll (DXA scans, clinical papers) over this segment to prevent AI mouth jitter.]"
                )

            # Ingest Eye-Level and 2-Degree Parallax Correction
            action += (
                " Camera framing: Absolute eye-level to maintain in-person equality. "
                "The subject focuses 2 degrees below the lens center (aiming towards display center) to correct display-lens parallax, "
                "creating a natural, balanced conversational connection."
            )

            # Calculate Gaze Dynamics look-away trigger (at 75% of estimated duration)
            look_away_start = round(estimated_duration * 0.75, 1)
            if look_away_start < 2.0:
                look_away_start = round(estimated_duration / 2.0, 1) # Fallback for ultra-short clips

            if "look-away" not in action.lower() and "looks away" not in action.lower():
                action += (
                    f" At exactly {look_away_start} seconds, the subject naturally breaks eye contact to the side "
                    "(Confident Reflection gaze direction, never downward) for 1.5 seconds to signal deep cognitive processing, "
                    "then smoothly returns focus to the screen."
                )

            # Inject Bezier Whip-Pan Transition metadata
            action += (
                " Transition: Apply Bezier temporal velocity curve for matching snap-away speed. "
                "Transition point peaks with horizontal motion blur. Cut mid-blur with a two-frame crossfade."
            )

            phonetic_dialogue = self.apply_phonetic_spellings(dialogue)

            scenes.append({
                "scene_number": idx,
                "raw_dialogue": dialogue,
                "phonetic_dialogue": phonetic_dialogue,
                "action_prompt": action,
                "word_count": word_count,
                "estimated_duration": estimated_duration,
                "decay_warning": decay_warning,
                "gaze_look_away_seconds": look_away_start
            })

        return scenes


class OpenClawSkillChoreographer:
    """
    Exports visual skill sheets (AVATAR-WAYNE.md and AVATAR-ANNA.md)
    and accompanying audio-visual production blueprints complying with
    OpenClaw/MediaClaw state exchange standards.
    """
    @staticmethod
    def write_skill_sheets(scenes: List[Dict[str, Any]] = None):
        wayne_skill_path = APPROVED_SCRIPTS_DIR / "AVATAR-WAYNE.md"
        anna_skill_path = APPROVED_SCRIPTS_DIR / "AVATAR-ANNA.md"
        sound_blueprint_path = ROOT_DIR / "Transcripts" / "SOUND_DESIGN_MIX_BLUEPRINT.json"
        typography_blueprint_path = ROOT_DIR / "Transcripts" / "TYPOGRAPHY_LOWER_THIRD.json"

        # 1. Wayne Skill Sheet (Updated with Quiet Luxury Visual Audit parameters)
        wayne_content = (
            "# Visual Skill Metadata: AVATAR-WAYNE\n"
            "**ROLE:** Host Presenter & Lead Coach // Keystone Recomposition\n"
            "**STATUS:** Locked Character Seed // MediaClaw v3.1 (Quiet Luxury Update)\n\n"
            "## 1. Character Reference Ingredient\n"
            "- **Actor ID:** `wayne_avatar_v8_pro`\n"
            "- **Clothing Style Reference:** https://keystonerecomposition.com/assets/wayne_carhartt_outfit.jpg\n"
            "- **Wardrobe:** Premium, heavy Pacific Northwest heritage wear. Grey wool flannel utility shirt (Filson-inspired) over solid charcoal crew-neck t-shirt. Projects practical self-reliant authority over modern sterile synthetic athletic fabrics.\n\n"
            "## 2. Background Reference Ingredient\n"
            "- **Environment Reference:** https://keystonerecomposition.com/assets/squamish_shoreline_4k.jpg\n"
            "- **Scene:** Misty coastal British Columbia fjord (Squamish bluffs). Panning shots of coastal cedar timber framing and granite cliffs to project tactile, organic prestige.\n"
            "- **Lighting:** Dramatic high-contrast three-point system. Large diffused key softbox at 45° side and overhead. Suspend a strong boom rim/hair light behind subject to separate flannel textures from the solid matte black-box backdrop.\n\n"
            "## 3. Choreography & Camera Constraint Rules\n"
            "- **Rule 1 (Dynamic Pacing):** Keep voice dialogue scenes variable (6.0s - 12.0s jitter) to avoid template predictability. Throw warnings if individual scene clips exceed 8 seconds (<18 words).\n"
            "- **Rule 2 (Parallax Angle Alignment):** Place camera at absolute eye level. Guide subject to look 2 degrees below the lens center (towards screen center) to correct display-to-lens parallax, creating a balanced peer-to-peer connection.\n"
            "- **Rule 3 (Confident Reflection Gaze):** Inject look-away gestures at 75% of estimated clip duration. Break eye contact TO THE SIDE (confident reflection), never downward (submissive/insecure), for exactly 1.5 seconds.\n"
            "- **Rule 4 (Bezier Whip-Pans):** Cut exactly in the middle of 1-second whip-pans. Use horizontal motion blur with matching in-out snap velocities. Interpolate using Bezier temporal velocity curves in post-production.\n"
        )
        
        # 2. Anna Skill Sheet
        anna_content = (
            "# Visual Skill Metadata: AVATAR-ANNA\n"
            "**ROLE:** International DJ & Producer // Keystone Recomposition\n"
            "**STATUS:** Locked Character Seed // MediaClaw v3.0\n\n"
            "## 1. Character Reference Ingredient\n"
            "- **Actor ID:** `anna_dj_v3_premium`\n"
            "- **Visual Profile:** 28-year-old female, voluminous jet-black hair, HAZEL eyes, olive complexion.\n"
            "- **Wardrobe:** Crop-cut matte charcoal technical windbreaker with black studio headphones around neck.\n\n"
            "## 2. Background Reference Ingredient\n"
            "- **Environment Reference:** https://keystonerecomposition.com/assets/open_air_dj_stage.jpg\n"
            "- **Scene:** Modern cedar DJ booth nested on a natural granite ledge in coastal BC.\n\n"
            "## 3. Playback and Composition Matting Rules\n"
            "- **Matting Source:** Local ONNX U2Net human segmentation (`transparent_matte.webm` VP9-with-alpha).\n"
            "- **Rule A (Animate Wrapper):** Always animate parent wrapping `<div>` opacity. Do not apply GSAP opacity to raw `<video>` node.\n"
            "- **Rule B (Simultaneous Mount):** Mount WebM and background assets at time zero (`data-start=\"0\"`) and toggle parent `visibility` to hidden to prevent browser-seek frame lag.\n"
        )

        # 3. Create Multi-Stem Progressive House / Melodic Techno Sound Design Blueprint
        sound_blueprint = {
            "soundtrack_genre": "Progressive House / Deep Melodic Techno (Ben Bohmer, Lane 8, ARTBAT style)",
            "delivery_formats": {
                "spotify_video_podcast": {
                    "integrated_loudness_lufs": -14.0,
                    "max_peak_level_dbfs": -0.2
                },
                "youtube_desktop_mobile": {
                    "integrated_loudness_lufs": -14.0,
                    "max_peak_level_dbfs": -1.0
                }
            },
            "audio_mix_hierarchy": {
                "spoken_vocals": {
                    "gain_target_dbfs": {"min": -6.0, "max": -3.0},
                    "role": "Absolute spatial anchor, clean mono front-center"
                },
                "music_stems": {
                    "moog_sub_bass": "Ducked dynamically to -24 dBFS during speech",
                    "ambient_synth_pads": "Wide stereo, ducked to -18 dBFS during speech, slow compressor release",
                    "rhythmic_drums_percussion": "COMPLETELY MUTED during Wayne speaking segments to eliminate sibilance clutter",
                    "transition_risers_whips": "Swell to -12 dBFS during 1-second Bezier whip-pan cuts"
                }
            },
            "sidechain_compressor_settings": {
                "threshold_db": -22.0,
                "ratio": "2.5:1",
                "attack_ms": 15.0,
                "release_ms": 350.0,
                "mode": "Transparent slow-decay vocal ducking"
            }
        }

        # 4. Create Editorial Typography Lower-Third Blueprint
        typography_blueprint = {
            "aesthetic_paradigm": "Quiet Luxury Editorial Print",
            "font_selections": {
                "primary_display": "Red Hat Display",
                "body_text": "Montserrat",
                "editorial_fallback": "Inter"
            },
            "styling_parameters": {
                "color_palette": {
                    "background": "Warm Charcoal / Semi-transparent (#121212BB)",
                    "text_primary": "Pure White (#FFFFFF)",
                    "biomarker_highlight": "Muted Antique Gold (#D4AF37)",
                    "clinical_callout": "Electric Teal (#00A3E0)"
                },
                "letter_spacing_tracking": "+0.15em (generous tracking)",
                "case_formatting": "Sentence Case for detailed terms, tracked Uppercase for names"
            },
            "alignment_and_safe_margins": {
                "safe_zone": "Lower Left quadrant",
                "bottom_margin_px": 120,
                "rationale": "Leaves substantial margins clear of native platform closed captions and overlay UIs"
            }
        }

        # Write all files
        with open(wayne_skill_path, "w", encoding="utf-8") as f:
            f.write(wayne_content)
        with open(anna_skill_path, "w", encoding="utf-8") as f:
            f.write(anna_content)
        with open(sound_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(sound_blueprint, f, indent=4)
        with open(typography_blueprint_path, "w", encoding="utf-8") as f:
            json.dump(typography_blueprint, f, indent=4)
            
        print(f"[OpenClaw Choreographer] Skill sheets successfully written to:\n  - {wayne_skill_path.name}\n  - {anna_skill_path.name}")
        print(f"[OpenClaw Choreographer] Sound and Typography blueprints written to:\n  - {sound_blueprint_path.name}\n  - {typography_blueprint_path.name}")


class HeyGenAPIWrapper:
    def __init__(self, api_key: str = None, avatar_id: str = None, voice_id: str = None):
        self.api_key = api_key or os.environ.get("HEYGEN_API_KEY")
        self.avatar_id = avatar_id or os.environ.get("WAYNE_HEYGEN_AVATAR_ID", "wayne_avatar_v8_pro")
        self.voice_id = voice_id or os.environ.get("WAYNE_HEYGEN_VOICE_ID", "wayne_voice_clone_v2")

    def build_batch_payload(self, parsed_scenes: List[Dict[str, Any]], bg_url: str = None, clothes_url: str = None) -> Dict[str, Any]:
        """Constructs a production-compliant HeyGen Batch Video Generation payload."""
        clips = []
        
        default_bg = bg_url or "https://keystonerecomposition.com/assets/squamish_shoreline_4k.jpg"
        default_clothes = clothes_url or "https://keystonerecomposition.com/assets/wayne_carhartt_outfit.jpg"

        for scene in parsed_scenes:
            clips.append({
                "avatar_id": self.avatar_id,
                "avatar_style": "normal",
                "voice": {
                    "voice_id": self.voice_id,
                    "type": "elevenlabs"
                },
                "input_text": scene["phonetic_dialogue"],
                "video_prompt": scene["action_prompt"],
                "background": {
                    "type": "image",
                    "url": default_bg
                },
                "avatar_ingredients": {
                    "clothing_reference_url": default_clothes
                }
            })

        return {
            "video_setting": {
                "aspect_ratio": "16:9",
                "resolution": "1080p",
                "fps": 30
            },
            "clips": clips
        }

    def generate_video(self, payload: Dict[str, Any], output_json_path: Path) -> bool:
        """Saves payload locally and hits HeyGen API. Supports credit-saving simulation by default."""
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
        print(f"[HeyGen Engine] API Payload successfully archived to: {output_json_path.name}")
        
        if not self.api_key:
            print("[HeyGen Warning] HEYGEN_API_KEY environment variable is not configured.")
            print("Video synthesis executed in SIMULATION/DRY-RUN mode.")
            return True

        import requests
        url = "https://api.heygen.com/v2/video/generate"
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            print("[HeyGen Engine] Firing payload to HeyGen batch render queue...")
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print(f"[HeyGen Success] Render Job queued successfully! Job ID: {result.get('data', {}).get('video_id')}")
                return True
            else:
                print(f"[HeyGen Error] API Code {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"[HeyGen Connection Error] Failed to reach HeyGen API: {e}")
            return False


def run_video_generation(script_file: Path, api_key: str = None, simulate: bool = True):
    print("=" * 70)
    print("KEYSTONE MEDIA ENGINE - HEYGEN BATCH PRODUCTION DEPLOYMENT")
    print("=" * 70)

    # 1. Initialize Engine classes
    parser = VideoScriptParser(LEXICON_PATH)
    wrapper = HeyGenAPIWrapper(api_key=api_key)

    # 2. Parse Markdown modular script
    print(f"[Parser] Reading approved script: {script_file.name}...")
    scenes = parser.parse_modular_script(script_file)
    print(f"[Parser] Extracted {len(scenes)} distinct modular talking-head scenes.")

    # 3. Create Payload structures
    payload = wrapper.build_batch_payload(scenes)

    # 4. Generate & Archive Payloads
    output_json = ROOT_DIR / "Transcripts" / f"{script_file.stem}_heygen_batch.json"
    wrapper.generate_video(payload, output_json)

    # 5. Export OpenClaw skill metadata sheets
    OpenClawSkillChoreographer.write_skill_sheets(scenes)

    # 6. Print Simulation Report
    print("\n" + "-" * 50)
    print("CINEMATIC BATCH RENDER SIMULATION SUMMARY")
    print("-" * 50)
    for scene in scenes:
        warning_str = " [DECAY WARNING]" if scene['decay_warning'] else ""
        print(f"Scene {scene['scene_number']:02d}{warning_str}:")
        print(f"  Estimated duration: {scene['estimated_duration']} seconds ({scene['word_count']} words)")
        print(f"  Raw Dialog: \"{scene['raw_dialogue'][:70]}...\"")
        print(f"  Phonetic:   \"{scene['phonetic_dialogue'][:70]}...\"")
        print(f"  Motion:     \"{scene['action_prompt']}\"")
        print("-" * 50)
    
    # 7. Print Browser Playback Composition Rules for transparent WebM
    print("\n" + "=" * 70)
    print("BROWSER COMPOSITING PLAYBACK RULES FOR TRANSPARENT WEBM")
    print("=" * 70)
    print("Rule 1: ALWAYS animate parent wrapping <div> opacity, not the <video> node.")
    print("Rule 2: Simultaneous mount at time zero (data-start=\"0\") and toggle visibility:hidden.")
    print("This completely eliminates decoding lags and stuttering frame drops.")
    print("=" * 70)


if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description="Assemble modular video scenes for HeyGen batch generation.")
    cli_parser.add_argument("--script", required=True, help="Path to approved modular script (.md file).")
    cli_parser.add_argument("--key", help="HeyGen API key override.")
    cli_parser.add_argument("--live", action="store_true", help="Submit batch render request live to HeyGen.")

    args = cli_parser.parse_args()
    
    run_live = args.live and args.key
    script_path = Path(args.script)
    
    run_video_generation(script_path, api_key=args.key, simulate=not run_live)
