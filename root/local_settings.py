from django.utils.timezone import timedelta

from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# actually ACCESS_TOKEN_LIFETIME is 5 minutes but development purpose
# ACCESS_TOKEN_LIFETIME is 1 day
SIMPLE_JWT.update({"ACCESS_TOKEN_LIFETIME": timedelta(days=1)})
