"""
WebSocket URL routing for the webchat app.

Defines the URL patterns for WebSocket connections to chat channels,
linking server and channel IDs to the ChatConsumer.
"""

from django.urls import path

from webchat import consumer

#: List of WebSocket URL patterns for chat channels.
#:
#: Each path routes a WebSocket connection to the ChatConsumer,
#: using dynamic server and channel IDs.
websocket_urlpatterns = [
    path('<str:serverId>/<str:channelId>', consumer.ChatConsumer.as_asgi()),
]
