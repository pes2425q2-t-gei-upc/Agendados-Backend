import pandas as pd

from apps.events.models import EventImage


def import_images(row, event):
    images_string = row['Imatges']
    if pd.isna(images_string):  #Return none if images is NaN
        return None
    images_array = images_string.split(",")
    result = []

    for image_url in images_array:
        image, created = EventImage.objects.get_or_create(image_url=parse_image(image_url), event_id=event.id)
        result.append(image)
    return result

def parse_image(image_string):
    return image_string.split("/")[-1]