from django.contrib.auth.models import User
from django.db import models

def user_profile_image_path(instance, filename):
    return f'profile_images/{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=20, default="cat")
    profile_image_url = models.CharField(max_length=500, blank=True)

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
        return f"{self.user_from.__str__()} -> {self.user_to.__str__()}"


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user1', 'user2'], name='unique_friendship'),
        ]

    def __str__(self):
        return f"{self.user1} <-> {self.user2}"


# Modelo para guardar tokens FCM de los usuarios
class UserFCMToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"


# Modelo para notificaciones internas
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} -> {self.user.username}"

