from playwright.sync_api import Page


class BasePage:
    """
    Base class for all page objects.
    Every page class inherits from this.
    """

    def __init__(self, page: Page, base_url: str = "http://localhost:8765"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = ""):
        """Navigate to a path relative to base URL"""
        self.page.goto(f"{self.base_url}/{path}")

    def get_title(self) -> str:
        """Get current page title"""
        return self.page.title()

    def get_url(self) -> str:
        """Get current page URL"""
        return self.page.url

    def wait_for_load(self):
        """Wait for page to fully load"""
        self.page.wait_for_load_state("networkidle")

    def take_screenshot(self, name: str = "screenshot"):
        """Take a screenshot"""
        self.page.screenshot(path=f"reports/{name}.png")
