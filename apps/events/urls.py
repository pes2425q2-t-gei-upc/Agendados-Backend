from django.urls import path
from apps.events.views import event_views, category_views, userevent_views, userdiscardedevent_views, schedule_views

urlpatterns = [
    path("", event_views.get_all_events, name="get_all_events"),
    path("recommended", event_views.get_recommended_events, name="get_recommended_events"),
    path("categories", category_views.get_all_categories, name="get_all_categories"),
    path("<int:event_id>", event_views.get_event_details, name="get_event_details"),
    path(
        "<int:event_id>/favorites",
        userevent_views.add_or_remove_favorites,
        name="add_or_remove_favorites",
    ),
    path("favorites", userevent_views.get_user_favorites, name="get_user_favorites"),
    path("<int:event_id>/discarded", userdiscardedevent_views.add_or_remove_discarded, name="add_or_remove_discarded"),
    path("discarded", userdiscardedevent_views.get_user_discarded, name="get_user_discarded"),
    path("<int:event_id>/share", event_views.generate_share_link, name="generate_share_link"),
    path("<int:event_id>/ics", schedule_views.generate_ics, name="add_or_remove_discarded"),
]
