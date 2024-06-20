import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  
})

