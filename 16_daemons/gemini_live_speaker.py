import asyncio
import json
import base64
import os
import sys
import websockets
import sounddevice as sd
import numpy as np
import msvcrt

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

LOCK_FILE_PATH = os.path.join(os.path.dirname(__file__), "speaker_instance.lock")

def acquire_single_instance_lock():
    try:
        if os.path.exists(LOCK_FILE_PATH):
            try:
                os.remove(LOCK_FILE_PATH)
            except Exception:
                pass
        lock_file = open(LOCK_FILE_PATH, "w")
        msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        return lock_file
    except Exception:
        print("[Gemini Live HD Voice] Stale lock bypassed — proceeding with speech synthesis.")
        return None

lock_handle = acquire_single_instance_lock()

API_KEY = os.environ.get("VITE_GEMINI_API_KEY", "AIzaSyDamgVRE56dbPZZf9K7_Jn-hFK3ABt1J28")
URL = f"wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key={API_KEY}"

VOLUME_CONFIG_PATH = r"C:\Users\Curtis\.gemini\antigravity\selected_volume.txt"

def get_current_volume(default_vol=80):
    try:
        if os.path.exists(VOLUME_CONFIG_PATH):
            with open(VOLUME_CONFIG_PATH, "r", encoding="utf-8") as f:
                v = int(f.read().strip())
                return max(0, min(100, v))
    except Exception:
        pass
    return default_vol

def find_output_device(target_name):
    target_sr = 24000
    if not target_name or target_name.strip().lower() in ["default", "system default", "system default (auto-switch)"]:
        try:
            default_info = sd.query_devices(kind='output')
            target_sr = int(default_info.get("default_samplerate", 24000))
        except Exception:
            target_sr = 24000
        print(f"[Gemini Live HD Voice] Using system default playback device (SR: {target_sr}, Core Audio auto-switch active).")
        return None, target_sr

    try:
        devices = sd.query_devices()
        hostapis = sd.query_hostapis()
        target_clean = target_name.strip().lower()
        wasapi_idx = next((i for i, h in enumerate(hostapis) if "wasapi" in h.get("name", "").lower()), None)

        if wasapi_idx is not None:
            # Pass 1: Exact match on WASAPI host API
            for idx, d in enumerate(devices):
                if d.get("hostapi") == wasapi_idx and d.get("max_output_channels", 0) > 0:
                    name = d.get("name", "").strip().lower()
                    if name == target_clean:
                        sr = int(d.get("default_samplerate", 24000))
                        print(f"[Gemini Live HD Voice] Exact WASAPI output match Device {idx}: '{d['name']}' (SR: {sr})")
                        return idx, sr

            # Pass 2: Substring match on WASAPI host API
            for idx, d in enumerate(devices):
                if d.get("hostapi") == wasapi_idx and d.get("max_output_channels", 0) > 0:
                    name = d.get("name", "").strip().lower()
                    if target_clean in name or name in target_clean:
                        sr = int(d.get("default_samplerate", 24000))
                        print(f"[Gemini Live HD Voice] WASAPI substring match Device {idx}: '{d['name']}' (SR: {sr})")
                        return idx, sr

        # Pass 3: Fallback exact match across all host APIs
        for idx, d in enumerate(devices):
            if d.get("max_output_channels", 0) > 0:
                name = d.get("name", "").strip().lower()
                if name == target_clean:
                    sr = int(d.get("default_samplerate", 24000))
                    print(f"[Gemini Live HD Voice] Fallback exact match Device {idx}: '{d['name']}' (SR: {sr})")
                    return idx, sr

        # Pass 4: Fallback substring match across all host APIs
        for idx, d in enumerate(devices):
            if d.get("max_output_channels", 0) > 0:
                name = d.get("name", "").strip().lower()
                if target_clean in name:
                    sr = int(d.get("default_samplerate", 24000))
                    print(f"[Gemini Live HD Voice] Fallback substring match Device {idx}: '{d['name']}' (SR: {sr})")
                    return idx, sr

    except Exception as e:
        print(f"[Gemini Live HD Voice] Device query error: {e}")

    try:
        default_info = sd.query_devices(kind='output')
        target_sr = int(default_info.get("default_samplerate", 24000))
    except Exception:
        target_sr = 24000
    print(f"[Gemini Live HD Voice] Speaker '{target_name}' not found, using default output (SR: {target_sr}).")
    return None, target_sr

def play_confirmation_chime(device_name, volume=None):
    """Play 1-second 440Hz -> 880Hz sine confirmation chime on target output device."""
    try:
        device_idx, sr = find_output_device(device_name)
        vol_pct = max(0, min(100, int(volume if volume is not None else get_current_volume())))
        gain = (vol_pct / 100.0) * 0.25
        t1 = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
        t2 = np.linspace(0, 0.5, int(sr * 0.5), endpoint=False)
        tone1 = gain * np.sin(2 * np.pi * 440 * t1)
        tone2 = gain * np.sin(2 * np.pi * 880 * t2)
        chime = np.concatenate([tone1, tone2]).astype(np.float32)

        with sd.OutputStream(device=device_idx, samplerate=sr, channels=1, dtype='float32') as stream:
            stream.write(chime)
        print(f"🔔 [Audio Chime] 1s confirmation chime played on '{device_name}' (device {device_idx}, volume {vol_pct}%)")
        return True
    except Exception as e:
        print(f"⚠️ [Audio Chime Error]: {e}")
        return False

async def speak_via_gemini_live(text_to_speak, voice_name="Aoede", target_speaker="default", volume=None):
    vol_pct = max(0, min(100, int(volume if volume is not None else get_current_volume())))
    digital_gain = (vol_pct / 100.0) * 1.8
    print(f"[Gemini Live HD Voice] Connecting to Google AI Studio WebSocket (Volume: {vol_pct}%, Digital Gain: {digital_gain:.2f})...")
    device_idx, target_sr = find_output_device(target_speaker)
    
    stream_sr = target_sr if target_sr else 24000
    try:
        stream = sd.OutputStream(device=device_idx, samplerate=stream_sr, channels=2, dtype='int16')
        stream.start()
        print(f"[Gemini Live HD Voice] Audio stream started successfully on device {device_idx} @ {stream_sr}Hz (Stereo 2-Channel)")
    except Exception as e:
        print(f"[Gemini Live HD Voice] Failed to open stream at {stream_sr}Hz on device {device_idx} ({e}). Falling back to default output...")
        stream_sr = 24000
        stream = sd.OutputStream(device=None, samplerate=24000, channels=2, dtype='int16')
        stream.start()

    async with websockets.connect(URL) as ws:
        print("[Gemini Live HD Voice] Connected to Google AI Studio WebSocket!")
        
        setup_payload = {
            "setup": {
                "model": "models/gemini-2.5-flash-native-audio-preview-12-2025",
                "generationConfig": {
                    "responseModalities": ["AUDIO"],
                    "speechConfig": {
                        "voiceConfig": {
                            "prebuiltVoiceConfig": {
                                "voiceName": voice_name
                            }
                        }
                    }
                },
                "systemInstruction": {
                    "parts": [
                        {
                            "text": "You are a strict 1-to-1 audio text-to-speech synthesizer. You must read ONLY the exact text provided in the prompt out loud word for word. Do NOT answer questions, do NOT hold a conversation, do NOT say you cannot do things, and do NOT add extra words."
                        }
                    ]
                }
            }
        }
        
        await ws.send(json.dumps(setup_payload))

        raw_setup_response = await ws.recv()
        msg = json.loads(raw_setup_response)
        print(f"[Gemini Live HD Voice] Received setup frame: {msg}")

        text_payload = {
            "clientContent": {
                "turns": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": text_to_speak}
                        ]
                    }
                ],
                "turnComplete": True
            }
        }

        print(f"[Gemini Live HD Voice] Injecting text prompt: '{text_to_speak}'")
        await ws.send(json.dumps(text_payload))

        chunks_played = 0
        while True:
            try:
                msg_raw = await asyncio.wait_for(ws.recv(), timeout=10.0)
                msg = json.loads(msg_raw)

                if "serverContent" in msg:
                    model_turn = msg["serverContent"].get("modelTurn", {})
                    parts = model_turn.get("parts", [])
                    for part in parts:
                        if "inlineData" in part and part["inlineData"].get("mimeType", "").startswith("audio/pcm"):
                            b64_data = part["inlineData"]["data"]
                            pcm_bytes = base64.b64decode(b64_data)
                            audio_array = np.frombuffer(pcm_bytes, dtype=np.int16)
                            # Apply user-scaled digital gain boost (0% silent, 80% comfortable, 100% full boost)
                            audio_array = np.clip(audio_array.astype(np.float32) * digital_gain, -32768, 32767)
                            if stream_sr != 24000:
                                if stream_sr == 48000:
                                    audio_array = np.repeat(audio_array, 2)
                                else:
                                    step = 24000.0 / stream_sr
                                    sample_indices = np.arange(0, len(audio_array), step)
                                    audio_array = np.interp(sample_indices, np.arange(len(audio_array)), audio_array)
                            audio_array = audio_array.astype(np.int16)
                            # Convert mono to 2-channel stereo for HDMI / WASAPI multi-channel sinks
                            stereo_array = np.column_stack((audio_array, audio_array))
                            stream.write(stereo_array)
                            chunks_played += 1

                    if msg["serverContent"].get("turnComplete") is True:
                        print(f"[Gemini Live HD Voice] Stream complete! Played {chunks_played} PCM audio chunks.")
                        break

            except asyncio.TimeoutError:
                print("[Gemini Live HD Voice] Stream finished.")
                break

    stream.stop()
    stream.close()
    print("[Gemini Live HD Voice] Stream closed.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--chime", "-c"]:
        speaker = sys.argv[2] if len(sys.argv) > 2 else "default"
        vol = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else get_current_volume()
        play_confirmation_chime(speaker, volume=vol)
    else:
        msg_text = sys.argv[1] if len(sys.argv) > 1 else "Hi, I'm Antigravity."
        voice = sys.argv[2] if len(sys.argv) > 2 else "Aoede"
        speaker = sys.argv[3] if len(sys.argv) > 3 else "default"
        vol = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else get_current_volume()
        asyncio.run(speak_via_gemini_live(msg_text, voice_name=voice, target_speaker=speaker, volume=vol))
