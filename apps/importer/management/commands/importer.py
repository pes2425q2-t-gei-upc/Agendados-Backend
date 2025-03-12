from django.core.management.base import BaseCommand
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "..", "..", "data", "events.csv")

class Command(BaseCommand):
    def handle(self, *args, **options):
        df = pd.read_csv(file_path, low_memory=False)
