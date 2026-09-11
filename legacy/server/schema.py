"""
OpenAPI schema extensions for the server app.

This module defines documentation for all major server-related API endpoints,
including server listing, creation, member management, and category/channel endpoints,
for use with drf_spectacular.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializers import (ChannelSerializer, ServerCategorySerializer,
                          ServerSerializer)

# --- Server List Endpoint ---
server_list_docs = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of servers to retrieve",
        ),
        OpenApiParameter(
            name="qty",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Number of servers to retrieve",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter servers by the current authenticated user (True/False)",
        ),
        OpenApiParameter(
            name="with_num_members",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the number of members for each server in your response",
        ),
        OpenApiParameter(
            name="by_serverid",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Include server by ID",
        ),
    ],
    description="List servers with optional filters such as category, user, and member count.",
    tags=["Server"],
)

# --- Server Retrieve Endpoint ---
server_retrieve_docs = extend_schema(
    responses=ServerSerializer,
    description="Retrieve a single server by its ID.",
    tags=["Server"],
)

# --- Server Create Endpoint ---
server_create_docs = extend_schema(
    request=ServerSerializer,
    responses=ServerSerializer,
    description="Create a new server. The authenticated user becomes the owner and first member.",
    tags=["Server"],
)

# --- Server Add Member Endpoint ---
server_add_member_docs = extend_schema(
    responses=None,
    description="Add the authenticated user as a member to the specified server.",
    tags=["Server"],
)

# --- Server Remove Member Endpoint ---
server_remove_member_docs = extend_schema(
    responses=None,
    description="Remove the authenticated user from the specified server's members.",
    tags=["Server"],
)

# --- ServerCategory List/Retrieve Endpoints ---
server_category_list_docs = extend_schema(
    responses=ServerCategorySerializer(many=True),
    description="List all server categories.",
    tags=["ServerCategory"],
)
server_category_retrieve_docs = extend_schema(
    responses=ServerCategorySerializer,
    description="Retrieve a single server category by ID.",
    tags=["ServerCategory"],
)

# --- Channel List/Create/Retrieve Endpoints ---
channel_list_docs = extend_schema(
    responses=ChannelSerializer(many=True),
    description="List all channels.",
    tags=["Channel"],
)
channel_create_docs = extend_schema(
    request=ChannelSerializer,
    responses=ChannelSerializer,
    description="Create a new channel.",
    tags=["Channel"],
)
channel_retrieve_docs = extend_schema(
    responses=ChannelSerializer,
    description="Retrieve a single channel by ID.",
    tags=["Channel"],
)
