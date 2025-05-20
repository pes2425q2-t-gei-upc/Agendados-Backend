from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.status import HTTP_400_BAD_REQUEST

from apps.events.models import Event
from apps.events.serializers import EventSerializer


@api_view(["GET"])
def get_events_in_area(request):
    lat_min = request.query_params.get("lat_min")
    lat_max = request.query_params.get("lat_max")
    lon_min = request.query_params.get("lon_min")
    lon_max = request.query_params.get("lon_max")

    if lat_min is None or lat_max is None or lon_min is None or lon_max is None:
        return Response({"error": "Missing required parameters"}, status=HTTP_400_BAD_REQUEST)

    try:
        lat_min = float(lat_min)
        lat_max = float(lat_max)
        lon_min = float(lon_min)
        lon_max = float(lon_max)

        events = Event.objects.filter(
            Q(location__latitude__gte=lat_min, location__latitude__lte=lat_max) &
            Q(location__longitude__gte=lon_min, location__longitude__lte=lon_max)
        )

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    except ValueError:
        return Response(
            {"error": "Coordinate parameters must be valid numbers"},
            status=HTTP_400_BAD_REQUEST
        )