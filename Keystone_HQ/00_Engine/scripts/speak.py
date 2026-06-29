"""
Keystone Sovereign Voice Engine v3.0 — Neural Edition
=======================================================
Uses Microsoft Edge Neural TTS for near-human voice quality.
Falls back to offline SAPI5 (pyttsx3) if no internet.
Free, no API key required.

Usage:
  python speak.py "Your text here"                        # Speak with default voice (Jenny)
  python speak.py --voice guy "Male neural voice"         # Use Guy Neural
  python speak.py --voice brian "Casual male"             # Use Brian Neural
  python speak.py --voice aria "News anchor female"       # Use Aria Neural
  python speak.py --file report.md                        # Read a file aloud
  python speak.py --rate +20% "Faster"                    # Speed up
  python speak.py --rate -30% "Slower"                    # Slow down
  python speak.py --offline "No internet fallback"        # Force SAPI5 offline mode
  python speak.py --list-voices                           # Show all available voices

Voice Shortcuts:
  jenny   -> en-US-JennyNeural    (Female, friendly — DEFAULT)
  guy     -> en-US-GuyNeural      (Male, passionate)
  brian   -> en-US-BrianNeural    (Male, casual & sincere)
  andrew  -> en-US-AndrewNeural   (Male, warm & confident)
  aria    -> en-US-AriaNeural     (Female, news anchor)
  ava     -> en-US-AvaNeural      (Female, caring & expressive)
  emma    -> en-US-EmmaNeural     (Female, cheerful)
  roger   -> en-US-RogerNeural    (Male, lively)
  ana     -> en-US-AnaNeural      (Female, cute/cartoon)
"""
import sys
import os
import re
import argparse
import asyncio
import tempfile
import subprocess

# Force UTF-8 on Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Voice shortcut map
VOICE_SHORTCUTS = {
    "jenny":     "en-US-JennyNeural",
    "guy":       "en-US-GuyNeural",
    "brian":     "en-US-BrianNeural",
    "andrew":    "en-US-AndrewNeural",
    "aria":      "en-US-AriaNeural",
    "ava":       "en-US-AvaNeural",
    "emma":      "en-US-EmmaNeural",
    "roger":     "en-US-RogerNeural",
    "ana":       "en-US-AnaNeural",
    "chris":     "en-US-ChristopherNeural",
    "michelle":  "en-US-MichelleNeural",
    "eric":      "en-US-EricNeural",
    "steffan":   "en-US-SteffanNeural",
}

DEFAULT_VOICE = "en-US-JennyNeural"


def resolve_voice(voice_input: str) -> str:
    """Resolve a shortcut name or full voice ID."""
    if not voice_input:
        return DEFAULT_VOICE
    low = voice_input.lower().strip()
    if low in VOICE_SHORTCUTS:
        return VOICE_SHORTCUTS[low]
    # If it already looks like a full voice ID, use it directly
    if "Neural" in voice_input:
        return voice_input
    return DEFAULT_VOICE


def clean_text_for_speech(text: str) -> str:
    """Strip markdown formatting for clean speech."""
    text = re.sub(r'#{1,6}\s*', '', text)                          # headings
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)          # bold/italic
    text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)                 # code blocks
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)           # links
    text = re.sub(r'^[\s]*[-*>|]+\s?', '', text, flags=re.MULTILINE)  # lists, quotes, tables
    text = re.sub(r'\n{2,}', '. ', text)                           # paragraph breaks
    text = re.sub(r'\s+', ' ', text).strip()
    return text


async def speak_neural(text: str, voice: str = DEFAULT_VOICE, rate: str = "+0%"):
    """Speak using Edge Neural TTS (high quality, free, needs internet)."""
    import edge_tts

    # Truncate very long text
    max_chars = 5000
    if len(text) > max_chars:
        text = text[:max_chars] + "... Content truncated for readability."
        print(f"[Voice] Text exceeds {max_chars} chars, truncating.")

    print(f"[Voice] Neural TTS | Voice: {voice} | Rate: {rate} | {len(text)} chars")

    # Generate audio to temp file, then play it
    tmp_path = os.path.join(tempfile.gettempdir(), "keystone_voice.mp3")
    
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(tmp_path)

    # Play using Windows built-in media player (hidden)
    # Using PowerShell's built-in media player for reliable playback
    ps_cmd = f'''
    Add-Type -AssemblyName PresentationCore
    $player = New-Object System.Windows.Media.MediaPlayer
    $player.Open([Uri]::new("{tmp_path.replace(os.sep, '/')}"))
    $player.Play()
    Start-Sleep -Milliseconds 500
    while ($player.NaturalDuration.HasTimeSpan -eq $false) {{ Start-Sleep -Milliseconds 100 }}
    $duration = $player.NaturalDuration.TimeSpan.TotalSeconds
    Start-Sleep -Seconds ($duration + 0.5)
    $player.Close()
    '''
    subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
    
    # Cleanup
    try:
        os.remove(tmp_path)
    except Exception:
        pass

    print("[Voice] Done.")


def speak_offline(text: str, rate: int = 180, voice_index: int = 0):
    """Fallback: Speak using local SAPI5 (pyttsx3) — no internet needed."""
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    voices = engine.getProperty('voices')
    if voices and 0 <= voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)

    max_chars = 4000
    if len(text) > max_chars:
        text = text[:max_chars] + "... Content truncated."

    print(f"[Voice] Offline SAPI5 | {len(text)} chars")
    engine.say(text)
    engine.runAndWait()
    print("[Voice] Done.")


def read_file(filepath: str) -> str:
    """Read and clean a text file for speech."""
    if not os.path.exists(filepath):
        print(f"[Voice] File not found: {filepath}")
        return ""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        return clean_text_for_speech(f.read())


def main():
    parser = argparse.ArgumentParser(description="Keystone Sovereign Voice Engine v3.0 — Neural Edition")
    parser.add_argument('text', nargs='*', help='Text to speak')
    parser.add_argument('--file', '-f', type=str, help='Read a text/markdown file aloud')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin pipe')
    parser.add_argument('--voice', '-v', type=str, default='jenny', help='Voice name or shortcut (default: jenny)')
    parser.add_argument('--rate', '-r', type=str, default='+0%', help='Speech rate adjustment (e.g. +20%%, -10%%)')
    parser.add_argument('--offline', action='store_true', help='Force offline SAPI5 mode')
    parser.add_argument('--list-voices', action='store_true', help='List all available voice shortcuts')
    args = parser.parse_args()

    if args.list_voices:
        print("[Voice] Available voice shortcuts:")
        print(f"  {'Shortcut':<12} {'Full Voice ID':<35} {'Notes'}")
        print(f"  {'-'*12} {'-'*35} {'-'*30}")
        notes = {
            "jenny": "Female, friendly (DEFAULT)",
            "guy": "Male, passionate",
            "brian": "Male, casual & sincere",
            "andrew": "Male, warm & confident",
            "aria": "Female, news anchor",
            "ava": "Female, caring & expressive",
            "emma": "Female, cheerful & clear",
            "roger": "Male, lively",
            "ana": "Female, cute/cartoon",
            "chris": "Male, reliable authority",
            "michelle": "Female, friendly & pleasant",
            "eric": "Male, rational",
            "steffan": "Male, rational",
        }
        for shortcut, full_id in VOICE_SHORTCUTS.items():
            note = notes.get(shortcut, "")
            print(f"  {shortcut:<12} {full_id:<35} {note}")
        return

    # Resolve the text to speak
    text = ""
    if args.file:
        text = read_file(args.file)
    elif args.stdin:
        text = clean_text_for_speech(sys.stdin.read())
    elif args.text:
        text = ' '.join(args.text)
    else:
        parser.print_help()
        return

    if not text.strip():
        print("[Voice] Nothing to say.")
        return

    if args.offline:
        speak_offline(text)
    else:
        voice = resolve_voice(args.voice)
        # Ensure rate has the % format edge-tts expects
        rate = args.rate
        if rate and not rate.endswith('%'):
            rate = rate + '%'
        if rate and not (rate.startswith('+') or rate.startswith('-')):
            rate = '+' + rate

        try:
            asyncio.run(speak_neural(text, voice=voice, rate=rate))
        except Exception as e:
            print(f"[Voice] Neural TTS failed ({e}), falling back to offline SAPI5...")
            speak_offline(text)


if __name__ == "__main__":
    main()
