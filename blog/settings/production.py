from .base import *


DEBUG = False

ALLOWED_HOSTS = ['ramilpowers.ru', 'www.ramilpowers.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environment_variables.DATABASE_NAME,
        'USER': environment_variables.DATABASE_USER,
        'PASSWORD': environment_variables.DATABASE_PASSWORD,
        'HOST': 'localhost'
    }
}

# Логгирование
ADMINS = (('RR', 'ingatushuy@gmail.com'),)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}