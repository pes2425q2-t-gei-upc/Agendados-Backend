from rest_framework import serializers
from django.contrib.auth.models import User

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