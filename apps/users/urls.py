from django.urls import path
from apps.users.views import auth_views

urlpatterns = [
    path("login", auth_views.login, name="login"),
    path("signup", auth_views.signup, name="signup"),
    path("test", auth_views.test, name="test"),
]
