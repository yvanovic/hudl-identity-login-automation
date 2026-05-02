# Hudl Login Test Suite

A **production-ready Playwright/Python test automation framework** for the Hudl login flow.

---

**Key design choices:**

---

## Test Coverage

## Prerequisites

| Tool | Minimum version |
|---|---|
| Python | 3.11 |
| pip | 23+ (bundled with Python 3.11) |

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/yvanovic/hudl-identity-login-automation.git
cd hudl-identity-login-automation
```


### Manual Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install --with-deps chromium firefox webkit
pre-commit install --install-hooks
cp .env.example .env
```

---

## Project Structure

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
pre-commit install          # only needed once
pre-commit run --all-files  # run manually against everything
```

Hooks: black, isort, flake8 (with flake8-bugbear), trailing whitespace, YAML validation, merge-conflict detection, private-key guard

---

## Reports

HTML reports land in `reports/` (git-ignored) when you run pytest with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```
```bash
open reports/report.html      # macOS
```
**Failure screenshots** are saved automatically to `reports/screenshots/<test_name>.png`
via the `pytest_runtest_makereport` hook in `conftest.py`.
