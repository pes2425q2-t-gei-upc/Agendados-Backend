from django.core.management.base import BaseCommand
import pandas as pd

from apps.importer.services.category_importer import import_categories
from apps.importer.services.event_importer import import_event
from apps.importer.services.location_importer import import_location
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "..", "data", "events.csv")

#Logger configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger_path = os.path.join(BASE_DIR, "..", "..", "data", "importer.log")
if os.path.exists(logger_path):
    os.remove(logger_path)

logging.basicConfig(
    filename=logger_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv(file_path, low_memory=False)
        for index, row in df.iterrows():
            logging.info('Processing row %s', index)
            #Categories import
            categories = import_categories(row)
            logging.info('Categories imported: %s', categories)

            #Location import
            location = import_location(row)
            logging.info('Location imported: %s', location)

            #Event import
            try:
                event = import_event(row, categories, location)
                logging.info('Event imported: %s', event)
            except Exception as e:
                logging.error('Error importing event: %s', e)
            logging.info('------------------------------------------------')
