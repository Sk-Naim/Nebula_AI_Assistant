import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        profile = os.path.expanduser("~/Library/Application Support/Google/Chrome")
        browser = await p.chromium.launch_persistent_context(
            profile,
            headless=False,
            no_viewport=True,
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        print("Navigating...")
        await page.goto("https://www.google.com")
        print("Navigated. URL:", page.url)
        await asyncio.sleep(2)
        await browser.close()

asyncio.run(main())
