# Generated by Django 5.1.3 on 2025-03-09 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="description",
            field=models.TextField(null=True),
        ),
    ]
