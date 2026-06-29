import asyncio
from playwright.async_api import async_playwright

async def screenshot_all():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        pages = context.pages
        count = 0
        for page in pages:
            url = page.url
            if "gemini.google.com" in url:
                try:
                    await page.screenshot(path=f"gemini_screenshot_{count}.png", full_page=True)
                    print(f"Saved gemini_screenshot_{count}.png for {url}")
                    count += 1
                except Exception as e:
                    print(f"Error on {url}: {e}")

if __name__ == "__main__":
    asyncio.run(screenshot_all())
