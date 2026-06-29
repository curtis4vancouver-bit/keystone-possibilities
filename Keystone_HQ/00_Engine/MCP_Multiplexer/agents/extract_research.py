import asyncio
import os
import time
from playwright.async_api import async_playwright

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Deep_Research_Results")
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)

async def extract_all():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        pages = context.pages
        count = 0
        for page in pages:
            url = page.url
            if "gemini.google.com" in url:
                try:
                    print(f"Checking {url}")
                    messages = await page.locator("message-content").all()
                    if messages:
                        result_text = await messages[-1].inner_text()
                        
                        # Get prompt to use as title/filename
                        user_messages = await page.locator("user-query").all()
                        prompt_text = "Unknown_Prompt"
                        if user_messages:
                            prompt_text = await user_messages[0].inner_text()
                            
                        safe_name = "".join([c for c in prompt_text[:30] if c.isalnum() or c in (' ', '_')]).rstrip()
                        filepath = os.path.join(RESULTS_DIR, f"Extracted_{safe_name}_{int(time.time())}.md")
                        
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(f"# Prompt:\n{prompt_text}\n\n## Response:\n{result_text}")
                            
                        print(f"Saved research to {filepath}")
                        count += 1
                except Exception as e:
                    print(f"Error extracting from {url}: {e}")
        print(f"Successfully extracted {count} research results.")

if __name__ == "__main__":
    asyncio.run(extract_all())
