"""Page Object Model for the Home Page."""

from playwright.sync_api import Page


class HomePage:
    """Page Object Model for the Home Page.
    Post-login landing page
    """

    def __init__(self, page: Page):
        # Locators
        self.page = page

    def wait_load_state(self) -> None:
        """Wait for the home page to load completely."""
        self.page.wait_for_load_state("networkidle", timeout=10000)
