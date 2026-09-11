"""
App configuration for the server application.

Defines the configuration class for the server app, setting default behaviors and metadata.
"""

from django.apps import AppConfig


class ServerConfig(AppConfig):
    """
    Configuration class for the 'server' Django application.

    Sets the default auto field and the app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "server"
