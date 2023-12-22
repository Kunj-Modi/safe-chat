import os

from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from global_chat.routing import websocket_urlpatterns as global_ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safe_chat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
                    AuthMiddlewareStack(
                        URLRouter(
                            global_ws_urlpatterns
                        )
                    )
                )
})
