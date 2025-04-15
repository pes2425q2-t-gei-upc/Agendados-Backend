from django.urls import path
from apps.users.views import auth_views, friendship_views

urlpatterns = [
    #Auth urls
    path("login", auth_views.login, name="login"),
    path("signup", auth_views.signup, name="signup"),
    path("test", auth_views.test, name="test"),
    #Friendship urls
    path("friendships", friendship_views.get_friendships, name="friendships"),
]
