import pytest
from pages.home_page import HomePage


class TestCrossBrowser:
    """
    Cross-browser test cases.
    Uses cross_browser_page fixture from conftest.py
    Runs each test on chromium, firefox, and webkit automatically.
    """

    def test_title_on_all_browsers(self, cross_browser_page):
        """Verify title on chromium, firefox, and webkit"""
        home = HomePage(cross_browser_page)
        home.open()

        title = home.get_title()
        assert "Example" in title

    def test_heading_on_all_browsers(self, cross_browser_page):
        """Verify heading visible on all browsers"""
        home = HomePage(cross_browser_page)
        home.open()

        assert home.is_heading_visible()
