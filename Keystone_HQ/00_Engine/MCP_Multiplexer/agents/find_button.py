import asyncio
from playwright.async_api import async_playwright

async def find_buttons():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = await browser.contexts[0].new_page()
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(8)
        
        print("Clicking the Pro dropdown...")
        pro_dropdown = page.get_by_text("Pro", exact=True).first
        if await pro_dropdown.is_visible():
            await pro_dropdown.click()
            print("Clicked Pro dropdown. Waiting for menu to appear...")
            await asyncio.sleep(2)
        else:
            print("Could not find 'Pro' dropdown.")
            
        print("Taking menu screenshot...")
        await page.screenshot(path="gemini_menu.png")
        print("Screenshot saved to gemini_menu.png")

        await page.close()

if __name__ == "__main__":
    asyncio.run(find_buttons())
