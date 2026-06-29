import asyncio
from playwright.async_api import async_playwright

async def test_thinking():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = await browser.contexts[0].new_page()
        await page.goto("https://gemini.google.com/app", wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(8)
        
        print("Clicking dropdown...")
        dropdown = page.locator("button:has-text('Pro'), button:has-text('Fast'), button:has-text('Thinking')").first
        if await dropdown.is_visible():
            await dropdown.click()
            await asyncio.sleep(2)
            
            print("Selecting Thinking...")
            thinking_opt = page.locator("div:has-text('Thinking')").nth(1)
            try:
                # Get the most specific element for Thinking
                thinking_opt = page.get_by_text("Thinking", exact=True).first
                if await thinking_opt.is_visible():
                    await thinking_opt.click()
                    print("Clicked Thinking mode.")
                else:
                    print("Could not find Thinking option.")
            except Exception as e:
                print(f"Error clicking Thinking: {e}")
        else:
            print("Could not find model dropdown.")
            
        await asyncio.sleep(2)
        print("Taking final screenshot...")
        await page.screenshot(path="gemini_thinking.png")
        await page.close()

if __name__ == "__main__":
    asyncio.run(test_thinking())
