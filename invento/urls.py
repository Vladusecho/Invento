"""Корневая маршрутизация проекта Invento."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("equipment/", include("equipment.urls")),
    path("operations/", include("operations.urls")),
]

handler404 = "homepage.views.page_not_found"
