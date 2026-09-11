"""
ASGI config for ping_me_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ping_me_api.settings")

# Load the Django ASGI application early to ensure models are ready
django_application = get_asgi_application()

# Import after Django setup
from webchat.middleware import JWTAuthMiddleware

from .routing import websocket_urlpatterns

#: The ASGI application callable for the project.
#:
#: Handles both HTTP and WebSocket protocols, applying JWT authentication
#: middleware to WebSocket connections.
application = ProtocolTypeRouter({
    "http": django_application,
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
