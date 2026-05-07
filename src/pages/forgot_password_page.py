"""Page object for the forgot password page."""

from playwright.sync_api import Page, expect


class ForgotPasswordPage:
    """Page Object Model for the Forgot Password Page."""

    def __init__(self, page: Page):
        # Locators
        self.page = page
        self.email_input = page.get_by_role("textbox", name="Email")
        self.continue_button = page.get_by_role("button", name="Continue", exact=True)
        self.go_back_button = page.get_by_role("button", name="Go Back")
        self.header = page.get_by_role("heading", name="Reset Password")
        self.reset_password_message = page.get_by_text(
            "We'll send you a link to reset your password."
        )

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def enter_email(self, email: str) -> None:
        """Enter the email into the input field."""
        self.email_input.clear()
        self.email_input.fill(email)

    def click_continue(self) -> None:
        """Click the continue button to attempt password reset."""
        self.continue_button.click()

    def click_go_back(self) -> None:
        """Click the go back button to navigate back to the previous page."""
        self.go_back_button.click()

    def assert_go_back_navigates_back(self) -> None:
        """Assert that go back button is present."""
        expect(self.go_back_button).to_be_visible()
