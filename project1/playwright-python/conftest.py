import pytest
from playwright.sync_api import sync_playwright, Page, BrowserContext


# ──────────────────────────────────────────────
# Browser Fixture
# ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def browser_instance():
    """
    Session-scoped: One browser for the entire test session.
    Saves time by not launching a new browser for every test.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=False for local dev (needs display)
        yield browser
        browser.close()


# ──────────────────────────────────────────────
# Context Fixture
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def context(browser_instance) -> BrowserContext:
    """
    Function-scoped: Fresh isolated context for every test.
    Each test gets clean cookies, storage, and session.
    """
    context = browser_instance.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    context.close()


# ──────────────────────────────────────────────
# Page Fixture
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def page(context) -> Page:
    """
    Function-scoped: Fresh page for every test.
    Built on top of context fixture.
    """
    page = context.new_page()
    yield page
    page.close()


# ──────────────────────────────────────────────
# Multi-Browser Fixture (for cross-browser testing)
# ──────────────────────────────────────────────
@pytest.fixture(params=["chromium", "firefox", "webkit"])
def cross_browser_page(request):
    """
    Runs each test on chromium, firefox, and webkit.
    Use this fixture for cross-browser tests.
    """
    with sync_playwright() as p:
        browser = getattr(p, request.param).launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()


# ──────────────────────────────────────────────
# Base URL Fixture
# ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8765"
