# Generated by Django 5.1.3 on 2025-03-19 17:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0012_userdiscardedevent_event_discarded_by"),
    ]

    operations = [
        migrations.RenameField(
            model_name="eventimage",
            old_name="image",
            new_name="image_url",
        ),
    ]
