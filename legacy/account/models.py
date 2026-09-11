"""
Defines the Account model and signal for automatic account creation.

This module extends Django's User model with additional profile information
and sets up a signal to create an Account instance whenever a new User is created.
"""

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Account(models.Model):
    """
    User profile model extending the default Django User.

    Stores additional user information such as location, profile image,
    and content, and links to the User model with a one-to-one relationship.
    """

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="account"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True)
    image = CloudinaryField(
        "image", folder="Avatars", default="default_profile_uxlg3a.jpg", blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """
        Return a string representation of the Account.

        Returns:
            str: The username of the account owner.
        """
        return f"{self.owner}"


def create_account(sender, instance, created, **kwargs):
    """
    Signal handler to create an Account instance when a new User is created.

    Args:
        sender (Model): The model class sending the signal.
        instance (User): The instance of the User being saved.
        created (bool): Whether this is a new User instance.
        **kwargs: Additional keyword arguments.
    """
    if created:
        Account.objects.create(owner=instance, username=instance.username)


# Connect the create_account signal handler to the User post_save signal.
post_save.connect(create_account, sender=User)
