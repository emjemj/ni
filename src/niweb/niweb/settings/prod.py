# -*- coding: utf-8 -*-
__author__ = 'lundberg'

"""Production settings and globals."""

from os import environ
import dotenv
import json
from apps.saml2auth import config
from common import *

# Read .env from project root
dotenv.read_dotenv(join(SITE_ROOT, '.env'))

########## PROJECT CONFIGURATION
# To be able to use the report mailing functionality you need to set a to address and a key.
REPORTS_TO = environ['REPORTS_TO'].split()
REPORTS_CC = environ.get('REPORTS_CC', '').split()     # Optional
REPORTS_BCC = environ.get('REPORTS_BCC', '').split()   # Optional
# EXTRA_REPORT_TO = {'ID': ['address', ]}
EXTRA_REPORT_TO = json.loads(environ.get('EXTRA_REPORT_TO', ''))
REPORT_KEY = environ['REPORT_KEY']

try:
    #NETAPP_REPORT_SETTINGS = [
    #    {
    #        'volumes': [re.compile('pattern')],
    #        'service_id': '',
    #        'contract_reference': '',
    #        'total_storage': 0.0
    #    }
    #]
    from secrets import NETAPP_REPORT_SETTINGS
except ImportError:
    NETAPP_REPORT_SETTINGS = []
########## PROJECT CONFIGURATION

########## END GENERAL CONFIGURATION
# djangosaml2 settings
LOGIN_URL = environ.get('LOGIN_URL', '')
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SAML_CREATE_UNKNOWN_USER = True

SAML_ATTRIBUTE_MAPPING = {
    'eduPersonPrincipalName': ('username', ),
    'mail': ('email', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),
    'displayName': ('display_name', ),
}
SAML_CONFIG = config.SAML_CONFIG
########## END GENERAL CONFIGURATION

########## AUTHENTICATION BACKENDS CONFIGURATION
AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
    'djangosaml2.backends.Saml2Backend',
)
######### END AUTHENTICATION BACKENDS CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS', '').split()
########## END ALLOWED HOST CONFIGURATION

########## SENTRY CONFIGURATION
# Set your DSN value
RAVEN_CONFIG = {
    'dsn': environ.get('SENTRY_DSN', ''),
}
########## END SENTRY CONFIGURATION

########## APP CONFIGURATION
INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
    'djangosaml2',
)
########## APP CONFIGURATION

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': environ.get('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
        'NAME': environ.get('DB_NAME', 'norduni'),
        'USER': environ.get('DB_USER', 'ni'),
        'PASSWORD': environ['DB_PASSWORD'],
        'HOST': environ.get('DB_HOST', 'localhost'),
        'PORT': environ.get('DB_PORT', '5432')
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': environ.get('CACHE_BACKEND', 'django.core.cache.backends.filebased.FileBasedCache'),
        'LOCATION': environ.get('CACHE_LOCATION', '/tmp/django_cache'),
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 3600  # 1h
CACHE_MIDDLEWARE_KEY_PREFIX = ''
########## END CACHE CONFIGURATION
