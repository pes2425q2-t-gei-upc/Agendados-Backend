from django.urls import path

from apps.private_rooms import views

urlpatterns = [
    path("", views.create_private_room, name="create_private_room"),
]