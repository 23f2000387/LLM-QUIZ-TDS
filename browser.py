# browser.py
import asyncio
import nest_asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 60_000

# Fix for Flask / Gunicorn event loop
nest_asyncio.apply()

async def render_page_async(url: str) -> tuple[str, str]:
    """
    Launch headless Chromium, load URL, and return:
    1. Full page HTML
    2. Submit URL extracted from JS-generated .origin element
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()

        try:
            await page.goto(url, timeout=BROWSER_TIMEOUT_MS)
            await page.wait_for_load_state("networkidle", timeout=BROWSER_TIMEOUT_MS)

            # Extract the dynamically generated submit URL
            submit_url = await page.evaluate("""
                () => {
                    const el = document.querySelector('.origin');
                    if (!el) return null;
                    return el.textContent + '/submit';
                }
            """)

            if not submit_url:
                raise RuntimeError("Submit URL could not be found in the page")

            # Get full HTML (for question extraction)
            html = await page.content()

        except PlaywrightTimeoutError:
            raise RuntimeError(f"Page timed out: {url}")
        finally:
            await browser.close()

        return html, submit_url

def render_page(url: str) -> tuple[str, str]:
    """
    Synchronous wrapper for Flask/Gunicorn
    Returns (html, submit_url)
    """
    return asyncio.run(render_page_async(url))
