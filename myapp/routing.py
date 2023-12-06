from django.urls import path
from . import consumers

webscoket_urlspatterns = [
    path('ws/sc/chat/<str:chat_with>/',consumers.MySyncConsumer.as_asgi()),
    path('ws/sc/status/',consumers.OnlineStatusConsumer.as_asgi()),
    path('ws/asc/',consumers.MyAsyncConsumer.as_asgi()),
]