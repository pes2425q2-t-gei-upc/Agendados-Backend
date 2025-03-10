from django.urls import path
from apps.events.views import event_views, category_views, userevent_views

urlpatterns = [
    path("", event_views.get_all_events, name="get_all_events"),
    path("/categories", category_views.get_all_categories, name="get_all_categories"),
    path("/<int:event_id>/favorites", userevent_views.add_to_favorites, name="add_to_favorites"),
]
