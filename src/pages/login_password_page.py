"""
Page Object Model for the Login Password Page.
Second step of the login flow, where users enter their password after providing their email.
"""

from playwright.sync_api import Page, expect


class LoginPasswordPage:
    """Page Object Model for the Login Password Page."""

    def __init__(self, page: Page):
        # Locators
        self.page = page
        self.password_input = page.get_by_role("textbox", name="Password")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)
        self.forgot_password_link = page.get_by_role("link", name="Forgot Password?")
        self.edit_email_link = page.get_by_role("link", name="Edit Email")
        self.show_password_button = page.get_by_role("button", name="Show password")
        self.hide_password_button = page.get_by_role("button", name="Hide password")
        self.error_message_incorrect_password = page.get_by_text(
            "Your email or password is incorrect. Try again."
        )
        self.error_message_incorrect_email_password = page.get_by_text(
            "Incorrect username or password."
        )

    def enter_password(self, password: str) -> None:
        """Enter the password into the input field."""
        self.password_input.clear()
        self.password_input.fill(password)

    def click_continue(self) -> None:
        """Click the continue button to attempt login."""
        self.continue_button.click()

    def login_with_password(self, password: str) -> None:
        """Perform the login action using password."""
        self.enter_password(password)
        self.click_continue()

    def click_forgot_password(self) -> None:
        """Click the forgot password link to navigate to the password reset page."""
        self.forgot_password_link.click()

    def click_edit_email(self) -> None:
        """Click the edit email link to navigate back to the email input page."""
        self.edit_email_link.click()

    def click_show_password(self) -> None:
        """
        Click the show password button to reveal the password.
        """
        self.show_password_button.click()

    def click_hide_password(self) -> None:
        """
        Click the hide password button to conceal the password.
        """
        self.hide_password_button.click()

    def assert_incorrect_password(self) -> None:
        """
        Assert that an error message is shown when an
        incorrect password is entered.
        """
        expect(self.error_message_incorrect_password).to_be_visible()

    def assert_incorrect_email_password(self) -> None:
        """
        Assert that an error message is shown when an incorrect
        unregistered email is entered.
        """
        expect(self.error_message_incorrect_email_password).to_be_visible()

    def wait_for_password_step(self) -> None:
        """Wait for the password input to be visible."""
        self.password_input.wait_for(state="visible")
