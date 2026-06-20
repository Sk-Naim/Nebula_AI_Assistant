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
        print("Navigating to swiggy...")
        try:
            await page.goto("https://www.swiggy.com/city/bardhaman/order-online", timeout=15000)
            print("Navigated. URL:", page.url)
        except Exception as e:
            print("Error:", e)
        await asyncio.sleep(2)
        await browser.close()

asyncio.run(main())
