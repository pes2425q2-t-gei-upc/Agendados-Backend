from django.db import models
from django.contrib.auth.models import User

class PrivateRoom(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=False, unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="private_rooms"
    )
    participants = models.ManyToManyField(
        User, related_name="participated_rooms", blank=True
    )

    def __str__(self):
        return self.name