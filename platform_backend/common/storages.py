from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage


class StaticS3Storage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = "public-read"
    location = "staticfiles"

    def _get_security_token(self):
        """https://github.com/jschneier/django-storages/issues/606"""
        return None


class PublicS3MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    default_acl = "public-read"
    location = "media"

    def _get_security_token(self):
        """https://github.com/jschneier/django-storages/issues/606"""
        return None
