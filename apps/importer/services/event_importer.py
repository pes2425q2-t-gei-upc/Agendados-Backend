from apps.events.models import Event
import pandas as pd
from datetime import datetime

def import_event(row, category, location):
    codi = row['codi']
    event = Event.objects.filter(id=codi).first()
    if event:
        return event

    title = row['Denominació']
    date_ini = clean_value(row['Data inici'])
    date_end = clean_value(row['Data fi'])
    description = clean_value(row['Descripcio'])
    info_tickets = clean_value(row['Entrades'])
    schedule = clean_value(row['Horari'])

    if location:
        event, created = Event.objects.get_or_create(id=codi, title=title, date_ini=format_date(date_ini), date_end=format_date(date_end), description=description, info_tickets=info_tickets, schedule=schedule, location=location)
        if created and category:
            event.categories.set([category])

def clean_value(value):
    return None if pd.isna(value) else value

def format_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return None
