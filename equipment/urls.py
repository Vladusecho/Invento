"""Маршруты приложения equipment."""

from django.urls import path
from . import views

app_name = "equipment"

urlpatterns = [
    path("", views.equipment, name="list"),
    path(
        "<int:equipment_id>/",
        views.equipment_detail,
        name="detail",
    ),
]
