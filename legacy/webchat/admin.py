"""
Admin configuration for the webchat app.

Registers the ConversationModel and Messages models with the Django admin site
to allow management through the admin interface.
"""

from django.contrib import admin

from .models import ConversationModel, Messages

# Register the ConversationModel with the admin site.
admin.site.register(ConversationModel)

# Register the Messages model with the admin site.
admin.site.register(Messages)
