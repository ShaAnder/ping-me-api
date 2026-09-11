"""
Admin configuration for the server app.

Registers the Channel, Server, and ServerCategory models with the Django admin site
to allow management through the admin interface.
"""

from django.contrib import admin

from .models import Channel, Server, ServerCategory

# Register the Channel model with the admin site.
admin.site.register(Channel)

# Register the Server model with the admin site.
admin.site.register(Server)

# Register the ServerCategory model with the admin site.
admin.site.register(ServerCategory)
