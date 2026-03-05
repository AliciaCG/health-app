"""
Database layer — connection management and schema initialisation.
Uses sqlite3 with row_factory for dict-like row access.
"""

import sqlite3
from contextlib import contextmanager
from app.config import settings


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")   # better concurrent read performance
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def get_db():
    """Context manager that yields a connection and always closes it."""
    conn = _get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they do not exist. Safe to call on every startup."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id         INTEGER  PRIMARY KEY AUTOINCREMENT,
                firstname  TEXT     NOT NULL,
                lastname   TEXT     NOT NULL,
                age        INTEGER  NOT NULL CHECK(age >= 0 AND age <= 150),
                sex        TEXT     NOT NULL,
                health     TEXT     NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
