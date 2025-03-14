from apps.events.models import Event


def import_event(row, category, location):
    title = row['Denominació']
    date_ini = row['Data inici']
    date_end = row['Data fi']
    description = row['Descripcio']
    info_tickets = row['Entrades']
    schedule = row['Horari']

    event, created = Event.objects.get_or_create(title=title, date_ini=date_ini, date_end=date_end, description=description, info_tickets=info_tickets, schedule=schedule, categories=category, location=location)