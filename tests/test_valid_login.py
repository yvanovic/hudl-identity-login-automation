"""
Test cases for valid login functionality.
=======================================
Full two step login flow with valid credentials,
ensuring successful navigation to the home page.

Requires a valid email and password to be set in the test configuration.
"""

from config.settings import settings
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.login_password_page import LoginPasswordPage


class TestValidLogin:
    """Test cases for valid login functionality."""

    def test_valid_login(self, page):
        """Test the full login flow with valid credentials."""
        login_page = LoginPage(page)
        login_page.navigate(settings.BASE_URL)
        login_page.login_with_email(settings.VALID_EMAIL)

        password_page = LoginPasswordPage(page)
        password_page.wait_for_password_step()
        password_page.login_with_password(settings.VALID_PASSWORD)

        home_page = HomePage(page)
        home_page.wait_load_state()
        assert (
            home_page.is_home_page()
        ), "User should be navigated to the home page after successful login."
