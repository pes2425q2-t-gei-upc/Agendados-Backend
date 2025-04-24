from django.urls import path
from apps.users.views import auth_views, friendship_views, user_views

urlpatterns = [
    #Auth urls
    path("login", auth_views.login, name="login"),
    path("signup", auth_views.signup, name="signup"),
    path("test", auth_views.test, name="test"),
    #Friendship urls
    path("friendships", friendship_views.get_friendships, name="friendships"),
    path("friendships/<int:user_id>", friendship_views.send_friend_request, name="send_friend_request"),
    path("friendships/accept/<int:request_id>", friendship_views.accept_friend_request, name="accept_friend_request"),
    path("friendships/decline/<int:request_id>", friendship_views.decline_friend_request, name="decline_friend_request"),
    path("friendships/pending", friendship_views.get_pending_friend_requests, name="get_pending_friend_requests"),
    path("/", user_views.get_users, name="get_users"),
]
