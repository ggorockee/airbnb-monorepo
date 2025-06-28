from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

import os

load_dotenv()


# env = environ.Env(
#     DEBUG=(bool, False),
# )

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

ALLOWED_HOSTS_STRING = os.getenv("DJANGO_ALLOWED_HOSTS")
if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = [ALLOWED_HOST for ALLOWED_HOST in ALLOWED_HOSTS_STRING.split(",")]


# Application definition

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PART_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
]

CUSTOM_APPS = [
    "user.apps.UserConfig",
    "room.apps.RoomConfig",
    "common.apps.CommonConfig",
    "experience.apps.ExperienceConfig",
    "category.apps.CategoryConfig",
    "review.apps.ReviewConfig",
    "wishlist.apps.WishlistConfig",
    "booking.apps.BookingConfig",
    "media.apps.MediaConfig",
    "direct_messages.apps.DirectMessagesConfig",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PART_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

REST_FRAMEWORK = {
    # Set the default authentication class for all API views to JWTAuthentication.
    # This means that Django Rest Framework will expect a JWT in the 'Authorization' header
    # for authenticating requests.
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Note: Other settings like 'DEFAULT_PERMISSION_CLASSES' can remain as they are.
    # For example:
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}


# This assumes you have 'from django.conf import settings' or have SECRET_KEY defined.
# It's often better to let it use the default.
# from django.conf import settings


# ... (at the bottom of your settings.py file)

SIMPLE_JWT = {
    # Set the lifespan of the access token.
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # Example: 1 hour
    # Set the lifespan of the refresh token.
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # Example: 1 day
    # If True, a new refresh token will be issued when a refresh token is used to obtain a new access token.
    # This enhances security as old refresh tokens become invalid.
    "ROTATE_REFRESH_TOKENS": False,
    # If True, the old refresh token will be added to a blacklist after it is used (rotated).
    # This prevents the reuse of compromised refresh tokens.
    # Requires 'rest_framework_simplejwt.token_blacklist' in INSTALLED_APPS.
    "BLACKLIST_AFTER_ROTATION": False,
    # --- Token Signature and Algorithm ---
    # The digital signature algorithm to sign the tokens.
    "ALGORITHM": "HS256",
    # The secret key used for the HS256 signature.
    # By default, this uses your project's SECRET_KEY. It's recommended to leave it unset
    # to use the default unless you have a specific reason to use a different key.
    # "SIGNING_KEY": settings.SECRET_KEY,
    # --- Header and Token Type Configuration ---
    # Specifies the "type" of header that will be checked for the token.
    # This means the client must send the header as "Authorization: Bearer <token>".
    "AUTH_HEADER_TYPES": ("Bearer",),
    # The actual header name on the incoming request to look for the token.
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # The key in the token payload that identifies the user.
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    # Allows you to add custom claims to the token payload.
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}


APPEND_SLASH = False
