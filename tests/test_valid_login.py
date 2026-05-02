"""
Test cases for valid login functionality.
=======================================
Full two steps login flow with valid credentials,
ensuring successful navigation to the home page.

Requires a valid email and password to be set in the test configuration.
"""

from playwright.sync_api import Page

from config.settings import settings


class TestValidLogin:
    """Test cases for valid login functionality."""

    def test_valid_login(
        self, page: Page, login_page, login_password_page, home_page
    ) -> None:
        """Test the full login flow with valid credentials."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.VALID_PASSWORD)

        home_page.wait_load_state()
        assert (
            home_page.is_home_page()
        ), "User should be navigated to the home page after successful login."

    def test_valid_email_advances_password_page(
        self, login_page, login_password_page
    ) -> None:
        """Test valid email submission advances to password page."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
