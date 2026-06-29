import asyncio
import os
import sys
from playwright.async_api import async_playwright

async def main():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
    port = lines[0].strip()
    ws_path = lines[1].strip()
    ws_url = f"ws://127.0.0.1:{port}{ws_path}"
    
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp(ws_url)
            print("Connected!")
            context = browser.contexts[0]
            pages = context.pages
            print(f"Total open pages: {len(pages)}")
            for i, page in enumerate(pages):
                print(f"Page {i}: {page.url} ({await page.title()})")
                if "gemini.google.com" in page.url:
                    screenshot_path = f"c:\\Users\Curtis\\New folder\\construction-website\\Keystone_HQ\\00_Master_Brain\\scratch\\gemini_page_{i}.png"
                    await page.screenshot(path=screenshot_path)
                    print(f"Saved screenshot for page {i} to {screenshot_path}")
            await browser.close()
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
