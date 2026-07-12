import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.asgi import get_asgi_application
from notifications.routing import websocket_urlpatterns

from channels.routing import ProtocolTypeRouter, URLRouter

from notifications.jwt_middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({

    "http": get_asgi_application(),

    "websocket":
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        ),

})