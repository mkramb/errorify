DEBUG = False
TEMPLATE_DEBUG = DEBUG

PROJECT_URL = 'http://www.errorify.com'
PREPEND_WWW = True

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

SESSION_COOKIE_DOMAIN = 'errorify.com'
COMPRESS_OFFLINE = True
