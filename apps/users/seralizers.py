from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import FriendRequest

class UserSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "language"]

    def get_language(self, obj):
        profile = getattr(obj, 'userprofile', None)
        if profile:
            return profile.language
        return None

class FriendRequestSerializer(serializers.ModelSerializer):
    user_from = UserSerializer(read_only=True)
    user_to = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'user_from', 'user_to', 'created_at']
