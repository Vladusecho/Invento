"""Представления приложения homepage."""

from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:
    """Главная страница приложения Invento."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception=None) -> HttpResponse:
    """Пользовательский обработчик ошибки 404."""
    return render(request, "404.html", status=404)
