import os
#from apps.saml2auth import config

# Django settings for niweb project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SOUTH_TESTS_MIGRATE = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
NIWEB_ROOT = BASE_DIR

# URL without the host name,
# eg. /niweb/ for http://www.example.com/niweb/.
NIWEB_URL = '/'

# Static files collection
STATIC_ROOT = os.path.join(NIWEB_ROOT, 'sitestatic/')

# Static URL
STATIC_URL = '/static/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(NIWEB_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Django mail settings, change these if needed.
SERVER_EMAIL = 'django@example.com'
ADMINS = (
    ('Admin', 'webmaster@example.com'),
)
MANAGERS = ADMINS

# To be able to use the report mailing functionality you need to set a to address and a key.
REPORTS_TO = []
#REPORTS_CC = []    #  Optional
#REPORTS_BCC = []   #  Optional
#EXTRA_REPORT_TO = {'ID': ['address', ]}
REPORT_KEY = 'secret_key'

NETAPP_REPORT_SETTINGS = [
    # {'volumes': [re.compile('pattern')], 'service_id': '', 'contract_reference': '', 'total_storage': 0.0}
]

# Please fill in a mail server.
DEFAULT_FROM_EMAIL = 'postmaster@example.com'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(NIWEB_ROOT, 'niweb.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Neo4j settings
NEO4J_RESOURCE_URI = 'http://localhost:7474'
NEO4J_MAX_DATA_AGE = '24'  # hours

# Login settings
LOGIN_URL = '/login/'
AUTH_PROFILE_MODULE = 'userprofile.UserProfile'

# djangosaml2 settings
#LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SAML_CREATE_UNKNOWN_USER = True

SAML_ATTRIBUTE_MAPPING = {
    'eduPersonPrincipalName': ('username', ),
    'mail': ('email', ),
    'givenName': ('first_name', ),
    'sn': ('last_name', ),
    'displayName': ('display_name', ),
}

#SAML_CONFIG = config.SAML_CONFIG

ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'sites.site', 'comments.comment', 'noclook.NodeHandle'),
    'MANAGER': 'actstream.managers.ActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'secret_key_here'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'djangosaml2.backends.Saml2Backend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'niweb.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(NIWEB_ROOT, 'templates/'),
)

STATICFILES_DIRS = (
    os.path.join(NIWEB_ROOT, 'static/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'tastypie',
    #'djangosaml2',
    'south',
    'actstream',
    'apps.userprofile',
    'apps.noclook',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django_error.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
            }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
            },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
            },
        }
}