import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import myapi.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Manejador HTTP de Django
    'websocket':AuthMiddlewareStack(
        URLRouter(
            myapi.routing.websocket_urlpatterns
        )
    )
})

