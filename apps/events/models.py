from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=400)
    description = models.TextField(null=True)
    date_ini = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    info_tickets = models.TextField(null=True)
    schedule = models.TextField(null=True)
    categories = models.ManyToManyField("Category", related_name="events")
    scopes = models.ManyToManyField("Scope", related_name="events")
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE, null=True)
    attendees = models.ManyToManyField(
        User, through="UserEvent", related_name="attended_events"
    )
    discarded_by = models.ManyToManyField(
        User, through="UserDiscardedEvent", related_name="discarded_events"
    )


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

class UserDiscardedEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_discarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Scope(models.Model):
    name = models.CharField(max_length=50)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(null=True, blank=True)


class EventLink(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="links")
    link = models.URLField(max_length=500)
