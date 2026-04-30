"""
Settings loaded from environment variables.
"""

import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=False)


class Settings:
    """Configuration settings for the test suite."""

    BASE_URL = os.getenv("BASE_URL")
    VALID_EMAIL = os.getenv("VALID_EMAIL")
    VALID_PASSWORD = os.getenv("VALID_PASSWORD")


settings = Settings()
