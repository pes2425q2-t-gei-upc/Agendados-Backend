import pandas as pd

from apps.events.models import EventLink


def import_links(row, event):
    links_strings = row['Enllaços']
    if pd.isna(links_strings):  #Return none if links is NaN
        return None
    links_array = links_strings.split(",")
    result = []

    for link_string in links_array:
        link, created = EventLink.objects.get_or_create(link=link_string, event_id=event.id)
        result.append(link)
    return result
