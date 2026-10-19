"""Пакет для работы с базой данных SQLite."""

from .database import DB_PATH, get_connection

__all__ = ["DB_PATH", "get_connection"]
