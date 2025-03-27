from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.locations.models import Location, Region, Town
from apps.locations.serializers import (
    LocationSerializer,
    RegionSerializer,
    TownSerializer,
)


@api_view(["GET"])
def get_all_locations(request):
    locations = Location.objects.all()
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_regions(request):
    regions = Region.objects.all()
    serializer = RegionSerializer(regions, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_towns(request):
    towns = Town.objects.all()
    serializer = TownSerializer(towns, many=True)
    return Response(serializer.data)
