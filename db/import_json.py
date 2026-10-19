"""Скрипт импорта данных из JSON-файлов в базу данных SQLite (ПР7)."""

import json
from db.database import get_connection

EQUIPMENT_FILE = "data/equipment.json"
EMPLOYEES_FILE = "data/employees.json"
OPERATIONS_FILE = "data/operations.json"


def load_json(filename: str) -> list:
    """Загрузить данные из JSON-файла с кодировкой UTF-8."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn) -> None:
    """Очистить таблицы перед импортом в порядке учета внешних ключей."""
    conn.execute("DELETE FROM operations;")
    conn.execute("DELETE FROM employees;")
    conn.execute("DELETE FROM equipment;")


def import_equipment(conn) -> None:
    """Импортировать записи оборудования в таблицу equipment."""
    equipment = load_json(EQUIPMENT_FILE)
    conn.executemany(
        """
        INSERT INTO equipment (
            id,
            name,
            category,
            model,
            serial_number,
            location,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item["id"],
                item["name"],
                item["category"],
                item["model"],
                item["serial_number"],
                item["location"],
                item.get("status", "в эксплуатации"),
            )
            for item in equipment
        ],
    )


def import_employees(conn) -> None:
    """Импортировать записи сотрудников в таблицу employees."""
    employees = load_json(EMPLOYEES_FILE)
    conn.executemany(
        """
        INSERT INTO employees (
            id,
            name,
            department,
            email
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                emp["id"],
                emp["name"],
                emp["department"],
                emp["email"],
            )
            for emp in employees
        ],
    )


def import_operations(conn) -> None:
    """Импортировать записи операций в таблицу operations."""
    operations = load_json(OPERATIONS_FILE)
    conn.executemany(
        """
        INSERT INTO operations (
            id,
            equipment_id,
            employee_id,
            operation_type,
            date,
            note,
            is_completed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                op["id"],
                op["equipment_id"],
                op.get("employee_id"),
                op["operation_type"],
                op["date"],
                op.get("note", ""),
                int(bool(op.get("is_completed", False))),
            )
            for op in operations
        ],
    )


def main() -> None:
    """Точка входа скрипта переноса данных в базу SQLite."""
    conn = get_connection()
    try:
        clear_tables(conn)
        import_equipment(conn)
        import_employees(conn)
        import_operations(conn)
        conn.commit()
        print("Импорт данных из JSON в SQLite успешно завершен.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
