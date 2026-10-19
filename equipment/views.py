"""Представления приложения equipment."""

from django.shortcuts import render
from models.equipment import find_equipment_by_id
from storage import load_equipment


def equipment(request):
    """Отображение списка оборудования."""
    equipment_list = load_equipment()
    context = {
        "equipment": equipment_list,
    }
    return render(
        request,
        "equipment/equipment_list.html",
        context,
    )


def equipment_detail(request, equipment_id: int):
    """Карточка отдельной единицы оборудования."""
    equipment_list = load_equipment()
    item = find_equipment_by_id(equipment_list, equipment_id)
    context = {
        "equipment": item,
    }
    return render(
        request,
        "equipment/equipment_detail.html",
        context,
        status=404 if item is None else 200,
    )
