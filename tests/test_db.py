"""Тесты слоя базы данных SQLite (ПР7)."""

import sqlite3
from db.database import DB_PATH, get_connection
from db.import_json import (
    clear_tables,
    import_employees,
    import_equipment,
    import_operations,
)


def test_db_connection_and_foreign_keys():
    """Проверка подключения к SQLite и включения PRAGMA foreign_keys."""
    conn = get_connection()
    fk_status = conn.execute("PRAGMA foreign_keys;").fetchone()[0]
    conn.close()
    assert fk_status == 1


def test_db_tables_exist():
    """Проверка наличия всех требуемых таблиц в invento.sqlite."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    table_names = {row[0] for row in rows}
    conn.close()
    assert {"equipment", "employees", "operations"}.issubset(table_names)


def test_import_json_data():
    """Проверка повторного корректного импорта данных из JSON."""
    conn = get_connection()
    clear_tables(conn)
    import_equipment(conn)
    import_employees(conn)
    import_operations(conn)
    conn.commit()

    eq_count = conn.execute("SELECT COUNT(*) FROM equipment;").fetchone()[0]
    emp_count = conn.execute("SELECT COUNT(*) FROM employees;").fetchone()[0]
    op_count = conn.execute("SELECT COUNT(*) FROM operations;").fetchone()[0]
    conn.close()

    assert eq_count > 0
    assert emp_count > 0
    assert op_count > 0
