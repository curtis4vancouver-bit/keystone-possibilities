import os
import sys
import json
import time
import pyautogui
from PIL import ImageGrab
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load local environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# Safety: Fail-safe to top-left corner of the screen aborts pyautogui execution
pyautogui.FAILSAFE = True

class KeystoneDesktopOperator:
    def __init__(self):
        # 1. Dynamically discover API credentials from config
        self.config_path = os.path.join(
            os.path.expanduser("~"), ".gemini", "antigravity", "voice_bridge_config.json"
        )
        self.api_key = self._discover_api_key()
        
        # 2. Initialize the GenAI Client
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            # Fallback to system environment default
            self.client = genai.Client()
            
        # Get actual screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"[Operator] Screen resolution: {self.screen_width}x{self.screen_height}")

    def _discover_api_key(self) -> str:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    # We can use the CSRF token or read other environment keys if needed
                    # If the key is written directly to environment variable by Antigravity, 
                    # genai.Client() automatically picks up GEMINI_API_KEY or GOOGLE_API_KEY.
                    pass
            except Exception:
                pass
        return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

    def capture_and_save_screenshot(self) -> str:
        """Captures the active screen and saves it as a temporary PNG."""
        screenshot_path = os.path.join(
            os.path.expanduser("~"), ".gemini", "antigravity", "operator_screenshot.png"
        )
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        
        # Grab and save the screenshot
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path, "PNG")
        return screenshot_path

    def scale_coordinates(self, norm_x: int, norm_y: int) -> tuple:
        """Converts Gemini 0-999 normalized coordinates to actual screen pixels."""
        pixel_x = int((norm_x / 1000.0) * self.screen_width)
        pixel_y = int((norm_y / 1000.0) * self.screen_height)
        return pixel_x, pixel_y

    def run_task(self, goal: str, max_steps: int = 15):
        print(f"\n[Operator] Target Goal: '{goal}'")
        print("=" * 60)
        
        # Track history of actions
        history = []
        
        for step in range(1, max_steps + 1):
            print(f"\n[Step {step}/{max_steps}] Capturing screen...")
            screenshot_path = self.capture_and_save_screenshot()
            
            # Prepare image input
            import base64
            with open(screenshot_path, "rb") as img_file:
                img_data = img_file.read()
            encoded_image = base64.b64encode(img_data).decode('utf-8')
            
            print(f"[Step {step}] Sending screenshot to Gemini 3.5 Flash...")
            try:
                # Call Gemini interactions with Computer Use tool enabled
                response = self.client.interactions.create(
                    model="gemini-3.5-flash",
                    input=[
                        {"type": "text", "text": f"Current Goal: {goal}\nPrevious Actions: {history}"},
                        {"type": "image", "data": encoded_image, "mime_type": "image/png"}
                    ],
                    tools=[{"type": "computer_use", "environment": "desktop"}]
                )
                
                # Check for tool calls or actions in response steps
                tool_calls = []
                for s in getattr(response, "steps", []):
                    if getattr(s, "type", "") == "function_call":
                        tool_calls.append(s)
                        
                if not tool_calls:
                    print(f"[Finished] Gemini finished the task: {getattr(response, 'output_text', '')}")
                    break
                    
                for call in tool_calls:
                    action_raw = getattr(call, "name", "")
                    action = action_raw.split(":")[-1] # strip prefixes like "pyautogui:"
                    params = getattr(call, "arguments", {})
                    intent = params.get("intent", "Executing action...")
                    print(f"[AI Intent] {intent}")
                    
                    if action == "take_screenshot":
                        print("[Action] Taking fresh screenshot...")
                        history.append("Took new screenshot")
                        
                    elif action == "click":
                        norm_x, norm_y = params.get("x", 500), params.get("y", 500)
                        x, y = self.scale_coordinates(norm_x, norm_y)
                        print(f"[Action] Clicking at ({x}, {y}) [Normalized: {norm_x}, {norm_y}]")
                        pyautogui.click(x, y)
                        history.append(f"Clicked at normalized x={norm_x}, y={norm_y}")
                        
                    elif action == "type":
                        text = params.get("text", "")
                        print(f"[Action] Typing: '{text}'")
                        pyautogui.write(text)
                        history.append(f"Typed text: '{text}'")
                        
                    elif action == "key":
                        key = params.get("key", "")
                        print(f"[Action] Pressing key: '{key}'")
                        pyautogui.press(key)
                        history.append(f"Pressed key: '{key}'")
                        
                    elif action == "drag":
                        norm_x, norm_y = params.get("x", 500), params.get("y", 500)
                        x, y = self.scale_coordinates(norm_x, norm_y)
                        print(f"[Action] Dragging to ({x}, {y})")
                        pyautogui.dragTo(x, y, duration=0.5)
                        history.append(f"Dragged to normalized x={norm_x}, y={norm_y}")
                        
                    elif action == "wait":
                        duration = params.get("duration", 2.0)
                        print(f"[Action] Waiting for {duration}s...")
                        time.sleep(duration)
                        history.append(f"Waited for {duration} seconds")
                        
                # Add delay between loop steps to comply with rate limits
                time.sleep(1.5)
                
            except Exception as e:
                print(f"[Error] Failed to execute loop step: {e}")
                break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/keystone_desktop_operator.py \"<goal description>\"")
        sys.exit(1)
        
    goal_arg = sys.argv[1]
    operator = KeystoneDesktopOperator()
    operator.run_task(goal_arg)
