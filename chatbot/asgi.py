import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
import myapi.routing
from channels.auth import AuthMiddlewareStack



application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Manejador HTTP de Django
    'websocket':AuthMiddlewareStack(
        URLRouter(
            myapi.routing.websocket_urlpatterns
        )
    )
})

