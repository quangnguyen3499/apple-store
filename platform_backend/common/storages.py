from django.conf import settings

from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError
import boto3
import logging


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


def create_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response

def create_presigned_url_post(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client("s3")
    try:
        response = s3_client.generate_presigned_post(
            bucket_name, 
            object_name,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response
