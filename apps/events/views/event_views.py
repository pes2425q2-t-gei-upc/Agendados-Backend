from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from apps.events.models import Event, Category, UserReportedEvent
from apps.events.serializers import EventSerializer, EventSummarizedSerializer, ShareLinkSerializer, \
    UserReportedEventSerializer
from apps.events.services.event_recommender import event_recommender


@api_view(["GET"])
def get_event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_recommended_events(request):
    #Get the limit of events to return
    limit = request.query_params.get("limit", 50)
    try:
        limit = int(limit)
    except ValueError:
        return Response({"error": "Invalid limit value"}, status=400)

    user = request.user

    events = event_recommender(user, limit)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_share_link(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        serializer = ShareLinkSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({"error": "Evento no encontrado"}, status=404)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def report_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Prevent duplicate report
    if UserReportedEvent.objects.filter(user=request.user, event=event).exists():
        return Response(status=400)

    reason = request.data.get('reason', None)
    UserReportedEvent.objects.create(
        user=request.user,
        event=event,
        reason=reason
    )
    return Response(status=HTTP_201_CREATED)