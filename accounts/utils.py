from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import activation_token

domain = Site.objects.get_current().domain


def get_website_url(request):
    protocol = "https" if request.is_secure() else "http"
    return protocol + "://" + domain


def send_verification_email(request, user):
    token = activation_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    url = reverse(
        "accounts:email_verification", kwargs={"uidb64": uidb64, "token": token}
    )
    activation_link = get_website_url(request) + url
    subject = "Account Verification"
    body = (
        "Hi, "
        + user.first_name
        + " "
        + user.last_name
        + f"\nWelcome to {domain}. Click this link to verify your account.\n"
        + activation_link
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject, body, f"{domain} <{from_email}>", [user.email]
    )
    msg.send(fail_silently=False)


def send_verification_email_for_change_email(request, email):
    user = request.user
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    emailb64 = urlsafe_base64_encode(force_bytes(email))
    token = activation_token.make_token(user)
    url = reverse(
        "accounts:change_email_verification",
        kwargs={"uidb64": uidb64, "emailb64": emailb64, "token": token},
    )
    activation_link = get_website_url(request) + url
    subject = "Verify New Email Address"
    body = (
        "Hi, "
        + user.first_name
        + " "
        + user.last_name
        + f"\nWelcome to {domain}. Click this link to verify your email.\n"
        + activation_link
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject, body, f"{domain} <{from_email}>", [user.email]
    )
    msg.send(fail_silently=False)


def send_reset_password_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    url = reverse(
        "accounts:reset_password_email", kwargs={"uidb64": uidb64, "token": token}
    )
    activation_link = get_website_url(request) + url
    subject = "Reset your password"
    body = (
        "Hi, "
        + user.first_name
        + " "
        + user.last_name
        + f"\nWelcome to {domain}. Click this link to reset password your account.\n"
        + activation_link
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(
        subject, body, f"{domain} <{from_email}>", [user.email]
    )
    msg.send(fail_silently=False)
