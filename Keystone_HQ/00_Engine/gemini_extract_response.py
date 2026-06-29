import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            
            page = None
            for pg in context.pages:
                if "gemini" in pg.url:
                    page = pg
                    break
            
            if not page:
                print("Gemini page not found.")
                return
            
            text = await page.evaluate("document.body.innerText")
            with open("gemini_transcript.txt", "w", encoding="utf-8") as f:
                f.write(text)
                    
            await browser.disconnect()
        except Exception as e:
            print("Error:", e)

asyncio.run(main())
