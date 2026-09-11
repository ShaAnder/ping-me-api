"""
Serializers for the Account app.

This module provides serializers for account creation, registration,
verification, and password reset processes, as well as user profile retrieval.
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ping_me_api.utils import validate_image_file  # Adjust path if needed
from server.serializers import ServerSerializer

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.

    Handles serialization and validation for user account data,
    including image upload and user profile retrieval.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        Validate the uploaded image file.

        Args:
            value (File): The uploaded image file.

        Returns:
            File: The validated image file.
        """
        return validate_image_file(value)

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_image_url(self, obj):
        """
        Retrieve the URL of the user's profile image.

        Args:
            obj (Account): The account instance.

        Returns:
            str or None: The URL of the image or None if not set.
        """
        if obj.image:
            url = obj.image.url
            # Force HTTPS for Cloudinary URLs
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retrieve the authenticated user's account details and servers.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The response containing account and server data.
        """
        user = request.user
        account = user.account
        servers = account.servers.all()

        return Response({
            "id": account.id,
            "username": account.username,
            "email": user.email,
            "avatar": account.image.url if account.image else None,
            "servers": ServerSerializer(servers, many=True).data,
        })

    class Meta:
        """
        Meta options for AccountSerializer.
        """
        model = Account
        fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
            "username",
            "location",
            "content",
            "image",
            "image_url",
        ]


class AccountRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Handles user creation, email validation, and password validation.
    """
    email2 = serializers.EmailField(write_only=True)

    class Meta:
        """
        Meta options for AccountRegistrationSerializer.
        """
        model = User
        fields = ['username', 'email', 'email2', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """
        Validate that both emails match and are not already registered.

        Args:
            data (dict): The input data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If emails do not match or already exist.
        """
        if data['email'] != data['email2']:
            raise serializers.ValidationError("Emails must match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already registered.")
        return data

    def validate_password(self, value):
        """
        Validate the user's password using Django's validators.

        Args:
            value (str): The password.

        Returns:
            str: The validated password.

        Raises:
            ValidationError: If the password is not valid.
        """
        validate_password(value)
        return value

    def create(self, validated_data):
        """
        Create a new user with the provided validated data.

        Args:
            validated_data (dict): The validated registration data.

        Returns:
            User: The created user instance.
        """
        validated_data.pop('email2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Inactive until email is verified
        )
        return user


class ResendVerificationSerializer(serializers.Serializer):
    """
    Serializer for resending verification emails.

    Validates the email field for the resend verification process.
    """
    email = serializers.EmailField()


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    Validates the email field for the password reset request.
    """
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.

    Validates the reset token and new passwords.
    """
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate that the two new passwords match and are valid.

        Args:
            data (dict): The input data.

        Returns:
            dict: The validated data.

        Raises:
            serializers.ValidationError: If passwords do not match or are invalid.
        """
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data['new_password1'])
        return data
