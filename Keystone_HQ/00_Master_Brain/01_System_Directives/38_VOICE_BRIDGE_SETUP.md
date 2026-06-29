# AIDA Voice Bridge Setup Guide
> **Last Updated:** 2026-06-27 (Post-Deadlock & Audio Routing Fixes)

## 1. Overview
The AIDA Voice Bridge provides zero-latency, two-way Push-To-Talk (PTT) communication directly with the Antigravity agent over the Google Gemini Live API. 

## 2. Requirements
* **Python 3.11+**
* **Audio Drivers:** Windows WASAPI or MME.
* **Dependencies:** `pip install sounddevice numpy websockets pynput`

## 3. How to Connect the Bridge to a New Chat
When you start a new conversation with Antigravity, follow these steps to link the voice bridge:

1. **Start the Agent Session:** Ensure Antigravity is running and has generated a Conversation ID.
2. **Start the Voice Bridge:**
   Run the voice bridge daemon from the `00_Master_Brain` directory:
   ```powershell
   python scripts\voice_bridge.py
   ```
   *Alternatively, click the microphone button in the AIDA frontend dashboard, which automatically calls the `/api/voice/start` endpoint.*
3. **Auto-Discovery:** The bridge will automatically scan the active `server.py` state, detect the new Conversation ID, and attach itself to the active session. 
4. **Push-To-Talk (PTT):** Hold **F8** (or F9) anywhere in Windows to speak. The audio is streamed directly to Gemini.

## 4. Troubleshooting Audio Routing (Crucial)
If Wayne cannot hear the agent's voice, **Windows is likely misrouting the audio.**

* **The Problem:** PortAudio (the underlying audio engine) often defaults to the HDMI monitor output (`EP-HDMI-RX`) instead of the headset, even if the headset is selected in the system tray.
* **The Fix:**
  1. Open Windows **Sound Settings** -> **More sound settings** (Sound Control Panel).
  2. Find the phantom HDMI output device (e.g., `EP-HDMI-RX` or `NVIDIA High Definition Audio`).
  3. Right-click and select **Disable**.
  4. Ensure `Speakers (Logitech PRO X Gaming Headset)` or `Realtek Digital Output` is set as the **Default Device** (not just the Default Communications Device).
  5. Restart the voice bridge script.

## 5. Agent Instructions for Voice Output
Gemini Live is strictly configured as a tool-caller and will not speak conversationally by default.
To force Gemini to speak to Wayne out loud, the Agent must write a message to `scripts/voice_outbox.txt`. 

The bridge will automatically format the text with the bypass command:
`Repeat this back to the speaker exactly word for word, with NO extra words, NO introduction, and NO conversation: [Message]`
Gemini's system prompt has an explicit exception to obey this command and synthesize the audio.