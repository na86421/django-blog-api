from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

INTERNAL_IPS = [
    '127.0.0.1',
]
