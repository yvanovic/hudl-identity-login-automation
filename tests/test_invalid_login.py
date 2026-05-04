"""
Test suite: Invalid login scenarios
====================================
All negative tests — wrong credentials, unregistered email,
malformed email, empty fields, whitespace.
None of these tests require a real valid account.
"""

import pytest

from config.settings import settings


class TestInvalidEmailsRejections:
    """Errors rejected by invalid emails at the step 1"""

    @pytest.mark.negative
    @pytest.mark.smoke
    def test_empty_email_shows_errors(self, login_page) -> None:
        """
        Test that submitting an empty email shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.EMPTY_STRING)
        login_page.assert_email_required()

    @pytest.mark.negative
    def test_malformed_email_shows_errors(self, login_page) -> None:
        """
        Test that submitting a malformed email shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.MALFORMED_EMAIL)
        login_page.assert_invalid_email_error()

    @pytest.mark.negative
    def test_unregistered_email(self, login_page, login_password_page) -> None:
        """Test that submitting an unregistered email shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.UNREGISTERED_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.enter_password(settings.INVALID_PASSWORD)
        login_password_page.click_continue()
        login_password_page.assert_incorrect_email_password()

    @pytest.mark.negative
    @pytest.mark.smoke
    def test_incorrect_password(self, login_page, login_password_page) -> None:
        """Test that submitting an incorrect password shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.INVALID_PASSWORD)
        login_password_page.assert_incorrect_password()

    @pytest.mark.negative
    @pytest.mark.smoke
    def test_empty_password(self, login_page, login_password_page) -> None:
        """Test that submitting an empty password shows the appropriate error message."""
        login_page.login_with_email(settings.VALID_EMAIL)
        login_password_page.wait_for_password_step()
        login_password_page.login_with_password(settings.EMPTY_STRING)
        login_password_page.assert_empty_password_error()
