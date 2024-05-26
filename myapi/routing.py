from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/forum/$', consumers.ForumConsumer.as_asgi()),
]