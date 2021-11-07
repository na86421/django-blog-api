from .base import *

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '8u96f9df9h.execute-api.ap-northeast-2.amazonaws.com',]

S3_BUCKET_NAME = get_secret("S3_BUCKET")
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_NAME
# serve the static files directly from the specified s3 bucket
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % S3_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret("AWS_DB_NAME"),
        'USER': get_secret("AWS_DB_USER"),
        'PASSWORD': get_secret("AWS_DB_PASSWORD"),
        'HOST': get_secret("AWS_DB_HOST"),
        'PORT': '5432',
    }
}