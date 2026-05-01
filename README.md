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