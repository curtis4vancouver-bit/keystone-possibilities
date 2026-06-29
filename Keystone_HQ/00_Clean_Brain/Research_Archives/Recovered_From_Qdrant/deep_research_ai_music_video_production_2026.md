# Recovered from Qdrant Vector Database
# Original source_id: deep_research/ai_music_video_production_2026
# Chunks recovered: 2
# Recovery date: 2026-06-14

---

Deep Research: [[STATE|State]] of AI-Generated [[music|Music]] Videos in 2026. Domain: Video Prod. Researched: 2026-06-10 01:30. Source: Google Deep Research via Chrome Automation.

Foundation Models (May 2026):
- Kling 3.0: Native 4K, 30 FPS, bind_subject for character lock. Cinematic consistency leader.
- Runway Gen-4.5: High-motion, 3D lighting, generative editing. ~$0.12/sec. Higher cost.
- Luma Ray-3: Reasoning model, HDR, /extend + /interpolate endpoints. $1.20/5s (1080p).
- Veo 3.1: Photorealistic, fluid dynamics. Native audio.
- Sora 2: Unavailable post April 26, 2026.

Quality Benchmarks:
- Character consistency: Nano Banana 2.0 for [[Brand_Constitution/protocol/IDENTITY|identity]] lock (5 characters, 14 objects). Character Sheet = front/left/right/back + close-ups.
- Temporal coherence: 30-60 FPS minimum, native 4K. Reasoning models for physics.
- Multi-Modal Verifier: VLM ([[GEMINI|Gemini]] Flash) as automated QA. Score physical realism, instruction following, character consistency. Reject below threshold.

AutoMV Multi-Agent [[ARCHITECTURE|Architecture]] (4 stages):
1. MIR: SongFormer segmentation, htdemucs stem separation, Whisper ASR, Qwen2.5-Omni captioning
2. Screenwriter + Director [[AGENTS|Agents]]: Narrative → machine-readable shot scripts with durations/camera instructions
3. Keyframe + Video Generation: PiAPI/Flux keyframes → Kling/Runway/Luma I2V rendering
4. Assembly + Verification: Gemini Verifier → moviepy assembly → n8n publishing

Beat Synchronization (librosa + moviepy):
- librosa.beat.beat_track: Tempo-based for metronomic tracks

- librosa.onset.onset_strength_multi: Bass/onset detection for dynamic tracks
- CRITICAL: Cast numpy arrays to float before frames_to_time (Python 3.10 TypeError fix)
- MoviePy: Sequential subclip extraction matching beat deltas, loop fallback for short clips

Audio-Reactive Latent Modulation:
- ComfyUI + Deforum: Frame-by-frame parameter injection
- librosa.feature.rms → camera zoom. spectral_centroid → prompt weight scheduling
- Continuous interpolation: Visuals 'breathe' with audio

Kling SDK: kling-ai-sdk (Pydantic v2, async HTTPX). ImageToVideoRequest with bind_subject=True, resolution='4K'.
Runway SDK: runwayml package. X-Runway-Version: 2024-11-06. Polling GET /v1/tasks/{id}.
Luma SDK: lumaai package. /extend with frame0: {type: 'generation', id: base_id}.

Production Cost: ~$15 per full music video in API compute. 30-minute cycle vs 120-hour manual.

---
📁 **See also:** [[Research_Archives/Recovered_From_Qdrant/INDEX|← Directory Index]]

**Related:** [[music_video_flow_blueprint]] · [[19_AUTOMATED_VIDEO_PRODUCTION_PIPELINES]] · [[20260610_VIDEO_PROD_research_video_upscaling_technology_in_2026_—_topaz_video_ai]]
