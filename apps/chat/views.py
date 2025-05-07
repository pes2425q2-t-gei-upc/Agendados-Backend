from django.db.models import OuterRef, Subquery
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.chat.models import Message
from apps.events.models import Event
from apps.events.serializers import EventSerializer


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_events_by_user_has_messaged(request):
    user = request.user

    latest_messages = Message.objects.filter(
        sender=user,
        event=OuterRef('pk')
    ).order_by('-timestamp').values('timestamp')[:1]

    event_ids = Message.objects.filter(sender=user).values_list('event', flat=True).distinct()
    events = Event.objects.filter(id__in=event_ids).annotate(
        latest_message_date=Subquery(latest_messages)
    ).order_by('-latest_message_date')

    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)