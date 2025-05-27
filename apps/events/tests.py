import os
import unittest
from django.test import TestCase
from apps.events.models import Event, Category
from apps.locations.models import Location, Town, Region
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User


class EventModelTest(TestCase):
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
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            code="TEST001",
            date_ini="2023-01-01",
            date_end="2023-01-02",
            info_tickets="Free entry",
            schedule="10:00 - 20:00",
            location=self.location
        )
        self.event.categories.add(self.category)

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Test Event")
        self.assertEqual(self.event.description, "Test Description")
        self.assertEqual(self.event.location, self.location)
        self.assertEqual(self.event.categories.count(), 1)
        self.assertEqual(self.event.categories.first(), self.category)


class EventAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

        # Set up API client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

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
        self.category = Category.objects.create(name="Music")
        self.event = Event.objects.create(
            title="Test Event",
            description="Test Description",
            code="TEST001",
            date_ini="2023-01-01",
            date_end="2023-01-02",
            info_tickets="Free entry",
            schedule="10:00 - 20:00",
            location=self.location
        )
        self.event.categories.add(self.category)

        # Create additional events for testing filters
        self.event2 = Event.objects.create(
            title="Another Test Event",
            description="Another Description",
            code="TEST002",
            date_ini="2023-02-01",
            date_end="2023-02-02",
            info_tickets="Paid entry",
            schedule="11:00 - 21:00",
            location=self.location
        )

        # Create data for POST test
        self.valid_event_data = {
            "title": "New Event",
            "description": "New Description",
            "code": "NEW001",
            "date_ini": "2023-03-01",
            "date_end": "2023-03-02",
            "info_tickets": "Online tickets",
            "schedule": "09:00 - 19:00",
            "location": self.location.id,
            "categories": [self.category.id]
        }

    def test_get_event_detail(self):
        response = self.client.get(reverse('get_event_details', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Event')
        self.assertEqual(response.data['description'], 'Test Description')

    def test_get_all_events(self):
        response = self.client.get(reverse('get_all_events'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
    
    @unittest.skipIf(
        os.environ.get("CI") == "true", 
        "Skip in CI environment due to SQLite limitations with DurationField"
    )
    def test_get_recommended_events(self):
        response = self.client.get(reverse('get_recommended_events'))
        self.assertEqual(response.status_code, 200)

    def test_get_all_categories(self):
        response = self.client.get(reverse('get_all_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_add_remove_favorites(self):
        response = self.client.post(reverse('add_or_remove_favorites', args=[self.event.id]))
        self.assertIn(response.status_code, [200, 201, 204])

    def test_get_user_favorites(self):
        response = self.client.get(reverse('get_user_favorites'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_favorites_by_id(self):
        # Primero añadimos un evento a los favoritos del usuario
        self.client.post(reverse('add_or_remove_favorites', args=[self.event.id]))
        
        # Luego probamos el endpoint sin autenticación
        client = APIClient()
        response = client.get(reverse('get_user_favorites_by_id', args=[self.user.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.event.id)
        
        # Probamos con un usuario que no existe
        response = client.get(reverse('get_user_favorites_by_id', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_get_user_discarded(self):
        response = self.client.get(reverse('get_user_discarded'))
        self.assertEqual(response.status_code, 200)