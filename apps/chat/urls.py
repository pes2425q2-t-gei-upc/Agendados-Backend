from django.urls import path
from apps.chat import views

urlpatterns = [
    path("events_where_user_messaged", views.get_events_by_user_has_messaged, name="get_events_by_user_has_messaged"),
]