"""
URL configuration for agendadosDjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from apps.events.views import external_service_views
from apps.users.views import reset_password_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/events/", include("apps.events.urls")),
    path("api/locations/", include("apps.locations.urls")),
    path("api/eventsInArea", external_service_views.get_events_in_area, name="get_events_in_area"),
    path("api/chat/", include("apps.chat.urls")),
    path("reset-password/<uidb64>/<token>/", reset_password_views.ResetPasswordView.as_view(), name="reset_password"),
]
