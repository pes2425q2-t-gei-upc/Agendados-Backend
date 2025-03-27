from django.conf import settings
from rest_framework import serializers
from .models import Event, Category, Scope, EventImage, EventLink, UserEvent
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
        images_domain = "https://agenda.cultura.gencat.cat"

        if instance.image_url:
            representation["image_url"] = f"{images_domain}{instance.image_url}"
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