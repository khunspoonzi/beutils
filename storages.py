# -------------------------------------------------------------------------------------
# GENERAL IMPORTS
# -------------------------------------------------------------------------------------

from storages.backends.s3boto3 import S3Boto3Storage

# -------------------------------------------------------------------------------------
# PROJECT IMPORTS
# -------------------------------------------------------------------------------------

from django.conf import settings


# -------------------------------------------------------------------------------------
# STATIC FILE STORAGE BACKEND
# -------------------------------------------------------------------------------------


class StaticStorage(S3Boto3Storage):
    """ Amazon AWS S3 StaticStorage Class """

    # Overwrite files
    file_overwrite = True

    # Set default ACL
    default_acl = "public-read"

    # Define bucket name
    bucket_name = settings.AWS_STATIC_BUCKET_NAME

    # Define location
    location = settings.STATICFILES_LOCATION

    # Define custom domain
    custom_domain = settings.AWS_S3_STATIC_DOMAIN


# -------------------------------------------------------------------------------------
# MEDIA FILE STORAGE BACKEND
# -------------------------------------------------------------------------------------


class MediaStorage(S3Boto3Storage):
    """ Amazon AWS S3 MediaStorage Class """

    # Overwrite files
    file_overwrite = False

    # Set default ACL
    default_acl = None

    # Define bucket name
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    # Define location
    location = settings.MEDIAFILES_LOCATION

    # Define custom domain
    custom_domain = settings.AWS_S3_STORAGE_DOMAIN
