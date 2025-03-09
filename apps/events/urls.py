from django.urls import path
from apps.events.views import event_views, category_views

urlpatterns = [
    path("events", event_views.get_all_events, name="get_all_events"),
    path("categories", category_views.get_all_categories, name="get_all_categories"),
]
