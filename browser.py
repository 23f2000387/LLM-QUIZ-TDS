# browser.py
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 30_000  # 30 seconds

def render_page(url: str) -> str:
    """
    Launch headless Chromium, load the URL, wait for network idle,
    and return HTML content as string.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()

    try:
        # Load the page
        page.goto(url, timeout=BROWSER_TIMEOUT_MS)
        page.wait_for_load_state("networkidle")
        
        # Get the full page HTML
        html = page.content()
    except PlaywrightTimeoutError:
        raise RuntimeError(f"Page timed out while loading: {url}")
    finally:
        # Clean up
        browser.close()
        p.stop()

    return html
