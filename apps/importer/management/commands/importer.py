from django.core.management.base import BaseCommand
import pandas as pd
from apps.importer.services.category_importer import import_category
from apps.importer.services.event_importer import import_event
from apps.importer.services.location_importer import import_location
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "..", "data", "events.csv")

#Logger configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger_path = os.path.join(BASE_DIR, "..", "data", "importer.log")
if os.path.exists(file_path):
    os.remove(file_path)

logging.basicConfig(
    filename=file_path,
    level=logger_path.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv(file_path, low_memory=False)
        for index, row in df.iterrows():

            #category = import_category(row)
            location = import_location(row)
            #import_event(row, category, location)
