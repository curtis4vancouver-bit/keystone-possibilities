import asyncio
import os
import re
import sys
import time
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

PROJECT_ROOT = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Master_Brain")
PROMPTS_FILE = PROJECT_ROOT / "DEEP_RESEARCH_PROMPTS_SYSTEM_LOCKDOWN.md"
DEEP_RESEARCH_RESULTS_ENGINE = Path(r"c:\Users\Curtis\New folder\construction-website\Keystone_HQ\00_Engine\Deep_Research_Results")
DEEP_RESEARCH_RESULTS_BRAIN = PROJECT_ROOT / "Deep_Research_Results"

def launch_chrome_with_junction():
    link_path = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data Link"
    target_path = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data"
    
    # 1. Clean up old junction if exists
    if os.path.exists(link_path):
        print(f"[Launcher] Junction {link_path} already exists. Cleaning up first...")
        if os.path.isdir(link_path):
            subprocess.run(f'rmdir "{link_path}"', shell=True)
        else:
            try:
                os.remove(link_path)
            except Exception:
                pass
                
    # 2. Create the directory junction
    print(f"[Launcher] Creating directory junction from {link_path} to {target_path}...")
    res = subprocess.run(f'mklink /J "{link_path}" "{target_path}"', shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print("[Launcher] Failed to create junction:")
        print("stdout:", res.stdout)
        print("stderr:", res.stderr)
        raise RuntimeError("mklink failed")
        
    # 3. Launch Chrome with port=0
    # Also delete old DevToolsActivePort first to ensure we read a fresh one
    active_port_file = os.path.join(target_path, "DevToolsActivePort")
    if os.path.exists(active_port_file):
        try:
            os.remove(active_port_file)
            print("[Launcher] Removed old DevToolsActivePort file.")
        except Exception as e:
            print("[Launcher] Warning: could not remove old DevToolsActivePort:", e)
            
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    cmd = [
        chrome_path,
        "--remote-debugging-port=0",
        "--remote-allow-origins=*",
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--user-data-dir={link_path}"
    ]
    
    print("[Launcher] Launching Chrome headlessly with remote-debugging-port=0...")
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 4. Wait for DevToolsActivePort to be written
    ws_url = None
    for i in range(20):
        time.sleep(0.5)
        if os.path.exists(active_port_file):
            print("[Launcher] DevToolsActivePort file detected!")
            try:
                with open(active_port_file, "r") as f:
                    lines = f.read().splitlines()
                if len(lines) >= 2:
                    port = lines[0].strip()
                    ws_path = lines[1].strip()
                    ws_url = f"ws://localhost:{port}{ws_path}"
                    print(f"[Launcher] Found dynamic WebSocket URL: {ws_url}")
                    break
            except Exception as e:
                print("[Launcher] Waiting: error reading DevToolsActivePort:", e)
                
    if not ws_url:
        proc.terminate()
        proc.wait()
        # cleanup junction
        subprocess.run(f'rmdir "{link_path}"', shell=True)
        raise RuntimeError("[Launcher] Could not retrieve WebSocket URL from DevToolsActivePort.")
        
    return proc, ws_url, link_path

def parse_prompts():
    if not PROMPTS_FILE.exists():
        print(f"Error: Prompts file not found at {PROMPTS_FILE}")
        return []
    
    content = PROMPTS_FILE.read_text(encoding="utf-8")
    # Parse sections starting with ## PROMPT X — [Name]
    pattern = re.compile(r"## PROMPT (\d+)\s*—\s*([^\n]+)\n\s*```\n(.*?)\n```", re.DOTALL)
    matches = pattern.findall(content)
    
    prompts = []
    for match in matches:
        p_id = int(match[0])
        name = match[1].strip()
        prompt_text = match[2].strip()
        
        # Slugify name for filename
        slug = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
        
        prompts.append({
            "id": p_id,
            "name": name,
            "slug": slug,
            "prompt": prompt_text
        })
    return prompts

async def select_deep_research(page, index):
    print(f"[{index}] Checking if Deep Research is selected...")
    deselect_btn = page.locator("button:has-text('Deselect Deep research'), button:has-text('Deselect Deep Research'), button[aria-label='Deselect Deep research']")
    if await deselect_btn.count() > 0:
        print(f"[{index}] Deep Research is already selected.")
        return True
    
    print(f"[{index}] Deep Research is not selected. Clicking Upload & tools...")
    plus_btn = page.locator("button[aria-label='Upload & tools'], button:has-text('Upload & tools'), button[aria-label='Add files or tools'], button[aria-label='Upload']").first
    await plus_btn.wait_for(state="visible", timeout=15000)
    await plus_btn.click()
    await asyncio.sleep(2)
    
    print(f"[{index}] Selecting Deep Research menu item...")
    dr_menu_item = page.locator("menuitemcheckbox:has-text('Deep research'), menuitemcheckbox:has-text('Deep Research'), [role='menuitemcheckbox']:has-text('Deep research'), [role='menuitemcheckbox']:has-text('Deep Research')").first
    await dr_menu_item.wait_for(state="visible", timeout=10000)
    await dr_menu_item.click()
    await asyncio.sleep(2)
    
    # Check for Start New Chat dialog
    dialog_new_chat = page.locator("button:has-text('New chat'), button:has-text('New Chat'), dialog button:has-text('New chat')").first
    if await dialog_new_chat.count() > 0 and await dialog_new_chat.is_visible():
        print(f"[{index}] Start new chat dialog appeared. Clicking New chat...")
        await dialog_new_chat.click()
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(5)
        
        # Double check if selected now
        if await deselect_btn.count() > 0:
            print(f"[{index}] Deep Research successfully selected after new chat.")
            return True
        else:
            print(f"[{index}] Warning: Deep Research still not showing as selected.")
    return False

async def handle_captcha(page, name):
    url = page.url
    if "sorry" in url or "captcha" in url:
        print(f"[{name}] WARNING: CAPTCHA / Sorry page detected!")
        for frame in page.frames:
            if "recaptcha" in frame.url:
                print(f"[{name}] Found recaptcha frame. Attempting to click anchor...")
                try:
                    anchor = frame.locator("#recaptcha-anchor")
                    if await anchor.count() > 0:
                        await anchor.click()
                        print(f"[{name}] Clicked recaptcha anchor. Waiting 10s for reload...")
                        await asyncio.sleep(10)
                        return True
                except Exception as e:
                    print(f"[{name}] Error clicking recaptcha anchor: {e}")
    return False

async def run_prompt_tab(context, item):
    index = item["id"]
    name = item["name"]
    prompt = "Activate Deep Research. " + item["prompt"]
    
    print(f"\nInitializing Tab {index}: {name}...")
    page = await context.new_page()
    await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
    await asyncio.sleep(5)
    
    # Check CAPTCHA
    await handle_captcha(page, name)
    
    # Enable deep research
    await select_deep_research(page, index)
    
    # Focus input and insert text
    input_box = page.locator("div[role='textbox'], rich-textarea, textarea").first
    await input_box.wait_for(state="visible", timeout=15000)
    await input_box.click()
    await asyncio.sleep(1)
    
    print(f"[{index}] Typing prompt...")
    await page.keyboard.insert_text(prompt)
    await asyncio.sleep(2)
    
    print(f"[{index}] Clicking Send message...")
    send_btn = page.locator("button[aria-label='Send message'], button:has-text('Send message')").first
    await send_btn.click()
    await asyncio.sleep(2)
    
    return page

async def start_research_on_tab(page, index, name):
    print(f"\n[{index}] Bringing page to front to start research: {name}...")
    await page.bring_to_front()
    await asyncio.sleep(2)
    
    # Check CAPTCHA
    await handle_captcha(page, name)
    
    start_btn = page.locator("button:has-text('Start research'), button:has-text('Start Research'), button:has-text('Start')").first
    
    # Poll up to 60 seconds for the Start research button
    clicked_start = False
    for i in range(30):
        if await start_btn.count() > 0 and await start_btn.is_visible() and await start_btn.is_enabled():
            print(f"[{index}] Found 'Start research' button. Clicking it!")
            await start_btn.click()
            clicked_start = True
            break
        await asyncio.sleep(2)
        
    if not clicked_start:
        print(f"[{index}] Warning: Could not find 'Start research' button. Checking body text...")
        body = await page.evaluate("document.body.innerText")
        if "completed your research" in body.lower():
            print(f"[{index}] Research completed immediately or already in progress.")
        else:
            print(f"[{index}] Research might have auto-started or is in error state.")

async def monitor_batch(pages_map):
    print("\nEntering monitor loop for batch...")
    max_wait = 1200  # 20 minutes max per batch
    start_time = time.time()
    
    pending = list(pages_map.keys())
    
    while pending:
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            print("❌ TIMEOUT reached for this batch!")
            break
            
        print(f"\n[Monitor] {len(pending)} pages pending. Elapsed: {int(elapsed)}s. Checking status...")
        
        for name in list(pending):
            page, index, slug = pages_map[name]
            try:
                # Detect and handle sorry page/CORS block by reloading
                if "sorry/index" in page.url or "captcha" in page.url:
                    print(f"  - [{name}] Warning: Sorry page detected. Attempting reload...")
                    await page.reload()
                    await asyncio.sleep(5)
                    continue
                    
                # Check for Share / Export button or complete text
                share_btn = page.locator("button:has-text('Share & Export'), button[aria-label='Share & Export'], button:has-text('Share'), button[aria-label='Share']").first
                body_text = await page.evaluate("document.body.innerText")
                
                is_complete = await share_btn.count() > 0 and await share_btn.is_visible()
                if not is_complete:
                    is_complete = "completed your research" in body_text.lower() or "here is the strategic" in body_text.lower() or "research results" in body_text.lower()
                    
                lines = body_text.split("\n")
                status_lines = [l for l in lines if any(k in l.lower() for k in ["searching", "reading", "analyzing", "researching", "generating research plan", "thought for"])]
                if status_lines:
                    print(f"  - [{name}] Status: {status_lines[-1]}")
                else:
                    print(f"  - [{name}] Processing...")
                
                if is_complete:
                    print(f"  - [{name}] ✅ Deep Research complete! Extracting report...")
                    
                    messages = await page.locator("message-content, .model-response, [role='log'] message-content").all()
                    if not messages:
                        print(f"  - [{name}] ❌ Error: message-content not found in DOM.")
                        pending.remove(name)
                        continue
                        
                    report_text = await messages[-1].inner_text()
                    print(f"  - [{name}] Extracted {len(report_text)} characters.")
                    
                    # Save to results
                    fn = f"20260624_prompt_{index}_{slug}.md"
                    path_engine = DEEP_RESEARCH_RESULTS_ENGINE / fn
                    path_brain = DEEP_RESEARCH_RESULTS_BRAIN / fn
                    
                    DEEP_RESEARCH_RESULTS_ENGINE.mkdir(parents=True, exist_ok=True)
                    DEEP_RESEARCH_RESULTS_BRAIN.mkdir(parents=True, exist_ok=True)
                    
                    path_engine.write_text(report_text, encoding="utf-8")
                    path_brain.write_text(report_text, encoding="utf-8")
                        
                    print(f"  - [{name}] Saved to {fn}")
                    await page.close()
                    print(f"  - [{name}] Closed tab.")
                    pending.remove(name)
                    
            except Exception as e:
                print(f"  - [{name}] Error checking status: {e}")
                if "closed" in str(e).lower():
                    pending.remove(name)
                    
        if pending:
            await asyncio.sleep(20)

async def main():
    prompts = parse_prompts()
    print(f"Parsed {len(prompts)} prompts from {PROMPTS_FILE}")
    
    # Map of prompt ID to manual filename used in previous batches
    completed_mapping = {
        1: "20260624_qdrant_namespace_strategy.md",
        2: "20260624_qdrant_hybrid_search.md",
        3: "20260624_qdrant_performance_tuning.md",
        4: "20260624_ai_agent_session_bootstrap.md",
        5: "20260624_ai_agent_behavioral_drift_prevention.md",
        6: "20260624_ai_agent_mcp_tool_integration.md",
        7: "20260624_docker_ai_infrastructure_optimization.md",
        8: "20260624_ai_agent_skill_adherence.md",
    }
    
    remaining_prompts = []
    for p in prompts:
        fn_default = f"20260624_prompt_{p['id']}_{p['slug']}.md"
        fn_mapped = completed_mapping.get(p['id'], "")
        
        exists = False
        for fn in [fn_default, fn_mapped]:
            if not fn:
                continue
            path_engine = DEEP_RESEARCH_RESULTS_ENGINE / fn
            path_brain = DEEP_RESEARCH_RESULTS_BRAIN / fn
            if path_engine.exists() or path_brain.exists():
                exists = True
                break
                
        if exists:
            print(f"Prompt {p['id']} ({p['name']}) is already completed. Skipping.")
        else:
            remaining_prompts.append(p)
            
    print(f"Remaining prompts to run: {len(remaining_prompts)}")
    if not remaining_prompts:
        print("All prompts completed!")
        return
        
    proc, ws_url, link_path = launch_chrome_with_junction()
    
    try:
        async with async_playwright() as p:
            print(f"Connecting to Chrome DevTools on {ws_url}...")
            browser = await p.chromium.connect_over_cdp(ws_url)
            context = browser.contexts[0]
            
            # Ensure at least one about:blank page is open to keep Chrome alive
            keep_alive_page = None
            for page in context.pages:
                if page.url == "about:blank":
                    keep_alive_page = page
                    break
            if not keep_alive_page:
                print("[Orchestrator] Opening keep-alive page (about:blank)...")
                keep_alive_page = await context.new_page()
                await keep_alive_page.goto("about:blank")
                
            # Batch size of 4
            batch_size = 4
            for i in range(0, len(remaining_prompts), batch_size):
                batch = remaining_prompts[i:i+batch_size]
                print(f"\n==========================================")
                print(f"STARTING BATCH {i//batch_size + 1} ({len(batch)} prompts)")
                print(f"==========================================")
                
                pages_list = []
                pages_map = {}
                
                # 1. Initialize tabs, select deep research, type and send prompts
                for item in batch:
                    page = await run_prompt_tab(context, item)
                    pages_list.append((page, item["id"], item["name"], item["slug"]))
                    await asyncio.sleep(8)  # Stagger launch to prevent overlap
                    
                # 2. Wait 30 seconds (as requested by Wayne)
                print("\n[Orchestrator] Waiting 30 seconds before triggering Start Research...")
                await asyncio.sleep(30)
                
                # 3. Click start research on each page
                for page, idx, name, slug in pages_list:
                    await start_research_on_tab(page, idx, name)
                    await asyncio.sleep(5)  # 5s stagger between starting research
                    
                # 4. Monitor batch completion
                pages_map = {name: (page, idx, slug) for page, idx, name, slug in pages_list}
                await monitor_batch(pages_map)
                
                print(f"\nBatch {i//batch_size + 1} complete.")
                await asyncio.sleep(10) # Stagger between batches
    finally:
        print("[Orchestrator] Terminating Chrome...")
        proc.terminate()
        proc.wait()
        if os.path.exists(link_path):
            print(f"[Orchestrator] Removing directory junction {link_path}...")
            subprocess.run(f'rmdir "{link_path}"', shell=True)

if __name__ == "__main__":
    asyncio.run(main())
