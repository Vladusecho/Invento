"""Представления приложения homepage."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Сформировать единый каркас HTML-страницы с Bootstrap 5.3."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav bg-light p-2 mb-4 border-bottom">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/equipment/">Оборудование</a>
        <a class="nav-link" href="/operations/">Операции</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request) -> HttpResponse:
    """Главная страница приложения Invento."""
    content = """
    <h1 class="display-4">Invento</h1>
    <p class="lead">Автоматизированная система учета оборудования (АСУО).</p>
    <p>Основные разделы системы:</p>
    <a href="/equipment/" class="btn btn-primary me-2">Оборудование</a>
    <a href="/operations/" class="btn btn-secondary">Операции</a>
    """
    return HttpResponse(page("Invento – Главная", content))


def page_not_found(request, exception) -> HttpResponse:
    """Пользовательский обработчик ошибки 404."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную страницу.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
