from pathlib import Path
from datetime import timedelta
import os
import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(str, ""),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")


ALLOWED_HOSTS_STRING = env("DJANGO_ALLOWED_HOSTS")
if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ALLOWED_HOSTS_STRING.split(",")


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
    "corsheaders",
]

CUSTOM_APPS = [
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
    "common.apps.CommonConfig",
    "experiences.apps.ExperiencesConfig",
    "categories.apps.CategoriesConfig",
    "reviews.apps.ReviewsConfig",
    "wishlists.apps.WishlistsConfig",
    "bookings.apps.BookingsConfig",
    "medias.apps.MediasConfig",
    "direct_messages.apps.DirectMessagesConfig",
]

INSTALLED_APPS = SYSTEM_APPS + THIRD_PART_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    # "common.middleware.AccessLogMiddleware",
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

# if DEBUG:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.getenv("POSTGRES_DB"),
#             "USER": os.getenv("POSTGRES_USER"),
#             "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
#             "HOST": os.getenv("POSTGRES_HOST"),
#             "PORT": os.getenv("POSTGRES_PORT", "5432"),  # 기본 포트 5432
#         }
#     }
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),  # 기본 포트 5432
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

AUTH_USER_MODEL = "users.User"

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

KAKAO_CLIENT_ID = env("KAKAO_CLIENT_ID")


APPEND_SLASH = False
CORS_ALLOW_CREDENTIALS = True

# if DEBUG:
#     # 개발 환경에서는 localhost:3000만 허용
#     CORS_ALLOWED_ORIGINS = [
#         "http://localhost:3000",
#     ]
# else:
#     # 프로덕션 환경에서는 실제 서비스 도메인만 허용
#     CORS_ALLOWED_ORIGINS = [
#         "http://airbnb-beta.ggorockee.com",
#         "http://airbnb.ggorockee.com",
#     ]

# # --- CSRF Settings ---
# # CORS 설정과 마찬가지로, 환경에 따라 신뢰하는 출처를 분리하여 관리합니다.
# if DEBUG:
#     CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
# else:
#     CSRF_TRUSTED_ORIGINS = [
#         "http://airbnb-beta.ggorockee.com",
#         "http://airbnb.ggorockee.com",
#     ]


# ## logging setting
# # 🪵 로깅 설정
# if DEBUG:
#     # --- 개발용 로깅 설정 ---
#     LOGGING = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "verbose": {
#                 "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
#             },
#         },
#         "handlers": {
#             "console": {
#                 "level": "DEBUG", # 개발 시에는 모든 레벨의 로그를 확인
#                 "class": "logging.StreamHandler",
#                 "formatter": "verbose",
#             },
#         },
#         "root": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#         },
#     }
# else:
#     # --- 운영용 로깅 설정 ---
#     LOGGING = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "verbose": {
#                 "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(module)s:%(lineno)d)",
#             },
#             "simple": {
#                 "format": "%(asctime)s [%(levelname)s] %(message)s",
#             },
#         },
#         "handlers": {
#             # WARNING, ERROR 레벨 로그를 파일에 기록
#             "file_warning": {
#                 "level": "WARNING",
#                 "class": "logging.handlers.RotatingFileHandler",
#                 "filename": BASE_DIR / "logs/app_warning.log",
#                 "maxBytes": 1024 * 1024 * 5,  # 5 MB
#                 "backupCount": 5,
#                 "formatter": "verbose",
#             },
#             # Access Log를 별도 파일에 기록
#             "file_access": {
#                 "level": "INFO",
#                 "class": "logging.handlers.RotatingFileHandler",
#                 "filename": BASE_DIR / "logs/access.log",
#                 "maxBytes": 1024 * 1024 * 5,  # 5 MB
#                 "backupCount": 5,
#                 "formatter": "simple", # Access Log는 간단한 포맷 사용
#             },
#             # ERROR 레벨 로그 발생 시 이메일 발송
#             "mail_admins": {
#                 "level": "ERROR",
#                 "class": "django.utils.log.AdminEmailHandler",
#                 "formatter": "verbose",
#             }
#         },
#         "loggers": {
#             # Django 기본 로거
#             "django": {
#                 "handlers": ["file_warning"],
#                 "level": "INFO",
#                 "propagate": True,
#             },
#             # 500 에러 등 요청 처리 실패 로거
#             "django.request": {
#                 "handlers": ["mail_admins", "file_warning"],
#                 "level": "ERROR",
#                 "propagate": False,
#             },
#             # Access Log를 위한 커스텀 로거
#             "access": {
#                 "handlers": ["file_access"],
#                 "level": "INFO",
#                 "propagate": False,
#             },
#         },
#         # 위에 명시되지 않은 모든 로거들의 기본 설정
#         "root": {
#             "handlers": ["file_warning"],
#             "level": "WARNING",
#         },
#     }
