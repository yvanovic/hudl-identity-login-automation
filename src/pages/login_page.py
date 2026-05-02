"""Page Object Model for the Login Page."""

from playwright.sync_api import Page, expect

from config.settings import settings


class LoginPage:
    """Page Object Model for the Login Page."""

    URL = settings.LOGIN_URL

    def __init__(self, page: Page):
        # Locators
        self.page = page

        self.email_input = page.get_by_role("textbox", name="Email*")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)
        self.create_account_link = page.get_by_role("link", name="Create Account")
        self.google_button = page.get_by_role("button", name="Continue with Google")
        self.facebook_button = page.get_by_role("button", name="Continue with Facebook")
        self.apple_button = page.get_by_role("button", name="Continue with Apple")
        self.error_message_invalid_email = page.get_by_text("Enter a valid email.")
        self.error_message_empty = page.get_by_text("Please enter your email address")

    def navigate(self) -> None:
        """Navigate to the login page."""
        self.page.goto(self.URL, wait_until="domcontentloaded")
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
        expect(self.error_message_empty).to_be_visible()

    def assert_invalid_email_error(self) -> None:
        """Assert that an error message is shown when an invalid email is provided."""
        expect(self.error_message_invalid_email).to_be_visible()

    def assert_oauth_buttons_visible(self) -> None:
        """Assert that the OAuth login buttons are visible on the page."""
        expect(self.google_button).to_be_visible()
        expect(self.facebook_button).to_be_visible()
        expect(self.apple_button).to_be_visible()

    def wait_for_email_login_step(self) -> None:
        """Wait for the password input to be visible."""
        self.email_input.wait_for(state="visible")

    def click_create_account_link(self) -> None:
        """Click the create account link button."""
        self.create_account_link.click()
