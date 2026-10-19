
"""Configuration and environment validation."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_google_api_key() -> str:
    """Return the configured Google API key."""
    api_key = os.getenv("GOOGLE_API_KEY", "").strip()

    if not api_key or api_key == "your_google_api_key_here":
        raise RuntimeError(
            "GOOGLE_API_KEY is missing. Configure it in your .env file."
        )

    return api_key


def validate_google_api_key() -> None:
    """Ensure the Google API key is configured."""
    get_google_api_key()
