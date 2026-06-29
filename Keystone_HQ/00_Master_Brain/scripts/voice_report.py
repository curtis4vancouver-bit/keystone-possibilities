"""
Voice Outbox Helper — Write status updates that get spoken to Wayne.
Usage from Antigravity agent:
    python voice_report.py "I just finished the SEO audit. Three issues found."
"""
import sys
import os

OUTBOX = os.path.join(os.path.expanduser("~"), ".gemini", "antigravity", "voice_outbox.txt")

def send_voice_report(message: str):
    """Write a message to the voice outbox. The Voice Bridge speaks it to Wayne."""
    os.makedirs(os.path.dirname(OUTBOX), exist_ok=True)
    with open(OUTBOX, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")
    print(f"[Voice Report sent] {message[:80]}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        send_voice_report(" ".join(sys.argv[1:]))
    else:
        print("Usage: python voice_report.py 'Your message to Wayne'")
