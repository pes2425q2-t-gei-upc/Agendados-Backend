from django.db import models
from django.contrib.auth.models import User

from apps.events.models import Event


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.sender}: {self.content}'
