from django.utils.timezone import make_aware, get_current_timezone

from apps.events.models import Event
import pandas as pd
from datetime import datetime

def import_event(row, categories, location):
    code = row['codi']
    title = row['Denominació']
    date_ini = clean_value(row['Data inici'])
    date_end = clean_value(row['Data fi'])
    description = clean_value(row['Descripcio'])
    info_tickets = clean_value(row['Entrades'])
    schedule = clean_value(row['Horari'])

    event = Event.objects.create(code=code, title=title, date_ini=format_date(date_ini), date_end=format_date(date_end), description=description, info_tickets=info_tickets, schedule=schedule, location=location)
    if categories:
        event.categories.set(categories)

    return event

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
