"""
Root conftest — fixtures shared across the entire test suite.

Fixture summary
---------------
Login_email_page          LoginEmailPage — step 1, URL already open     (function)

"""

import pytest
from playwright.sync_api import Page

from src.pages.login_page import LoginPage
from src.pages.login_password_page import LoginPasswordPage

# ---------------------------------------------------------------------------
# Page Object fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(name="login_page")
def _login_page(page: Page) -> LoginPage:
    """LoginEmailPage with the Hudl login URL already open."""
    login_page = LoginPage(page)
    login_page.navigate()
    return login_page


@pytest.fixture(name="password_page")
def _password_page(page: Page) -> LoginPasswordPage:
    return LoginPasswordPage(page)
