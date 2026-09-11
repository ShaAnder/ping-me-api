"""
OpenAPI schema extensions for the account app.

This module defines documentation for all major account-related API endpoints,
including registration, verification, password reset, and user profile management,
for use with drf_spectacular.
"""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from server.serializers import ServerSerializer

from .serializers import (AccountRegistrationSerializer, AccountSerializer,
                          PasswordResetConfirmSerializer,
                          PasswordResetRequestSerializer,
                          ResendVerificationSerializer)

# --- Account Registration ---
register_account_docs = extend_schema(
    request=AccountRegistrationSerializer,
    responses={201: None, 400: None},
    description="Register a new user account. Sends a verification email.",
    tags=["Account"],
)

# --- Email Verification ---
verify_email_docs = extend_schema(
    parameters=[
        OpenApiParameter(
            name="uid",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Base64-encoded user ID",
            required=True,
        ),
        OpenApiParameter(
            name="token",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Verification token",
            required=True,
        ),
    ],
    responses={302: None, 400: None},
    description="Verify a user's email address using UID and token.",
    tags=["Account"],
)

# --- Resend Verification Email ---
resend_verification_docs = extend_schema(
    request=ResendVerificationSerializer,
    responses={200: None},
    description="Resend the email verification link to the user.",
    tags=["Account"],
)

# --- Password Reset Request ---
password_reset_docs = extend_schema(
    request=PasswordResetRequestSerializer,
    responses={200: None},
    description="Send a password reset email to the user.",
    tags=["Account"],
)

# --- Password Reset Confirm ---
password_reset_confirm_docs = extend_schema(
    request=PasswordResetConfirmSerializer,
    responses={200: None, 400: None},
    description="Confirm a password reset and set a new password for the user.",
    tags=["Account"],
)

# --- Get Authenticated User Profile ---
me_docs = extend_schema(
    responses=AccountSerializer,
    description="Retrieve the authenticated user's account details.",
    tags=["Account"],
)

# --- Edit Authenticated User Profile ---
edit_me_docs = extend_schema(
    request=AccountSerializer(partial=True),
    responses=AccountSerializer,
    description="Edit the authenticated user's account.",
    tags=["Account"],
)

# --- List User's Servers ---
my_servers_docs = extend_schema(
    responses=ServerSerializer(many=True),
    description="Retrieve the list of servers the authenticated user is a member of.",
    tags=["Account"],
)

# --- (Optional) Account List Endpoint ---
account_list_docs = extend_schema(
    responses=AccountSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="user",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="User ID",
        ),
    ],
    description="List accounts, optionally filtering by user ID.",
    tags=["Account"],
)
