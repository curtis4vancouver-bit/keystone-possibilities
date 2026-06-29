import asyncio
import os
import sys
import json
import time
import psutil
import subprocess
from playwright.async_api import async_playwright

PROJECT_ROOT = r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain"
sys.path.append(PROJECT_ROOT)

from overnight_research_daemon import OvernightResearchDaemon

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    for _ in range(30):
        if os.path.exists(active_port_file):
            try:
                with open(active_port_file, "r") as f:
                    lines = f.read().splitlines()
                port = lines[0].strip()
                ws_path = lines[1].strip()
                return f"ws://127.0.0.1:{port}{ws_path}"
            except Exception:
                pass
        time.sleep(1)
    raise FileNotFoundError("DevToolsActivePort file not found or not readable. Make sure Chrome is running with remote debugging port 9222.")

async def run_batch(batch):
    ws_url = get_websocket_url()
    print(f"Connecting to Chrome over CDP on {ws_url}...")
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        
        page_runs = []
        
        # 1. Open tabs and type prompts (Staggered)
        for idx, item in enumerate(batch):
            index = idx + 1
            print(f"[{index}] Opening tab for topic: {item['topic']}")
            page = await context.new_page()
            
            try:
                # Go to Gemini
                await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(8)
                
                # Check if Deep Research is selected
                deselect_btn = page.locator("button:has-text('Deselect Deep research'), button:has-text('Deselect Deep Research'), button[aria-label='Deselect Deep research']")
                if await deselect_btn.count() > 0:
                    print(f"[{index}] Deep Research is already selected.")
                else:
                    print(f"[{index}] Deep Research is not selected. Selecting it...")
                    plus_btn = page.locator("button[aria-label='Upload & tools'], button:has-text('Upload & tools'), button[aria-label='Add files or tools'], button[aria-label='Upload']").first
                    if await plus_btn.is_visible():
                        await plus_btn.click()
                        await asyncio.sleep(2)
                        
                        dr_menu_item = page.locator("menuitemcheckbox:has-text('Deep research'), menuitemcheckbox:has-text('Deep Research'), [role='menuitemcheckbox']:has-text('Deep research'), [role='menuitemcheckbox']:has-text('Deep Research')").first
                        if await dr_menu_item.is_visible():
                            await dr_menu_item.click()
                            print(f"[{index}] Clicked Deep Research menu item.")
                            await asyncio.sleep(2)
                        else:
                            print(f"[{index}] Warning: Deep Research menu item not found.")
                    else:
                        print(f"[{index}] Warning: Plus button not found.")
                
                # Focus input and insert text
                input_box = page.locator("div[role='textbox'], rich-textarea, textarea").first
                await input_box.wait_for(state="visible", timeout=15000)
                await input_box.click()
                await asyncio.sleep(1)
                
                await page.keyboard.insert_text(item["prompt"])
                await page.keyboard.press("Space")
                await asyncio.sleep(2)
                
                print(f"[{index}] Submitting prompt...")
                send_btn = page.locator("button[aria-label='Send message'], button:has-text('Send message')").first
                if await send_btn.is_visible() and await send_btn.is_enabled():
                    await send_btn.click()
                    print(f"[{index}] Clicked Send message button.")
                else:
                    await page.keyboard.press("Enter")
                    print(f"[{index}] Pressed Enter.")
                
                # Register the page run
                page_runs.append({
                    "page": page,
                    "item": item,
                    "index": index,
                    "state": "planning"
                })
                
                # Wait 8 seconds before opening the next tab to stagger requests
                await asyncio.sleep(8)
                
            except Exception as e:
                print(f"[{index}] ❌ Error during tab initialization: {e}")
                # Close the page if it failed to initialize
                try:
                    await page.close()
                except Exception:
                    pass
        
        # 2. Go back through the tabs to click "Start research"
        for run in page_runs:
            page = run["page"]
            index = run["index"]
            item = run["item"]
            
            print(f"[{index}] Bringing to front to click Start Research...")
            try:
                await page.bring_to_front()
                await asyncio.sleep(2)
                
                # Wait for "Start research" button (up to 90 seconds)
                start_btn = page.locator("button:has-text('Start research'), button:has-text('Start Research')").first
                found_start = False
                for _ in range(45):
                    if await start_btn.is_visible() and await start_btn.is_enabled():
                        print(f"[{index}] Found 'Start research' button. Clicking it...")
                        await start_btn.click()
                        found_start = True
                        run["state"] = "running"
                        run["start_time"] = time.time()
                        break
                    
                    # Double check if it has already started or completed
                    body_text = await page.evaluate("document.body.innerText")
                    if "completed your research" in body_text.lower():
                        print(f"[{index}] Research completed immediately.")
                        run["state"] = "running"
                        run["start_time"] = time.time()
                        found_start = True
                        break
                    await asyncio.sleep(2)
                    
                if not found_start:
                    print(f"[{index}] Warning: 'Start research' button not found/enabled. Proceeding as running anyway.")
                    run["state"] = "running"
                    run["start_time"] = time.time()
                    
                # Pause slightly before the next tab activation
                await asyncio.sleep(5)
            except Exception as e:
                print(f"[{index}] Error during Start Research click: {e}")
                run["state"] = "completed"
                run["success"] = False
                
        # 3. Monitor tabs loop until all complete
        print("[Supervisor] All tabs started. Entering monitor loop...")
        max_wait = 900  # 15 minutes max wait time per topic
        
        while any(run["state"] == "running" for run in page_runs):
            print("[Supervisor] Sleeping 30 seconds before checking page statuses...")
            await asyncio.sleep(30)
            
            for run in page_runs:
                if run["state"] != "running":
                    continue
                    
                page = run["page"]
                index = run["index"]
                item = run["item"]
                
                try:
                    # Bring page to front briefly to ensure it runs/updates (optional but keeps active tab running well)
                    # await page.bring_to_front()
                    
                    share_btn = page.locator("button:has-text('Share & Export'), button[aria-label='Share & Export'], button:has-text('Share'), button[aria-label='Share']").first
                    body_text = await page.evaluate("document.body.innerText")
                    
                    is_complete = await share_btn.is_visible() or "completed your research" in body_text.lower()
                    elapsed = time.time() - run["start_time"]
                    
                    if is_complete:
                        print(f"[{index}] ✅ Research finished! Extracting content...")
                        run["state"] = "extracting"
                        
                        messages = await page.locator("message-content").all()
                        if not messages:
                            raise ValueError("No response messages found.")
                            
                        report_text = await messages[-1].inner_text()
                        print(f"[{index}] Extracted {len(report_text)} characters.")
                        
                        # Save to temp file
                        temp_file = os.path.join(PROJECT_ROOT, "scratch", f"temp_report_{index}.txt")
                        with open(temp_file, "w", encoding="utf-8") as f:
                            f.write(report_text)
                            
                        # Run ingestion script
                        print(f"[{index}] Ingesting report to brain...")
                        process_script = os.path.join(PROJECT_ROOT, "scratch", "process_completed_topic.py")
                        res = subprocess.run(
                            [sys.executable, process_script, item["domain"], item["topic"], temp_file],
                            cwd=PROJECT_ROOT,
                            capture_output=True,
                            text=True
                        )
                        if res.returncode == 0:
                            print(f"[{index}] ✅ Saved and ingested successfully!")
                            run["success"] = True
                        else:
                            print(f"[{index}] ❌ Ingestion failed: {res.stderr}")
                            run["success"] = False
                            
                        # Close the tab
                        print(f"[{index}] Closing tab.")
                        await page.close()
                        run["state"] = "completed"
                        
                    elif elapsed > max_wait:
                        print(f"[{index}] ❌ Timeout reached after 15 minutes.")
                        await page.close()
                        run["state"] = "completed"
                        run["success"] = False
                        
                except Exception as e:
                    print(f"[{index}] Error checking page status: {e}")
                    if "Target page, context or browser has been closed" in str(e):
                        run["state"] = "completed"
                        run["success"] = False
        
        # 4. Disconnect Playwright (NEVER close the remote browser process)
        print("CDP session complete. Exiting...")
        
    return [run.get("success", False) for run in page_runs]

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--batches", type=int, default=30, help="Number of batches/topics to run")
    args = parser.parse_args()
    
    daemon = OvernightResearchDaemon()
    max_batches = args.batches
    
    print("Checking credit availability before starting...")
    credit_status = daemon.should_wait_for_credits()
    if not credit_status["can_continue"]:
        print("\n==========================================")
        print("CREDIT CHECK FAILED")
        print(credit_status["recommendation"])
        print("==========================================")
        sys.exit(0)
        
    for b_idx in range(max_batches):
        # Double check credits before each batch
        credit_status = daemon.should_wait_for_credits()
        if not credit_status["can_continue"]:
            print("\n==========================================")
            print("CREDIT CHECK FAILED DURING RUN")
            print(credit_status["recommendation"])
            print("==========================================")
            break
            
        batch = daemon.get_next_batch(batch_size=3)
        if not batch:
            print("No more pending topics. Research queue completed!")
            break
            
        print(f"\n==========================================")
        print(f"STARTING BATCH {b_idx+1} ({len(batch)} topics)")
        print(f"==========================================")
        for item in batch:
            print(f"  - [{item['domain']}] {item['topic'][:80]}...")
            
        results = asyncio.run(run_batch(batch))
        print(f"Batch {b_idx+1} results: {results}")
        
        # If successfully processed, record prompts used
        success_count = sum(1 for r in results if r is True)
        if success_count > 0:
            daemon.record_prompts_used(success_count)
            print(f"Recorded {success_count} prompt credits used. Progress saved.")
        
        # Pause slightly between batches
        if b_idx < max_batches - 1:
            print("Waiting 10 seconds before next batch...")
            time.sleep(10)

if __name__ == "__main__":
    main()
