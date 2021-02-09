# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ GENERAL IMPORTS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

import django_heroku
import os

from corsheaders.defaults import default_headers
from decouple import config
from pathlib import Path


# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ SECRET KEY                                                                         │
# └────────────────────────────────────────────────────────────────────────────────────┘

SECRET_KEY = config("SECRET_KEY")

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ BASE DIRECTORY                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

BASE_DIR = Path(__file__).resolve().parent.parent

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PROJECT ENVIRONMENT                                                                │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Set project name
PROJECT_NAME = config("PROJECT_NAME")

# Set debug value
DEBUG = config("DEBUG", cast=bool, default=False)

# Django Debug Toolbar
ENABLE_DJANGO_DEBUG_TOOLBAR = config(
    "ENABLE_DJANGO_DEBUG_TOOLBAR", cast=bool, default=DEBUG
)

# Django Admin and Browsable API
ENABLE_DJANGO_ADMIN = config("ENABLE_DJANGO_ADMIN", cast=bool, default=False)
ENABLE_BROWSABLE_API = config("ENABLE_BROWSABLE_API", cast=bool, default=False)

# Define environments
LOCAL = "local"
STAGING = "staging"
PRODUCTION = "production"
TEMPORARY = "temporary"

ENVIRONMENT = config("ENVIRONMENT", default=TEMPORARY)

# Django Admin Colors
LITE = "Lite"
DARK_BLUE = "Dark Blue"
GRAY = "Gray"

ADMIN_COLORS_MAPPING = {LOCAL: LITE, STAGING: DARK_BLUE, PRODUCTION: GRAY}
ADMIN_COLORS = [
    ("Default", []),
    (LITE, "admincolors/css/lite.css"),
    (DARK_BLUE, "admincolors/css/dark-blue.css"),
    (GRAY, "admincolors/css/gray.css"),
]

# Admins
SEAN = ("Sean O'Leary", "khunspoonzi@gmail.com")

# Admin List
ADMINS = [SEAN]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ SERVER SETTINGS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

# WSGI Application
WSGI_APPLICATION = "config.wsgi.application"

# Allowed Hosts
ALLOWED_HOSTS = [h.strip() for h in config("ALLOWED_HOSTS", default="").split(",")]

# Internal IPs (Django Debug Toolbar)
INTERNAL_IPS = ["127.0.0.1"]

# Staging and Production Environments
if ENVIRONMENT in [STAGING, PRODUCTION]:

    # Enforce https in Staging and Production
    SECURE_SSL_REDIRECT = True

    # Other Settings
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # Needed for Heroku
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year

# Cors
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "Content-Case",  # For specifying the case of a JSON response
]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ URL CONFIGURATION                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

# API Route
API_ROUTE = "api/"

# API Versions
API_VERSIONS = ("v1",)
LATEST_API_VERSION = API_VERSIONS[-1]

# URL Configuration
ROOT_URLCONF = "config.urls"

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CUSTOM USER MODEL                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Custom User Model
AUTH_USER_MODEL = "user.User"

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ INSTALLED APPS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

INSTALLED_APPS = [
    # Django Contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django Debug Toolbar
    "debug_toolbar",
    # Django Extensions
    "django_extensions",
    # Django Storages
    "storages",
    # Django REST Framework
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "dynamic_rest",
    "drf_multiple_model",
    # Django Celery Beat
    "django_celery_beat",
]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ MIDDLEWARE                                                                         │
# └────────────────────────────────────────────────────────────────────────────────────┘

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ PASSWORD VALIDATORS                                                                │
# └────────────────────────────────────────────────────────────────────────────────────┘

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TEMPLATE SETTINGS                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
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

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DATABASE SETTINGS                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

DB_ENGINE = "django.db.backends.postgresql_psycopg2"
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER", default="postgres")
DB_PASSWORD = config("DB_PASSWORD", default="postgres")
DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", cast=int, default=5432)

DATABASES = {
    "default": {
        "ENGINE": DB_ENGINE,
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ STATIC FILES AND MEDIA SETTINGS                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

USE_LOCAL_STORAGE = (
    config("USE_LOCAL_STORAGE", cast=bool, default=True)
    if ENVIRONMENT == LOCAL
    else False
)


# Handle case of local storage
if USE_LOCAL_STORAGE:

    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Otherwise handle AWS configuration
else:

    # AWS Credentials
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")

    # Static Bucket
    AWS_STATIC_BUCKET_NAME = config("AWS_STATIC_BUCKET_NAME")
    AWS_S3_STATIC_DOMAIN = f"{AWS_STATIC_BUCKET_NAME}.s3.amazonaws.com"

    # Media Bucket
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_STORAGE_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    # S3 Object Parameters
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    # Static and Media Location
    STATICFILES_LOCATION = "static"
    MEDIAFILES_LOCATION = "media"

    # Static and Media Storage
    STATICFILES_STORAGE = "beutils.storages.StaticStorage"
    DEFAULT_FILE_STORAGE = "beutils.storages.MediaStorage"

    # Static and Media URL
    STATIC_URL = f"https://{AWS_S3_STATIC_DOMAIN}/{STATICFILES_LOCATION}/"
    MEDIA_URL = f"https://{AWS_S3_STORAGE_DOMAIN}/{MEDIAFILES_LOCATION}/"

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ TIMEZONE SETTINGS                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

TIME_ZONE = "UTC"

USE_TZ = True

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ LANGUAGE SETTINGS                                                                  │
# └────────────────────────────────────────────────────────────────────────────────────┘

LANGUAGE_CODE = "en-us"

USE_I18N = False

USE_L10N = False

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO REST FRAMEWORK SETTINGS                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Rest Framework Configuration
REST_FRAMEWORK = {
    "ORDERING_PARAM": "ordering_fields",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
}

# Dynamic Rest Configuration
DYNAMIC_REST = {"ENABLE_BROWSABLE_API": ENABLE_BROWSABLE_API}

# Check if browsable API is enabled
if ENABLE_BROWSABLE_API:

    # Restrict renderers to JSON renderer
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ REDIS SETTINGS                                                                     │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Redis URL
REDIS_URL = config("REDISTOGO_URL")

# Redis Settings
BROKER_URL = REDIS_URL
BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ CELERY SETTINGS                                                                    │
# └────────────────────────────────────────────────────────────────────────────────────┘

# Celery Settings
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ALWAYS_EAGER = config("CELERY_ALWAYS_EAGER", cast=bool, default=False)

# ┌────────────────────────────────────────────────────────────────────────────────────┐
# │ DJANGO HEROKU SETTINGS                                                             │
# └────────────────────────────────────────────────────────────────────────────────────┘

django_heroku.settings(locals(), staticfiles=False, databases=False)
