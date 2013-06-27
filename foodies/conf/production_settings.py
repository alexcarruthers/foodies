import os

PROJECT_NAME = 'foodies'

CONF_ROOT = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.split(CONF_ROOT)[0]
SITE_ROOT = os.path.split(PROJECT_ROOT)[0]

DEBUG = False

#----------------------------------------------------------------------------------------
# Database
#----------------------------------------------------------------------------------------

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': os.environ['RDS_DB_NAME'],
		'USER': os.environ['RDS_USERNAME'],
		'PASSWORD': os.environ['RDS_PASSWORD'],
		'HOST': os.environ['RDS_HOSTNAME'],
    'PORT': os.environ['RDS_PORT'],
   }
}

#----------------------------------------------------------------------------------------
# Static and Media Storage
#----------------------------------------------------------------------------------------

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#TODO: CURRENTLY USING A USER WHO HAS FULL S3 ACCESS INSTEAD OF RESTRICTION TO A BUCKET!
#TODO: SECURITY RISK! WE SHOULD BE USING ROLES OR SOMETHING...
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']
AWS_STORAGE_BUCKET_NAME = 'foodies-prod-fs'

#----------------------------------------------------------------------------------------
# Logging Settings
#----------------------------------------------------------------------------------------
#TODO: LOGGING SHOULD BE ROTATED TO S3...
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
            'filename': os.path.join(SITE_ROOT, 'logs/%s.log' % PROJECT_NAME),
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
