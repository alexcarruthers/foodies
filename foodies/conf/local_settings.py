import os

PROJECT_NAME = 'foodies'
CONF_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.split(CONF_ROOT)[0]
SITE_ROOT = os.path.split(PROJECT_ROOT)[0]

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': os.path.join(SITE_ROOT, 'data/dev.sqlite'), # Or path to database file if using sqlite3.
		'USER': '',                      # Not used with sqlite3.
		'PASSWORD': '',                  # Not used with sqlite3.
		'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
	}
}

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media/')

LOGFILE_PATH = os.path.join(SITE_ROOT, 'logs/%s.log' % (PROJECT_NAME, ))

LOCAL_MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',)

LOCAL_INSTALLED_APPS = ('debug_toolbar',)

#TODO: NOT LOGGING FOR SOME REASON ?? :S
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
            'handlers': ['rotating', 'console'],
            'propagate': False
        },
    },
    'root': {
        'level': 'INFO',
        'handlers':['console'],
    }
}
