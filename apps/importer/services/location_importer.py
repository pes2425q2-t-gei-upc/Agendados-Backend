from apps.locations.models import Region, Location
from apps.locations.models import Town
import pandas as pd

def import_location(row):
    region = import_region(row)
    town = import_town(row, region)

    if region and town:
        latitude = row['Latitud']
        longitude = row['Longitud']
        address = row['Adreça']
        space = row['Espai']
        location, created = Location.objects.get_or_create(region=region, town=town, latitude=latitude, longitude=longitude,
                                                  address=address, space=space)
        return location
    else:
        return None



def import_region(row):
    region_name = row['Comarca']
    if pd.isna(region_name) or not region_name.strip():
        return None

    parsed_region = parser(region_name)
    if not parsed_region:
        return None

    region, created = Region.objects.get_or_create(name=parsed_region)
    return region

def import_town(row, region):
    if not region:
        return None

    town_name = row['Municipi']
    if pd.isna(town_name):
        return None
    # Create the town
    town, created = Town.objects.get_or_create(name=parser(town_name), region_id=region.id)
    return town

def parser(name):
    formatted_name = name.split("/")[-1]
    formatted_name = formatted_name.replace("-", " ").title()
    return formatted_name