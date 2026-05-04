## Hudl Login Flow Test Suite

A **production-ready Playwright/Python test automation framework** for the Hudl login flow.

---

## Table of Contents

- [Known Issues](#known-issues)
- [Architecture Overview](#architecture-overview)
- [Test Coverage](#test-coverage)
- [Quick Start](#quick-start)
- [CI/CD](#cicd)
- [Browser Compatibility](#browser-compatibility)
- [Code Quality](#code-quality)
- [Reports](#reports)
- [Additional Resources](#additional-resources)

---

## Known Issues

See **[KNOWN_ISSUES.md](./KNOWN_ISSUES.md)** for:

- Failing tests and root causes
- Browser-specific limitations
- Assumptions about test environment

---

**Key design choices:**

- **`Page` injected directly** — `LoginPage(page: Page)`. No base class, no inheritance chain, no hidden behavior.
- **Page objects own nothing** — they receive the `Page` instance, expose locators as properties, and provide action/state methods.
- **Fixtures build and deliver** — `conftest.py` constructs page objects and ensures the correct navigation state before each test.
- **Environment-driven config** — no hard-coded URLs or credentials anywhere.

---

## Architecture Overview

### Page Object Model Pattern

This project follows a **lightweight Page Object Model (POM)** without inheritance:

```python
# Each page is instantiated with the Playwright Page object
login_page = LoginPage(page)

# Pages expose locators as properties
login_page.email_input  # Locatorpy
login_page.continue_button  # Locator

# Pages provide action methods
login_page.enter_email("user@example.com")
login_page.click_continue()

# Pages provide assertion methods
login_page.assert_invalid_email_error()
```

### Test Execution Flow

1. **Setup** — `conftest.py` fixtures instantiate page objects
2. **Navigation** — Fixtures handle initial navigation (e.g., `login_page.navigate()`)
3. **Action** — Tests call page object methods (enter data, click buttons)
4. **Assertion** — Tests use Playwright's `expect()` for assertions
5. **Cleanup** — Playwright handles automatic browser teardown

### Auto-Screenshot on Failure

When a test fails, `pytest_runtest_makereport` hook in `conftest.py` automatically captures a screenshot to `reports/screenshots/{test_name}.png`.

---

## Test Coverage

### Markers

| Marker     | Purpose                         | Run when                              |
| ---------- | ------------------------------- | ------------------------------------- |
| `smoke`    | Critical-path, must always pass | Push, Pull-request, On Manual trigger |
| `security` | SQL Injection, XSS payload      | On manual trigger                     |
| `ui`       | Visual/interaction state        | On Manual trigger                     |

### Test Modules

| Module                        | Scenarios                                                                            | Markers               |
| ----------------------------- | ------------------------------------------------------------------------------------ | --------------------- |
| `test_valid_login.py`         | Valid credentials, email advancement, full login flow, password step transition      | `smoke`, `regression` |
| `test_invalid_login.py`       | Invalid email, missing email, unregistered email, wrong password, error handling     | `smoke`               |
| `test_login_security.py`      | XSS payload injection, SQL injection attempts, malformed inputs, security edge cases | `security`            |
| `test_login_ui.py`            | OAuth buttons visibility, form layout, button states, input validation messages      | `ui`                  |
| `test_login_accessibility.py` | ARIA labels, keyboard navigation, screen reader compatibility, contrast ratios       | `regression`          |

**~31 test cases** total.

---

## Environment Variables Reference

All configuration is driven by environment variables loaded from `.env` file:

| Variable           | Default                    | Purpose                                          |
| ------------------ | -------------------------- | ------------------------------------------------ |
| `BASE_URL`         | `https://www.hudl.com`     | Application base URL                             |
| `LOGIN_URL`        | `{BASE_URL}/login`         | Login page URL                                   |
| `VALID_EMAIL`      | _(required)_               | Valid test account email for login tests         |
| `VALID_PASSWORD`   | _(required)_               | Valid test account password                      |
| `DEFAULT_TIMEOUT`  | `15000` (ms)               | Playwright element and page timeout              |
| `INVALID_EMAIL`    | `notauser_xyz@example.com` | Test data: unregistered email for negative tests |
| `INVALID_PASSWORD` | `wrongpassword123`         | Test data: wrong password for negative tests     |
| `MALFORMED_EMAIL`  | `notanemail@gmail.`        | Test data: invalid email format                  |

**Note:** `VALID_EMAIL` and `VALID_PASSWORD` must be configured in `.env` before running tests. These should be valid credentials for a test account you control.

---

## Prerequisites

| Tool   | Minimum version                |
| ------ | ------------------------------ |
| Python | 3.11                           |
| pip    | 23+ (bundled with Python 3.11) |
| Git    | Any recent version             |

---

## Quick Start

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yvanovic/hudl-identity-login-automation.git
   cd hudl-identity-login-automation
   ```

2. **Create virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
    pip install -r requirements.txt

   # Installing Playwright browser
    playwright install --with-deps
   ```

4. **Install pre-commit into this repo's git hooks**
   ```bash
   # downloads all the tools listed in .pre-commit-config.yaml upfront
   pre-commit install --install-hooks
   ```
5. **Configure credentials:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your credentials:
   - **Never commit `.env`** — it contains secrets
   - Add `.env` to `.gitignore` (already configured)
   - `.env` is loaded automatically by `config/settings.py`
     - `VALID_EMAIL`: Your valid email to use
     - `VALID_PASSWORD`: Your valid password
     - `BASE_URL`: The base url target for this test suite

   ```bash
   cp .env.example .env
   # And edit .env with your actual credentials

   # Loads environment variables from a .env file into the current shell session.
   export $(cat .env | xargs)
   ```

6. **Run the tests :**

   ```bash
   # Full suite (all tests, chromium browser)
   pytest

   # By marker (see Test Coverage section)
   pytest -m smoke          # Fast, critical-path tests
   pytest -m security       # Security tests (injection, XSS)
   pytest -m ui             # UI/visual state tests

   # Specific browser
   pytest --browser=firefox
   pytest --browser=webkit

   # Headed mode (watch the browser execute)
   HEADLESS=false pytest -m smoke
   pytest --headed -m smoke

   # Single test file
   pytest tests/test_valid_login.py

   # Single test function
   pytest tests/test_login_security.py::TestLoginSecurity::test_xss_injected_payload_password

   # By test name pattern
   pytest -k "test_valid_login"
   pytest -k "password"  # All tests with 'password' in name

   # With HTML report and screenshots
   pytest --html=reports/report.html --self-contained-html

   # Custom timeout
   DEFAULT_TIMEOUT=20000 pytest tests/test_valid_login.py

   # Verbose output with timing
   pytest -v --tb=short
   ```

---

## CI/CD

`.github/workflows/ci.yaml` runs on every push and pull request:

1. **Test matrix** — Smoke tests across Chromium, Firefox, WebKit in parallel.

How it behaves across every trigger

| Trigger                                | Tests run     | Why                                   |
| -------------------------------------- | ------------- | ------------------------------------- |
| `push` to main/develop                 | Smoke only    | Fast feedback, not blocking your flow |
| `pull_request` to main                 | Smoke only    | Gate check before merge               |
| `schedule`                             | All tests     | Gate check before merge               |
| `workflow_dispatch`, marker blank      | All tests     | Manual full run on demand             |
| `workflow_dispatch`, marker = security | Security only | Targeted manual run                   |

---

### Triggering a manual run

From the GitHub Actions UI, trigger `workflow_dispatch` with a `marker` input:
`smoke` | `security` | `ui`

---

### GitHub Secrets (for CI)

| Secret           | Purpose                                                          |
| ---------------- | ---------------------------------------------------------------- |
| `VALID_EMAIL`    | The test account email. Override if the demo password changes    |
| `VALID_PASSWORD` | The test account password. Override if the demo password changes |

Secrets are stored in GitHub repo settings and injected at runtime. These are **not visible** in workflow logs or artifacts.

---

## Browser Compatibility

Tests run across **three major browser engines** via Playwright:

| Browser  | Version | Status | CI  |
| -------- | ------- | ------ | --- |
| Chromium | Latest  | Tested | ✅  |
| Firefox  | Latest  | Tested | ✅  |
| WebKit   | Latest  | Tested | ✅  |

Default browser is **Chromium**. Use `--browser` flag to test other engines:

```bash
pytest --browser=firefox
pytest --browser=webkit
```

CI runs all three browsers in parallel for every commit (see CI/CD section).

---

## Code Quality

### Linting & formatting

```bash
black .          # format code
isort .          # sort imports
flake8 .         # lint
```

Config lives in `setup.cfg` (`[flake8]` and `[isort]` sections). Line length is 100 for both.

### Pre-commit hooks

Runs automatically on `git commit`:

```bash
pre-commit run --all-files  # run manually against everything
```

Hooks: black, isort, flake8 (with flake8-bugbear), trailing whitespace, YAML validation, merge-conflict detection, private-key guard

---

## Reports

HTML reports land in `reports/` (git-ignored) when you run pytest with HTML report

```bash
pytest --html=reports/report.html --self-contained-html
open reports/report.html
```

**Report contents:**

- Test results (passed/failed/skipped)
- Execution time per test
- Failure details and assertions
- System information (browser, OS, Python version)
- Linked failure screenshots

**Failure screenshots** are saved automatically to `reports/screenshots/{test_name}.png` via the `pytest_runtest_makereport` hook in `conftest.py`. When a test fails, the screenshot is embedded in the HTML report.

**CI artifacts:** GitHub Actions uploads reports as artifacts (2-day retention) for easy inspection.

---

## Additional Resources

- **[Playwright Documentation](https://playwright.dev)** — Official docs, API reference
- **[Playwright Python API](https://playwright.dev/python)** — Python-specific guides
- **[pytest Documentation](https://docs.pytest.org)** — pytest markers, fixtures, plugins
- **[Page Object Model Pattern](https://playwright.dev/python/docs/pom)** — Best practices
