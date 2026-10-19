"""Представления приложения operations."""

from django.http import HttpResponse
from homepage.views import page
from models.operations import find_operation_by_id
from storage import load_employees, load_equipment, load_operations


def operations(request) -> HttpResponse:
    """Отображение списка операций."""
    equipment = load_equipment()
    employees = load_employees()
    operations_list = load_operations(equipment, employees)

    items = ""
    for op in operations_list:
        status = "завершена" if op.is_completed else "активна"
        badge = "bg-secondary" if op.is_completed else "bg-success"
        emp = op.employee.name if op.employee else "—"
        link = (
            f'<a href="/operations/{op.id}/">'
            f'{op.operation_type.capitalize()}: {op.equipment.name}</a>'
        )
        meta = (
            f'<div><span class="text-muted me-3">Дата: {op.date} | '
            f'Сотрудник: {emp}</span>'
            f'<span class="badge {badge}">{status}</span></div>'
        )
        items += (
            f'<li class="list-group-item d-flex justify-content-between '
            f'align-items-center">{link}{meta}</li>'
        )

    content = f"""
    <h1>Журнал операций</h1>
    <p class="text-muted">История перемещений, ремонтов и выдачи:</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Invento – Операции", content))


def operation_detail(request, operation_id: int) -> HttpResponse:
    """Детальная карточка операции с оборудованием."""
    equipment = load_equipment()
    employees = load_employees()
    operations_list = load_operations(equipment, employees)
    op = find_operation_by_id(operations_list, operation_id)

    if op is None:
        content = """
        <h1 class="text-danger">Операция не найдена</h1>
        <p>Операция с указанным идентификатором не найдена в системе.</p>
        <a href="/operations/" class="btn btn-outline-secondary">
            ← к списку операций
        </a>
        """
        return HttpResponse(
            page("Операция не найдена", content),
            status=404,
        )

    status = "завершена" if op.is_completed else "активна"
    badge = "bg-secondary" if op.is_completed else "bg-success"
    emp_info = (
        f"{op.employee.name} ({op.employee.department})"
        if op.employee
        else "Не назначен"
    )
    note_text = op.note if op.note else "—"

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h5 class="card-title">
                Операция №{op.id}: {op.operation_type.capitalize()}
            </h5>
            <p class="card-text">
                <strong>Оборудование:</strong>
                <a href="/equipment/{op.equipment.id}/">{op.equipment.name}</a>
                (SN: {op.equipment.serial_number})
            </p>
            <p class="card-text">
                <strong>Ответственный:</strong> {emp_info}
            </p>
            <p class="card-text">
                <strong>Дата:</strong> {op.date}
            </p>
            <p class="card-text">
                <strong>Примечание:</strong> {note_text}
            </p>
            <p class="card-text">
                <strong>Статус:</strong>
                <span class="badge {badge}">{status}</span>
            </p>
            <a href="/operations/" class="btn btn-outline-secondary">
                ← к списку операций
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Операция №{op.id}", content),
        status=200,
    )
