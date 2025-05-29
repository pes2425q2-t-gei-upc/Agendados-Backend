from uuid import uuid4

import boto3
from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser

from apps.users.serializers import UserSerializer
from apps.users.models import UserProfile

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


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile_image(request):
    """
    Endpoint para subir o actualizar la imagen de perfil en S3
    """
    try:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if 'profile_image' not in request.FILES:
            return Response(
                {"error": "No se ha enviado ninguna imagen"},
                status=HTTP_400_BAD_REQUEST
            )

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        image_file = request.FILES['profile_image']
        file_extension = image_file.name.split('.')[-1]
        s3_filename = f"profile_images/{request.user.id}/{uuid4()}.{file_extension}"

        s3_client.upload_fileobj(
            image_file.file,
            settings.AWS_STORAGE_BUCKET_NAME,
            s3_filename,
            ExtraArgs={
                'ContentType': image_file.content_type,
            }
        )

        profile.profile_image_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_filename}"
        profile.save()

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=HTTP_400_BAD_REQUEST
        )
