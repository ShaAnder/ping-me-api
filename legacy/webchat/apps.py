"""
App configuration for the webchat application.

Defines the configuration class for the webchat app, setting default behaviors and metadata.
"""

from django.apps import AppConfig


class WebchatConfig(AppConfig):
    """
    Configuration class for the 'webchat' Django application.

    Sets the default auto field and the app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "webchat"
