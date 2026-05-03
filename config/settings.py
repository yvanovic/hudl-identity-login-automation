"""
Settings loaded from environment variables.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)


class Settings:
    """Configuration settings for the test suite."""

    # Application
    BASE_URL = os.getenv("BASE_URL", "https://www.hudl.com")
    LOGIN_URL = BASE_URL + "/login"

    # Hudl test credentials
    VALID_EMAIL = os.getenv("VALID_EMAIL")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD")

    # Negative test values
    UNREGISTERED_EMAIL: str = os.getenv("INVALID_EMAIL", "notauser_xyz@example.com")
    INVALID_PASSWORD: str = os.getenv("INVALID_PASSWORD", "wrongpassword123")
    MALFORMED_EMAIL: str = os.getenv("MALFORMED_EMAIL", "notanemail@gmail.")
    EMPTY_STRING: str = ""

    # Playwright
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "15000"))


settings = Settings()
