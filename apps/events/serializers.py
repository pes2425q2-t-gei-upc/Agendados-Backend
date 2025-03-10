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
        fields = ["image"]


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
    attendees = UserEventSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = [
            "code",
            "title",
            "description",
            "dateIni",
            "dateEnd",
            "infoTickets",
            "schedule",
            "categories",
            "scopes",
            "location",
            "images",
            "links",
            "attendees",
        ]
