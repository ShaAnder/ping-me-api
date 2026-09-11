"""
Custom JWT authentication middleware for Django Channels.

This middleware authenticates WebSocket connections using JWT tokens
passed as a query parameter, enabling user authentication in Channels consumers.
"""

from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()

class JWTAuthMiddleware:
    """
    Custom middleware for JWT authentication in Django Channels.

    Extracts the JWT token from the query string, authenticates the user,
    and attaches the user to the connection scope.
    """

    def __init__(self, app):
        """
        Initialize the middleware with the ASGI application.

        Args:
            app: The ASGI application instance.
        """
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        Process the incoming connection and authenticate the user.

        Args:
            scope (dict): The connection scope.
            receive: The receive callable.
            send: The send callable.

        Returns:
            Awaitable: The result of calling the wrapped application.
        """
        query_string = scope.get('query_string', b'').decode()
        token_list = parse_qs(query_string).get('token')
        user = AnonymousUser()
        if token_list:
            user = await self.get_user(token_list[0])
        scope['user'] = user
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, raw_token):
        """
        Validate the JWT token and return the associated user.

        Args:
            raw_token (str): The JWT token string.

        Returns:
            User or AnonymousUser: The authenticated user or AnonymousUser if invalid.
        """
        try:
            validated_token = UntypedToken(raw_token)
            jwt_auth = JWTAuthentication()
            user = jwt_auth.get_user(validated_token)
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()
