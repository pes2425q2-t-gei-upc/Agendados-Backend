from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import FriendRequest, UserFCMToken, Notification, UserProfile

class UserSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "language", "profile_image"]

    def get_language(self, obj):
        profile = getattr(obj, 'userprofile', None)
        if profile:
            return profile.language
        return None
        
    def get_profile_image(self, obj):
        profile = getattr(obj, 'userprofile', None)
        if profile and profile.profile_image:
            # Obtener la URL completa de S3
            url = profile.profile_image.url
            if url.startswith('/'):
                from django.conf import settings
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                region = settings.AWS_S3_REGION_NAME
                url = f"https://{bucket_name}.s3.{region}.amazonaws.com{url}"
            return url
        return None

class FriendRequestSerializer(serializers.ModelSerializer):
    user_from = UserSerializer(read_only=True)
    user_to = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'user_from', 'user_to', 'created_at']


# --- Agregados para notificaciones ---
class UserFCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFCMToken
        fields = ['id', 'user', 'token', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'body', 'is_read', 'created_at']
