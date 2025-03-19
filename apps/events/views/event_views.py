from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.events.models import Event
from apps.events.serializers import EventSerializer

@api_view(["GET"])
def get_event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    serializer = EventSerializer(event)
    return Response(serializer.data)

@api_view(["GET"])
def get_all_events(request):
    limit = request.query_params.get("limit", 50)
    try:
        limit = int(limit)
    except ValueError:
        return Response({"error": "Invalid limit value"}, status=400)

    events = Event.objects.all()[:limit]
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
