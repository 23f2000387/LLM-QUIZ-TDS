# browser.py

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

BROWSER_TIMEOUT_MS = 30_000  # 30s

def render_page(url: str) -> str:
    """
    Launches a headless browser, loads the quiz URL,
    waits for JS to finish, and returns the page HTML as a string.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context()
    page = ctx.new_page()

    try:
        page.goto(url, timeout=BROWSER_TIMEOUT_MS)
        page.wait_for_load_state("networkidle")
        html = page.content()  # return HTML string
    except PlaywrightTimeoutError:
        browser.close()
        p.stop()
        raise RuntimeError("Page timed out while loading")
    finally:
        # Clean up browser resources
        browser.close()
        p.stop()

    return html
