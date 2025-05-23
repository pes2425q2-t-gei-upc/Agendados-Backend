import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agendadosDjango.settings')
django.setup()

from apps import chat, private_rooms
import apps.chat.routing
import apps.private_rooms.routing
from apps.chat.auth_middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            private_rooms.routing.websocket_urlpatterns
        )
    ),
})

application = TokenAuthMiddleware(application)
