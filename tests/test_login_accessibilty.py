"""
Test suite: Accessibility — login flow
========================================
Validates that the Hudl login flow meets core accessibility standards.
Tests:
  Keyboard navigation  — full flow operable without a mouse
"""

import re

from playwright.sync_api import expect

from config.settings import settings


class TestKeyboardNavigationEmailStep:
    """The email step must be fully operable using only the keyboard."""

    def test_keyboard_navigation_email_step(
        self, login_page, login_password_page, home_page
    ) -> None:
        """Test that the email step is fully operable using only the keyboard,
        and that it advances to the password step.
        """
        login_page.navigate()

        expect(login_page.email_input).to_be_focused()
        login_page.enter_email(settings.VALID_EMAIL)
        login_page.page.keyboard.press("Tab")
        expect(login_page.continue_button).to_be_focused()
        login_page.page.keyboard.press("Enter")

        login_password_page.wait_for_password_step()
        expect(login_password_page.password_input).to_be_focused()
        login_password_page.enter_password(settings.VALID_PASSWORD)
        login_password_page.page.keyboard.press("Tab")
        expect(login_password_page.show_password_button).to_be_focused()
        login_password_page.page.keyboard.press("Tab")
        expect(login_password_page.forgot_password_link).to_be_focused()
        login_password_page.page.keyboard.press("Tab")
        expect(login_password_page.continue_button).to_be_focused()
        login_password_page.page.keyboard.press("Enter")

        home_page.wait_load_state()
        expect(home_page.page).to_have_url(re.compile("https://fan.hudl.com"))
