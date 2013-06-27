import os
import dj_database_url

DEBUG = False

PROJECT_NAME = 'foodies'
CONF_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.split(CONF_ROOT)[0]
SITE_ROOT = os.path.split(PROJECT_ROOT)[0]

DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Whether to send broken-link emails.
SEND_BROKEN_LINK_EMAILS = True

# List of compiled regular expression objects representing URLs that need not
# be reported when SEND_BROKEN_LINK_EMAILS is True. Here are a few examples:
import re
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon.ico$'),
    re.compile(r'^/robots.txt$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'\.(cgi|php|pl)$'),
)

# https://docs.djangoproject.com/en/1.4/topics/logging/
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
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
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
            'handlers': ['console'],
            'propagate': False
        },
    },
    'root': {
        'level': 'INFO',
        'handlers':['console'],
    }
}

