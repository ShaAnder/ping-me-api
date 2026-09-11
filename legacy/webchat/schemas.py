"""
OpenAPI schema extensions for the webchat app.

This module provides documentation for the message list, retrieve, update, and delete
API endpoints, including response schemas and query parameters for use with drf_spectacular.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import MessageSerializer

# --- Message List Endpoint ---
list_message_docs = extend_schema(
    responses=MessageSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="channel_id",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="ID of the channel",
            required=True,
        )
    ],
    description="List all messages in a conversation by channel_id.",
    tags=["Messages"],
)

# --- Message Retrieve Endpoint ---
retrieve_message_docs = extend_schema(
    responses=MessageSerializer,
    description="Retrieve a single message by its primary key.",
    tags=["Messages"],
)

# --- Message Partial Update Endpoint ---
partial_update_message_docs = extend_schema(
    request=MessageSerializer(partial=True),
    responses=MessageSerializer,
    description="Partially update a message (PATCH). Only the sender can update.",
    tags=["Messages"],
)

# --- Message Delete Endpoint ---
delete_message_docs = extend_schema(
    responses=None,
    description="Delete a message by its primary key. Only the sender can delete.",
    tags=["Messages"],
)
