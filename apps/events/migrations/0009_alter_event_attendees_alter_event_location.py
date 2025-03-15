# Generated by Django 5.1.3 on 2025-03-15 17:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0008_alter_event_attendees"),
        ("locations", "0004_alter_location_address_alter_location_latitude_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(
                related_name="attended_events",
                through="events.UserEvent",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="locations.location",
            ),
        ),
    ]
