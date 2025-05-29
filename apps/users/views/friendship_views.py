from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth.models import User

from apps.users.models import Friendship, FriendRequest
from apps.users.serializers import UserSerializer, FriendRequestSerializer


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


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_friend_request(request, user_id):
    user_from = request.user
    user_to = get_object_or_404(User, id=user_id)

    # Verify user is not the same
    if user_from.id == user_to.id:
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify users are not already friends
    existing_friendship = Friendship.objects.filter(
        (Q(user1=user_from) & Q(user2=user_to)) |
        (Q(user1=user_to) & Q(user2=user_from))
    ).exists()

    if existing_friendship:
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    # Verify if a friend request already exists
    existing_request = FriendRequest.objects.filter(
        user_from=user_from,
        user_to=user_to
    ).exists()

    if existing_request:
        return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    # If an opposite request exists, create a friendship and delete the request
    opposite_request = FriendRequest.objects.filter(
        user_from=user_to,
        user_to=user_from
    ).first()

    if opposite_request:
        friendship = Friendship(
            user1=user_from if user_from.id < user_to.id else user_to,
            user2=user_to if user_from.id < user_to.id else user_from
        )
        friendship.save()
        opposite_request.delete()
        return Response(status=status.HTTP_201_CREATED)

    friend_request = FriendRequest(user_from=user_from, user_to=user_to)
    friend_request.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, request_id):
    user = request.user
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        user_to=user
    )

    user_from = friend_request.user_from
    user_to = friend_request.user_to

    friendship = Friendship(
        user1=user_from if user_from.id < user_to.id else user_to,
        user2=user_to if user_from.id < user_to.id else user_from
    )
    friendship.save()

    friend_request.delete()

    return Response(status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def decline_friend_request(request, request_id):
    user = request.user
    friend_request = get_object_or_404(
        FriendRequest,
        id=request_id,
        user_to=user
    )

    friend_request.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_pending_friend_requests(request):
    user = request.user

    pending_requests = FriendRequest.objects.filter(user_to=user)
    serializer = FriendRequestSerializer(pending_requests, many=True)

    return Response(serializer.data)
