"""Маршруты приложения equipment."""

from django.urls import path
from . import views

app_name = "equipment"

urlpatterns = [
    path("", views.equipment, name="list"),
    path("available/", views.available_equipment, name="available"),
    path("<int:equipment_id>/", views.equipment_detail, name="detail"),
]
