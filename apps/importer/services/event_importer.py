from django.utils.timezone import make_aware, get_current_timezone, now

from apps.events.models import Event
import pandas as pd
from datetime import datetime
import logging

from apps.importer.services.category_importer import import_categories
from apps.importer.services.image_importer import import_images
from apps.importer.services.link_importer import import_links
from apps.importer.services.location_importer import import_location


def import_event(row):
    code = row['codi']
    title = row['Denominació']
    date_ini = clean_value(row['Data inici'])
    date_end = clean_value(row['Data fi'])
    description = clean_value(row['Descripcio'])
    info_tickets = clean_value(row['Entrades'])
    schedule = clean_value(row['Horari'])

    formatted_date_ini = format_date(date_ini)
    formatted_date_end = format_date(date_end)

    if formatted_date_end and formatted_date_end >= now():
        # Categories import
        categories = import_categories(row)
        logging.info('Categories imported: %s', categories)

        # Location import
        location = import_location(row)
        logging.info('Location imported: %s', location)
        event = Event.objects.create(code=code, title=title, date_ini=formatted_date_ini, date_end=formatted_date_end, description=description, info_tickets=info_tickets, schedule=schedule, location=location)
        if categories:
            event.categories.set(categories)
        if event:
            import_images(row, event)
            import_links(row, event)
        return event
    return None

def clean_value(value):
    return None if pd.isna(value) else value

def format_date(date_str):
    if not date_str:
        return None
    try:
        naive_datetime = datetime.strptime(date_str, "%d/%m/%Y")
        aware_datetime = make_aware(naive_datetime, get_current_timezone())
        return aware_datetime
    except ValueError:
        return None
