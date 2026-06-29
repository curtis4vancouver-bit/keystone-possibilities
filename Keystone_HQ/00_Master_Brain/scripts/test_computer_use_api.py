"""Quick test: Verify Computer Use API is connected and responding."""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, base64, io
from PIL import Image

load_dotenv()
client = genai.Client()

# Create a fake 1920x1080 "desktop" screenshot (dark gray)
img = Image.new('RGB', (1920, 1080), (30, 30, 30))
buf = io.BytesIO()
img.save(buf, format='PNG')
encoded = base64.b64encode(buf.getvalue()).decode()

print("Testing Computer Use API endpoint...")
print(f"API Key: {os.environ.get('GEMINI_API_KEY','')[:8]}...")

try:
    response = client.models.generate_content(
        model='gemini-2.5-computer-use-preview-10-2025',
        contents=[{
            'parts': [
                {'text': 'Click on the Start menu button in the bottom-left corner.'},
                {'inline_data': {'mime_type': 'image/png', 'data': encoded}}
            ]
        }],
        config=types.GenerateContentConfig(
            tools=[types.Tool(computer_use=types.ComputerUse(
                environment=types.Environment.ENVIRONMENT_DESKTOP
            ))]
        )
    )
    
    print("\n=== COMPUTER USE API: CONNECTED ===")
    print(f"Response candidates: {len(response.candidates)}")
    for i, part in enumerate(response.candidates[0].content.parts):
        ptype = type(part).__name__
        if hasattr(part, 'function_call') and part.function_call:
            fc = part.function_call
            print(f"  Part {i}: FUNCTION_CALL -> {fc.name}({dict(fc.args)})")
        elif hasattr(part, 'text') and part.text:
            print(f"  Part {i}: TEXT -> {part.text[:200]}")
        else:
            print(f"  Part {i}: {ptype}")
    
    print("\nAPI KEY IS PROPERLY CONNECTED FOR COMPUTER USE.")
    
except Exception as e:
    print(f"\nERROR: {e}")
    print("\nTroubleshooting:")
    print("  - Check if computer_use is enabled on your API key")
    print("  - Check rate limits (free tier = 15 RPM)")
