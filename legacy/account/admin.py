"""
Admin configuration for the Account model.

This module registers the Account model with the Django admin site,
allowing it to be managed through the Django admin interface.
"""

from django.contrib import admin

from .models import Account

# Register the Account model with the Django admin site.
admin.site.register(Account)
