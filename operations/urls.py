"""Маршруты приложения operations."""

from django.urls import path
from . import views

app_name = "operations"

urlpatterns = [
    path("", views.operations, name="list"),
    path(
        "<int:operation_id>/",
        views.operation_detail,
        name="detail",
    ),
]
