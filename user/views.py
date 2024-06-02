import logging

import requests
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from talent_buzz.settings import PLATFORM_DOMAIN
from .serializers import UserSerializer, PasswordResetSerializer, SetPasswordSerializer

logger = logging.getLogger(__name__)

GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
User = get_user_model()


def save_user(serializer, password):
    instance = serializer.save(is_active=False)
    instance.set_password(password)
    instance.save()
    return instance


def generate_token_and_uid(instance):
    uidb64 = urlsafe_base64_encode(force_bytes(instance.pk))
    token = default_token_generator.make_token(instance)
    return uidb64, token


def send_activation_email(instance, uidb64, token):
    instance.send_activation_email(uidb64, token)


class UserCreateView(generics.CreateAPIView):
    """
       User Registration Endpoint.

       Use this endpoint to register a new user. Once successfully registered,
       an activation email will be sent to the provided email address.

       POST Data:
       - `username`: Desired username.
       - `email`: User's email address.
       - `password`: User's password.

       Returns:
       - 201 Created if registration is successful.
       - 400 Bad Request if there are input errors.
       """
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        instance = save_user(serializer, password)
        uidb64, token = generate_token_and_uid(instance)
        send_activation_email(instance, uidb64, token)


class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow owners of an account or admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return obj == request.user or request.user.is_staff
        if request.method == 'GET':
            return obj == request.user
        return False


class UserEditView(generics.RetrieveUpdateAPIView):
    """
        User Edit Endpoint.

        Use this endpoint to retrieve or edit user information. Only the user
        themselves or an admin can access and edit this information.

        Returns:
        - 200 OK if retrieval or update is successful.
        - 400 Bad Request if there are input errors.
        - 403 Forbidden if unauthorized access.
        """
    permission_classes = (IsAdminOrSelf,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        # Check if password is included in the request
        password = self.request.data.get('password')
        instance = serializer.save()
        if password:
            instance.set_password(password)
            instance.save()


class PasswordResetView(APIView):
    """
        Password Reset Request Endpoint.
        If the provided email is associated with an account, this endpoint sends a password
        reset email containing a link to set a new password.
        POST Data:
        - `email`: Email address associated with the account.
        Returns:
        - 200 OK if password reset email is sent successfully.
        - 400 Bad Request if there are errors.
    """

    EMAIL_SUBJECT = 'Password Reset Requested'
    PERMISSION_CLASSES = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                self.send_reset_email(user)
                return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
            return Response({"error": "Email not found."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_reset_email(self, user):
        # Generate token and uid
        token = default_token_generator.make_token(user)
        unique_user_id_base64 = urlsafe_base64_encode(force_bytes(user.pk))
        message = self.build_message(user, unique_user_id_base64, token)
        from_email = EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(self.EMAIL_SUBJECT, message, from_email, recipient_list)

    def build_message(self, user, unique_user_id_base64, token):
        message = f'Hi {user.username},\n\nYou requested a password reset.' \
                  f'Click the link below to reset your password:\n\n' \
                  f'{PLATFORM_DOMAIN}/set-password/{unique_user_id_base64}/{token}/\n\n' \
                  f'If you did not request this, please ignore this email.\n\nThanks,' \
                  '\nYour Team'

        return message


class SetPasswordView(APIView):
    permission_classes = (AllowAny,)
    """
    Set Password Endpoint.

    Use this endpoint to set a user's password. You will need a valid UID and token, typically generated 
    and sent to the user's email when they request a password reset.

    POST Data:
    - `password`: The new password.
    - `password_confirm`: Confirmation of the new password.

    Returns:
    - 200 OK if password reset is successful.
    - 400 Bad Request if there are errors, e.g., mismatching passwords or invalid token/UID.
    """

    def post(self, request, uidb64, token):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = urlsafe_base64_decode(uidb64)
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, token):
                password = serializer.validated_data['password']
                password_confirm = serializer.validated_data['password_confirm']
                if password == password_confirm:
                    user.set_password(password)
                    user.save()
                    return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Invalid token or UID."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    """
    Account Activation Endpoint.

    Use this endpoint to activate a user account. Requires a valid UID and token,
    typically provided in the activation email sent upon registration.

    Returns:
     - 200 OK if account activation is successful.
        - 400 Bad Request if there's an error, like an invalid token or UID.
     """
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and not user.is_active and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid token or UID."}, status=status.HTTP_400_BAD_REQUEST)


class GoogleLoginView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def login_or_signup(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({"detail": "access_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = self.get_google_user_info(access_token)
        if not user_info:
            return Response({"detail": "Error fetching user information from Google."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = self.get_or_create_user(user_info)

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token, "refresh_token": str(refresh)}, status=status.HTTP_200_OK)

    @staticmethod
    def get_google_user_info(access_token):
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(GOOGLE_USER_INFO_URL, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error fetching Google user info: {response.text}")
            return None

        return response.json()

    @staticmethod
    def get_or_create_user(user_info):
        user = User.objects.filter(email=user_info.get("email")).first()
        if not user:
            user = User.objects.create_user(
                first_name=user_info.get("given_name", ""),
                last_name=user_info.get("family_name", ""),
                email=user_info.get("email", ""),
                username=user_info.get("email", ""),
                is_active=True
            )
        return user


class FacebookLoginView(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def login_or_signup(self, request):
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({"detail": "access_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_info = self.get_facebook_user_info(access_token)
        if not user_info:
            return Response({"detail": "Error fetching user information from Google."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = self.get_or_create_user(user_info)

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token, "refresh_token": str(refresh)}, status=status.HTTP_200_OK)

    @staticmethod
    def get_facebook_user_info(access_token):
        params = {
            'fields': 'id,name,email,picture',
            'access_token': access_token
        }

        response = requests.get("https://graph.facebook.com/v13.0/me", params=params)

        # If the request was successful, parse the data
        if response.status_code == 200:
            user_data = response.json()
            print(user_data)
            return user_data
        else:
            print("Error:", response.json())

    @staticmethod
    def get_or_create_user(user_info):
        user = User.objects.filter(email=user_info.get("email")).first()
        if not user:
            user = User.objects.create_user(
                first_name=user_info.get("given_name", ""),
                last_name=user_info.get("family_name", ""),
                email=user_info.get("email", ""),
                is_active=True
            )
        return user


# @login_required
class GetUserIdView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_id = user.id
        return Response({'user_id': user_id})
