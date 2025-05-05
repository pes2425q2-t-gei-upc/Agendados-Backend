from django.db.models import Q
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Event, Category
from apps.events.serializers import EventSerializer, EventSummarizedSerializer, ShareLinkSerializer
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
