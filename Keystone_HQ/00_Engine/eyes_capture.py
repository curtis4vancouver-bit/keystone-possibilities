import os
import time
import sys
import json
import uuid
import datetime
import pyautogui
from PIL import Image

try:
    import google.generativeai as genai
    # Automatically uses GEMINI_API_KEY env var
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
except Exception as e:
    print(f"Failed to import or configure Google Generative AI: {e}")
    genai = None

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LEARNINGS_DIR = os.path.join(PROJECT_ROOT, ".learnings")
ERRORS_DIR = os.path.join(LEARNINGS_DIR, "errors")
SCRATCH_DIR = os.path.join(PROJECT_ROOT, "scratch")

os.makedirs(ERRORS_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

def capture_screen(output_filename="screenshot.png") -> str:
    """Takes a screenshot of the current display and saves it to scratch directory."""
    path = os.path.join(SCRATCH_DIR, output_filename)
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print(f"[Eyes] Screenshot saved to {path}")
        return path
    except Exception as e:
        print(f"[Eyes] Failed to capture screen: {e}")
        return ""

def analyze_screenshot(image_path: str) -> dict:
    """Sends the screenshot to Gemini multimodal API to detect UI errors or crashes."""
    if not genai:
        return {"status": "error", "message": "GenAI SDK not available"}
        
    try:
        img = Image.open(image_path)
        
        # Try using gemini-2.5-flash (standard multimodal model)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = """
        Analyze this screenshot. Look for any application crash messages, compiler/runtime errors,
        IDE error popups, Windows error dialogs, or hanging/frozen processes.
        Return your response strictly in the following JSON format:
        {
            "has_error": true/false,
            "error_type": "type of error found or None",
            "context": "description of what application/screen is open",
            "details": "exact error text or visual evidence found"
        }
        """
        
        print("[Eyes] Querying Gemini Multimodal endpoint for visual check...")
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        
        # Remove markdown JSON wrappers if present
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        return json.loads(text)
    except Exception as e:
        print(f"[Eyes] Visual analysis error: {e}")
        return {"status": "error", "message": str(e)}

def run_eyes_check():
    """Runs a single visual check. If an error is detected, writes an error card to trigger self-healing."""
    print(f"\n--- [Eyes] Starting visual check at {datetime.datetime.now()} ---")
    img_path = capture_screen("eyes_screenshot.png")
    if not img_path:
        return
        
    res = analyze_screenshot(img_path)
    print(f"[Eyes] Visual analysis result: {json.dumps(res, indent=2)}")
    
    if res.get("has_error"):
        error_type = res.get("error_type", "VisualUIError")
        details = res.get("details", "UI crash detected visually")
        context = res.get("context", "Desktop screen")
        
        print(f"[Eyes] 🚨 Visual error detected! Compiling error card...")
        
        # Generate error card for self_evolution.py
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        uuid_str = str(uuid.uuid4())[:8]
        filename = f"{date_str}-{error_type}-{uuid_str}.md"
        filepath = os.path.join(ERRORS_DIR, filename)
        
        error_card = f"""# Error: Visual UI Crash Detected
Timestamp: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Type: {error_type}
Severity: Critical
Fingerprint: VIS-{uuid_str}

## What Happened
The Screen Capture Pipeline (Eyes) detected a visual UI crash or error dialog.

## Execution Context
Context ID: {context}
Trigger Query: Automated Screen Watcher
Parameters: {{"screenshot": "{img_path}"}}

## Root Cause Analysis
Visual Evidence:
{details}

## Recommended Mitigations
1. Terminate any frozen application processes.
2. Run repair cycles if compiler or environment errors are visible.
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(error_card)
        print(f"[Eyes] Visual error card written to {filepath}")
    else:
        print("[Eyes] Screen check passed. No UI errors visible.")

if __name__ == "__main__":
    run_eyes_check()
