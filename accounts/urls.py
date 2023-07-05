from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

app_name = "accounts"
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="buyer_signup"),
    path("signup/seller/", SellerSignUpView.as_view(), name="seller_signup"),
    path(
        "verification/<uidb64>/<token>/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("change/email/", EmailChangeView.as_view(), name="change_email"),
    path(
        "verification/<uidb64>/<emailb64>/<token>/",
        ChangeEmailVerificationView.as_view(),
        name="change_email_verification",
    ),
    path("change/password/", PasswordChangeView.as_view(), name="change_password"),
    path("check/password/", PasswordCheckView.as_view(), name="check_password"),
    path("reset-password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "reset-password/<uidb64>/<token>/",
        PasswordResetVerificationView.as_view(),
        name="reset_password_email",
    ),
    path("data/", UserDataView.as_view(), name="data"),
]
