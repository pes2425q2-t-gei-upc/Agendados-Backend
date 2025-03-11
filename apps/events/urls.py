from django.urls import path
from apps.events.views import event_views, category_views, userevent_views

urlpatterns = [
    path("", event_views.get_all_events, name="get_all_events"),
    path("/categories", category_views.get_all_categories, name="get_all_categories"),
    path("/<int:event_id>", event_views.get_event_details, name="get_event_details"),
    path(
        "/<int:event_id>/favorites",
        userevent_views.add_or_remove_favorites,
        name="add_or_remove_favorites",
    ),
    path("/favorites", userevent_views.get_user_favorites, name="get_user_favorites"),
]
