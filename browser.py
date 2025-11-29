# browser.py
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 30_000  # 30s

def render_page(url: str) -> str:
    """
    Launch headless browser, load the URL, wait for network idle,
    return page HTML as string.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()

    try:
        page.goto(url, timeout=BROWSER_TIMEOUT_MS)
        page.wait_for_load_state("networkidle")
        html = page.content()  # <-- get HTML as string
    except PlaywrightTimeoutError:
        raise RuntimeError("Page timed out while loading")
    finally:
        browser.close()
        p.stop()

    return html
