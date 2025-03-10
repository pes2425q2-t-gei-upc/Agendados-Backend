from rest_framework import serializers
from .models import Location, Region, Town

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["name"]

class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ["name"]

class LocationSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    town = TownSerializer()

    class Meta:
        model = Location
        fields = ["region", "town", "latitude", "longitude", "address", "space"]