"""Page object for the create account page."""

import email

from playwright.sync_api import Page, expect


class CreateAccountPage:
    """Page Object Model for the Create Account Page."""

    def __init__(self, page: Page):
        # Locators
        self.page = page
        self.first_name_input = page.get_by_role("textbox", name="First name")
        self.last_name_input = page.get_by_role("textbox", name="Last name")
        self.email_input = page.get_by_role("textbox", name="Email*")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)
        self.error_message_invalid_email = page.get_by_text("Enter a valid email.")
        self.error_message_empty = page.get_by_text("Please enter your email")
        self.error_message_empty_first_name = page.get_by_text("Enter a first name.")
        self.error_message_empty_last_name = page.get_by_text("Enter a last name.")
        self.google_button = page.get_by_role("button", name="Continue with Google")
        self.facebook_button = page.get_by_role("button", name="Continue with Facebook")
        self.apple_button = page.get_by_role("button", name="Continue with Apple")

    def enter_name(self, first_name: str, last_name: str) -> None:
        """Enter the first and last name into the input fields."""
        self.first_name_input.clear()
        self.first_name_input.fill(first_name)
        self.last_name_input.clear()
        self.last_name_input.fill(last_name)
        self.email_input.clear()
        self.email_input.fill(email)

    def click_continue(self) -> None:
        """Click the continue button to proceed with account creation."""
        self.continue_button.click()

    def assert_first_name_required(self) -> None:
        """Assert that an error message is shown when first name is not provided."""
        expect(self.error_message_empty_first_name).to_be_visible()

    def assert_last_name_required(self) -> None:
        """Assert that an error message is shown when last name is not provided."""
        expect(self.error_message_empty_last_name).to_be_visible()

    def assert_email_required(self) -> None:
        """Assert that an error message is shown when email is not provided."""
        expect(self.error_message_empty).to_be_visible()

    def assert_invalid_email_error(self) -> None:
        """Assert that an error message is shown when an invalid email is provided."""
        expect(self.error_message_invalid_email).to_be_visible()

    def wait_for_create_account_step(self) -> None:
        """Wait for the create account inputs to be visible."""
        self.first_name_input.wait_for(state="visible")

    def assert_oauth_buttons_visible(self) -> None:
        """Assert that the OAuth login buttons are visible on the page."""
        expect(self.google_button).to_be_visible()
        expect(self.facebook_button).to_be_visible()
        expect(self.apple_button).to_be_visible()
