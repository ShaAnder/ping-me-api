"""
WebSocket consumer for real-time chat functionality in the webchat app.

Defines the ChatConsumer for handling WebSocket connections, message broadcasting,
and message persistence in chat channels.
"""

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import ConversationModel, Messages

User = get_user_model()

class ChatConsumer(JsonWebsocketConsumer):
    """
    WebSocket consumer for handling chat messages in a channel.

    Handles connection, message receipt, broadcasting, and disconnect logic.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the consumer and set default attributes.
        """
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        """
        Handle WebSocket connection.

        Extracts server and channel IDs from the URL, authenticates the user,
        and joins the appropriate room group for message broadcasting.
        """
        self.server_id  = self.scope["url_route"]["kwargs"]["serverId"]
        self.channel_id = self.scope["url_route"]["kwargs"]["channelId"]

        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            self.close()
            return

        # Build a unique room name to prevent ID collisions across servers
        self.room_group_name = f"chat_s{self.server_id}_c{self.channel_id}"
        
        # Accept the WebSocket connection and join the group
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

    def receive_json(self, content, **kwargs):
        """
        Handle receipt of a JSON message from the WebSocket.

        Saves the message to the database and broadcasts it to the room group.

        Args:
            content (dict): The JSON message content.
            **kwargs: Additional keyword arguments.
        """
        channel_id = self.channel_id
        sender = self.user
        message = content["message"]

        conversation, created = ConversationModel.objects.get_or_create(channel_id=channel_id)
        new_message = Messages.objects.create(conversation=conversation, sender=sender, content=message)

        # Get sender's Account and avatar image URL
        account = getattr(sender, "account", None)
        avatar_url = None
        if account and account.image:
            avatar_url = account.image.url
            # Force HTTPS for Cloudinary URLs
            if avatar_url.startswith('http://'):
                avatar_url = avatar_url.replace('http://', 'https://', 1)
        sender_username = account.username if account else sender.username

        print("Sender:", sender)
        print("Account:", account)
        print("Account image:", account.image if account else None)
        print("Avatar URL:", avatar_url)

        # Only broadcast to the exact room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "new_message": {
                    "id": new_message.id,
                    "user": {
                        "id": sender.id,
                        "username": sender_username,
                        "image_url": avatar_url,
                    },
                    "content": new_message.content,
                    "timestamp_created": new_message.timestamp_created.isoformat(),
                    "timestamp_updated": new_message.timestamp_updated.isoformat(),
                }
            }
        )

    def chat_message(self, event):
        """
        Handler for broadcasting a chat message to all sockets in the room group.

        Args:
            event (dict): The event data containing the new message.
        """
        self.send_json({
            "message": event["new_message"]
        })

    def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        Removes the socket from the room group.
        
        Args:
            close_code (int): The close code for the WebSocket connection.
        """
        if hasattr(self, "room_group_name"):
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )
        super().disconnect(close_code)
