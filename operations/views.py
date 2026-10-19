"""Представления приложения operations (база данных SQLite, ПР7)."""

import sqlite3
from django.shortcuts import render
from db.database import get_connection
from models.employees import Employee
from models.equipment import Equipment
from models.operations import Operation


def operations(request):
    """Журнал операций из SQLite с соединением таблиц (JOIN)."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    operations_list = conn.execute(
        """
        SELECT
            o.id,
            o.equipment_id,
            o.employee_id,
            o.operation_type,
            o.date,
            o.note,
            o.is_completed,
            e.name AS equipment_name,
            emp.name AS employee_name
        FROM operations o
        JOIN equipment e ON o.equipment_id = e.id
        LEFT JOIN employees emp ON o.employee_id = emp.id
        ORDER BY o.date DESC, o.id DESC;
        """
    ).fetchall()
    conn.close()

    context = {
        "operations": operations_list,
    }
    return render(
        request,
        "operations/operations_list.html",
        context,
    )


def statistics(request):
    """Страница статистики учета оборудования (GROUP BY, COUNT, LEFT JOIN)."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # Статистика операций по оборудованию (LEFT JOIN, GROUP BY, COUNT)
    operations_by_equipment = conn.execute(
        """
        SELECT
            e.id AS equipment_id,
            e.name AS equipment_name,
            e.category,
            COUNT(o.id) AS operations_count
        FROM equipment e
        LEFT JOIN operations o ON e.id = o.equipment_id
        GROUP BY e.id, e.name, e.category
        ORDER BY operations_count DESC, e.name ASC;
        """
    ).fetchall()

    # Статистика распределения по категориям (GROUP BY, COUNT)
    category_stats = conn.execute(
        """
        SELECT
            category,
            COUNT(*) AS equipment_count
        FROM equipment
        GROUP BY category
        ORDER BY equipment_count DESC, category ASC;
        """
    ).fetchall()

    # Сводные агрегатные показатели (COUNT)
    summary = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM equipment) AS total_equipment,
            (SELECT COUNT(*) FROM equipment
             WHERE status = 'в эксплуатации') AS in_use_equipment,
            (SELECT COUNT(*) FROM operations) AS total_operations,
            (SELECT COUNT(*) FROM operations
             WHERE is_completed = 0) AS active_operations;
        """
    ).fetchone()

    conn.close()

    context = {
        "operations_by_equipment": operations_by_equipment,
        "category_stats": category_stats,
        "summary": summary,
    }
    return render(
        request,
        "operations/statistics.html",
        context,
    )


def operation_detail(request, operation_id: int):
    """Детальная карточка операции с объединением связанных данных."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    op_row = conn.execute(
        """
        SELECT
            o.id,
            o.equipment_id,
            o.employee_id,
            o.operation_type,
            o.date,
            o.note,
            o.is_completed,
            e.name AS equipment_name,
            e.serial_number AS equipment_serial_number,
            emp.name AS employee_name,
            emp.department AS employee_department
        FROM operations o
        JOIN equipment e ON o.equipment_id = e.id
        LEFT JOIN employees emp ON o.employee_id = emp.id
        WHERE o.id = ?;
        """,
        [operation_id],
    ).fetchone()
    conn.close()

    if op_row is None:
        return render(
            request,
            "operations/operation_detail.html",
            {"operation": None},
            status=404,
        )

    eq = Equipment(
        equipment_id=op_row["equipment_id"],
        name=op_row["equipment_name"],
        category="",
        model="",
        serial_number=op_row["equipment_serial_number"],
        location="",
    )
    emp = (
        Employee(
            employee_id=op_row["employee_id"],
            name=op_row["employee_name"],
            department=op_row["employee_department"],
            email="",
        )
        if op_row["employee_id"]
        else None
    )
    op = Operation(
        operation_id=op_row["id"],
        equipment=eq,
        employee=emp,
        operation_type=op_row["operation_type"],
        date=op_row["date"],
        note=op_row["note"],
    )
    op.is_completed = bool(op_row["is_completed"])

    context = {
        "operation": op,
    }
    return render(
        request,
        "operations/operation_detail.html",
        context,
        status=200,
    )
