from rest_framework import serializers
from .models import Event, Category, Scope, EventImage, EventLink, UserEvent
from ..locations.serializers import LocationSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]


class ScopeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scope
        fields = ["name"]


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ["image_url"]


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