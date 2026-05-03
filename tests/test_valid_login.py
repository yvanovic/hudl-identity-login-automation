"""
Test cases for valid login functionality.
=======================================
Full two steps login flow with valid credentials,
ensuring successful navigation to the home page.

Requires a valid email and password to be set in the test configuration.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config.settings import settings


class TestValidLogin:
    """Test cases for valid login functionality."""

    @pytest.mark.smoke
    def test_valid_login(
        self, page: Page, login_page, login_password_page, home_page
    ) -> None:
        """Test the full login flow with valid credentials."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.VALID_PASSWORD)

        home_page.wait_load_state()
        expect(home_page.page).to_have_url(re.compile(".*/home"))

    def test_valid_email_advances_password_page(
        self, login_page, login_password_page
    ) -> None:
        """Test valid email submission advances to password page."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()

    @pytest.mark.smoke
    def test_valid_login_from_account_page(
        self, login_page, login_password_page, create_account_page, home_page
    ) -> None:
        """Test valid login from account page."""
        login_page.navigate()
        login_page.click_create_account_link()

        create_account_page.wait_for_create_account_step()
        create_account_page.click_login()

        login_page.wait_for_email_login_step()
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.VALID_PASSWORD)

        home_page.wait_load_state()

    @pytest.mark.smoke
    def test_valid_email_case_insensitive(
        self, login_page, login_password_page, home_page
    ) -> None:
        """Test valid email submission case insensitive."""
        login_page.login_with_email(settings.VALID_EMAIL.upper())
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.VALID_PASSWORD)

        home_page.wait_load_state()
        expect(home_page.page).to_have_url(re.compile(".*/home"))
