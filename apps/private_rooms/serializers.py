from rest_framework import serializers
from apps.private_rooms.models import PrivateRoom
from apps.users.serializers import UserSerializer


class PrivateRoomSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateRoom
        fields = [
            'id',
            'code',
            'name',
            'created_at',
            'updated_at',
            'admin',
            'participants',
        ]