# browser.py

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 30_000  # 30s

def render_page(url: str):
    """
    Launches a headless browser, loads the quiz URL,
    waits for JS to finish, and returns the page object.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()

    try:
        page.goto(url, timeout=BROWSER_TIMEOUT_MS)
        page.wait_for_load_state("networkidle")
    except PlaywrightTimeoutError:
        browser.close()
        p.stop()
        raise RuntimeError("Page timed out while loading")

    # We return (page, browser, p) so caller can close them later
    return page, browser, p
