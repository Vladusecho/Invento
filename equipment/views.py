"""Представления приложения equipment."""

from django.http import HttpResponse
from homepage.views import page
from models.equipment import find_equipment_by_id
from storage import load_equipment


def equipment(request) -> HttpResponse:
    """Отображение списка оборудования."""
    items = ""
    for item in load_equipment():
        if item.is_in_use():
            badge = "bg-success"
        elif item.is_broken():
            badge = "bg-danger"
        else:
            badge = "bg-secondary"

        link = f'<a href="/equipment/{item.id}/">{item.name}</a>'
        desc = f"{item.category}, SN: {item.serial_number}"
        span = f'<span class="badge {badge}">{item.status}</span>'
        items += (
            f'<li class="list-group-item d-flex justify-content-between '
            f'align-items-center"><div>{link} – {desc}</div>{span}</li>'
        )

    content = f"""
    <h1>Оборудование</h1>
    <p class="text-muted">Перечень материально-технических ценностей:</p>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Invento – Оборудование", content))


def equipment_detail(request, equipment_id: int) -> HttpResponse:
    """Карточка отдельной единицы оборудования."""
    equipment_list = load_equipment()
    item = find_equipment_by_id(equipment_list, equipment_id)

    if item is None:
        content = """
        <h1 class="text-danger">Оборудование не найдено</h1>
        <p>Единица оборудования с указанным ID отсутствует в системе.</p>
        <a href="/equipment/" class="btn btn-outline-secondary">
            ← к списку оборудования
        </a>
        """
        return HttpResponse(
            page("Оборудование не найдено", content),
            status=404,
        )

    if item.is_in_use():
        badge = "bg-success"
    elif item.is_broken():
        badge = "bg-danger"
    else:
        badge = "bg-secondary"

    content = f"""
    <div class="card shadow-sm">
        <div class="card-body">
            <h5 class="card-title">{item.name}</h5>
            <p class="card-text">
                <strong>Категория:</strong> {item.category}
            </p>
            <p class="card-text"><strong>Модель:</strong> {item.model}</p>

            <p class="card-text">
                <strong>Серийный номер:</strong> {item.serial_number}
            </p>
            <p class="card-text"><strong>Локация:</strong> {item.location}</p>
            <p class="card-text">
                <strong>Состояние:</strong>
                <span class="badge {badge}">{item.status}</span>
            </p>
            <a href="/equipment/" class="btn btn-outline-secondary">
                ← к списку оборудования
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(item.name, content),
        status=200,
    )
