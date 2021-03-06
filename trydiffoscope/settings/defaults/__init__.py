import os
import copy
import email
import djcelery

from os.path import dirname, abspath
from celery.schedules import crontab

from django.utils.log import DEFAULT_LOGGING

from apps import *
from setup_warnings import *

djcelery.setup_loader()

BASE_DIR = '/usr/share/python/trydiffoscope'

# Fallback to relative location
if not __file__.startswith(BASE_DIR):
    BASE_DIR = dirname(dirname(dirname(dirname(abspath(__file__)))))

DEBUG = False
ALLOWED_HOSTS = ('*',)

SECRET_KEY = 'overriden-in-production'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'trydiffoscope',
        'USER': 'trydiffoscope',
        'PASSWORD': 'trydiffoscope',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
    },
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'trydiffoscope.urls'
WSGI_APPLICATION = 'trydiffoscope.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'trydiffoscope.utils.context_processors.settings_context',
            ],
            'builtins': [
                'django.contrib.staticfiles.templatetags.staticfiles',
            ],
        },
    },
]

LOGIN_URL = '/login' # 'account:login'
LOGIN_REDIRECT_URL = '/' # 'static:landing'

USE_TZ = False
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
LANGUAGE_CODE = 'en-gb'
DATETIME_FORMAT = 'r' # RFC 2822

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'media'),)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

MEDIA_URL = '/storage/'
MEDIA_ROOT = 'overriden-in-production'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

BROKER_URL = 'redis://localhost:6379/0'

CELERYBEAT_SCHEDULE = {
    'cleanup': {
        'task': 'trydiffoscope.container.tasks.cleanup',
        'schedule': crontab(minute=30),
    },
    'retention-policy': {
        'task': 'trydiffoscope.compare.retention_policy.tasks.purge',
        'schedule': crontab(minute=0),
    },
    'update-container': {
        'task': 'trydiffoscope.container.tasks.update_container',
        'schedule': crontab(hour=0, minute=0),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SITE_URL = 'overriden-in-production'
DEFAULT_FROM_EMAIL = 'overriden-in-production'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 86400 * 365 * 10
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
)

AUTH_PASSWORD_VALIDATORS = (
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'trydiffoscope',
    }
}

# Always log to the console, even in production (ie. gunicorn)
LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['handlers']['console']['filters'] = []

TRYDIFFOSCOPE_RESULTS_RETENTION_DAYS = 30
TRYDIFFOSCOPE_MAX_UPLOAD_SIZE_MEGABYTES = 20 # overriden-in-production
