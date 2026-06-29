import asyncio
from playwright.async_api import async_playwright

async def find_left_side():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = await browser.contexts[0].new_page()
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(8)
        
        print("Clicking the + button...")
        plus_btn = page.locator("button[aria-label*='upload'], button[aria-label*='Add'], mat-icon:has-text('add')").first
        try:
            await plus_btn.click(timeout=5000)
            await asyncio.sleep(2)
            await page.screenshot(path="gemini_plus.png")
            print("Saved gemini_plus.png")
            await page.keyboard.press("Escape")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"No + button found: {e}")

        print("Clicking Tools...")
        tools = page.get_by_text("Tools", exact=False).first
        try:
            await tools.click(timeout=5000)
            await asyncio.sleep(2)
            await page.screenshot(path="gemini_tools.png")
            print("Saved gemini_tools.png")
            await page.keyboard.press("Escape")
        except Exception as e:
            print(f"No Tools found: {e}")
            
        print("Looking for any deep research toggles...")
        locators = await page.locator("[role='switch'], button").all()
        for l in locators:
            aria = await l.get_attribute("aria-label")
            text = await l.inner_text()
            if aria and "deep" in aria.lower():
                print(f"Found deep in aria: {aria}")
            if text and "deep" in text.lower():
                print(f"Found deep in text: {text}")

        await page.close()

if __name__ == "__main__":
    asyncio.run(find_left_side())
