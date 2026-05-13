"""
Test suite: Mobile and responsive device login tests
=====================================================
Validates login flow works correctly on various device types and screen sizes.
Uses Playwright's device emulation for iOS, Android, and tablet viewports.
"""

import re

import pytest
from playwright.sync_api import Page, expect

from config.settings import settings
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.login_password_page import LoginPasswordPage


class TestMobileLoginFlow:
    """Test login flow on mobile and tablet devices."""

    @pytest.mark.mobile
    def test_valid_login_on_mobile_device(self, mobile_page: Page) -> None:
        """Test valid login flow works correctly on mobile device."""
        page = mobile_page

        # Setup page objects
        login_page = LoginPage(mobile_page)
        login_password_page = LoginPasswordPage(page)
        home_page = HomePage(page)

        # Perform login
        login_page.navigate()

        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.VALID_PASSWORD)

        # Verify successful login
        home_page.wait_load_state()
        expect(home_page.page).to_have_url(re.compile("https://fan.hudl.com"))


class TestMobileInvalidLoginFlow:
    """Test invalid login flow on mobile and tablet devices."""

    @pytest.mark.mobile
    def test_invalid_email_on_mobile_device(self, mobile_page: Page) -> None:
        """Test invalid email error handling on mobile device."""
        page = mobile_page

        login_page = LoginPage(page)

        # Attempt login with invalid email
        login_page.navigate()
        login_page.login_with_email(settings.MALFORMED_EMAIL)

        # Verify error message is shown
        expect(login_page.error_message_invalid_email).to_be_visible()

    @pytest.mark.mobile
    def test_empty_email_on_mobile_device(self, mobile_page: Page) -> None:
        """Test empty email error handling on mobile device."""
        page = mobile_page
        login_page = LoginPage(page)

        # Attempt login with empty email
        login_page.navigate()
        login_page.login_with_email(settings.EMPTY_STRING)

        # Verify error message is shown
        expect(login_page.error_message_empty).to_be_visible()


class TestMobileOAuthButtons:
    """Test that OAuth login buttons are visible and accessible on mobile devices."""

    @pytest.mark.mobile
    def test_oauth_buttons_visible_on_mobile(self, mobile_page: Page) -> None:
        """Test OAuth buttons are visible and accessible on mobile device."""
        page = mobile_page
        login_page = LoginPage(page)

        # Navigate to login page
        login_page.navigate()

        # Verify OAuth buttons are visible on mobile
        login_page.assert_oauth_buttons_visible()
