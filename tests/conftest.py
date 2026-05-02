"""
Root conftest — fixtures shared across the entire test suite.

Fixture summary
---------------
Login_email_page          LoginEmailPage — step 1, URL already open     (function)

"""

import pytest
from playwright.sync_api import Page

from config.settings import settings
from src.pages.create_account_page import CreateAccountPage
from src.pages.forgot_password_page import ForgotPasswordPage
from src.pages.home_page import HomePage
from src.pages.login_page import LoginPage
from src.pages.login_password_page import LoginPasswordPage

# ---------------------------------------------------------------------------
# Page Object fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(name="login_page")
def _login_page(page: Page) -> LoginPage:
    """LoginEmailPage with the Hudl login URL already open."""
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    login_page = LoginPage(page)
    login_page.navigate()
    return login_page


@pytest.fixture(name="login_password_page")
def _login_password_page(page: Page) -> LoginPasswordPage:
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    return LoginPasswordPage(page)


@pytest.fixture(name="home_page")
def _home_page(page: Page) -> HomePage:
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    return HomePage(page)


@pytest.fixture(name="forgot_password_page")
def _forgot_password_page(page: Page) -> ForgotPasswordPage:
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    return ForgotPasswordPage(page)


@pytest.fixture(name="create_account_page")
def _create_account_page(page: Page) -> CreateAccountPage:
    page.set_default_timeout(settings.DEFAULT_TIMEOUT)
    return CreateAccountPage(page)


# ---------------------------------------------------------------------------
# Auto-screenshot on failure
# ---------------------------------------------------------------------------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Automatically captures a screenshot when a test fails"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page: Page = item.funcargs.get("page", None)
        if page:
            screenshot_path = f"reports/screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
