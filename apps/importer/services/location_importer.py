from apps.locations.models import Region
from apps.locations.models import Town
import pandas as pd

def import_location(row):
    region = import_region(row)
    town = import_town(row, region)


def import_region(row):
    region_name = row['Comarca']
    if pd.isna(region_name):
        return None

    #Create the region
    region, created = Region.objects.get_or_create(name=parser(region_name))
    return region

def import_town(row, region):
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