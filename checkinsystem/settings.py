"""
Django settings for checkin project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
# new view
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # Own apps
    'center',
    'wechat',
    'user_system',
    'school',
    'course',
    'checkin',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Own middleware
    'user_system.middleware.UserMiddleware',
]

ROOT_URLCONF = 'checkinsystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                # Own processors
                'course.context_processors.todaylesson',
                'school.context_processors.school_settings',
                'user_system.context_processors.auth',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'checkinsystem.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = False

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

FILE_UPLOAD_PERMISSIONS = 0o644

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'request': {
            'format': '%(asctime)s [%(levelname)s] [status_code:%(status_code)s]- %(message)s'
        },
        'mainlog': {
            'format': '%(asctime)s [%(levelname)s] - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'request': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/', 'request.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'request',
        },
        'userfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/', 'userlog.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'mainlog',
        },
        'wechatfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/', 'wechatlog.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'mainlog',
        },
        'coursefile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/', 'courselog.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'mainlog',
        },
        'checkinfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/', 'checkinlog.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'mainlog',
        },
        'schoolfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('logs/', 'schoollog.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'mainlog',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['request'],
            'propagate': True,
            'level': 'WARNING',
        },
        'user': {
            'handlers': ['userfile', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'wechat': {
            'handlers': ['wechatfile', 'console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'course': {
            'handlers': ['coursefile', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'checkin': {
            'handlers': ['checkinfile', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
        'school': {
            'handlers': ['schoolfile', 'console'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}
from celery.schedules import crontab

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {
    'auto_stop_lesson': {
        'task': 'auto_stop_lesson',  # the same goes in the task name
        'schedule': 300.0,
        'args': ('today',)
    },
    # 'send_birthday_blessing': {
    #    'task': 'send_birthday_blessing',  # the same goes in the task name
    #    'schedule': crontab(hour=2, minute=56),
    # },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = None  # Disable the RequestDataTooBig check

try:
    from settings_local import *
except:
    pass
