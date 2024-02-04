"""Production settings and globals."""

from .base import *

SECRET_KEY = os.getenv('django_secret_key')

DEBUG = False

ALLOWED_HOSTS =[]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#Aws configuration

AWS_ACCESS_KEY_ID =os.getenv('access_key')
AWS_SECRET_ACCESS_KEY = os.getenv('secret_key')

#
AWS_STORAGE_BUCKET_NAME = os.getenv('bucket_name')
AWS_S3_CUSTOM_DOMAIN = 'myBucket.s3.amazonaws.com'  
AWS_S3_FILE_OVERWRITE = False

#Boto3 storage configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


STORAGE = {
    #Media File management
    "default":{
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },

    #Static file management
    "staticfiles":{
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'FleetingFiles/static'),
    os.path.join(BASE_DIR, 'room/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIAFILES_LOCATION = 'media'
MEDIA_URL= 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)