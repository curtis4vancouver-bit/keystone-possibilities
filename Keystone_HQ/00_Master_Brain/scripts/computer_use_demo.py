"""
Keystone Computer Use Demo — DaVinci Resolve Controller
Uses the official Gemini Interactions API for multi-turn desktop control.
"""

import os
import sys
import time
import json
import base64
import ctypes
from io import BytesIO

# Load API key
env_path = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain\.env"
with open(env_path) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()
            break

from google import genai
from google.genai import types

try:
    from PIL import Image
    import pyautogui
    import mss
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.1
except ImportError:
    print("Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "pyautogui", "mss"])
    from PIL import Image
    import pyautogui
    import mss
    pyautogui.FAILSAFE = False
    pyautogui.PAUSE = 0.1

# Enable DPI awareness for accurate coords on high-DPI screens
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# ── Config ──
MODEL = "gemini-3.5-flash"
MAX_STEPS = 25
SCREEN_W, SCREEN_H = pyautogui.size()
print(f"[*] Screen resolution: {SCREEN_W}x{SCREEN_H}")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# Persistent mss instance
sct = mss.mss()


def take_screenshot_b64() -> str:
    """Capture the screen, downscale for performance, and return as base64 PNG."""
    monitor = sct.monitors[1]  # Primary monitor
    sct_img = sct.grab(monitor)
    img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    
    # Resize to 1280x720 for fast upload and API processing
    img_resized = img.resize((1280, 720), Image.Resampling.LANCZOS)
    
    buf = BytesIO()
    img_resized.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")


def scale_coord(x_norm: int, y_norm: int) -> tuple[int, int]:
    """Scale 0-1000 normalized coords to actual screen pixels."""
    real_x = int(x_norm * SCREEN_W / 1000)
    real_y = int(y_norm * SCREEN_H / 1000)
    return real_x, real_y


def execute_action(step) -> str:
    """Execute a Computer Use function call on the real desktop."""
    name = step.name
    args = dict(step.arguments) if step.arguments else {}
    
    intent = args.get("intent", "")
    print(f"  [ACTION] {name} | {intent}")
    print(f"           args: {args}")
    
    try:
        if name == "click" or name == "click_at":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            print(f"           -> clicking at ({x}, {y})")
            pyautogui.click(x, y)
            time.sleep(0.5)
            
        elif name == "double_click":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            print(f"           -> double-clicking at ({x}, {y})")
            pyautogui.doubleClick(x, y)
            time.sleep(0.5)
            
        elif name == "right_click":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            print(f"           -> right-clicking at ({x}, {y})")
            pyautogui.rightClick(x, y)
            time.sleep(0.5)
            
        elif name == "type" or name == "type_text":
            text = args.get("text", "")
            press_enter = args.get("press_enter", False)
            print(f"           -> typing: '{text}'")
            pyautogui.typewrite(text, interval=0.03) if text.isascii() else pyautogui.write(text)
            if press_enter:
                pyautogui.press("enter")
            time.sleep(0.3)
            
        elif name == "press_key":
            key = args.get("key", "")
            print(f"           -> pressing key: {key}")
            pyautogui.press(key.lower())
            time.sleep(0.3)
            
        elif name == "hotkey":
            keys = args.get("keys", [])
            print(f"           -> hotkey: {keys}")
            pyautogui.hotkey(*[k.lower() for k in keys])
            time.sleep(0.3)
            
        elif name == "drag_and_drop":
            sx, sy = scale_coord(int(args.get("start_x", 0)), int(args.get("start_y", 0)))
            ex, ey = scale_coord(int(args.get("end_x", 0)), int(args.get("end_y", 0)))
            print(f"           -> dragging ({sx},{sy}) to ({ex},{ey})")
            pyautogui.moveTo(sx, sy)
            time.sleep(0.2)
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.moveTo(ex, ey, duration=0.5)
            pyautogui.mouseUp()
            time.sleep(0.5)
            
        elif name == "mouse_down":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            pyautogui.moveTo(x, y)
            pyautogui.mouseDown()
            time.sleep(0.1)
            
        elif name == "mouse_up":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            pyautogui.moveTo(x, y)
            pyautogui.mouseUp()
            time.sleep(0.3)
            
        elif name == "move":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            pyautogui.moveTo(x, y)
            time.sleep(0.1)
            
        elif name == "scroll":
            x, y = scale_coord(int(args.get("x", 0)), int(args.get("y", 0)))
            direction = args.get("direction", "down")
            magnitude = int(args.get("magnitude_in_pixels", 300))
            clicks = magnitude // 30  # rough conversion
            if direction == "up":
                pyautogui.scroll(clicks, x, y)
            elif direction == "down":
                pyautogui.scroll(-clicks, x, y)
            time.sleep(0.3)
            
        elif name == "take_screenshot":
            print("           -> (model requested screenshot)")
            time.sleep(0.2)
            
        elif name == "wait" or name == "wait_5_seconds":
            secs = int(args.get("seconds", 5))
            print(f"           -> waiting {secs}s")
            time.sleep(secs)
            
        elif name == "open_web_browser":
            print("           -> opening browser (skipping, using desktop)")
            
        else:
            print(f"           -> UNKNOWN action: {name}")
            
        return "Action executed successfully."
        
    except Exception as e:
        print(f"           -> ERROR: {e}")
        return f"Error executing action: {e}"


def run_computer_use(task: str):
    """Main Computer Use agentic loop using official Interactions API."""
    print(f"\n{'='*60}")
    print(f"  COMPUTER USE AGENT (Interactions API)")
    print(f"  Task: {task}")
    print(f"{'='*60}\n")
    
    # Take initial screenshot
    print("[Step 0] Taking initial screenshot...")
    screenshot_b64 = take_screenshot_b64()
    
    # First interaction
    print("[Step 1] Sending initial request...")
    try:
        interaction = client.interactions.create(
            model=MODEL,
            input=[
                {"type": "text", "text": task},
                {"type": "image", "data": screenshot_b64, "mime_type": "image/png"}
            ],
            tools=[{
                "type": "computer_use",
                "environment": "desktop",
                "enable_prompt_injection_detection": True
            }]
        )
    except Exception as e:
        print(f"  [ERROR] Initial interaction failed: {e}")
        return
        
    # Agent Loop
    for turn in range(1, MAX_STEPS + 1):
        print(f"\n--- Turn {turn} ---")
        
        # Check if there are function calls
        has_function_calls = any(step.type == "function_call" for step in interaction.steps)
        if not has_function_calls:
            # Try to get model text response
            text_response = ""
            for step in interaction.steps:
                if step.type == "model_output":
                    for content_block in step.content:
                        if content_block.type == "text":
                            text_response += content_block.text + " "
            print("\n" + "="*60)
            print("  TASK COMPLETE — Model stopped issuing actions.")
            print("  Final message:", text_response.strip())
            print("="*60)
            break
            
        # Execute actions
        results = []
        for step in interaction.steps:
            if step.type == "function_call":
                # Execute the action
                res_msg = execute_action(step)
                action_result = {"result": res_msg}
                results.append((step.name, step.id, action_result))
                
        # Capture new screen state
        print("Capturing state...")
        time.sleep(1.5)
        new_screenshot_b64 = take_screenshot_b64()
        
        # Build function responses list in official format
        function_responses = []
        for name, call_id, result in results:
            function_responses.append({
                "type": "function_result",
                "name": name,
                "call_id": call_id,
                "result": [
                    {
                        "type": "text",
                        "text": json.dumps(result)
                    },
                    {
                        "type": "image",
                        "data": new_screenshot_b64,
                        "mime_type": "image/png"
                    }
                ]
            })
            
        # Continue conversation with function responses
        try:
            interaction = client.interactions.create(
                model=MODEL,
                previous_interaction_id=interaction.id,
                input=function_responses,
                tools=[{
                    "type": "computer_use",
                    "environment": "desktop",
                    "enable_prompt_injection_detection": True
                }]
            )
        except Exception as e:
            print(f"  [ERROR] Continuation failed: {e}")
            break
            
    print("\n[*] Computer Use session ended.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        task = sys.argv[1]
    else:
        task = (
            "Open DaVinci Resolve Studio from the Windows taskbar or Start menu. "
            "Once it opens, wait for the Project Manager to load. "
            "Then create a new project by clicking the 'New Project' button. "
            "Name it 'Computer Use Demo'. "
            "After the project opens, go to the Edit page and drag something in the timeline area."
        )
    run_computer_use(task)
