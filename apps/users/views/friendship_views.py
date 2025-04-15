from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from apps.users.models import Friendship
from apps.users.seralizers import UserSerializer


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_friendships(request):
    user = request.user

    friendships = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    )
    #Obtain the user that is not the request user
    friends = [
        f.user2 if f.user1 == user else f.user1
        for f in friendships
    ]

    serialized_friends = UserSerializer(friends, many=True)

    return Response(serialized_friends.data)