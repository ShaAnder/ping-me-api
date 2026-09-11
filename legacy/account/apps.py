"""
App configuration for the account application.

This module defines the configuration class for the account app,
setting default behaviors and metadata for Django.
"""

from django.apps import AppConfig


class AccountConfig(AppConfig):
    """
    Configuration class for the 'account' Django application.

    Sets the default auto field and the app name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
