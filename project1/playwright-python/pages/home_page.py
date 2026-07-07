from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Page Object for Home Page.
    Contains all locators and actions for the home page.
    """

    # ── Locators ──────────────────────────────
    HEADING        = "h1"
    MORE_INFO_LINK = "a[href='/more-info']"

    def __init__(self, page: Page):
        super().__init__(page, base_url="http://localhost:8765")

    # ── Actions ───────────────────────────────
    def open(self):
        """Open home page"""
        self.navigate("")
        self.wait_for_load()
        return self

    def get_heading_text(self) -> str:
        """Get heading text"""
        return self.page.locator(self.HEADING).inner_text()

    def click_more_info(self):
        """Click the More information link"""
        self.page.click(self.MORE_INFO_LINK)
        self.wait_for_load()

    def is_heading_visible(self) -> bool:
        """Check if heading is visible"""
        return self.page.locator(self.HEADING).is_visible()
