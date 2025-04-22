from uuid import uuid4

import pandas as pd
import urllib.parse
import boto3
import io
from django.conf import settings

from apps.events.models import EventImage


def import_images(row, event):
    images_string = row['Imatges']
    if pd.isna(images_string):  #Return none if images is NaN
        return None
    images_array = images_string.split(",")
    result = []

    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    for image_url in images_array:
        try:
            encoded_url = urllib.parse.quote(image_url, safe=":/")
            image_url = f"https://agenda.cultura.gencat.cat{encoded_url}"
            image_name = f"events/{event.id}/{uuid4()}.jpg"

            #Download image data
            with urllib.request.urlopen(image_url) as response:
                image_data = response.read()

            s3_client.upload_fileobj(
                io.BytesIO(image_data),
                settings.AWS_STORAGE_BUCKET_NAME,
                image_name,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )

            # Generar URL de S3
            s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{image_name}"

            image, created = EventImage.objects.get_or_create(
                event_id=event.id,
                defaults={
                    'image_url': s3_url,
                }
            )
            if not created:
                image.image_url = s3_url
                image.save()

            result.append(image)
        except Exception as e:
            print(f"Error importing image {image_url}: {e}")
            continue

    return result