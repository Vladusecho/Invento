"""Тесты веб-представлений проекта Invento (ПР6 и ПР7)."""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "invento.settings")
django.setup()

from django.test import Client  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.urls import reverse  # noqa: E402

setup_test_environment()


def test_homepage_view():
    """Проверка доступности главной страницы."""
    client = Client()
    response = client.get(reverse("homepage:index"))
    assert response.status_code == 200
    assert "Invento" in response.content.decode("utf-8")
    assert reverse("equipment:list") in response.content.decode("utf-8")
    assert reverse("operations:list") in response.content.decode("utf-8")
    assert reverse("operations:statistics") in response.content.decode("utf-8")


def test_equipment_list_view():
    """Проверка страницы списка оборудования."""
    client = Client()
    response = client.get(reverse("equipment:list"))
    assert response.status_code == 200
    assert "equipment" in response.context
    assert "Всего единиц:" in response.content.decode("utf-8")


def test_equipment_available_view_no_params():
    """Проверка страницы поиска доступного оборудования без параметров."""
    client = Client()
    response = client.get(reverse("equipment:available"))
    assert response.status_code == 200
    assert "Поиск доступного оборудования" in response.content.decode("utf-8")
    assert response.context["search_date"] is None


def test_equipment_available_view_with_date():
    """Проверка поиска доступного оборудования с передачей даты."""
    client = Client()
    response = client.get(
        reverse("equipment:available"),
        {"date": "2026-10-15"},
    )
    assert response.status_code == 200
    assert "Доступно на 2026-10-15" in response.content.decode("utf-8")
    assert "equipment" in response.context
    assert len(response.context["equipment"]) > 0


def test_equipment_detail_view_success():
    """Проверка страницы существующего оборудования."""
    client = Client()
    response = client.get(reverse("equipment:detail", args=[1]))
    assert response.status_code == 200
    assert response.context["equipment"] is not None
    assert response.context["equipment"].id == 1


def test_equipment_detail_view_404():
    """Проверка 404 для несуществующего оборудования."""
    client = Client()
    response = client.get(reverse("equipment:detail", args=[9999]))
    assert response.status_code == 404
    assert "Оборудование не найдено" in response.content.decode("utf-8")


def test_operations_list_view():
    """Проверка страницы журнала операций."""
    client = Client()
    response = client.get(reverse("operations:list"))
    assert response.status_code == 200
    assert "operations" in response.context
    assert "Журнал операций" in response.content.decode("utf-8")


def test_operations_statistics_view():
    """Проверка страницы аналитики и статистики."""
    client = Client()
    response = client.get(reverse("operations:statistics"))
    assert response.status_code == 200
    assert "operations_by_equipment" in response.context
    assert "category_stats" in response.context
    assert "summary" in response.context
    assert "Статистика и аналитика" in response.content.decode("utf-8")


def test_operations_detail_view_success():
    """Проверка страницы существующей операции."""
    client = Client()
    response = client.get(reverse("operations:detail", args=[1]))
    assert response.status_code == 200
    assert response.context["operation"] is not None
    assert response.context["operation"].id == 1


def test_operations_detail_view_404():
    """Проверка 404 для несуществующей операции."""
    client = Client()
    response = client.get(reverse("operations:detail", args=[9999]))
    assert response.status_code == 404
    assert "Операция не найдена" in response.content.decode("utf-8")
