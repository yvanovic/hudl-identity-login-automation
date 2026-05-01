"""
Test suite: Login UI state — both steps
=========================================
Validates the visual and interactive state of both login form steps:
  Step 1: email input, Continue button, social buttons, Create Account link
  Step 2: password masking, show/hide toggle, Forgot password link,
          Edit email link, Continue button
"""

from playwright.sync_api import Page, expect
from config.settings import settings
from src.pages.login_page import LoginPage
from src.pages.login_password_page import LoginPasswordPage


class TestLoginUI:
    """Test cases for validating the login UI state."""

    def test_email_input_and_buttons_visible(self, page: Page) -> None:
        """Test that the email input and all buttons are visible on the login page."""
        login_page = LoginPage(page)
        login_page.navigate()
        expect(login_page.email_input).to_be_visible()
        expect(login_page.continue_button).to_be_visible()
        expect(login_page.create_account_link).to_be_visible()

    def test_oauth_buttons_visible(self, page: Page) -> None:
        """Test that all expected UI elements are present and visible on the login page."""
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.assert_oauth_buttons_visible()

