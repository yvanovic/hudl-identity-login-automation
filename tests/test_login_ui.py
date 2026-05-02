"""
Test suite: Login UI state — both steps
=========================================
Validates the visual and interactive state of both login form steps:
  Step 1: email input, Continue button, social buttons, Create Account link
  Step 2: password masking, show/hide toggle, Forgot password link,
          Edit email link, Continue button
"""

import re

from playwright.sync_api import Page, expect

from config.settings import settings


class TestLoginUI:
    """Test cases for validating the login UI state."""

    def test_email_input_and_buttons_visible(self, login_page) -> None:
        """Test that the email input and all buttons are visible on the login page."""
        expect(login_page.email_input).to_be_visible()
        expect(login_page.continue_button).to_be_visible()
        expect(login_page.create_account_link).to_be_visible()

    def test_oauth_buttons_visible(self, login_page) -> None:
        """Test that all expected UI elements are present and visible on the login page."""
        login_page.assert_oauth_buttons_visible()


class TestLoginPasswordPage:
    """Test cases for validating the login UI state on Password page."""

    def test_password_input_visible(self, login_page, login_password_page) -> None:
        """Test that the password input is visible on the password
        page after entering a valid email.
        """
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        expect(login_password_page.password_input).to_be_visible()
        expect(login_password_page.email_input).to_have_value(settings.VALID_EMAIL)

    def test_continue_button_visible(self, login_page, login_password_page) -> None:
        """Test that the continue button is visible on the password page."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        expect(login_password_page.continue_button).to_be_visible()

    def test_password_input_masked_by_default(
        self, login_page, login_password_page
    ) -> None:
        """Test that the password input is masked by default on the password page."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        expect(login_password_page.password_input).to_have_attribute("type", "password")

    def test_show_hide_password_toggle(self, login_page, login_password_page) -> None:
        """Test the show/hide password functionality on the password step."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()

        # Verify that the password input is of type "password" by default
        expect(login_password_page.password_input).to_have_attribute("type", "password")

        # Click the show/hide password button to show the password
        login_password_page.click_show_password()
        expect(login_password_page.password_input).to_have_attribute("type", "text")

        # Click the show/hide password button again to hide the password
        login_password_page.click_hide_password()
        expect(login_password_page.password_input).to_have_attribute("type", "password")

    def test_forgot_password_links_visible(
        self, login_page, login_password_page
    ) -> None:
        """Test that the forgot password link are visible on the password page."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.wait_for_password_step()
        expect(login_password_page.forgot_password_link).to_be_visible()

    def test_edit_email_link_visible(self, login_page, login_password_page) -> None:
        """Test that the edit email link is visible on the password page."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        expect(login_password_page.edit_email_link).to_be_visible()

    def test_create_account_link_visible(self, login_page) -> None:
        """Test that the create account link is visible on the login page."""
        expect(login_page.create_account_link).to_be_visible()


class TestEditEmailLinkNavigation:
    """Test cases for validating the Edit Email link functionality."""

    def test_edit_email_link_navigates_back_to_email_step(
        self, login_page, login_password_page
    ) -> None:
        """Test that clicking the edit email link navigates back to the email input step."""
        login_page.login_with_email(settings.VALID_EMAIL)

        login_password_page.wait_for_password_step()
        login_password_page.click_edit_email()
        expect(login_page.email_input).to_be_visible()
        login_page.assert_oauth_buttons_visible()
        expect(login_page.create_account_link).to_be_visible()


class TestForgotPasswordLinkNavigation:
    """Test cases for validating the Forgot Password link functionality."""

    def test_forgot_password_link_navigates_to_reset_page(
        self, page: Page, login_page, login_password_page, forgot_password_page
    ) -> None:
        """Test that clicking the forgot password link navigates to the password reset page."""
        login_page.login_with_email(settings.VALID_EMAIL)

        login_password_page.wait_for_password_step()
        login_password_page.click_forgot_password()

        expect(forgot_password_page.page).to_have_url(re.compile(".*/reset-password"))
        expect(forgot_password_page.header).to_be_visible()
        expect(forgot_password_page.reset_password_message).to_be_visible()
        expect(forgot_password_page.email_input).to_have_value(settings.VALID_EMAIL)

    def test_go_back_button_navigates_back_to_password_step(
        self, page: Page, login_page, login_password_page, forgot_password_page
    ) -> None:
        """Test that clicking the go back button on the forgot
        password page navigates back to the password step.
        """
        login_page.login_with_email(settings.VALID_EMAIL)

        login_password_page.wait_for_password_step()
        login_password_page.click_forgot_password()

        forgot_password_page.click_go_back()
        expect(login_password_page.wait_for_password_step())


class TestCreateAccountLinkNavigation:
    """Test cases for validating the Create Account link functionality."""

    def test_create_account_link_navigates_to_create_account_page(
        self, login_page, create_account_page
    ) -> None:
        """Test that clicking the create account link navigates to the create account page."""
        login_page.create_account_link.click()
        create_account_page.wait_for_create_account_step()
        expect(create_account_page.page).to_have_url(re.compile(".*/signup"))
        expect(create_account_page.first_name_input).to_be_visible()
        expect(create_account_page.last_name_input).to_be_visible()
        expect(create_account_page.email_input).to_be_visible()
        expect(create_account_page.continue_button).to_be_visible()
        create_account_page.assert_oauth_buttons_visible()
