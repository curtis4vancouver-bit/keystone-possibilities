import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

QUEUE_FILE = os.path.join(os.path.dirname(__file__), "deep_research_queue.json")
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Deep_Research_Results")

async def run_diagnostic():
    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)
        
    pending = [item for item in queue if item["status"] == "pending"]
    if not pending:
        print("No pending tasks in queue.")
        return

    item = pending[0]
    item["status"] = "processing"
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

    prompt_text = item["prompt"]
    print(f"Starting task: {item['batch_name']}")

    async with async_playwright() as p:
        print("Connecting to Chrome CDP on localhost:9222...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        
        print("Creating new page...")
        page = await context.new_page()
        
        try:
            print("Navigating to https://gemini.google.com/app ...")
            await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
            
            print("Page loaded. Waiting 8 seconds for UI to settle...")
            await asyncio.sleep(8)
            
            print("Attempting to locate input box...")
            input_locator = page.locator("rich-textarea, div[contenteditable='true'], textarea").first
            await input_locator.wait_for(state="visible", timeout=15000)
            
            print("Input box located. Clicking...")
            await input_locator.click()
            await asyncio.sleep(1)
            
            print("Inserting text...")
            await page.keyboard.insert_text(prompt_text)
            
            print("Pressing Space to trigger framework events...")
            await page.keyboard.press("Space")
            
            print("Waiting 5 seconds before submission...")
            await asyncio.sleep(5)
            
            print("Submitting prompt (Enter)...")
            await page.keyboard.press("Enter")
            
            print("Waiting 15 seconds to verify submission...")
            await asyncio.sleep(15)
            
            print("Task successfully injected! Setting status to completed for diagnostic.")
            item["status"] = "completed"
            
        except Exception as e:
            print(f"ERROR OCCURRED: {str(e)}")
            item["status"] = "failed"
            item["error"] = str(e)
        finally:
            print("Closing page...")
            await page.close()

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)
        
    print("Diagnostic complete.")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
