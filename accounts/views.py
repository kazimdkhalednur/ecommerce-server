from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404
from django.shortcuts import redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView, Response

from .models import User
from .serializers import *
from .tokens import activation_token
from .utils import (
    send_reset_password_email,
    send_verification_email,
    send_verification_email_for_change_email,
)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save(is_active=False)
            send_verification_email(request, user)

            return Response(
                {"success": "User created Successfully"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerSignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(role="seller", is_active=False)
            send_verification_email(request, user)

            return Response(
                {"success": "User created Successfully"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token, format=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and activation_token.check_token(user, token):
            user.is_active = True
            user.save()

            return redirect(
                settings.CLIENT_URL + "/email-verified",
                status=status.HTTP_301_MOVED_PERMANENTLY,
            )
        return Http404


class EmailChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        serializer = EmailChangeSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            send_verification_email_for_change_email(request, email)
            return Response(
                {"success": "send verification email successdully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeEmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, emailb64, token, format=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            email = force_str(urlsafe_base64_decode(emailb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if (
            user is not None
            and user.is_active
            and activation_token.check_token(user, token)
        ):
            user.email = email
            user.save()

            return redirect(
                settings.CLIENT_URL + "/email-changed",
                status=status.HTTP_301_MOVED_PERMANENTLY,
            )
        return Http404


class PasswordChangeView(APIView):
    def patch(self, request, format=None):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"success": "Password Updated"}, status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordCheckView(APIView):
    def post(self, request, format=None):
        serializer = PasswordCheckSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            return Response({"success": "Correct password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(APIView):
    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = PasswordResetEmailSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data["email"])
            send_reset_password_email(request, user)

            return Response(
                {"success": "Reset password email send successfully"},
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerificationView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, uidb64, token, format=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if (
            user is not None
            and user.is_active
            and default_token_generator.check_token(user, token)
        ):
            serializer = PasswordResetSerializer(
                data=request.data, context={"user": user}
            )

            if serializer.is_valid():
                serializer.save()

                return redirect(
                    settings.CLIENT_URL + "/password-reset-done",
                    status=status.HTTP_301_MOVED_PERMANENTLY,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Http404
