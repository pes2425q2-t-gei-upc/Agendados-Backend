from django.core.management.base import BaseCommand
import pandas as pd
import os

from apps.importer.services.category_importer import import_category
from apps.importer.services.event_importer import import_event
from apps.importer.services.location_importer import import_location

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "..", "data", "events.csv")

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv(file_path, low_memory=False)
        for index, row in df.iterrows():
            category = import_category(row)
            location = import_location(row)
            import_event(row, category, location)
