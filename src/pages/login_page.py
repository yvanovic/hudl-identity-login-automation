"""Page Object Model for the Login Page."""

from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object Model for the Login Page."""

    def __init__(self, page: Page):
        # Locators
        self.page = page

        self.email_input = page.get_by_role("textbox", name="Email*")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)
        self.create_account_link = page.get_by_role("link", name="Create Account")
        self.google_button = page.get_by_role("button", name="Continue with Google")
        self.facebook_button = page.get_by_role("button", name="Continue with Facebook")
        self.apple_button = page.get_by_role("button", name="Continue with Apple")
        self.error_message = page.get_by_text("Enter a valid email.")

    def navigate(self, base_url: str) -> None:
        """Navigate to the login page."""
        self.page.goto(f"{base_url}/login")
        self.email_input.wait_for(state="visible")

    def enter_email(self, email: str) -> None:
        """Enter the email address into the input field."""
        self.email_input.clear()
        self.email_input.fill(email)

    def click_continue(self) -> None:
        """Click the continue button to proceed with login."""
        self.continue_button.click()

    def login_with_email(self, email: str) -> None:
        """Perform the login action using email."""
        self.enter_email(email)
        self.click_continue()

    def assert_email_required(self) -> None:
        """Assert that an error message is shown when email is not provided."""
        expect(self.email_input).to_be_visible()

    def assert_oauth_buttons_visible(self) -> None:
        """Assert that the OAuth login buttons are visible on the page."""
        expect(self.google_button).to_be_visible()
        expect(self.facebook_button).to_be_visible()
        expect(self.apple_button).to_be_visible()
