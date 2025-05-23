from django.db import models
from django.contrib.auth.models import User

from apps.events.models import Event


class PrivateRoom(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=False, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="private_rooms"
    )
    participants = models.ManyToManyField(
        User, related_name="participated_rooms", blank=True
    )
    events = models.ManyToManyField(
        Event, related_name="private_room_events", blank=True, through="PrivateRoomEvent"
    )

    def __str__(self):
        return self.name

class PrivateRoomEvent(models.Model):
    private_room = models.ForeignKey(PrivateRoom, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ('private_room', 'event')
    def __str__(self):
        return f"{self.private_room.name} - {self.event.id} (Flag: {self.is_current})"

class PrivateRoomVote(models.Model):
    private_room_event = models.ForeignKey(PrivateRoomEvent, on_delete=models.CASCADE, related_name="votes")
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_votes")
    vote = models.BooleanField()

    class Meta:
        unique_together = ('private_room_event', 'participant')

    def __str__(self):
        return f"Vote by {self.participant.username} on {self.private_room_event}: {self.vote}"