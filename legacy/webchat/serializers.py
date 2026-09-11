"""
Serializers for the webchat app.

Defines the MessageSerializer for serializing message data, including user details.
"""

from rest_framework import serializers

from account.serializers import AccountSerializer

from .models import Messages


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Messages model.

    Includes the related user's account details, message content, and timestamps.
    """
    user = AccountSerializer(source='sender.account', read_only=True)

    class Meta:
        model = Messages
        fields = [
            "id",
            "user",
            "content",
            "timestamp_created",
            "timestamp_updated",
        ]
