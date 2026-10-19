"""Маршруты приложения equipment."""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.equipment, name="equipment_list"),
    path(
        "<int:equipment_id>/",
        views.equipment_detail,
        name="equipment_detail",
    ),
]
