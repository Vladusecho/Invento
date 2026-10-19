"""Модуль подключения к базе данных SQLite."""

import sqlite3

DB_PATH = "data/invento.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать подключение к БД с проверкой внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
