import pytest
from pages.home_page import HomePage


class TestHomePage:
    """
    Test cases for Home Page.
    All tests run in parallel using pytest-xdist (-n auto)
    """

    # ── Test 1: Title ─────────────────────────
    def test_page_title(self, page):
        """Verify page title contains 'Example'"""
        home = HomePage(page)
        home.open()

        title = home.get_title()
        assert "Example" in title, f"Expected 'Example' in title but got: {title}"

    # ── Test 2: Heading Visible ────────────────
    def test_heading_visible(self, page):
        """Verify h1 heading is visible on page"""
        home = HomePage(page)
        home.open()

        assert home.is_heading_visible(), "Heading h1 is not visible on the page"

    # ── Test 3: Heading Text ───────────────────
    def test_heading_text(self, page):
        """Verify heading text content"""
        home = HomePage(page)
        home.open()

        heading = home.get_heading_text()
        assert heading != "", "Heading text should not be empty"
        print(f"\nHeading found: {heading}")

    # ── Test 4: URL ────────────────────────────
    def test_page_url(self, page):
        """Verify correct URL is loaded"""
        home = HomePage(page)
        home.open()

        url = home.get_url()
        assert "localhost:8765" in url, f"Unexpected URL: {url}"

    # ── Test 5: More Info Link ─────────────────
    def test_more_info_link(self, page):
        """Verify More Information link navigates correctly"""
        home = HomePage(page)
        home.open()
        home.click_more_info()

        url = home.get_url()
        assert "more-info" in url, f"Expected more-info page but got: {url}"
