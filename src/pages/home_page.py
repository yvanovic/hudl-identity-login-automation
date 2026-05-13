"""Page Object Model for the Home Page."""

from playwright.sync_api import Page, expect


class HomePage:
    """Page Object Model for the Home Page.
    Post-login landing page
    """

    def __init__(self, page: Page):
        # Locators
        self.page = page

        self.search_input = page.get_by_placeholder("Search Hudl Fan")
        self.top_videos = page.locator("[data-qa-id='TopVideos-header-text']")

    def wait_load_state(self) -> None:
        """Wait for the home page to load completely."""
        # networkidle is used to ensure all network requests have completed,
        # which is important for a post-login page that may load user-specific data.
        self.page.wait_for_load_state("networkidle", timeout=10000)

    def assert_search_input_visible(self) -> None:
        """Assert that the search input is visible on the home page."""
        expect(self.search_input).to_be_visible()

    def assert_top_videos(self) -> None:
        """Assert that the top videos page is visible on the home page."""
        expect(self.top_videos).to_be_visible()
