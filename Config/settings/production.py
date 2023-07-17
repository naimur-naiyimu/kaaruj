# from decouple import csv
from decouple import config

from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=csv())
# ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [host.strip() for host in v.split(',')])
ALLOWED_HOSTS = ['*']
MEDIA_HOST = config('MEDIA_HOST', default='localhost')
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST'),
#         'PORT': config('DB_PORT', cast=int),
#         'ATOMIC_REQUESTS': True,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = ''
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': config('CACHE_LOCATION'),
#     }
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'logfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/server.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
        },

    },
    'loggers': {
        'django': {
            'handlers': ['logfile']
        },
    },
}
CRONJOBS = [
    ('*/1 * * * *', 'sales.api.inventory.views.DailySalesReportAPIView')
]