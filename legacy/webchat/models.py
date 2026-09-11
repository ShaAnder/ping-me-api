"""
Models for the webchat application.

Defines ConversationModel for chat channels and Messages for individual chat messages.
"""

from django.contrib.auth import get_user_model
from django.db import models


class ConversationModel(models.Model):
    """
    Model representing a chat conversation within a channel.

    Fields:
        channel_id (str): The unique identifier for the channel.
        created_at (datetime): Timestamp when the conversation was created.
    """
    channel_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the conversation.

        Returns:
            str: Channel ID.
        """
        return f"Conversation in channel {self.channel_id}"


class Messages(models.Model):
    """
    Model representing a message in a conversation.

    Fields:
        conversation (ConversationModel): The related conversation.
        sender (User): The user who sent the message.
        content (str): The message content.
        timestamp_created (datetime): When the message was created.
        timestamp_updated (datetime): When the message was last updated.
    """
    conversation = models.ForeignKey(
        ConversationModel,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    content = models.TextField()
    timestamp_created = models.DateTimeField(auto_now_add=True)
    timestamp_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the message.

        Returns:
            str: Short preview of the message content.
        """
        return f"Message by {self.sender} in {self.conversation}: {self.content[:30]}"
