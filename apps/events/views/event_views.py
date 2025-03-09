from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.events.models import Event
from apps.events.serializers import EventSerializer


@api_view(["GET"])
def get_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
