from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('chat/<str:other>', ChatConsumer.as_asgi()),
]
