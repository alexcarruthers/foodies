import json
import os

DEBUG = False

PROJECT_NAME = 'foodies'
CONF_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.split(CONF_ROOT)[0]
SITE_ROOT = os.path.split(PROJECT_ROOT)[0]

with open("/home/dotcloud/environment.json") as f:
	env = json.load(f)

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'foodies',
		'USER': env['DOTCLOUD_DB_SQL_LOGIN'],
		'PASSWORD': env['DOTCLOUD_DB_SQL_PASSWORD'],
		'HOST': env['DOTCLOUD_DB_SQL_HOST'],
		'PORT': int(env['DOTCLOUD_DB_SQL_PORT'])
	}
}

MEDIA_ROOT = '/home/dotcloud/data/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/dotcloud/volatile/static/'

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/var/log/supervisor/%s.log' % PROJECT_NAME,
            'maxBytes': 1024*1024*25, # 25 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        # Catch All Logger -- Captures any other logging
        '': {
            'handlers': ['console', 'log_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

