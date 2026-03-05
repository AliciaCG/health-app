"""
Application configuration.
Settings are read from environment variables with sensible defaults.
"""

import os


class Settings:
    APP_NAME: str = "Health Records API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Database
    DB_PATH: str = os.getenv(
        "DB_PATH", os.path.join(os.path.dirname(__file__), "..", "records.db")
    )

    # CORS — tighten allowed_origins in production
    CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "*").split(",")

    # Validation constants
    VALID_HEALTH: frozenset[str] = frozenset({"athletic", "good", "average", "poor"})
    VALID_SEX: frozenset[str] = frozenset({"male", "female", "unknown"})
    MIN_AGE: int = 0
    MAX_AGE: int = 150


settings = Settings()
