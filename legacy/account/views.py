"""
Views for account registration, authentication, verification, and user profile management.

This module contains the AccountViewSet, which handles user registration, email verification,
resending verification emails, password reset, and user profile endpoints for the account app.
"""

import os

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from dotenv import load_dotenv
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ping_me_api.permissions import IsOwnerOrReadOnly
from ping_me_api.utils import generate_token, verify_token
from server.serializers import ServerSerializer

from .serializers import (AccountRegistrationSerializer, AccountSerializer,
                          PasswordResetConfirmSerializer,
                          PasswordResetRequestSerializer,
                          ResendVerificationSerializer)

load_dotenv()

class AccountViewSet(viewsets.ViewSet):
    """
    ViewSet for handling account registration, authentication, verification,
    password reset, and user profile management.
    """
    serializer_class = AccountSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new user account.

        Validates the provided registration data, creates a new user,
        generates a verification token, and sends a verification email.

        Args:
            request (Request): The HTTP request containing registration data.

        Returns:
            Response: Success message or validation errors.
        """

        serializer = AccountRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uidb64, token = generate_token(user)
            verify_url = f"https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/account/verify_email/?uid={uidb64}&token={token}"
            logo_url = "http://localhost:8000/static/admin/img/pingMe.png"
            html_message = render_to_string(
                'emails/verify_email.html',
                {
                    'user': user,
                    'verification_url': verify_url,
                    'logo_url': logo_url,
                }
            )
            plain_message = f"Hi {user.username}, click to verify: {verify_url}"

            send_mail(
                'Verify your email',
                plain_message,
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )
            return Response({'message': 'Registration successful. Check your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def verify_email(self, request):
        """
        Verify a user's email address.

        Validates the provided UID and token, activates the user if valid,
        and redirects to the frontend.

        Args:
            request (Request): The HTTP request containing UID and token.

        Returns:
            HttpResponseRedirect or Response: Redirects on success, error message otherwise.
        """
        uidb64 = request.GET.get('uid')
        token = request.GET.get('token')
        user = verify_token(uidb64, token)
        if user:
            user.is_active = True
            user.save()
            if os.environ.get("DEV"):
                redirect_url = os.environ.get("CLIENT_ORIGIN_DEV")
            else:
                redirect_url = os.environ.get("CLIENT_ORIGIN")
            return HttpResponseRedirect(redirect_url)
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def resend_verification(self, request):
        """
        Resend the email verification link to the user.

        Args:
            request (Request): The HTTP request containing the user's email.

        Returns:
            Response: Success message or error.
        """
        serializer = ResendVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({'message': 'Account already verified.'}, status=status.HTTP_200_OK)
            uidb64, token = generate_token(user)
            verify_url = (
                f"https://ping-me-pp5-backend-6aaeef173b97.herokuapp.com/api/account/verify_email/?uid={uidb64}&token={token}"
            )
            send_mail(
                'Verify your email',
                f"Hi {user.username}, click to verify: {verify_url}",
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Verification email resent.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'If this email is registered and not yet verified, a verification email has been sent.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset(self, request):
        """
        Send a password reset email to the user.

        Args:
            request (Request): The HTTP request containing the user's email.

        Returns:
            Response: Success message regardless of whether the email exists.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            if os.environ.get("DEV"):
                frontend_origin = os.environ.get("CLIENT_ORIGIN_DEV")
            else:
                frontend_origin = os.environ.get("CLIENT_ORIGIN")
            reset_url = f"{frontend_origin}/app/reset/{uid}/{token}"
            logo_url = "http://localhost:8000/static/admin/img/pingMe.png"
            html_message = render_to_string(
                'emails/reset_password.html',
                {
                    'user': user,
                    'reset_url': reset_url,
                    'logo_url': logo_url,
                }
            )
            plain_message = f"Hi {user.username}, click to reset your password: {reset_url}"
            send_mail(
                "Reset your PingMe password",
                plain_message,
                'pingmepp5@gmail.com',
                [user.email],
                fail_silently=False,
                html_message=html_message,
            )
        except User.DoesNotExist:
            pass
        return Response({'message': 'If this email is registered, a password reset link has been sent.'})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def password_reset_confirm(self, request):
        """
        Confirm a password reset and set a new password for the user.

        Args:
            request (Request): The HTTP request containing the UID, token, and new password.

        Returns:
            Response: Success message and redirect URL, or error message.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password1']
        try:
            uid_int = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_int)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                if os.environ.get("DEV"):
                    redirect_url = os.environ.get("CLIENT_ORIGIN_DEV")
                else:
                    redirect_url = os.environ.get("CLIENT_ORIGIN")
                return Response({
                    'message': 'Password has been reset successfully.',
                    'redirect_url': redirect_url + '/login'
                })
            else:
                return Response({'error': 'Invalid or expired token.'}, status=400)
        except Exception:
            return Response({'error': 'Invalid request.'}, status=400)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retrieve the authenticated user's account details.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: The user's account data.
        """
        account = request.user.account
        serializer = AccountSerializer(account)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly])
    def edit_me(self, request):
        """
        Edit the authenticated user's account.

        Args:
            request (Request): The HTTP request containing updated account data.

        Returns:
            Response: The updated account data.
        """
        account = request.user.account
        serializer = AccountSerializer(account, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated, IsOwnerOrReadOnly], url_path='delete_me')
    def delete_me(self, request):
        """
        Delete the authenticated user's account and associated user.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: Success message with 204 NO CONTENT status.
        """
        user = request.user
        account = user.account
        
        # Delete the account (this will cascade to related objects)
        account.delete()
        
        # Delete the user
        user.delete()
        
        return Response(
            {"message": "Account successfully deleted"}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, IsOwnerOrReadOnly],
        url_path='my_servers'
    )
    def my_servers(self, request):
        """
        Retrieve the list of servers the authenticated user is a member of.

        Args:
            request (Request): The HTTP request.

        Returns:
            Response: Serialized list of servers.
        """
        account = request.user.account
        servers = account.servers.select_related("owner", "category").prefetch_related("members", "channel_server").all()
        serializer = ServerSerializer(servers, many=True, context={'request': request})
        return Response(serializer.data)
