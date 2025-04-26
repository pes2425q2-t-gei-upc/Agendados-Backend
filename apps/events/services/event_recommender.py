from django.db.models import Count, ExpressionWrapper, FloatField, Q, F
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.events.models import Category, Event
from apps.users.models import Friendship, User 

def event_recommender(user, limit):
    # Categorías favoritas / descartadas
    favorite_categories = Category.objects.filter(events__attendees=user).annotate(
        favorite_count=Count("events", filter=Q(events__attendees=user))
    )
    discarded_categories = Category.objects.filter(events__discarded_by=user).annotate(
        discarded_count=Count("events", filter=Q(events__discarded_by=user))
    )

    #  Base de eventos
    events = Event.objects.exclude(Q(attendees=user) | Q(discarded_by=user))

    # Peso categorías
    events = events.annotate(
        favorite_count=Coalesce(
            Count("categories", filter=Q(categories__in=favorite_categories)), 0
        ),
        discarded_count=Coalesce(
            Count("categories", filter=Q(categories__in=discarded_categories)), 0
        ),
    ).annotate(
        weight=ExpressionWrapper(
            F("favorite_count") - F("discarded_count") * 0.5,
            output_field=FloatField(),
        )
    )

    # Factor social: cuantos amigos asisten
    # obtenemos IDs de amigos desde el modelo Friendship
    friend_ids = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).values_list("user1_id", "user2_id")
    # aplanamos y excluimos al propio user
    flat_ids = set(sum((list(t) for t in friend_ids), [])) - {user.id}
    friends = User.objects.filter(id__in=flat_ids)
    events = events.annotate(
        friend_count=Coalesce(
            Count("attendees", filter=Q(attendees__in=friends)), 0
        )
    )

    # Popularidad y recencia
    events = events.annotate(
        popularity=Coalesce(Count("attendees"), 0),
        recency=ExpressionWrapper(
            1.0 / (F("date_ini") - timezone.now()).seconds,
            output_field=FloatField(),
        ),
    )

    # Score final combinando señales
    events = events.annotate(
        final_score=ExpressionWrapper(
            F("weight") * 0.4
            + F("friend_count") * 0.3
            + F("popularity") * 0.2
            + F("recency") * 0.1,
            output_field=FloatField(),
        )
    ).order_by("-final_score")

    # Añadir un 10% de 'explore' aleatorio
    explore_count = int(limit * 0.1)
    main_count = limit - explore_count

    main = list(events[:main_count])
    explore = list(
        Event.objects.exclude(id__in=[e.id for e in main]).order_by("?")[:explore_count]
    )

    return main + explore