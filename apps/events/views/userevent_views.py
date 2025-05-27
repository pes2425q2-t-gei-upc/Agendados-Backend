from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from apps.events.models import Event, UserEvent
from apps.events.serializers import EventSerializer
from django.contrib.auth.models import User


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_favorites(request):
    user = request.user
    user_events = UserEvent.objects.filter(user=user)
    events = [user_event.event for user_event in user_events]
    print(events)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)



@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_favorites_by_id(request, user_id):
    try:
        target_user = User.objects.get(id=user_id)
        user_events = UserEvent.objects.filter(user=target_user)
        events = [user_event.event for user_event in user_events]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado"}, status=HTTP_404_NOT_FOUND)


@api_view(["POST", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_or_remove_favorites(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        user_event, created = UserEvent.objects.get_or_create(user=user, event=event)
        if created:
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_200_OK)
    elif request.method == "DELETE":
        user_event = UserEvent.objects.filter(user=user, event=event).first()
        if user_event:
            user_event.delete()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
