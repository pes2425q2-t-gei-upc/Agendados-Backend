from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, default="cat")
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

class FriendRequest(models.Model):
    user_from = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_from', 'user_to'], name='unique_friend_request')
        ]

    def __str__(self):
        return f"{self.user_from.username} -> {self.user_to.username}"

