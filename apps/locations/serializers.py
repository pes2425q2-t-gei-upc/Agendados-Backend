from rest_framework import serializers
from .models import Location, Region, Town


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["id", "name"]


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ["id", "name"]


class LocationSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    town = TownSerializer()

    class Meta:
        model = Location
        fields = ["id", "region", "town", "latitude", "longitude", "address", "space"]
