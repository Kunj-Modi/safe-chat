from django.urls import path
from .consumers import *

websocket_urlpatterns = [
    path('global/', GlobalConsumer.as_asgi()),
]
