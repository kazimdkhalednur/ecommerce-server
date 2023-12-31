"""
Django settings for root project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import json
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# read config.json file
with open(BASE_DIR / "config.json", "r") as file:
    CONFIG = json.loads(file.read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get("DEBUG")

ALLOWED_HOSTS = [ALLOWED_HOST for ALLOWED_HOST in CONFIG.get("ALLOWED_HOSTS")]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # my apps
    "accounts.apps.AccountsConfig",
    "products.apps.ProductsConfig",
    # third party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "mptt",
    "ckeditor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "root.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": CONFIG.get("DB_ENGINE"),
        "NAME": CONFIG.get("DB_NAME"),
        "USER": CONFIG.get("DB_USER"),
        "PASSWORD": CONFIG.get("DB_PASSWORD"),
        "HOST": CONFIG.get("DB_HOST"),
        "PORT": CONFIG.get("DB_PORT"),
    }
}


AUTH_USER_MODEL = "accounts.User"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_TZ = True


SITE_ID = 1


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "image/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# rest_framework configurations
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# rest_framework JWT configurations
SIMPLE_JWT_SECRET_KEY = CONFIG.get("SIMPLE_JWT_SECRET_KEY")
SIMPLE_JWT = {
    "SIGNING_KEY": SIMPLE_JWT_SECRET_KEY,
}


# django-cors-headers configurations
CORS_ALLOWED_ORIGINS = [
    CORS_ALLOWED_ORIGIN for CORS_ALLOWED_ORIGIN in CONFIG.get("CORS_ALLOWED_ORIGINS")
]

# email configurations
EMAIL_BACKEND = CONFIG.get("EMAIL_BACKEND")
EMAIL_PORT = CONFIG.get("EMAIL_PORT")
EMAIL_HOST = CONFIG.get("EMAIL_HOST")
EMAIL_HOST_USER = CONFIG.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = CONFIG.get("EMAIL_HOST_PASSWORD")
SERVER_EMAIL = CONFIG.get("EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = CONFIG.get("DEFAULT_FROM_EMAIL")

EMAIL_VERIFY_TIMEOUT = 180  # in seconds


CLIENT_URL = CONFIG.get("CLIENT_URL")


# import local_settings when DEBUG mode is True
if DEBUG:
    try:
        from .local_settings import *
    except ImportError as e:
        pass
