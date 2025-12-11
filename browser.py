# browser.py
import asyncio
import nest_asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 60_000

# Fix for Flask / Gunicorn event loop
nest_asyncio.apply()

async def render_page_async(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()
        try:
            await page.goto(url, timeout=BROWSER_TIMEOUT_MS)
            await page.wait_for_load_state("networkidle", timeout=BROWSER_TIMEOUT_MS)
            html = await page.content()
        except PlaywrightTimeoutError:
            raise RuntimeError(f"Page timed out: {url}")
        finally:
            await browser.close()
        return html

def render_page(url: str) -> str:
    return asyncio.run(render_page_async(url))
