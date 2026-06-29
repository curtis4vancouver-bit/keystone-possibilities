import asyncio
import json
import os
import time
import threading
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

mcp = FastMCP("Gemini_Deep_Researcher")

QUEUE_FILE = os.path.join(os.path.dirname(__file__), "deep_research_queue.json")
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Deep_Research_Results")

if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

if not os.path.exists(QUEUE_FILE):
    with open(QUEUE_FILE, "w") as f:
        json.dump([], f)

@mcp.tool()
def add_prompts_to_queue(prompts: list[str], batch_name: str) -> str:
    """
    Adds a list of prompts to the background Deep Research queue.
    The agent will process these in the background (3 at a time) using Gemini Chrome Pro.
    Results will be saved in 00_Master_Brain/Deep_Research_Results.
    """
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
    except:
        queue = []
        
    for p in prompts:
        queue.append({
            "prompt": p,
            "batch_name": batch_name,
            "status": "pending"
        })
        
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)
        
    return f"Successfully added {len(prompts)} prompts to the queue. Background agent will process them 3 at a time."

@mcp.tool()
def check_queue_status() -> str:
    """Returns the current status of the background deep research queue."""
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
        pending = len([q for q in queue if q["status"] == "pending"])
        processing = len([q for q in queue if q["status"] == "processing"])
        completed = len([q for q in queue if q["status"] == "completed"])
        failed = len([q for q in queue if q["status"] == "failed"])
        return f"Queue Status: {pending} pending, {processing} processing, {completed} completed, {failed} failed."
    except Exception as e:
        return f"Error reading queue: {e}"

async def run_single_task(browser, item, index):
    prompt_text = item["prompt"]
    batch_name = item["batch_name"]
    context = browser.contexts[0]
    page = await context.new_page()
    
    try:
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(8) # Wait for UI to settle
        
        # Click Tools -> Deep research
        try:
            tools_btn = page.get_by_text("Tools", exact=True).first
            if await tools_btn.is_visible(timeout=5000):
                await tools_btn.click()
                await asyncio.sleep(2)
                deep_research_opt = page.locator("div:has-text('Deep research')").nth(-1)
                try:
                    deep_research_opt = page.get_by_text("Deep research", exact=True).first
                    if await deep_research_opt.is_visible(timeout=5000):
                        await deep_research_opt.click()
                        await asyncio.sleep(2)
                except:
                    pass
        except:
            pass # Continue even if we can't find it
            
        # Enter prompt
        try:
            # Most robust way to type into rich-text editors in Playwright
            input_locator = page.locator("rich-textarea, div[contenteditable='true'], textarea").first
            await input_locator.wait_for(state="visible", timeout=15000)
            await input_locator.click()
            await asyncio.sleep(1)
            # Insert text instead of type for speed, then press space to trigger react/angular events
            await page.keyboard.insert_text(prompt_text)
            await page.keyboard.press("Space")
        except Exception as input_err:
            raise Exception(f"Failed to find or type into input box: {str(input_err)}")
        
        # Wait 30 seconds as instructed
        await asyncio.sleep(30)
        
        # Submit
        await page.keyboard.press("Enter")
        
        # Wait 3 minutes initially
        await asyncio.sleep(180)
        
        # Check every minute for completion (blue line circle gets all the way through)
        for _ in range(30): # Up to 30 minutes wait
            await asyncio.sleep(60)
            progress_circle = page.locator("svg circle, mat-progress-spinner, [role='progressbar']")
            if await progress_circle.count() == 0:
                break
                
        # Extract response
        messages = await page.locator("message-content").all()
        result_text = "No response found."
        if messages:
            result_text = await messages[-1].inner_text()
            
        # Save to file
        safe_name = "".join([c for c in batch_name if c.isalnum() or c in (' ', '_')]).rstrip()
        filename = f"{safe_name}_task_{index}.md"
        filepath = os.path.join(RESULTS_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Prompt: {prompt_text}\n\n## Response:\n{result_text}")
            
        item["status"] = "completed"
        
    except Exception as e:
        item["status"] = "failed"
        item["error"] = str(e)
    finally:
        await page.close()

async def background_worker():
    """Continuously monitors the queue and processes up to 3 tasks in parallel."""
    while True:
        try:
            with open(QUEUE_FILE, "r") as f:
                queue = json.load(f)
                
            pending_tasks = [item for item in queue if item["status"] == "pending"]
            
            if pending_tasks:
                # Grab up to 3
                batch = pending_tasks[:3]
                for item in batch:
                    item["status"] = "processing"
                    
                with open(QUEUE_FILE, "w") as f:
                    json.dump(queue, f, indent=2)
                    
                async with async_playwright() as p:
                    try:
                        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
                        
                        tasks = []
                        for i, item in enumerate(batch):
                            # Give a unique timestamp-based index for filenames
                            tasks.append(run_single_task(browser, item, int(time.time()) + i))
                            
                        await asyncio.gather(*tasks)
                    except Exception as e:
                        # Revert status on connection failure
                        for item in batch:
                            item["status"] = "pending"
                            item["error"] = str(e)
                            
                # Update queue with results
                with open(QUEUE_FILE, "w") as f:
                    json.dump(queue, f, indent=2)
                    
                # Check if all tasks are officially done
                remaining_active = [item for item in queue if item["status"] in ["pending", "processing"]]
                if not remaining_active:
                    import subprocess
                    ps_script = '''
                    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                    $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
                    $textNodes = $template.GetElementsByTagName("text")
                    $textNodes.Item(0).AppendChild($template.CreateTextNode("Keystone Master Brain")) | Out-Null
                    $textNodes.Item(1).AppendChild($template.CreateTextNode("All Background Deep Research tasks have finished! Check the folder.")) | Out-Null
                    $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
                    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Antigravity")
                    $notifier.Show($toast)
                    '''
                    subprocess.run(["powershell", "-Command", ps_script], shell=True)
                    
        except Exception as e:
            pass # ignore read/write errors and retry
            
        await asyncio.sleep(10) # check every 10 seconds

def start_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(background_worker())

# Start the background worker in a separate thread so the MCP server stays unblocked
threading.Thread(target=start_background_loop, daemon=True).start()

if __name__ == "__main__":
    mcp.run()
