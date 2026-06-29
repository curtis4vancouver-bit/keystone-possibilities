import asyncio
from playwright.async_api import async_playwright

async def main():
    active_port_file = r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort"
    with open(active_port_file, "r") as f:
        lines = f.read().splitlines()
    port = lines[0].strip()
    ws_path = lines[1].strip()
    ws_url = f"ws://127.0.0.1:{port}{ws_path}"
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        print("Connected!")
        for context in browser.contexts:
            for page in context.pages:
                print(f"Page: {page.url}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
