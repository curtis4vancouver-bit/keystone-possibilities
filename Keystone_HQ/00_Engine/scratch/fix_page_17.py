import asyncio
from playwright.async_api import async_playwright
import os

def get_websocket_url():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
    port = lines[0].strip()
    ws_path = lines[1].strip()
    return f"ws://127.0.0.1:{port}{ws_path}"

async def main():
    ws_url = get_websocket_url()
    print(f"Connecting to Chrome over CDP on {ws_url}...")
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        pages = context.pages
        
        target_page = None
        for page in pages:
            if "gemini.google.com/app" in page.url and len(page.url.split("/")) <= 4:
                target_page = page
                break
                
        if not target_page:
            print("Page 17 not found. Current pages:")
            for p_idx, page in enumerate(pages):
                print(f"{p_idx}: {page.url}")
            await browser.disconnect()
            return
            
        print(f"Found target page: {target_page.url}")
        await target_page.bring_to_front()
        await asyncio.sleep(2)
        
        # Select Deep Research if not selected
        deselect_btn = target_page.locator("button:has-text('Deselect Deep research'), button:has-text('Deselect Deep Research'), button[aria-label='Deselect Deep research']")
        if await deselect_btn.count() > 0:
            print("Deep Research already selected.")
        else:
            print("Deep Research not selected. Selecting it...")
            plus_btn = target_page.locator("button[aria-label='Upload & tools'], button:has-text('Upload & tools'), button[aria-label='Add files or tools'], button[aria-label='Upload']").first
            if await plus_btn.is_visible():
                await plus_btn.click()
                await asyncio.sleep(2)
                dr_menu_item = target_page.locator("menuitemcheckbox:has-text('Deep research'), menuitemcheckbox:has-text('Deep Research'), [role='menuitemcheckbox']:has-text('Deep research'), [role='menuitemcheckbox']:has-text('Deep Research')").first
                await dr_menu_item.click()
                await asyncio.sleep(2)
                
        # Click textbox, enter prompt
        input_box = target_page.locator("div[role='textbox'], rich-textarea, textarea").first
        await input_box.click()
        await asyncio.sleep(1)
        
        prompt = (
            "Activate Deep Research. Thoroughly analyze: DaVinci Resolve Studio (v18/v19) timeline assembly Python scripting API. "
            "Focus on programmatically adding color-coded markers, generating/importing SRT subtitle files directly into dedicated subtitle tracks, "
            "and implementing automated audio ducking between A1 (speech) and A2 (music). "
            "Context: This research is for an autonomous AI agent system (Keystone Sovereign) that manages a construction business, YouTube channels, and health content empire. "
            "Domain area: KITCHEN UPGRADES. Provide actionable, specific technical details, code examples where applicable, "
            "current best practices as of May 2026, and any tools, libraries, or services mentioned. Include specific version numbers, URLs, and configuration details."
        )
        await target_page.keyboard.insert_text(prompt)
        await target_page.keyboard.press("Space")
        await asyncio.sleep(2)
        
        # Click send
        send_btn = target_page.locator("button[aria-label='Send message'], button:has-text('Send message')").first
        if await send_btn.is_visible() and await send_btn.is_enabled():
            await send_btn.click()
            print("Clicked Send button.")
        else:
            await target_page.keyboard.press("Enter")
            print("Pressed Enter.")
            
        await asyncio.sleep(8)
        
        # Wait and click Start Research
        start_btn = target_page.locator("button:has-text('Start research'), button:has-text('Start Research')").first
        for _ in range(45):
            if await start_btn.is_visible() and await start_btn.is_enabled():
                await start_btn.click()
                print("Clicked Start Research!")
                break
            await asyncio.sleep(2)
            
        await browser.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
