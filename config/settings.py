"""
Settings loaded from environment variables.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# load .env file if it exists, but don't override existing environment variables
# The .env file is expected to be in the project root, hence the use of parent.parent
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)
# override=False ensures that if an environment variable is already set (e.g. via CI secrets), it won't be overwritten by the .env file


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


# Instantiate settings to be used across the test suite
settings = Settings()
