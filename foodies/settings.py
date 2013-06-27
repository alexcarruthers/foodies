# Django settings for InterviewMemo project.

import os
import django.conf.global_settings as DEFAULT_SETTINGS

PROJECT_NAME = 'foodies'
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
SITE_ROOT = os.path.split(PROJECT_ROOT)[0]

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Rami Sayar', 'rami.sayar@gmail.com'),
)

MANAGERS = ADMINS

if DEBUG:
    EMAIL_HOST = '127.0.0.1'
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'testing@example.com'
#if DEBUG:
#    import warnings
#    warnings.filterwarnings(
#        'error', r"DateTimeField received a naive datetime",
#        RuntimeWarning, r'django\.db\.models\.fields')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Montreal'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'global_static/')
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6(-k3_i5#y*z7mxl1k1+28t1adzgu7_d3a_(6f8!ofag#0-h$&'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'announcements.middleware.AnnouncementsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'foodies.urls'

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures/'),
)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'foodies.wsgi.application'

ANONYMOUS_USER_ID=-1

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.sites',
    'django.contrib.sitemaps', 'django.contrib.messages', 'django.contrib.staticfiles', 'django.contrib.redirects',
    'django.contrib.comments', 'django.contrib.admin', 'django.contrib.admindocs',
    'django.contrib.localflavor', 'django.contrib.humanize', 'django.contrib.flatpages',

    'announcements', 'django_extensions', 'storages',
    'compressor', 'south', 'analytical', 'gargoyle',

    'django_nose',  # django_nose must come after south
    'djangoratings',

    'foodies.recipe',
    'foodies.account',
    'foodies.blog',

    'guardian'  # guardian must go after foodies.account as it depends on the UserProfile module.
)

#----------------------------------------------------------------------------------------
# Custom Settings
#----------------------------------------------------------------------------------------
AUTH_PROFILE_MODULE = 'account.UserProfile'
from django.core.urlresolvers import reverse_lazy
LOGIN_REDIRECT_URL = reverse_lazy('list_recipes')

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS +\
                              ('django.core.context_processors.request',
                               'announcements.context_processors.announcements')

APPEND_SLASH = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

LOGFILE_PATH = os.path.join(SITE_ROOT, 'logs/%s.log' % (PROJECT_NAME, ))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
         'require_debug_false': {
             '()': 'django.utils.log.RequireDebugFalse'
         }
     },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'brief': {
            'format':'%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
         'mail_admins': {
             'level': 'ERROR',
             'filters': ['require_debug_false'],
             'class': 'django.utils.log.AdminEmailHandler'
         },
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'rotating': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOGFILE_PATH,
            'maxBytes': 10485760, # 10 megabytes.
            'backupCount': 30,
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers':['rotating', 'console'],
            'level':'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        PROJECT_NAME: {
            'level': 'INFO',
            'handlers': ['rotating', 'console', 'mail_admins'],
            'propagate': False
        },
    },
    'root': {
        'level': 'INFO',
        'handlers':['console'],
    }
}

#----------------------------------------------------------------------------------------
# Django Activity Stream
#----------------------------------------------------------------------------------------
ACTSTREAM_USE_JSONFIELD = True
ACTSTREAM_SETTINGS = {
    'MODELS': ('auth.user', 'auth.group', 'sites.site', 'comments.comment'),
    #'MANAGER': 'myapp.streams.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 1,
}

#----------------------------------------------------------------------------------------
# Django Grappelli
#----------------------------------------------------------------------------------------
GRAPPELLI_ADMIN_TITLE = "Foodies Admin"

#----------------------------------------------------------------------------------------
# Django Nose
#----------------------------------------------------------------------------------------

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#----------------------------------------------------------------------------------------
# Django Compressor Settings
#----------------------------------------------------------------------------------------

COMPRESS_CSS_FILTERS=['compressor.filters.css_default.CssAbsoluteFilter', 
                      'compressor.filters.cssmin.CSSMinFilter']
#TODO: SETUP GOOGLE CLOSURES JS MINIFIER, THE CURRENT DEFAULT IS rJSmin

# NOTE: If we ever use LESS, CoffeeScript, we can set the COMPRESS_PRECOMPILER
# tuple.

#----------------------------------------------------------------------------------------
# TinyMCE Settings
#----------------------------------------------------------------------------------------
TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = STATIC_ROOT + 'js/tiny_mce'
TINYMCE_COMPRESSOR = True
TINYMCE_DEFAULT_CONFIG = {
    # custom plugins
    'plugins': "table,spellchecker,paste,searchreplace",
    # editor theme
    'theme': "advanced",
    # custom CSS file for styling editor area
    #'content_css': STATIC_URL + "css/custom_tinymce.css",
    # use absolute urls when inserting links/images
    'relative_urls': False,
}

# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Every cache key will get prefixed with this value - here we set it to
# the name of the directory the project is in to try and use something
# project specific.
CACHE_MIDDLEWARE_KEY_PREFIX = 'foodies'

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

if os.path.exists("/home/dotcloud/environment.json") or ('PLATFORM' in os.environ and os.environ['PLATFORM'] == 'dotcloud'):
    try:
        from conf.dotcloud_settings import *
    except ImportError, e:
        print "ERROR: DETECTED DOTCLOUD BUT COULD NOT IMPORT CONFIGURATION.\n%s" % str(e)
elif 'PLATFORM' in os.environ and os.environ['PLATFORM'] == 'heroku':
    try:
        from conf.heroku_settings import *
    except ImportError, e:
        print "ERROR: DETECTED HEROKU BUT COULD NOT IMPORT CONFIGURATION.\n%s" % str(e)
elif 'PLATFORM' in os.environ and os.environ['PLATFORM'] == 'production':
    try:
        from conf.production_settings import *
    except ImportError, e:
        print "ERROR: DETECTED PRODUCTION BUT COULD NOT IMPORT CONFIGURATION.\n%s" % str(e)
elif 'PLATFORM' in os.environ and os.environ['PLATFORM'] == 'staging':
    try:
        from conf.staging_settings import *
    except ImportError, e:
        print "ERROR: DETECTED STAGING BUT COULD NOT IMPORT CONFIGURATION.\n%s" % str(e)
elif 'PLATFORM' in os.environ and os.environ['PLATFORM'] == 'testing':
    try:
        from conf.testing_settings import *
    except ImportError, e:
        print "ERROR: DETECTED TESTING BUT COULD NOT IMPORT CONFIGURATION.\n%s" % str(e)
else:
    try:
        from conf.local_settings import *
        MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + LOCAL_MIDDLEWARE_CLASSES
        INSTALLED_APPS = INSTALLED_APPS + LOCAL_INSTALLED_APPS
    except ImportError, e:
        print "ERROR: DETECTED LOCAL BUT COULD NOT IMPORT CONFIGURATION.\n%s" % str(e)

