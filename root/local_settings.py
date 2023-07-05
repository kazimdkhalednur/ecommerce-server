from django.utils.timezone import timedelta

from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# actually ACCESS_TOKEN_LIFETIME is 5 minutes but development purpose
# ACCESS_TOKEN_LIFETIME is 30 day
SIMPLE_JWT.update({"ACCESS_TOKEN_LIFETIME": timedelta(days=30)})


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
