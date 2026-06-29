import asyncio
import os
import sys
import json
import time
from playwright.async_api import async_playwright

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

async def main():
    daemon = OvernightResearchDaemon()
    batch = daemon.get_next_batch(batch_size=1)
    if not batch:
        print("No pending topics in queue.")
        return
        
    item = batch[0]
    domain = item["domain"]
    topic = item["topic"]
    prompt = item["prompt"]
    
    print(f"Next topic to research: [{domain}] {topic}")
    
    # Read the active devtools port
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
    port = lines[0].strip()
    ws_path = lines[1].strip()
    ws_url = f"ws://127.0.0.1:{port}{ws_path}"
    
    async with async_playwright() as p:
        print(f"Connecting to Chrome via WebSocket: {ws_url}...")
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        
        print("Opening new tab...")
        page = await context.new_page()
        
        try:
            print("Navigating to Gemini...")
            await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(5)
            
            # Check if Deep Research is selected
            # Look for "Deselect Deep research" button
            deselect_btn = page.locator("button:has-text('Deselect Deep research')")
            if await deselect_btn.count() > 0:
                print("Deep Research is already selected.")
            else:
                print("Deep Research is not selected. Attempting to select it...")
                # Try to click "Deep research" button or toggle
                deep_btn = page.locator("button:has-text('Deep research'), div:has-text('Deep research')").first
                if await deep_btn.is_visible():
                    await deep_btn.click()
                    print("Clicked Deep Research button.")
                    await asyncio.sleep(2)
                else:
                    print("Warning: Could not find Deep Research button. Proceeding anyway.")
            
            # Locate input textbox
            # Try rich-textarea or contenteditable div
            input_box = page.locator("rich-textarea, div[contenteditable='true'], textarea").first
            await input_box.wait_for(state="visible", timeout=15000)
            await input_box.focus()
            
            print("Typing prompt...")
            # insert_text is much faster than type
            await page.keyboard.insert_text(prompt)
            await page.keyboard.press("Space")
            await asyncio.sleep(2)
            
            print("Submitting prompt...")
            await page.keyboard.press("Enter")
            
            # Wait for "Start research" button (Gemini builds a plan first)
            print("Waiting for 'Start research' button to appear...")
            start_btn = page.locator("button:has-text('Start research')").first
            
            # Wait up to 60 seconds
            found_start = False
            for _ in range(30):
                if await start_btn.is_visible():
                    print("Found 'Start research' button. Clicking it...")
                    await start_btn.click()
                    found_start = True
                    break
                await asyncio.sleep(2)
                
            if not found_start:
                print("Warning: 'Start research' button not found. Maybe it started automatically?")
                
            print("Waiting for Deep Research to complete...")
            # Poll for completion: look for "Share & Export" or check if progress spinner is gone
            completed = False
            start_time = time.time()
            max_wait = 900 # 15 minutes
            
            while time.time() - start_time < max_wait:
                await asyncio.sleep(15)
                # Check for completion indicators
                # e.g., presence of "Share & Export" button
                share_btn = page.locator("button:has-text('Share & Export'), button[aria-label='Share & Export']").first
                # Or check if "I've completed your research" text is present
                body_text = await page.evaluate("document.body.innerText")
                
                if await share_btn.is_visible() or "completed your research" in body_text.lower():
                    print("Research complete!")
                    completed = True
                    break
                else:
                    elapsed = int(time.time() - start_time)
                    print(f"Still running... {elapsed}s elapsed.")
            
            if not completed:
                print("Error: Research timed out after 15 minutes.")
                return
                
            # Extract response
            print("Extracting report text...")
            messages = await page.locator("message-content").all()
            if not messages:
                print("Error: No messages found on the page.")
                return
                
            last_message = messages[-1]
            report_text = await last_message.inner_text()
            print(f"Extracted {len(report_text)} characters.")
            
            # Save using the process script
            temp_file = os.path.join(PROJECT_ROOT, "scratch", "temp_test_report.txt")
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(report_text)
                
            print("Processing and ingesting report...")
            process_script = os.path.join(PROJECT_ROOT, "scratch", "process_completed_topic.py")
            
            # Run the process script in a subprocess
            import subprocess
            res = subprocess.run(
                [sys.executable, process_script, domain, topic, temp_file],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )
            print("STDOUT:", res.stdout)
            print("STDERR:", res.stderr)
            
            if res.returncode == 0:
                print("Success!")
            else:
                print(f"Process failed with return code {res.returncode}")
                
        except Exception as e:
            print(f"Exception occurred during run: {e}")
        finally:
            print("Closing page...")
            await page.close()
            print("Done.")

if __name__ == "__main__":
    asyncio.run(main())
