import string
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from apps.private_rooms.models import PrivateRoom
from apps.private_rooms.serializers import PrivateRoomSerializer
import secrets

def generate_room_code():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_private_room(request):
    # Extract data from the request
    user = request.user
    data = request.data

    # Create the private room
    private_room = PrivateRoom.objects.create(
        code=generate_room_code(), name=data["name"], admin=user
    )
    room_serialized = PrivateRoomSerializer(private_room)
    # Return the created room details
    return Response(room_serialized.data, HTTP_201_CREATED)
