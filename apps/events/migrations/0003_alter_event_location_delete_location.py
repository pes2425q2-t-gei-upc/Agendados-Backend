# Generated by Django 5.1.3 on 2025-03-10 15:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0002_event_description"),
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="locations.location"
            ),
        ),
        migrations.DeleteModel(
            name="Location",
        ),
    ]
