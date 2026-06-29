import asyncio
from playwright.async_api import async_playwright

async def click_start_all():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        pages = context.pages
        for page in pages:
            url = page.url
            if "gemini.google.com" in url:
                try:
                    print(f"Checking {url}")
                    start_btn = page.locator("button:has-text('Start research')").first
                    if await start_btn.is_visible(timeout=5000):
                        print("Clicking Start research...")
                        await start_btn.click()
                        await asyncio.sleep(2)
                except Exception as e:
                    print(f"Error on {url}: {e}")

if __name__ == "__main__":
    asyncio.run(click_start_all())
