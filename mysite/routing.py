from django.urls import re_path
from .consumer import RoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<pk>\d+)/$', RoomConsumer.as_asgi()),
]
