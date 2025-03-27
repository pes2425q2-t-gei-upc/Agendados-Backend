from django.test import TestCase
from apps.locations.models import Region, Town, Location
from django.urls import reverse
from rest_framework.test import APIClient
import re


class RegionModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Catalunya")

    def test_region_creation(self):
        self.assertEqual(self.region.name, "Catalunya")
        self.assertTrue(isinstance(self.region, Region))
        self.assertTrue(re.match(r"Region object \(\d+\)", str(self.region)))


class TownModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Catalunya")
        self.town = Town.objects.create(name="Barcelona", region=self.region)

    def test_town_creation(self):
        self.assertEqual(self.town.name, "Barcelona")
        self.assertEqual(self.town.region, self.region)
        self.assertTrue(isinstance(self.town, Town))
        self.assertTrue(re.match(r"Town object \(\d+\)", str(self.town)))


class LocationModelTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Catalunya")
        self.town = Town.objects.create(name="Barcelona", region=self.region)
        self.location = Location.objects.create(
            space="Test Space",
            address="Test Address",
            latitude=41.3851,
            longitude=2.1734,
            town=self.town,
            region=self.region
        )

    def test_location_creation(self):
        self.assertEqual(self.location.space, "Test Space")
        self.assertEqual(self.location.address, "Test Address")
        self.assertEqual(self.location.latitude, 41.3851)
        self.assertEqual(self.location.longitude, 2.1734)
        self.assertEqual(self.location.town, self.town)
        self.assertEqual(self.location.region, self.region)
        self.assertTrue(isinstance(self.location, Location))


class LocationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data
        self.region1 = Region.objects.create(name="Catalunya")
        self.region2 = Region.objects.create(name="Madrid")

        self.town1 = Town.objects.create(name="Barcelona", region=self.region1)
        self.town2 = Town.objects.create(name="Girona", region=self.region1)
        self.town3 = Town.objects.create(name="Madrid City", region=self.region2)

        self.location1 = Location.objects.create(
            space="Sagrada Familia",
            address="Carrer de Mallorca, 401",
            latitude=41.4036,
            longitude=2.1744,
            town=self.town1,
            region=self.region1
        )

        self.location2 = Location.objects.create(
            space="Park Güell",
            address="Carrer d'Olot",
            latitude=41.4145,
            longitude=2.1527,
            town=self.town1,
            region=self.region1
        )

        self.location3 = Location.objects.create(
            space="Madrid Location",
            address="Test Address Madrid",
            latitude=40.4168,
            longitude=-3.7038,
            town=self.town3,
            region=self.region2
        )

    def test_get_all_locations(self):
        response = self.client.get(reverse('get_all_locations'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_get_all_regions(self):
        response = self.client.get(reverse('get_all_regions'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        region_names = [region['name'] for region in response.data]
        self.assertIn('Catalunya', region_names)
        self.assertIn('Madrid', region_names)

    def test_get_all_towns(self):
        response = self.client.get(reverse('get_all_towns'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        town_names = [town['name'] for town in response.data]
        self.assertIn('Barcelona', town_names)
        self.assertIn('Girona', town_names)
        self.assertIn('Madrid City', town_names)


class LocationImportTest(TestCase):
    def test_parser(self):
        from apps.importer.services.location_importer import parser

        self.assertEqual(parser("test/name"), "Name")
        self.assertEqual(parser("test-name"), "Test Name")
        self.assertEqual(parser("test name"), "Test Name")

    def test_clean_value(self):
        from apps.importer.services.location_importer import clean_value
        import pandas as pd
        import numpy as np

        self.assertEqual(clean_value("test"), "test")
        self.assertIsNone(clean_value(pd.NA))
        self.assertIsNone(clean_value(np.nan))
