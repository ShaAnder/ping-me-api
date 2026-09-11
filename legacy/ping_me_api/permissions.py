"""
Custom permission classes for the API.

This module defines permissions to restrict editing to object owners,
with special handling for Channel and Server ownership.
"""

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.

    For Channel objects, allows both the channel owner and the server owner
    to edit. For other models, checks common owner fields.
    """

    owner_fields = ['owner', 'user', 'account']

    def has_object_permission(self, request, view, obj):
        """
        Determine if the requesting user has permission to access or modify the object.

        Allows safe methods for all users. For Channel objects, checks if the user
        is the channel owner or the server owner. For other models, checks if the
        user matches any of the common owner fields.

        Args:
            request (Request): The HTTP request object.
            view (View): The view being accessed.
            obj (Model): The object being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # Allow safe methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # For Channel: allow if channel owner or server owner
        if obj.__class__.__name__ == "Channel":
            # Check if request.user has an account
            account = getattr(request.user, "account", None)
            if not account:
                return False
            # Channel owner or server owner
            return obj.owner == account or getattr(obj.server, "owner", None) == account

        # For other models: check common owner fields (must compare to Account, not User)
        account = getattr(request.user, "account", None)
        for field in self.owner_fields:
            if hasattr(obj, field):
                return getattr(obj, field) == account
        return False
