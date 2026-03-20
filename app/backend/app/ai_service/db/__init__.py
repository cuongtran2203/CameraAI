"""Database helpers and connection management.

This package is intentionally left minimal as a starting point.
Add database initialization and connection helpers here as needed.
"""

from .session import get_db

__all__ = ["get_db"]
