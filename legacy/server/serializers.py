"""
Serializers for the server app.

Provides serializers for channels, servers, and server categories, including
custom fields and methods for image URLs and member counts.
"""

from django.db import transaction
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from .models import Channel, Server, ServerCategory


class ChannelSerializer(serializers.ModelSerializer):
    """
    Serializer for the Channel model.

    Serializes all fields of the Channel model, with the owner field as read-only.
    """
    class Meta:
        model = Channel
        fields = "__all__"
        read_only_fields = ["owner"]


class ServerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Server model.

    Includes additional fields for member count, related channels, owner info,
    category name, and server image URLs.
    """
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True, read_only=True)
    owner_id = serializers.ReadOnlyField(source="owner.id")
    owner = serializers.ReadOnlyField(source="owner.owner.username")
    category_name = serializers.CharField(source="category.name", read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_server_image_urls(self, obj):
        """
        Retrieve URLs for the server's icon and banner images.

        Args:
            obj (Server): The server instance.

        Returns:
            dict: Dictionary with image URLs, if available.
        """
        image_urls = {}
        if obj.server_icon:
            url = obj.server_icon.url
            # Force HTTPS for Cloudinary URLs
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            image_urls["server_icon_url"] = url
        if obj.banner_image:
            url = obj.banner_image.url
            # Force HTTPS for Cloudinary URLs
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            image_urls["banner_image_url"] = url
        return image_urls

    server_image_urls = serializers.SerializerMethodField()
    server_icon = serializers.ImageField(write_only=True, required=False)
    banner_image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Server
        fields = "__all__"

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_num_members(self, obj):
        """
        Get the number of members for the server.

        Args:
            obj (Server): The server instance.

        Returns:
            int or None: The number of members, if available.
        """
        if hasattr(obj, "num_members"):
            return obj.num_members
        return None

    def to_representation(self, instance):
        """
        Customize the serialized representation of the server.

        Removes the num_members field if not present in the context.

        Args:
            instance (Server): The server instance.

        Returns:
            dict: The serialized data.
        """
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members", None)
        return data


class ServerCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ServerCategory model.

    Includes a method for retrieving the category icon URL.
    """
    class Meta:
        model = ServerCategory
        fields = "__all__"

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_category_icon_url(self, obj):
        """
        Retrieve the URL for the category's icon image.

        Args:
            obj (ServerCategory): The server category instance.

        Returns:
            str or None: The image URL, if available.
        """
        image = getattr(obj, "category_image", None)
        if image and hasattr(image, "url"):
            url = image.url
            # Force HTTPS for Cloudinary URLs
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None

    category_icon_url = serializers.SerializerMethodField()
    category_icon = serializers.ImageField(write_only=True, required=False)
    permission_classes = [AllowAny]
