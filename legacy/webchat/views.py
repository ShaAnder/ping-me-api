"""
ViewSet and permissions for message management in the webchat app.

Includes custom permissions and API endpoints for listing, retrieving,
updating, and deleting messages in conversations.
"""

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import ConversationModel, Messages
from .serializers import MessageSerializer


class IsSenderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to edit or delete it.

    Allows safe methods (GET, HEAD, OPTIONS) for all users.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request should be permitted.

        Args:
            request (Request): The incoming HTTP request.
            view (View): The view being accessed.
            obj (Messages): The message object.

        Returns:
            bool: True if safe method or sender is the user, else False.
        """
        return request.method in permissions.SAFE_METHODS or obj.sender == request.user


class MessageViewSet(viewsets.ViewSet):
    """
    ViewSet for managing messages.

    Provides list, retrieve, partial update, and delete actions for messages.
    """
    permission_classes = [permissions.IsAuthenticated, IsSenderOrReadOnly]

    def list(self, request):
        """
        List all messages in a conversation by channel_id.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: List of serialized messages or an empty list.
        """
        channel_id = request.query_params.get("channel_id")
        conversation = ConversationModel.objects.filter(channel_id=channel_id).select_related().first()
        if conversation:
            messages = conversation.messages.select_related("conversation").select_related("sender").all()
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        return Response([])

    def retrieve(self, request, pk=None):
        """
        Retrieve a single message by its primary key.

        Args:
            request (Request): The incoming HTTP request.
            pk (int): The primary key of the message.

        Returns:
            Response: Serialized message data or 404 if not found.
        """
        try:
            msg = Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, msg)
        serializer = MessageSerializer(msg)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """
        Partially update a message (PATCH).

        Args:
            request (Request): The incoming HTTP request.
            pk (int): The primary key of the message.

        Returns:
            Response: Updated serialized data or errors.
        """
        try:
            msg = Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, msg)
        serializer = MessageSerializer(msg, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Delete a message by its primary key.

        Args:
            request (Request): The incoming HTTP request.
            pk (int): The primary key of the message.

        Returns:
            Response: 204 NO CONTENT if deleted, 404 if not found.
        """
        try:
            msg = Messages.objects.get(pk=pk)
        except Messages.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, msg)
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
