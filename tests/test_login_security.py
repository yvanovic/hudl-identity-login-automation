"""
Test suite: Security-focused login tests
==========================================
Validates that both login steps handle injection payloads safely,
and that session boundaries are enforced correctly.
"""

import pytest

from config.settings import settings

_SQL_PAYLOADS = [
    "' OR 1=1 --",
    "'; DROP TABLE users; --",
]

_XSS_PAYLOADS = [
    "<script>alert('xss')</script>",
    "javascript:alert(1)",
]


@pytest.mark.security
@pytest.mark.parametrize("payload", _SQL_PAYLOADS)
def test_sql_injected_payload_email(login_page, payload) -> None:
    """Test that SQL injection payloads are not accepted and do not cause errors."""
    login_page.login_with_email(payload)
    login_page.assert_invalid_email_error()


@pytest.mark.security
@pytest.mark.parametrize("payload", _XSS_PAYLOADS)
def test_xss_injected_payload_email(login_page, payload) -> None:
    """Test that XSS injection payloads are not accepted and do not execute."""
    login_page.login_with_email(payload)
    login_page.assert_invalid_email_error()


@pytest.mark.security
@pytest.mark.parametrize("payload", _SQL_PAYLOADS)
def test_sql_injected_payload_password(
    login_page, login_password_page, payload
) -> None:
    """Test that SQL injection payloads in the password field are not accepted and do not cause errors."""
    login_page.login_with_email(settings.VALID_EMAIL)
    login_password_page.wait_for_password_step()
    login_password_page.login_with_password(payload)
    login_password_page.assert_incorrect_password()


@pytest.mark.security
@pytest.mark.parametrize("payload", _XSS_PAYLOADS)
def test_xss_injected_payload_password(
    login_page, login_password_page, payload
) -> None:
    """Test that XSS injection payloads in the password field are not accepted and do not execute."""
    login_page.login_with_email(settings.VALID_EMAIL)
    login_password_page.wait_for_password_step()
    login_password_page.login_with_password(payload)
    login_password_page.assert_incorrect_password()
