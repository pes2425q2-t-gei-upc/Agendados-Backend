import pandas as pd
import urllib.parse

from apps.events.models import EventImage


def import_images(row, event):
    images_string = row['Imatges']
    if pd.isna(images_string):  #Return none if images is NaN
        return None
    images_array = images_string.split(",")
    result = []

    for image_url in images_array:
        encoded_url = urllib.parse.quote(image_url, safe=":/")
        image, created = EventImage.objects.get_or_create(image_url=encoded_url, event_id=event.id)
        result.append(image)
    return result