# Audiobook [[.agents/rules/workspace|Workspace]] Layout: Builder's Health & Recomposition

Use this directory to stage, process, and compile the premium audiobook system assets.

## Directory Mapping

*   **`01_Raw_Voice/`**: Contains raw `.wav` narration files synthesized from the ElevenLabs Custom Voice Clone API.
*   **`02_Music_Stems/`**: Houses ambient focus stems, intro/outro music files, and "The Resonance Suite" audio tracks.
*   **`03_Mastered_Chapters/`**: Staging directory for final ACX-compliant `.mp3` master files (CBR, 192kbps, Mono).
*   **`04_Companion_Docs/`**: Stores PDF outlines, Notion templates, and pronunciation lexicons.

## Production Checklist

- [ ] Write text-normalization config (`lexicon.json`).
- [ ] Run automated synthesis scripts to download raw `.wav` outputs.
- [ ] Process stems in Audacity using the ACX Mastering Macro.
- [ ] Compile Notion project management dashboard.
- [ ] Package final bundle as a single `.zip` delivery file.
