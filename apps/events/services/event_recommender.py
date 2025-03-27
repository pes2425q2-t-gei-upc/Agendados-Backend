from django.db.models import Count, ExpressionWrapper, FloatField
from django.db.models import Q, F
from django.db.models.functions import Coalesce

from apps.events.models import Category, Event


def event_recommender(user, limit):
    # Count how many events the user has attended per category
    favorite_categories = Category.objects.filter(events__attendees=user).annotate(
        favorite_count=Count("events", filter=Q(events__attendees=user))
    )

    # Count how many events the user has discarded per category
    discarded_categories = Category.objects.filter(events__discarded_by=user).annotate(
        discarded_count=Count("events", filter=Q(events__discarded_by=user))
    )

    # Create a dictionary to store category weights based on favorites and discards
    category_weights = {}
    for category in favorite_categories:
        category_weights[category.id] = {"favorites": category.favorite_count, "discarded": 0}
    for category in discarded_categories:
        if category.id in category_weights:
            category_weights[category.id]["discarded"] = category.discarded_count
        else:
            category_weights[category.id] = {"favorites": 0, "discarded": category.discarded_count}
    print(category_weights)

    # Get all available events excluding those already attended or discarded
    events = Event.objects.exclude(Q(attendees=user) | Q(discarded_by=user))

    # Apply a weight based on the favorite/discarded relationship
    events = events.annotate(
        favorite_count=Coalesce(
            Count("categories", filter=Q(categories__in=favorite_categories)), 0
        ),
        discarded_count=Coalesce(
            Count("categories", filter=Q(categories__in=discarded_categories)), 0
        ),
    ).annotate(
        # Weight calculation: +1 for each favorite, -0.5 for each discarded (avoids negative weight)
        weight=ExpressionWrapper(
            F("favorite_count") - (F("discarded_count") * 0.5),
            output_field=FloatField(),
        )
    ).order_by("-weight")

    # Return the top recommended events based on the calculated weight
    recommended_events = events[:limit]
    return recommended_events