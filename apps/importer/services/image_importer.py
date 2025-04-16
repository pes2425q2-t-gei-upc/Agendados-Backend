from uuid import uuid4

import pandas as pd
import urllib.parse

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from apps.events.models import EventImage


def import_images(row, event):
    images_string = row['Imatges']
    if pd.isna(images_string):  #Return none if images is NaN
        return None
    images_array = images_string.split(",")
    result = []

    for image_url in images_array:
        try:
            encoded_url = urllib.parse.quote(image_url, safe=":/")
            image_url = f"https://agenda.cultura.gencat.cat{encoded_url}"
            image_name = f"events/{event.id}/{uuid4()}.jpg"

            #Download image data
            with urllib.request.urlopen(image_url) as response:
                image_data = response.read()
            s3_path = default_storage.save(image_name, ContentFile(image_data))
            s3_url = default_storage.url(s3_path)

            image, created = EventImage.objects.get_or_create(
                event_id=event.id,
                defaults={
                    'image_url': encoded_url,
                    's3_url': s3_url,
                    's3_key': image_name
                }
            )
            if not created:
                image.s3_url = s3_url
                image.s3_key = image_name
                image.save()

            result.append(image)
        except Exception as e:
            print(f"Error importing image {image_url}: {e}")
            continue

    return result