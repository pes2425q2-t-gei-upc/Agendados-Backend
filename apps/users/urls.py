from django.urls import path
from apps.users.views import auth_views, friendship_views, user_views, forgot_password_views
from .views.auth_views import google_auth

from apps.users.views import notification_views

urlpatterns = [
    #Auth urls
    path("login", auth_views.login, name="login"),
    path("signup", auth_views.signup, name="signup"),
    path("test", auth_views.test, name="test"),
    path("update-password", user_views.update_password, name="update_password"),
    path("forgot-password", forgot_password_views.forgot_password, name="forgot_password"),
    path('reset-password/<uidb64>/<token>/', forgot_password_views.forgot_password, name='reset-password'),
    #Friendship urls
    path("friendships", friendship_views.get_friendships, name="friendships"),
    path("friendships/<int:user_id>", friendship_views.send_friend_request, name="send_friend_request"),
    path("friendships/accept/<int:request_id>", friendship_views.accept_friend_request, name="accept_friend_request"),
    path("friendships/decline/<int:request_id>", friendship_views.decline_friend_request, name="decline_friend_request"),
    path("all", user_views.get_users, name="get_users"),
    path("friendships/pending", friendship_views.get_pending_friend_requests, name="get_pending_friend_requests"),
    path('auth/google/', google_auth, name='google-auth'),

    # Notificaciones y FCM
    path('notifications/register-fcm-token', notification_views.register_fcm_token, name='register_fcm_token'),
    path('notifications/send-push', notification_views.send_push_notification, name='send_push_notification'),
    path('notifications/list', notification_views.list_notifications, name='list_notifications'),
    path('notifications/mark-read', notification_views.mark_notification_read, name='mark_notification_read'),
]
