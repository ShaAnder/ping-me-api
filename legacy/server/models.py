"""
Models for the server application.

Defines the ServerCategory, Server, and Channel models, which represent
server categories, individual servers, and channels within servers.
"""

from cloudinary.models import CloudinaryField
from django.db import models

from account.models import Account


class ServerCategory(models.Model):
    """
    Model representing a category for servers.

    Attributes:
        name (str): The category name.
        description (str): Optional description of the category.
        category_image (CloudinaryField): Image representing the category.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category_image = CloudinaryField(
        "image", folder="ServerCategories", default="default_server_uxlg3a.jpg"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Save the category, ensuring the name is stored in lowercase.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.name = self.name.lower()
        super(ServerCategory, self).save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the category.

        Returns:
            str: The category name.
        """
        return self.name


class Server(models.Model):
    """
    Model representing a server.

    Attributes:
        name (str): The server name.
        owner (Account): The account that owns the server.
        category (ServerCategory): The category this server belongs to.
        description (str): Optional server description.
        members (ManyToMany[Account]): Members of the server.
        server_icon (CloudinaryField): Icon image for the server.
        banner_image (CloudinaryField): Banner image for the server.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
        is_private (bool): Whether the server is private.
    """

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="server_owner"
    )
    category = models.ForeignKey(
        ServerCategory, on_delete=models.PROTECT,
        related_name="server_category"
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    members = models.ManyToManyField(Account, related_name="servers")
    server_icon = CloudinaryField(
        "server icon", folder="ServerIcons",
        default="default_server_uxlg3a.jpg"
    )
    banner_image = CloudinaryField(
        "server banner", folder="ServerIcons",
        default="default_server_uxlg3a.jpg"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        """
        Return a string representation of the server.

        Returns:
            str: The server's category, ID, and name.
        """
        return f"[{self.category}]: [{self.id}] - {self.name}"


class Channel(models.Model):
    """
    Model representing a channel within a server.

    Attributes:
        name (str): The channel name.
        owner (Account): The account that owns the channel.
        type (str): The type of channel (e.g., text).
        server (Server): The server this channel belongs to.
        description (str): Optional channel description.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
    """

    text = "text"

    CHANNEL_TYPE_CHOICES = [
        (text, "Text"),
    ]

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="channel_owner"
    )
    type = models.CharField(
        max_length=5,
        choices=CHANNEL_TYPE_CHOICES,
        default=text,
    )
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="channel_server"
    )
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Save the channel, ensuring the name is stored in lowercase.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.name = self.name.lower()
        super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        """
        Return a string representation of the channel.

        Returns:
            str: The channel name.
        """
        return self.name
