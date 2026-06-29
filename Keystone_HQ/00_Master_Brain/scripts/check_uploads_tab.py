import asyncio
from playwright.async_api import async_playwright

async def main():
    try:
        with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
            lines = f.read().splitlines()
        port = lines[0]
        path = lines[1]
        ws_url = f"ws://127.0.0.1:{port}{path}"
        print(f"[+] Found WebSocket URL: {ws_url}")
    except Exception as e:
        print(f"[-] Error reading DevToolsActivePort: {e}")
        return

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        page = None
        for p_ in context.pages:
            if "labs.google/fx/tools/flow/project" in p_.url:
                page = p_
                break
                
        if not page:
            print("[-] Flow page not found")
            return
            
        print(f"[+] Connected to page: {page.url}")
        
        # Click Escape to clear dialogs
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(500)
        
        # Click + Create
        create_picker = page.get_by_role("button", name="Create").first
        if not await create_picker.is_visible():
            create_picker = page.locator("button[aria-haspopup='dialog']").first
        await create_picker.click(force=True)
        await page.wait_for_timeout(1000)
        
        # Click "Uploads" tab
        uploads_tab = page.get_by_role("tab", name="Uploads").first
        if await uploads_tab.is_visible():
            await uploads_tab.click(force=True)
            await page.wait_for_timeout(1000)
            print("[+] Clicked Uploads tab")
            
            # Print elements inside the dialog
            items = await page.locator("mat-dialog-container [role='gridcell'] or mat-dialog-container button").all()
            print(f"[+] Found {len(items)} items in dialog:")
            for idx, it in enumerate(items[:20]):
                try:
                    text = await it.inner_text()
                    print(f"  {idx}: {text.strip().replace('\n', ' | ')}")
                except Exception:
                    pass
        else:
            print("[-] Uploads tab not found")
            
        await page.keyboard.press("Escape")

if __name__ == "__main__":
    asyncio.run(main())
