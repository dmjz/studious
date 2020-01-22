from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = settings.AWS_STATIC_LOCATION

class LessonStorage(S3Boto3Storage):
    bucket_name = 'studious-lessons'
    location = 'lessons'
    file_overwrite = False
