from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    dateIni = models.DateTimeField()
    dateEnd = models.DateTimeField()
    infoTickets = models.TextField(null=True)
    schedule = models.TextField(null=True)
    categories = models.ManyToManyField("Category", related_name="events")
    scopes = models.ManyToManyField("Scope", related_name="events")
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(
        User, through="UserEvent", related_name="attended_events"
    )


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Scope(models.Model):
    name = models.CharField(max_length=50)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="events/images")


class EventLink(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="links")
    link = models.URLField()
