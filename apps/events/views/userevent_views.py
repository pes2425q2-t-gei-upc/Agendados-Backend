from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from apps.events.models import Event, UserEvent


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_to_favorites(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id)
    user_event, created = UserEvent.objects.get_or_create(user=user, event=event)

    if created:
        return Response(status=HTTP_201_CREATED)
    else:
        return Response(status=HTTP_200_OK)

