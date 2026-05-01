"""
Test suite: Invalid login scenarios
====================================
All negative tests — wrong credentials, unregistered email,
malformed email, empty fields, whitespace.
None of these tests require a real valid account.
"""

from config.settings import settings


class TestInvalidEmailsRejections:
    """Errors rejected by invalid emails at the step 1"""

    def test_empty_email_shows_errors(self, login_page) -> None:
        """
        Test that submitting an empty email shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.EMPTY_STRING)
        login_page.assert_email_required()

    def test_malformed_email_shows_errors(self, login_page) -> None:
        """
        Test that submitting a malformed email shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.MALFORMED_EMAIL)
        login_page.assert_invalid_email_error()

    def test_unregistered_email(self, login_page, password_page) -> None:
        """Test that submitting an unregistered email shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.UNREGISTERED_EMAIL)
        password_page.wait_for_password_step()
        password_page.enter_password(settings.INVALID_PASSWORD)
        password_page.click_continue()
        password_page.assert_incorrect_email_password()

    def test_incorrect_password(self, login_page, password_page) -> None:
        """Test that submitting an incorrect password shows the appropriate
        error message.
        """
        login_page.login_with_email(settings.VALID_EMAIL)
        password_page.wait_for_password_step()
        password_page.login_with_password(settings.INVALID_PASSWORD)
        password_page.assert_incorrect_password()
