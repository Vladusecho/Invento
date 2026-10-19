"""Представления приложения operations."""

from django.shortcuts import render
from models.operations import find_operation_by_id
from storage import load_employees, load_equipment, load_operations


def operations(request):
    """Отображение списка операций."""
    equipment = load_equipment()
    employees = load_employees()
    operations_list = load_operations(equipment, employees)
    context = {
        "operations": operations_list,
    }
    return render(
        request,
        "operations/operations_list.html",
        context,
    )


def operation_detail(request, operation_id: int):
    """Детальная карточка операции с оборудованием."""
    equipment = load_equipment()
    employees = load_employees()
    operations_list = load_operations(equipment, employees)
    op = find_operation_by_id(operations_list, operation_id)
    context = {
        "operation": op,
    }
    return render(
        request,
        "operations/operation_detail.html",
        context,
        status=404 if op is None else 200,
    )
