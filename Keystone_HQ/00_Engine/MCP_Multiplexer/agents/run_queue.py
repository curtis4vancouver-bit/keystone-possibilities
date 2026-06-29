import asyncio
import json
import os
import time
from playwright.async_api import async_playwright

QUEUE_FILE = os.path.join(os.path.dirname(__file__), "deep_research_queue.json")
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Deep_Research_Results")

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

async def run_queue():
    with open(QUEUE_FILE, "r") as f:
        queue = json.load(f)
        
    pending = [q for q in queue if q["status"] == "pending"]
    if not pending:
        print("No pending tasks.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        
        for item in pending:
            item["status"] = "processing"
            with open(QUEUE_FILE, "w") as f:
                json.dump(queue, f, indent=2)
                
            page = await context.new_page()
            try:
                await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(10)
                
                # Click Tools menu to select Deep research
                print("Clicking Tools menu...")
                tools_btn = page.get_by_text("Tools", exact=True).first
                if await tools_btn.is_visible(timeout=5000):
                    await tools_btn.click()
                    await asyncio.sleep(2)
                    
                    print("Clicking Deep research...")
                    deep_research_opt = page.locator("div:has-text('Deep research')").nth(-1)
                    try:
                        deep_research_opt = page.get_by_text("Deep research", exact=True).first
                        if await deep_research_opt.is_visible(timeout=5000):
                            await deep_research_opt.click()
                            await asyncio.sleep(2)
                    except:
                        pass
                
                # Verify Model is on Pro or Thinking (just ensure Pro is selected if needed, but default is fine)
                
                # Input
                input_locator = page.locator("rich-textarea, div[contenteditable='true'], textarea").first
                await input_locator.wait_for(state="visible", timeout=15000)
                await input_locator.click()
                await asyncio.sleep(1)
                
                await page.keyboard.insert_text(item["prompt"])
                await page.keyboard.press("Space")
                await asyncio.sleep(3)
                await page.keyboard.press("Enter")
                
                # After pressing enter, Deep Research often requires clicking a "Start research" confirmation button
                print("Checking for 'Start research' button...")
                try:
                    # Wait up to 45 seconds for the button to appear (Gemini takes time to build the plan)
                    start_btn = page.locator("button:has-text('Start research')").first
                    if await start_btn.is_visible(timeout=45000):
                        print("Found 'Start research' button, clicking it...")
                        await start_btn.click()
                        await asyncio.sleep(2)
                except Exception as e:
                    print(f"No 'Start research' button found or clicked: {e}")
                
                print("Waiting for research to complete (up to 30 mins)...")
                # Wait for generation to complete
                await asyncio.sleep(30) # Initial wait
                
                for _ in range(30): # Up to 30 mins
                    await asyncio.sleep(60)
                    progress_circle = page.locator("svg circle, mat-progress-spinner, [role='progressbar']")
                    if await progress_circle.count() == 0:
                        break
                        
                await asyncio.sleep(10) # Buffer after completion
                
                # Extract text
                messages = await page.locator("message-content").all()
                result_text = "No response found."
                if messages:
                    result_text = await messages[-1].inner_text()
                    
                safe_name = "".join([c for c in item["batch_name"] if c.isalnum() or c in (' ', '_')]).rstrip()
                filepath = os.path.join(RESULTS_DIR, f"{safe_name}_{int(time.time())}.md")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"# Prompt: {item['prompt']}\n\n## Response:\n{result_text}")
                    
                item["status"] = "completed"
                print(f"Completed {item['batch_name']}")
                
            except Exception as e:
                item["status"] = "failed"
                item["error"] = str(e)
                print(f"Failed {item['batch_name']}: {e}")
            finally:
                await page.close()
                with open(QUEUE_FILE, "w") as f:
                    json.dump(queue, f, indent=2)

if __name__ == "__main__":
    asyncio.run(run_queue())
