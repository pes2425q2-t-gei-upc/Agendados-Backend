from django.urls import path

from apps.locations import views

urlpatterns = [
    path("", views.get_all_locations, name="get_all_locations"),
    path("regions", views.get_all_regions, name="get_all_regions"),
    path("towns", views.get_all_towns, name="get_all_towns"),
]
