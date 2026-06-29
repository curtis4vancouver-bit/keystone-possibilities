import os
import sys
import json
from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load local environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

def test_api():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[Error] No GEMINI_API_KEY or GOOGLE_API_KEY found in environment or .env file.")
        return

    print("[Test] Initializing Gemini Client...")
    client = genai.Client(api_key=api_key)

    # 1. Create a dummy blank image in memory
    print("[Test] Generating dummy blank image...")
    dummy_img = Image.new("RGB", (1024, 768), color=(255, 255, 255))
    dummy_path = "dummy_screen.png"
    dummy_img.save(dummy_path, "PNG")

    # Read image bytes
    with open(dummy_path, "rb") as f:
        img_bytes = f.read()

    image_input = types.Part.from_bytes(
        data=img_bytes,
        mime_type="image/png"
    )

    print("[Test] Calling Gemini 3.5 Flash with computer_use tool...")
    try:
        # We call the model with the computer_use tool enabled
        response = client.models.generate_content(
            model="gemini-3.5-flash", # Using the 3.5 Flash stable model endpoint
            contents=[
                "You are a computer operator. The user wants to: 'Wait for 2 seconds and then finish'. Look at this blank screen, tell me what you see, and issue the appropriate tool call.",
                image_input
            ],
            config=types.GenerateContentConfig(
                tools=[{"type": "computer_use", "environment": "desktop"}] if hasattr(types, "computer_use") else None
            )
        )
        print("=" * 60)
        print("GEMINI RESPONSE SUCCESS!")
        print("=" * 60)
        print("Response text:", response.text)
        print("Candidates / Tool Calls:")
        print(response.candidates)
        print("=" * 60)

    except Exception as e:
        print(f"[Error] Gemini API call failed: {e}")
    finally:
        # Clean up dummy image
        if os.path.exists(dummy_path):
            os.remove(dummy_path)

if __name__ == "__main__":
    test_api()
