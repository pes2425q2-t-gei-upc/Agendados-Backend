from django.test import TestCase
from apps.importer.services.category_importer import import_categories
from apps.importer.services.event_importer import import_event
from apps.importer.services.location_importer import import_location
import pandas as pd
from unittest.mock import patch, MagicMock
import os


# Add this class at the top of your test file
class LocationMock(MagicMock):
    def __str__(self):
        return "Test Location"

class ImporterTestCase(TestCase):
    def setUp(self):
        self.event_data = {
            'codi': 'TEST001',
            'Denominació': 'Test Event Title',
            'Data inici': '01/01/2030',
            'Data fi': '02/01/2030',
            'Descripcio': 'Test Description',
            'Horari': '10:00 - 20:00',
            'Enllaç': 'http://example.com',
            'Preu': '10.00',
            'Observacions': 'Additional notes',
            'Tags categoríes': 'Category1,Category2',
            'Entrades': 'Ticket information',
            'Organitzador': 'Test Organizer',
            'Email': 'test@example.com',
            'Telèfon': '123456789',
            'Tipus': 'Test Type',
            'Web': 'http://example.com',
            'Data publicació': '01/01/2023',
            'Imatges': 'image1.jpg,image2.jpg'
        }

        self.location_data = {
            'Comarca': 'Test Region',
            'Municipi': 'Test City Name',
            'Adreça': 'Test Address',
            'Espai': 'Test Location',
            'Latitud': '41.123456',
            'Longitud': '2.123456'
        }

        self.category_data = {
            'Tags categoríes': 'Category1,Category2'
        }

    def test_import_event(self):
        # Patch import_location, Event.objects.create, import_images, and import_links
        with patch('apps.importer.services.event_importer.import_location') as mock_import_location, \
                patch('apps.events.models.Event.objects.create') as mock_create, \
                patch('apps.importer.services.event_importer.import_images') as mock_import_images, \
                patch('apps.importer.services.event_importer.import_links') as mock_import_links:
            # Create a mock location
            mock_location = MagicMock(spec=['id', 'space', 'address'])
            mock_location.id = 1
            mock_location.space = "Test Location"
            mock_location.address = "Test Address"
            mock_import_location.return_value = mock_location

            # Create a mock event that will be returned by Event.objects.create
            mock_event = MagicMock()
            mock_event.id = 1  # Set an ID for the event
            mock_event.title = 'Test Event Title'
            mock_event.description = 'Test Description'
            mock_event.code = 'TEST001'
            mock_event.info_tickets = 'Ticket information'
            mock_event.schedule = '10:00 - 20:00'
            mock_create.return_value = mock_event

            # Call the function
            event = import_event(pd.Series(self.event_data))

            # Verify import_images and import_links were called once
            mock_import_images.assert_called_once()
            mock_import_links.assert_called_once()

            # Check that the event parameter was passed correctly to both functions
            self.assertEqual(mock_import_images.call_args[0][1], mock_event)
            self.assertEqual(mock_import_links.call_args[0][1], mock_event)

            # Assertions
            self.assertIsNotNone(event)
            self.assertEqual(event.title, 'Test Event Title')
            self.assertEqual(event.description, 'Test Description')
            self.assertEqual(event.code, 'TEST001')
            self.assertEqual(event.info_tickets, 'Ticket information')
            self.assertEqual(event.schedule, '10:00 - 20:00')

            # Verify create was called with correct arguments
            mock_create.assert_called_once()

    def test_import_location(self):
        # Test the location importer functionality
        location = import_location(pd.Series(self.location_data))

        # Assertions
        self.assertIsNotNone(location)
        self.assertEqual(location.space, 'Test Location')  # Maps to 'Espai'
        self.assertEqual(location.address, 'Test Address')  # Maps to 'Adreça'
        self.assertEqual(location.latitude, '41.123456')  # Maps to 'Latitud'
        self.assertEqual(location.longitude, '2.123456')  # Maps to 'Longitud'
        self.assertEqual(location.town.name, 'Test City Name')  # Assuming town is related model, maps to 'Municipi'

    def test_import_event_with_missing_fields(self):
        # Test handling of missing fields
        incomplete_data = self.event_data.copy()
        del incomplete_data['Denominació']  # Remove required field, changed from 'name'

        # Test with missing required field
        with self.assertRaises(KeyError):  # Adjust to the specific exception you expect
            import_event(pd.Series(incomplete_data))

    def test_import_event_with_invalid_dates(self):
        # Test handling of invalid date formats
        invalid_data = self.event_data.copy()
        invalid_data['Data inici'] = 'INVALID-FORMAT'

        # We need to patch the format_date function to directly return None for invalid dates
        with patch('apps.importer.services.event_importer.format_date', return_value=None), \
                patch('apps.importer.services.event_importer.import_location') as mock_import_location, \
                patch('apps.importer.services.event_importer.import_links') as mock_import_links, \
                patch('apps.events.models.Event.objects.create') as mock_create:
            # Call the function with invalid data
            result = import_event(pd.Series(invalid_data))

            # Assert the result is None
            self.assertIsNone(result)

            # Verify import_location and create weren't called
            mock_import_location.assert_not_called()
            mock_import_links.assert_not_called()
            mock_create.assert_not_called()


@patch('pandas.read_csv')
@patch('apps.importer.management.commands.importer.import_event')
def test_command_integration(self, mock_import, mock_read_csv):
    # Setup mock DataFrame
    mock_df = pd.DataFrame([self.event_data])
    mock_read_csv.return_value = mock_df

    # Run the command
    from apps.importer.management.commands.importer import Command
    command = Command()
    command.handle()

    # Verify import_event was called
    mock_import.assert_called()