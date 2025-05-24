from rest_framework import serializers
from .models import Event, Category, Scope, EventImage, EventLink, UserEvent, UserReportedEvent
from ..locations.serializers import LocationSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ["name"]


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ["image_url"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.image_url:
            representation["image_url"] = instance.image_url
        return representation


class EventLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLink
        fields = ["link"]


class UserEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvent
        fields = ["user", "event", "date_joined"]


class EventSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    scopes = ScopeSerializer(many=True)
    location = LocationSerializer()
    images = EventImageSerializer(many=True)
    links = EventLinkSerializer(many=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "date_ini",
            "date_end",
            "info_tickets",
            "schedule",
            "categories",
            "scopes",
            "location",
            "images",
            "links",
        ]

class EventSummarizedSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    location = LocationSerializer()
    images = EventImageSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "title", "date_ini", "date_end", "categories", "location", "images"]

class ShareLinkSerializer(serializers.ModelSerializer):
    share_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'share_link']
    
    def get_share_link(self, obj):
        return f"agendados://event/{obj.id}"

class UserReportedEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReportedEvent
        fields = ['event', 'reason']
