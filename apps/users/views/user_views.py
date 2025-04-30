from django.contrib.auth import update_session_auth_hash
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.contrib.auth.models import User
from django.db.models import Q

from apps.users.seralizers import UserSerializer


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_users(request):
    query = request.GET.get('query', '')
    current_user = request.user

    if not query:
        users = User.objects.exclude(id=current_user.id)
    else:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        ).exclude(id=current_user.id).distinct()

    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_password(request):
    data = request.data
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    current_user = request.user

    if not current_password or not new_password:
        return Response(
            status=HTTP_400_BAD_REQUEST
        )

    if not current_user.check_password(current_password):
        return Response(
            {"error": "Incorrect current password"},
            status=HTTP_400_BAD_REQUEST
        )

    current_user.set_password(new_password)
    current_user.save()

    update_session_auth_hash(request, current_user)

    return Response(
        status=HTTP_200_OK
    )