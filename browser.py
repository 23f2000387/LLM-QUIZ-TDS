# browser.py
import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 60_000  # 30 seconds

async def render_page_async(url: str) -> str:
    """
    Launch headless Chromium asynchronously, load the URL, wait for network idle,
    and return HTML content as string.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()

        try:
            # Load the page
            await page.goto(url, timeout=BROWSER_TIMEOUT_MS)
            await page.wait_for_load_state("networkidle")

            # Get the full page HTML
            html = await page.content()
        except PlaywrightTimeoutError:
            raise RuntimeError(f"Page timed out while loading: {url}")
        finally:
            await browser.close()

        return html

def render_page(url: str) -> str:
    """
    Synchronous wrapper for render_page_async so existing code can call it normally.
    """
    return asyncio.run(render_page_async(url))

