"""
Test suite: Invalid login scenarios
====================================
All negative tests — wrong credentials, unregistered email,
malformed email, empty fields, whitespace.
None of these tests require a real valid account.
"""

# import pytest
from playwright.async_api import Page

from config.settings import settings
from src.pages.login_page import LoginPage


class TestInvalidEmailsRejections:
    """Errors rejected by invalid emails at the step 1"""

    def test_empty_email_shows_errors(self, page: Page) -> None:
        """Test that submitting an empty email shows the appropriate error message."""

        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login_with_email(settings.EMPTY_STRING)
        login_page.assert_email_required()

    def test_malformed_email_shows_errors(self, page: Page) -> None:
        """Test that submitting a malformed email shows the appropriate error message."""

        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login_with_email(settings.MALFORMED_EMAIL)
        login_page.assert_invalid_email_error()
