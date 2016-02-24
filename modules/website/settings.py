# -*- coding: utf-8 -*-

import os

# Django settings for website project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_URL = 'http://localhost:8000'

ADMINS = (
    ('Mitja Kramberger', 'mitja@errorify.com'),
)

#INTERNAL_IPS = ('127.0.0.1',)
MANAGERS = ADMINS
APPEND_SLASH = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'errorify',                   # Or path to database file if using sqlite3.
        'USER': 'errorify',                   # Not used with sqlite3.
        'PASSWORD': 'password',               # Not used with sqlite3.
        'HOST': '',                           # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                           # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
        }
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Default SITE_ID
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = os.path.join(PROJECT_URL, '/media/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'media/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '5)cviwn1i@30_f$s2fiao^5b8g-km=+wjwvw%9m7k1xu3091-f'

# Session cookie domain (make sure you adjust this according to the
# domains/subdomains that you are using!)
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_COOKIE_NAME = 'errorify_auth'
SESSION_COOKIE_AGE = 1209600 # (2 weeks, in seconds)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Authentication login/logout urls.
LOGIN_URL = '/auth/sign-in'
LOGOUT_URL = '/auth/sign-out'
LOGIN_REDIRECT_URL = '/events'

# Admin - login as
SU_REDIRECT_LOGIN = '/events'
SU_REDIRECT_EXIT = '/events'

# Authenticate user profile
AUTH_PROFILE_MODULE = 'auth.UserProfile'

# Date format
DATE_FORMAT = 'N j, Y'
TIME_FORMAT = 'H:i:s'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
    'website.apps.utils.context_processors.site',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django_pagination.middleware.PaginationMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'website.apps.utils.middlewares.TimezoneMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Pagination
PAGINATION_DEFAULT_PAGINATION = 12
PAGINATION_INVALID_PAGE_RAISES_404 = True

# Sorting
SORTING_INVALID_FIELD_RAISES_404 = True

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates/'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    # django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.admin',
    # third-party
    'gunicorn',
    'djcelery',
    'compressor',
    'crispy_forms',
    'debug_toolbar',
    'ajax_validation',
    'django_pagination',
    'django_extensions',
    'django_sorting',
    'django_filters',
    'django_su',
    # app
    'apps.api',
    'apps.auth',
    'apps.events',
    'apps.bundles',
    'apps.site',
    'apps.stats',
    'apps.tasks',
    'apps.thrift',
    'apps.utils',
)

# COMPRESS
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = False
COMPRESS_VERSION = True
COMPRESS_ROOT = os.path.join(PROJECT_ROOT, 'static/')
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

COMPRESS_JS_FILTERS = ['compressor.filters.closure.ClosureCompilerFilter']
COMPRESS_CLOSURE_COMPILER_BINARY =  ' java -jar ' + os.path.join(PROJECT_ROOT, '../../bin/compiler.jar')

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
       'console': {
            'format': '%(asctime)s %(levelname)8s %(name)s[%(funcName)s]: %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'stream': 'ext://sys.stdout',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'mail_admins'],
        'level': 'ERROR',
    },
}

# Email
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "mail@errorify.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = EMAIL_HOST_USER

# Piston configuration
PISTON_EMAIL_ERRORS = ADMINS[0][1]
PISTON_DISPLAY_ERRORS = DEBUG

# Celeryd
import djcelery
from celery.schedules import crontab

BROKER_HOST = "localhost"
BROKER_BACKEND="redis"
BROKER_USER = ""
BROKER_PASSWORD = ""
BROKER_VHOST = "0"
BROKER_POOL_LIMIT = 2

REDIS_PORT=6379
REDIS_HOST = "localhost"
REDIS_DB = 0
REDIS_CONNECT_RETRY = True

CELERYD_CONCURRENCY = 2
CELERY_ACKS_LATE = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_SEND_EVENTS=False
CELERY_TASK_RESULT_EXPIRES =  5*60*10
CELERY_DISABLE_RATE_LIMITS = True

CELERY_RESULT_BACKEND="redis"
CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"
CELERY_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
CELERY_SEND_TASK_ERROR_EMAILS = True

# periodic tasks
CELERYBEAT_SCHEDULE = {
#    'auth-package-expire': {
#        'task': 'website.apps.tasks.auth.AuthPackageExpire',
#        'schedule': crontab(minute=0, hour=0) # daily at midnight
#    },
    'stats-event-aggregate': {
        'task': 'website.apps.tasks.stats.StatsEventAggregate',
        'schedule': crontab(minute=0, hour=0) # daily at midnight
    },
    'auth-reset-events': {
        'task': 'website.apps.tasks.auth.AuthResetEvents',
        'schedule': crontab(minute=0, hour=0) # daily at midnight
    },
    'auth-reset-api': {
        'task': 'website.apps.tasks.auth.AuthResetApi',
        'schedule': crontab(minute=0, hour=0, day_of_week='mon') # every friday at midnight
    },
    'events-clear-data': {
        'task': 'website.apps.tasks.events.EventsClearData',
        'schedule': crontab(minute=0, hour=0, day_of_week='fri')  # every friday at midnight
    }
}

djcelery.setup_loader()

# Thrift
THRIFT_SERVER = "localhost"
THRIFT_PORT = 7911

# Debug toolbar
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [ 'localhost:11211' ],
        'TIMEOUT': 60*60*24*30, # 30 days
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Application config
APP_EVENTS_CLEAR_MONTHS = 2
APP_STATS_CLEAR_MONTHS = 4

try:
    from settings_local import *
except ImportError:
    pass
