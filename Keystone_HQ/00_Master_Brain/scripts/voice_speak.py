"""
Direct Voice Report — Uses Windows SAPI to speak directly through speakers.
No Gemini Live needed. Just plays audio.
Usage: python voice_speak.py "Your message to Wayne"
"""
import sys
import subprocess

def speak(text: str):
    """Speak text through Windows SAPI text-to-speech."""
    # Escape single quotes for PowerShell
    safe_text = text.replace("'", "''")
    ps_script = f"""
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 1
$synth.Speak('{safe_text}')
"""
    subprocess.run(
        ["powershell", "-Command", ps_script],
        capture_output=True, text=True, timeout=30
    )
    print(f"[Spoken] {text[:80]}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        speak(" ".join(sys.argv[1:]))
    else:
        print("Usage: python voice_speak.py 'Your message'")
