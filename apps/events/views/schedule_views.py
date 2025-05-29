from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from apps.events.models import Event
from apps.events.services.ics_generator import generate_event_ics, parse_ics_string_to_json


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_ics(request, event_id):
    if not event_id:
        return Response(status=HTTP_400_BAD_REQUEST)

    # Assuming you have a function to generate the ICS file
    event = Event.objects.get(id=event_id)
    ics = generate_event_ics(event.schedule, event.date_ini, event.date_end)
    result = parse_ics_string_to_json(ics)
    return JsonResponse({'events': result}, status=HTTP_200_OK)

