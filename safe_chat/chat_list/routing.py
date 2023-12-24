from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('list/', ChatListConsumer.as_asgi()),
]
