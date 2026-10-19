"""Представления приложения equipment (база данных SQLite, ПР7)."""

import sqlite3
from django.shortcuts import render
from db.database import get_connection
from models.equipment import Equipment


def equipment(request):
    """Отображение списка оборудования из базы данных SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    equipment_list = conn.execute(
        """
        SELECT
            id,
            name,
            category,
            model,
            serial_number,
            location,
            status
        FROM equipment
        ORDER BY id;
        """
    ).fetchall()
    conn.close()

    context = {
        "equipment": equipment_list,
    }
    return render(
        request,
        "equipment/equipment_list.html",
        context,
    )


def available_equipment(request):
    """Поиск доступного оборудования (свободного от активного ремонта)."""
    search_date = request.GET.get("date")
    equipment_list = []

    if search_date:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        equipment_list = conn.execute(
            """
            SELECT
                e.id,
                e.name,
                e.category,
                e.model,
                e.serial_number,
                e.location,
                e.status
            FROM equipment e
            WHERE e.id NOT IN (
                SELECT o.equipment_id
                FROM operations o
                WHERE o.operation_type = 'ремонт'
                  AND o.is_completed = 0
                  AND o.date <= ?
            )
            ORDER BY e.name;
            """,
            [search_date],
        ).fetchall()
        conn.close()

    context = {
        "equipment": equipment_list,
        "search_date": search_date,
    }
    return render(
        request,
        "equipment/available.html",
        context,
    )


def equipment_detail(request, equipment_id: int):
    """Карточка отдельной единицы оборудования из базы данных SQLite."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        SELECT
            id,
            name,
            category,
            model,
            serial_number,
            location,
            status
        FROM equipment
        WHERE id = ?;
        """,
        [equipment_id],
    ).fetchone()
    conn.close()

    item = Equipment.from_data(dict(row)) if row is not None else None

    context = {
        "equipment": item,
    }
    return render(
        request,
        "equipment/equipment_detail.html",
        context,
        status=404 if item is None else 200,
    )
