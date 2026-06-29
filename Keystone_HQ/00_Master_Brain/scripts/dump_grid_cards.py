import asyncio
from playwright.async_api import async_playwright

async def main():
    try:
        with open(r"C:\Users\Curtis\AppData\Local\Google\Chrome\User Data\DevToolsActivePort", "r") as f:
            lines = f.read().splitlines()
        port = lines[0]
        path = lines[1]
        ws_url = f"ws://127.0.0.1:{port}{path}"
    except Exception as e:
        print(f"[-] Error: {e}")
        return

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url)
        context = browser.contexts[0]
        page = context.pages[0]
        for p_ in context.pages:
            if "labs.google/fx/tools/flow/project" in p_.url:
                page = p_
                break
                
        print(f"[+] Connected to page: {page.url}")
        
        # If in edit detail view, click the back button or navigate to project URL
        if "/edit/" in page.url:
            print("[+] In edit view. Navigating back to project root...")
            project_url = page.url.split("/edit/")[0]
            await page.goto(project_url)
            await page.wait_for_timeout(3000)
            print(f"[+] Navigated to: {page.url}")
            
        # Find all draggable cards
        cards = await page.locator("[aria-roledescription='draggable']").all()
        print(f"[+] Found {len(cards)} cards:")
        for idx, card in enumerate(cards):
            text = await card.inner_text()
            # Find links
            links = await card.locator("a").all()
            link_urls = [await l.get_attribute("href") for l in links]
            print(f"  Card {idx}: text='{text.strip().replace(chr(10), ' | ')}' urls={link_urls}")

if __name__ == "__main__":
    asyncio.run(main())
